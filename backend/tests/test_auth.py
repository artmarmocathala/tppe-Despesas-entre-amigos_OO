import pytest
import jwt
from flask_jwt_extended import decode_token


@pytest.fixture
def test_user(client):
    user_data = {
        "nome": "Login User",
        "email": "login@test.com",
        "senha": "correct-password",
        "is_superuser": True
    }
    resp = client.post('/usuarios/', json=user_data)
    return user_data


def test_login_sucesso(client, test_user):
    login_data = {
        "email": test_user['email'],
        "senha": test_user['senha']
    }
    resp = client.post('/login', json=login_data)
    assert resp.status_code == 200
    json_data = resp.get_json()
    assert 'token' in json_data
    # Verifica se o claim is_superuser está presente e correto
    token = json_data['token']
    decoded = decode_token(token)
    assert decoded['is_superuser'] is True


def test_login_senha_incorreta(client, test_user):
    login_data = {
        "email": test_user['email'],
        "senha": "wrong-password"
    }
    resp = client.post('/login', json=login_data)
    assert resp.status_code == 401
    json_data = resp.get_json()
    assert json_data['message'] == "Credenciais inválidas"


def test_login_usuario_inexistente(client):
    login_data = {
        "email": "nouser@test.com",
        "senha": "password"
    }
    resp = client.post('/login', json=login_data)
    assert resp.status_code == 401
