import pytest
from flask_jwt_extended import create_access_token
from models import Usuario, Grupo, Pessoa, Despesa

def create_superuser_token(app, client):
    user = Usuario(nome='Admin', email='admin@stats.com', is_superuser=True)
    user.set_senha('admin')
    from database import db
    db.session.add(user)
    db.session.commit()
    token = create_access_token(identity=str(user.id), additional_claims={"is_superuser": True})
    return token, user

def create_normaluser_token(app, client):
    user = Usuario(nome='User', email='user@stats.com', is_superuser=False)
    user.set_senha('user')
    from database import db
    db.session.add(user)
    db.session.commit()
    token = create_access_token(identity=str(user.id), additional_claims={"is_superuser": False})
    return token, user

def test_stats_superuser(app, client):
    token, user = create_superuser_token(app, client)
    from database import db
    grupo = Grupo(nome='G1', usuario_id=user.id)
    db.session.add(grupo)
    db.session.commit()
    pessoa = Pessoa(nome='P1', cpf='12345678901', grupo_id=grupo.id)
    db.session.add(pessoa)
    db.session.commit()
    despesa = Despesa(valor=10, grupo_id=grupo.id, pagador_id=pessoa.id)
    db.session.add(despesa)
    db.session.commit()
    resp = client.get('/stats', headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'total_usuarios' in data
    assert 'total_grupos' in data
    assert 'total_pessoas' in data
    assert 'total_despesas' in data

def test_stats_normaluser(app, client):
    token, user = create_normaluser_token(app, client)
    from database import db
    grupo = Grupo(nome='MeuGrupo', usuario_id=user.id)
    db.session.add(grupo)
    db.session.commit()
    pessoa = Pessoa(nome='Eu', cpf='12345678902', grupo_id=grupo.id)
    db.session.add(pessoa)
    db.session.commit()
    despesa = Despesa(valor=20, grupo_id=grupo.id, pagador_id=pessoa.id)
    db.session.add(despesa)
    db.session.commit()
    resp = client.get('/stats', headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'meus_grupos' in data
    assert 'minhas_pessoas' in data
    assert 'minhas_despesas' in data
