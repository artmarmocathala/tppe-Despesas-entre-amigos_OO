from app import create_app
from models import db, Grupo, Pessoa, Compra, Imovel
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
        db.session.query(Imovel).delete()
        db.session.query(Pessoa).delete()
        db.session.query(Grupo).delete()
        db.session.commit()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


def test_registrar_listar_obter_deletar_compra(client):
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
    # Testa GET individual
    resp = client.get(f'/despesas/compras/{compra_id}')
    assert resp.status_code == 200
    compra_resp = resp.get_json()
    assert compra_resp['id'] == compra_id
    assert compra_resp['nome_mercado'] == "Mercado X"
    # Listar despesas
    resp = client.get(f'/grupos/{grupo_id}/despesas')
    despesas = resp.get_json()
    assert any(d['id'] == compra_id for d in despesas)
    # Deletar compra
    resp = client.delete(f'/despesas/compras/{compra_id}')
    assert resp.status_code == 200
    resp = client.get(f'/grupos/{grupo_id}/despesas')
    despesas = resp.get_json()
    assert not any(d['id'] == compra_id for d in despesas)


def test_registrar_listar_obter_deletar_imovel(client):
    grupo = client.post('/grupos', json={"nome": "Grupo Imovel"}).get_json()
    grupo_id = grupo['id']
    pessoa = client.post(
        f'/grupos/{grupo_id}/pessoas',
        json={"nome": "Carlos", "cpf": "22233344455"}
    ).get_json()
    pessoa_id = pessoa['id']
    imovel = {
        "valor": 200.0,
        "data": "2025-06-27",
        "pagador_id": pessoa_id,
        "endereco": "Rua XPTO, 123"
    }
    resp = client.post(f'/grupos/{grupo_id}/despesas/imoveis', json=imovel)
    assert resp.status_code == 201
    imovel_id = resp.get_json()['id']
    # Testa GET individual
    resp = client.get(f'/despesas/imoveis/{imovel_id}')
    assert resp.status_code == 200
    imovel_resp = resp.get_json()
    assert imovel_resp['id'] == imovel_id
    assert imovel_resp['endereco'] == "Rua XPTO, 123"
    # Listar despesas
    resp = client.get(f'/grupos/{grupo_id}/despesas')
    despesas = resp.get_json()
    assert any(d['id'] == imovel_id for d in despesas)
    # Deletar imovel
    resp = client.delete(f'/despesas/imoveis/{imovel_id}')
    assert resp.status_code == 200
    resp = client.get(f'/grupos/{grupo_id}/despesas')
    despesas = resp.get_json()
    assert not any(d['id'] == imovel_id for d in despesas)
