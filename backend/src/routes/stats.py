from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import Usuario, Grupo, Pessoa, Despesa
from database import db

stats_bp = Blueprint('stats', __name__)

@stats_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    user_id = get_jwt_identity()
    claims = get_jwt()
    is_superuser = claims.get('is_superuser', False)

    if is_superuser:
        total_usuarios = db.session.query(Usuario).count()
        total_grupos = db.session.query(Grupo).count()
        total_pessoas = db.session.query(Pessoa).count()
        total_despesas = db.session.query(Despesa).count()
        return jsonify({
            'total_usuarios': total_usuarios,
            'total_grupos': total_grupos,
            'total_pessoas': total_pessoas,
            'total_despesas': total_despesas
        })
    else:
        meus_grupos = db.session.query(Grupo).filter_by(usuario_id=int(user_id)).all()
        grupo_ids = [g.id for g in meus_grupos]
        minhas_pessoas = db.session.query(Pessoa).filter(Pessoa.grupo_id.in_(grupo_ids)).count() if grupo_ids else 0
        minhas_despesas = db.session.query(Despesa).filter(Despesa.grupo_id.in_(grupo_ids)).count() if grupo_ids else 0
        return jsonify({
            'meus_grupos': len(meus_grupos),
            'minhas_pessoas': minhas_pessoas,
            'minhas_despesas': minhas_despesas
        })
