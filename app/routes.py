# SISTEMA_MINI_TESTE/app/routes.py
from flask import Blueprint, request, jsonify
from . import db  # Importa a instância db de app/__init__.py
from .models import TestItem # Importa o modelo TestItem de app/models.py

# Cria um Blueprint para as rotas principais/de teste
# O prefixo /api será aplicado a todas as rotas neste blueprint
main_bp = Blueprint('main_bp', __name__, url_prefix='/api')

@main_bp.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    if not data or not data.get('nome'):
        return jsonify({"message": "O campo 'nome' é obrigatório"}), 400

    nome = data.get('nome')
    descricao = data.get('descricao')

    new_item = TestItem(nome=nome, descricao=descricao)

    try:
        db.session.add(new_item)
        db.session.commit()
        return jsonify(new_item.to_dict()), 201 # Retorna o item criado e status 201
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar item: {str(e)}") # Log do erro no servidor
        return jsonify({"message": "Erro interno ao criar item"}), 500

@main_bp.route('/items', methods=['GET'])
def get_items():
    try:
        items = TestItem.query.all()
        return jsonify([item.to_dict() for item in items]), 200
    except Exception as e:
        print(f"Erro ao buscar itens: {str(e)}") # Log do erro no servidor
        return jsonify({"message": "Erro interno ao buscar itens"}), 500

# Rota de health check simples (opcional, mas útil)
@main_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200