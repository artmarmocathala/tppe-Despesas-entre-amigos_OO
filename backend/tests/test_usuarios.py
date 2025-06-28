from app import create_app
from models import db, Usuario
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pytest


@pytest.fixture(scope='session')
def app():
    app = create_app('sqlite:///:memory:')
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(autouse=True)
def clean_db(app):
    with app.app_context():
        db.session.query(Usuario).delete()
        db.session.commit()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


def test_criar_listar_obter_atualizar_deletar_usuario(client):
    # Criar usuário
    resp = client.post('/usuarios', json={
        "nome": "Alice",
        "email": "alice@example.com",
        "senha": "123456",
        "is_superuser": True
    })
    assert resp.status_code == 201
    usuario = resp.get_json()
    usuario_id = usuario['id']
    assert usuario['nome'] == "Alice"
    assert usuario['is_superuser'] is True

    # Listar usuários
    resp = client.get('/usuarios')
    assert resp.status_code == 200
    usuarios = resp.get_json()
    assert any(u['id'] == usuario_id for u in usuarios)

    # Obter usuário individual
    resp = client.get(f'/usuarios/{usuario_id}')
    assert resp.status_code == 200
    usuario = resp.get_json()
    assert usuario['email'] == "alice@example.com"

    # Atualizar usuário
    resp = client.put(f'/usuarios/{usuario_id}', json={"nome": "Alice Nova", "is_superuser": False})
    assert resp.status_code == 200
    usuario = resp.get_json()
    assert usuario['nome'] == "Alice Nova"
    assert usuario['is_superuser'] is False

    # Deletar usuário
    resp = client.delete(f'/usuarios/{usuario_id}')
    assert resp.status_code == 200
    # Verificar remoção
    resp = client.get(f'/usuarios/{usuario_id}')
    assert resp.status_code == 404
