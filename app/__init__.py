# SISTEMA_MINI_TESTE/app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

# Importa as configurações (assumindo que você tem app/config.py como definimos)
from .config import config # Nosso mini sistema usa um dicionário 'config' diretamente

# Inicializa as extensões (sem app ainda, serão inicializadas dentro da factory)
db = SQLAlchemy()
cors = CORS() # CORS será inicializado dentro da factory com configurações específicas

def create_app(config_name=None):
    """Fábrica da aplicação Flask."""
    app = Flask(__name__)

    # Determina qual configuração usar (development, production, ou default)
    if not config_name:
        # Para o mini sistema, esperamos FLASK_CONFIG='development' ou FLASK_CONFIG='production'
        # Se não estiver definida, 'default' usará as configurações de DevelopmentConfig
        config_name = os.getenv('FLASK_CONFIG', 'default')

    # Carrega a configuração do nosso dicionário 'config' em app/config.py
    chosen_config_object = config.get(config_name)
    if not chosen_config_object:
        print(f"AVISO: Configuração '{config_name}' não encontrada. Usando 'default'.")
        chosen_config_object = config.get('default')

    app.config.from_object(chosen_config_object)
    
    print(f"INFO: Mini Sistema - Aplicação iniciada com configuração: {config_name.upper()}")
    print(f"INFO: Mini Sistema - DEBUG MODE: {app.config.get('DEBUG')}")
    # No nosso mini sistema, as variáveis de config têm o prefixo MINI_
    print(f"INFO: Mini Sistema - DATABASE_URI: {app.config.get('MINI_SQLALCHEMY_DATABASE_URI')}")
    print(f"INFO: Mini Sistema - CORS Origins (config): {app.config.get('MINI_CORS_ALLOWED_ORIGINS')}")


    # Inicializa as extensões com a instância da app
    db.init_app(app)
    Migrate(app, db) # Inicializa Flask-Migrate

    # --- INÍCIO DA SEÇÃO CORS CORRIGIDA ---
    # Configuração do CORS
    # No nosso mini sistema, a config é MINI_CORS_ALLOWED_ORIGINS
    cors_config_value = app.config.get("MINI_CORS_ALLOWED_ORIGINS", "*") # Pega da config, default para "*"
    
    final_origins_for_cors_extension = [] # Lista para passar para a extensão CORS

    if isinstance(cors_config_value, str):
        # Se for um texto (string), como "http://localhost:8080,http://127.0.0.1:5000"
        # Dividimos pela vírgula e limpamos os espaços
        final_origins_for_cors_extension = [origin.strip() for origin in cors_config_value.split(',') if origin.strip()]
    elif isinstance(cors_config_value, list):
        # Se já for uma lista Python, como ['http://localhost:8080', 'http://127.0.0.1:5000']
        # Apenas garantimos que cada item seja um texto e removemos espaços
        final_origins_for_cors_extension = [str(origin).strip() for origin in cors_config_value if str(origin).strip()]
    
    # Se, após o processamento, a lista de origens estiver vazia,
    # e a configuração original não era uma tentativa deliberada de definir uma lista vazia
    # (ex: MINI_CORS_ALLOWED_ORIGINS=""), então usar "*" como um fallback
    # para garantir que a API seja acessível durante o teste.
    if not final_origins_for_cors_extension:
        # Se a config original era None (não definida) ou explicitamente "*"
        if cors_config_value is None or (isinstance(cors_config_value, str) and cors_config_value == "*"):
            final_origins_for_cors_extension = "*" # Flask-CORS aceita "*" diretamente para "permitir todos"
        # Se a config era uma string vazia "" ou uma lista vazia [], a intenção era ser restritivo.
        elif cors_config_value == [] or (isinstance(cors_config_value, str) and cors_config_value == ""):
             print(f"INFO: Mini Sistema - CORS configurado para NÃO permitir explicitamente nenhuma origem (lista de origens vazia).")
             # Deixar final_origins_for_cors_extension como [] (lista vazia) será restritivo.
             # Para Flask-CORS, uma lista vazia em `origins` significa "sem origens permitidas".
        else: # Qualquer outra configuração inesperada que resultou em lista vazia
            print(f"AVISO: Configuração de CORS '{cors_config_value}' resultou em lista vazia. Usando '*' como fallback.")
            final_origins_for_cors_extension = "*" # Fallback para "permitir todos"

    cors.init_app(app,
                  resources={r"/api/*": {"origins": final_origins_for_cors_extension}},
                  methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                  supports_credentials=True)
    print(f"INFO: Mini Sistema - CORS inicializado para r'/api/*' com origins: {final_origins_for_cors_extension}")
    # --- FIM DA SEÇÃO CORS CORRIGIDA ---

    # Importar e registrar Blueprints (rotas)
    # Certifique-se que 'app/routes.py' existe e define 'main_bp'
    from .routes import main_bp
    app.register_blueprint(main_bp)
    print("INFO: Mini Sistema - Blueprint 'main_bp' registrado.")

    print("INFO: Mini Sistema - Aplicação Flask criada e configurada com sucesso.")
    return app