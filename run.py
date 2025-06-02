# SISTEMA_MINI_TESTE/run.py
import os
from app import create_app # Importa a factory create_app de app/__init__.py

# Obtém o nome da configuração da variável de ambiente FLASK_CONFIG,
# ou usa 'default' (que aponta para DevelopmentConfig) se não estiver definida.
config_name = os.getenv('FLASK_CONFIG', 'default')

# Cria a instância da aplicação Flask usando a factory
app = create_app(config_name)

# Este bloco if __name__ == '__main__': só é executado se você rodar
# 'python run.py' diretamente, útil para desenvolvimento local com o servidor Flask.
# Gunicorn não usa este bloco, ele importa a variável 'app' diretamente.
if __name__ == '__main__':
    # A porta 8080 é comumente usada pelo Cloud Run, mas para desenvolvimento local
    # você pode usar a porta padrão do Flask (5000) ou outra.
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)