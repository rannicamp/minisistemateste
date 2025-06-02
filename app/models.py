from . import db  # Importa a instância 'db' do arquivo app/__init__.py
from sqlalchemy.sql import func # Para usar a função now() do banco de dados para o padrão de data_criacao

class TestItem(db.Model):
    __tablename__ = 'test_items'  # Nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=True)
    data_criacao = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<TestItem {self.nome}>'

    def to_dict(self):
        """Retorna uma representação do objeto em dicionário."""
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None
        }