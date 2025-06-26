import pytest
import os
from app import create_app
from models import db, Grupo, Pessoa, Compra, Imovel

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

def test_criar_listar_grupo(client):
    # Criar grupo
    resp = client.post('/grupos', json={"nome": "Grupo Teste", "max_pessoas": 2})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['nome'] == "Grupo Teste"
    grupo_id = data['id']

    # Listar grupos
    resp = client.get('/grupos')
    assert resp.status_code == 200
    grupos = resp.get_json()
    assert any(g['id'] == grupo_id for g in grupos)

def test_adicionar_listar_pessoa(client):
    # Criar grupo
    resp = client.post('/grupos', json={"nome": "Grupo Pessoas", "max_pessoas": 2})
    grupo_id = resp.get_json()['id']

    # Adicionar pessoa
    resp = client.post(f'/grupos/{grupo_id}/pessoas', json={"nome": "Maria", "cpf": "12345678901"})
    assert resp.status_code == 201
    pessoa_id = resp.get_json()['id']

    # Listar pessoas
    resp = client.get(f'/grupos/{grupo_id}/pessoas')
    pessoas = resp.get_json()
    assert any(p['id'] == pessoa_id for p in pessoas)

def test_registrar_listar_deletar_compra(client):
    # Criar grupo e pessoa
    grupo = client.post('/grupos', json={"nome": "Grupo Compra"}).get_json()
    grupo_id = grupo['id']
    pessoa = client.post(f'/grupos/{grupo_id}/pessoas', json={"nome": "João", "cpf": "98765432100"}).get_json()
    pessoa_id = pessoa['id']

    # Registrar compra
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

    # Listar despesas
    resp = client.get(f'/grupos/{grupo_id}/despesas')
    despesas = resp.get_json()
    assert any(d['id'] == compra_id for d in despesas)

    # Deletar compra
    resp = client.delete(f'/despesas/compras/{compra_id}')
    assert resp.status_code == 200
    # Verificar remoção
    resp = client.get(f'/grupos/{grupo_id}/despesas')
    despesas = resp.get_json()
    assert not any(d['id'] == compra_id for d in despesas)

def test_deletar_pessoa_e_grupo(client):
    # Criar grupo e pessoa
    grupo = client.post('/grupos', json={"nome": "Grupo Del"}).get_json()
    grupo_id = grupo['id']
    pessoa = client.post(f'/grupos/{grupo_id}/pessoas', json={"nome": "Ana", "cpf": "11122233344"}).get_json()
    pessoa_id = pessoa['id']

    # Deletar pessoa
    resp = client.delete(f'/pessoas/{pessoa_id}')
    assert resp.status_code == 200
    # Deletar grupo
    resp = client.delete(f'/grupos/{grupo_id}')
    assert resp.status_code == 200