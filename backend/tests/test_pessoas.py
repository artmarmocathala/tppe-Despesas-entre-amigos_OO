from app import create_app
from models import db, Grupo, Pessoa
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
        db.session.query(Pessoa).delete()
        db.session.query(Grupo).delete()
        db.session.commit()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


def test_adicionar_listar_pessoa(client):
    resp = client.post('/grupos', json={"nome": "Grupo Pessoas", "max_pessoas": 2})
    grupo_id = resp.get_json()['id']
    resp = client.post(
        f'/grupos/{grupo_id}/pessoas',
        json={"nome": "Maria", "cpf": "12345678901"}
    )
    assert resp.status_code == 201
    pessoa_id = resp.get_json()['id']
    resp = client.get(f'/grupos/{grupo_id}/pessoas')
    pessoas = resp.get_json()
    assert any(p['id'] == pessoa_id for p in pessoas)


def test_deletar_pessoa(client):
    resp = client.post('/grupos', json={"nome": "Grupo Del"})
    grupo_id = resp.get_json()['id']
    pessoa = client.post(
        f'/grupos/{grupo_id}/pessoas',
        json={"nome": "Ana", "cpf": "11122233344"}
    ).get_json()
    pessoa_id = pessoa['id']
    resp = client.delete(f'/pessoas/{pessoa_id}')
    assert resp.status_code == 200
