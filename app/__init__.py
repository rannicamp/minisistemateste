# SISTEMA_MINI_TESTE/app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from .config import config_by_name # Importa as configurações do nosso config.py
from .models import db as models_db # Importa a instância db dos modelos (para evitar circularidade)

# Inicializa as extensões (sem app ainda, serão inicializadas dentro da factory)
db = SQLAlchemy() # Esta é a instância principal de SQLAlchemy para a aplicação
# Flask-Migrate pode ser adicionado depois se precisarmos de migrações complexas para o mini-sistema
# migrate = Migrate()
cors = CORS()

def create_app(config_name=None):
    """Fábrica da aplicação Flask."""
    app = Flask(__name__)

    # Determina qual configuração usar (development, production, ou default)
    if not config_name:
        config_name = os.getenv('FLASK_CONFIG', 'default')

    chosen_config = config_by_name.get(config_name)
    if not chosen_config:
        print(f"AVISO: Configuração '{config_name}' não encontrada. Usando 'default'.")
        chosen_config = config_by_name.get('default')

    app.config.from_object(chosen_config)
    print(f"INFO: Mini Sistema - Aplicação iniciada com configuração: {config_name.upper()}")
    print(f"INFO: Mini Sistema - DEBUG MODE: {app.config.get('DEBUG')}")
    print(f"INFO: Mini Sistema - DATABASE_URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")


    # Inicializa as extensões com a instância da app
    db.init_app(app) # Inicializa SQLAlchemy com a app
    # Se fosse usar Flask-Migrate:
    # from flask_migrate import Migrate
    # migrate = Migrate() # Cria a instância aqui
    # migrate.init_app(app, db)

    # Configuração do CORS
    cors_allowed_origins = app.config.get("CORS_ALLOWED_ORIGINS", "*") # Default para '*' se não definido
    cors.init_app(app, 
                  resources={r"/api/*": {"origins": cors_allowed_origins}},
                  methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                  supports_credentials=True)
    print(f"INFO: Mini Sistema - CORS inicializado para r'/api/*' com origins: {cors_allowed_origins}")

    # Importar e registrar Blueprints (rotas)
    # Criaremos um blueprint simples para os 'TestItems' no próximo passo
    from .routes import main_bp as main_blueprint # Assumindo que as rotas estarão em app/routes.py
    app.register_blueprint(main_blueprint)
    print("INFO: Mini Sistema - Blueprint 'main_bp' registrado.")


    # Contexto da aplicação para criação de tabelas (se não usar Flask-Migrate inicialmente)
    # Com Flask-Migrate, isso não é estritamente necessário aqui,
    # pois as migrações cuidarão da criação das tabelas.
    # with app.app_context():
    #     db.create_all() # Cria tabelas se não existirem (cuidado em produção)
    #     print("INFO: Mini Sistema - db.create_all() chamado (se necessário).")

    print("INFO: Mini Sistema - Aplicação Flask criada e configurada com sucesso.")
    return app