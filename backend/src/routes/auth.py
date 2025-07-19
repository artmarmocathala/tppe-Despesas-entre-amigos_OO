from flask import Blueprint, request, jsonify
from models import Usuario
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', None)
    senha = data.get('senha', None)

    if not email or not senha:
        return jsonify({"message": "Email e senha são obrigatórios"}), 400

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not usuario.verificar_senha(senha):
        return jsonify({"message": "Credenciais inválidas"}), 401

    additional_claims = {"is_superuser": usuario.is_superuser}
    access_token = create_access_token(identity=str(usuario.id), additional_claims=additional_claims)

    return jsonify(token=access_token)
