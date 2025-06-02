# SISTEMA_MINI_TESTE/app/config.py
import os
from dotenv import load_dotenv

# Define o diretório base do projeto
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) # Aponta para a raiz do projeto minisistemateste
load_dotenv(os.path.join(basedir, '.env')) # Carrega o arquivo .env da raiz do projeto, se existir

class Config:
    """Configurações base, das quais as outras herdam."""
    SECRET_KEY = os.environ.get('MINI_SECRET_KEY') or 'uma-chave-secreta-muito-dificil-de-adivinhar-para-o-minisistema'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MINI_CORS_ALLOWED_ORIGINS = os.environ.get('MINI_CORS_ALLOWED_ORIGINS', 'http://localhost:8080,http://127.0.0.1:8080,http://localhost:5000,http://127.0.0.1:5000')

    # Define o valor para a URI do banco de dados
    _effective_db_uri = os.environ.get('MINI_SQLALCHEMY_DATABASE_URI') or \
                        'sqlite:///' + os.path.join(basedir, 'mini_test_local.db')
    
    # Nossa variável customizada
    MINI_SQLALCHEMY_DATABASE_URI = _effective_db_uri
    # Variável padrão que Flask-SQLAlchemy espera <<< CORREÇÃO ADICIONADA
    SQLALCHEMY_DATABASE_URI = _effective_db_uri


class DevelopmentConfig(Config):
    """Configurações para o ambiente de desenvolvimento."""
    DEBUG = True
    
    _effective_dev_db_uri = os.environ.get('MINI_SQLALCHEMY_DATABASE_URI_DEV') or \
                            Config.MINI_SQLALCHEMY_DATABASE_URI # Herda da Config base se _DEV não estiver setada
    
    MINI_SQLALCHEMY_DATABASE_URI = _effective_dev_db_uri
    SQLALCHEMY_DATABASE_URI = _effective_dev_db_uri # <<< CORREÇÃO ADICIONADA
    
    MINI_CORS_ALLOWED_ORIGINS = os.environ.get('MINI_CORS_ALLOWED_ORIGINS') or '*'


class ProductionConfig(Config):
    """Configurações para o ambiente de produção."""
    DEBUG = False
    
    _effective_prod_db_uri = os.environ.get('MINI_SQLALCHEMY_DATABASE_URI') # DEVE ser setada no ambiente
    
    MINI_SQLALCHEMY_DATABASE_URI = _effective_prod_db_uri
    SQLALCHEMY_DATABASE_URI = _effective_prod_db_uri # <<< CORREÇÃO ADICIONADA
    
    MINI_CORS_ALLOWED_ORIGINS = os.environ.get('MINI_CORS_ALLOWED_ORIGINS') # DEVE ser setada no ambiente
    
    def __init__(self):
        super().__init__()
        if not self.MINI_SQLALCHEMY_DATABASE_URI:
            print("ALERTA DE PRODUÇÃO: MINI_SQLALCHEMY_DATABASE_URI (e, portanto, SQLALCHEMY_DATABASE_URI) não está definida!")
        if not self.MINI_CORS_ALLOWED_ORIGINS:
            print("ALERTA DE PRODUÇÃO: MINI_CORS_ALLOWED_ORIGINS não está definida!")


class DefaultConfig(DevelopmentConfig):
    """Configuração padrão usada se FLASK_CONFIG não estiver definida (usa Desenvolvimento)."""
    pass

# Dicionário que será importado pelo app/__init__.py para carregar a configuração correta
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DefaultConfig
}