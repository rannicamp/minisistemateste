# SISTEMA_MINI_TESTE/app/config.py
import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env (se existir, útil para desenvolvimento no Cloud Shell)
# O arquivo .env deve estar na raiz do projeto (ex: /home/usuario/minisistemateste/.env)
# Para Cloud Shell, o diretório base pode precisar ser ajustado ou o .env colocado no home do Cloud Shell
# Por simplicidade, vamos assumir que .env está na raiz do projeto `minisistemateste`
# Se você não for usar .env no Cloud Shell e for definir as vars diretamente no ambiente, pode remover load_dotenv.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
dotenv_path = os.path.join(project_root, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    # Se estiver rodando no Cloud Shell e o .env não for facilmente acessível na raiz do projeto clonado,
    # você pode definir as variáveis diretamente no ambiente do Cloud Shell ou pular o load_dotenv
    # e confiar nas variáveis de ambiente definidas no Cloud Run.
    # Para desenvolvimento local no Cloud Shell, pode ser mais fácil definir as vars no terminal antes de rodar.
    pass


class Config:
    """Configurações base para o mini sistema."""
    SECRET_KEY = os.environ.get('MINI_SECRET_KEY') or 'uma-chave-secreta-muito-segura-para-o-mini-teste'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # URL do banco de dados - será lida da variável de ambiente
    # No Cloud Run, esta será a string para o socket Unix.
    # Para desenvolvimento no Cloud Shell (com proxy), será algo como:
    # postgresql+psycopg2://postgres:SUA_SENHA@127.0.0.1:PORTA_DO_PROXY/mini_test_db
    SQLALCHEMY_DATABASE_URI = os.environ.get('MINI_SQLALCHEMY_DATABASE_URI') or \
                              'sqlite:///./mini_test_local.db' # Fallback para um SQLite local simples

    # Configuração CORS
    _raw_cors_origins_env = os.environ.get('MINI_CORS_ALLOWED_ORIGINS')
    if _raw_cors_origins_env:
        if _raw_cors_origins_env == '*':
            CORS_ALLOWED_ORIGINS = '*'
        else:
            CORS_ALLOWED_ORIGINS = [origin.strip() for origin in _raw_cors_origins_env.split(',')]
    else:
        # Para desenvolvimento no Cloud Shell, permitir localhost se estiver testando com o preview do Cloud Shell
        # ou a URL do preview do Cloud Shell.
        # Se o frontend for servido do Firebase, precisaremos da URL do Firebase aqui.
        CORS_ALLOWED_ORIGINS = [] # Deixe vazio por padrão; defina no ambiente.


class DevelopmentConfig(Config):
    """Configurações de desenvolvimento."""
    DEBUG = True
    FLASK_ENV = 'development'
    # Para desenvolvimento no Cloud Shell, se você for rodar o frontend localmente (ou via Firebase Hosting)
    # e o backend no Cloud Shell, você precisará adicionar a origem do frontend aqui,
    # ou definir MINI_CORS_ALLOWED_ORIGINS no ambiente do Cloud Shell.
    # Ex: CORS_ALLOWED_ORIGINS = ["http://localhost:PORTA_FRONTEND", "URL_DO_FIREBASE_HOSTING"]


class ProductionConfig(Config):
    """Configurações de produção (para Cloud Run)."""
    DEBUG = False
    FLASK_ENV = 'production'
    # MINI_CORS_ALLOWED_ORIGINS e MINI_SQLALCHEMY_DATABASE_URI devem ser
    # definidas como variáveis de ambiente no serviço do Cloud Run.


config_by_name = dict(
    development=DevelopmentConfig,
    production=ProductionConfig,
    default=DevelopmentConfig
)