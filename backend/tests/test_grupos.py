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

    resp = client.get(f'/grupos/{grupo_id}')
    assert resp.status_code == 200
    grupo = resp.get_json()
    assert grupo['id'] == grupo_id
    assert grupo['nome'] == "Grupo Teste"


def test_deletar_grupo(client):
    resp = client.post('/grupos', json={"nome": "Grupo Del"})
    grupo_id = resp.get_json()['id']
    resp = client.delete(f'/grupos/{grupo_id}')
    assert resp.status_code == 200


def test_dividir_despesas_grupo(client):
    # Cria grupo e pessoas
    resp = client.post('/grupos', json={"nome": "Grupo Divisao"})
    grupo_id = resp.get_json()['id']
    pessoa1 = client.post(f'/grupos/{grupo_id}/pessoas', json={"nome": "A", "cpf": "11111111111"}).get_json()
    pessoa2 = client.post(f'/grupos/{grupo_id}/pessoas', json={"nome": "B", "cpf": "22222222222"}).get_json()
    # Adiciona despesas
    compra = {
        "valor": 100.0,
        "data": "2025-06-27",
        "pagador_id": pessoa1['id'],
        "nome_mercado": "Mercado",
        "itens": ["item1"]
    }
    client.post(f'/grupos/{grupo_id}/despesas/compras', json=compra)
    imovel = {
        "valor": 50.0,
        "data": "2025-06-27",
        "pagador_id": pessoa2['id'],
        "endereco": "Rua 1"
    }
    client.post(f'/grupos/{grupo_id}/despesas/imoveis', json=imovel)
    # Testa divisão
    resp = client.get(f'/grupos/{grupo_id}/divisao')
    assert resp.status_code == 200
    divisao = resp.get_json()
    assert divisao['total_despesas'] == 150.0
    assert divisao['valor_por_pessoa'] == 75.0
    assert divisao['qtd_pessoas'] == 2
