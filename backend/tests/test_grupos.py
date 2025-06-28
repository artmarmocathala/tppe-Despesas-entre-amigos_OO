from app import create_app
from models import db, Grupo
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
        db.session.query(Grupo).delete()
        db.session.commit()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


def test_criar_listar_grupo(client):
    resp = client.post('/grupos', json={"nome": "Grupo Teste", "max_pessoas": 2})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['nome'] == "Grupo Teste"
    grupo_id = data['id']

    resp = client.get('/grupos')
    assert resp.status_code == 200
    grupos = resp.get_json()
    assert any(g['id'] == grupo_id for g in grupos)


def test_deletar_grupo(client):
    resp = client.post('/grupos', json={"nome": "Grupo Del"})
    grupo_id = resp.get_json()['id']
    resp = client.delete(f'/grupos/{grupo_id}')
    assert resp.status_code == 200
