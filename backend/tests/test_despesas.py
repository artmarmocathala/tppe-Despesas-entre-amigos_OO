from app import create_app
from models import db, Grupo, Pessoa, Compra
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
        db.session.query(Compra).delete()
        db.session.query(Pessoa).delete()
        db.session.query(Grupo).delete()
        db.session.commit()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


def test_registrar_listar_deletar_compra(client):
    grupo = client.post('/grupos', json={"nome": "Grupo Compra"}).get_json()
    grupo_id = grupo['id']
    pessoa = client.post(
        f'/grupos/{grupo_id}/pessoas',
        json={"nome": "João", "cpf": "98765432100"}
    ).get_json()
    pessoa_id = pessoa['id']
    compra = {
        "valor": 50.0,
        "data": "2025-06-26",
        "pagador_id": pessoa_id,
        "nome_mercado": "Mercado X",
        "itens": ["arroz", "feijão"]
    }
    resp = client.post(f'/grupos/{grupo_id}/despesas/compras', json=compra)
    assert resp.status_code == 201
    compra_id = resp.get_json()['id']
    resp = client.get(f'/grupos/{grupo_id}/despesas')
    despesas = resp.get_json()
    assert any(d['id'] == compra_id for d in despesas)
    resp = client.delete(f'/despesas/compras/{compra_id}')
    assert resp.status_code == 200
    resp = client.get(f'/grupos/{grupo_id}/despesas')
    despesas = resp.get_json()
    assert not any(d['id'] == compra_id for d in despesas)
