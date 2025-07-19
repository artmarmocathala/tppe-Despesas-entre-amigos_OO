import pytest
from flask_jwt_extended import decode_token

def test_criar_usuario_publico(client):
    """Testa a rota de criação de usuário, que é pública."""
    resp = client.post('/usuarios/', json={
        "nome": "Alice", "email": "alice@example.com", "senha": "password", "cpf": "12345678909"
    })
    assert resp.status_code == 201
    assert resp.get_json()['email'] == "alice@example.com"

def test_listar_usuarios(auth_client):
    """Testa a listagem de usuários (requer autenticação de superusuário)."""
    resp = auth_client.get('/usuarios/')
    assert resp.status_code == 200
    assert len(resp.get_json()) > 0
    assert any(u['email'] == 'test@example.com' for u in resp.get_json())


def test_listar_usuarios_negado_para_nao_superuser(client):

    user_data = {"nome": "Bob", "email": "bob@naosuper.com", "senha": "password", "is_superuser": False, "cpf": "12345678901"}
    resp = client.post('/usuarios/', json=user_data)
    assert resp.status_code == 201

    login_data = {"email": user_data['email'], "senha": user_data['senha']}
    resp_login = client.post('/login', json=login_data)
    token = resp_login.get_json()['token']
    client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'

    resp = client.get('/usuarios/')
    assert resp.status_code == 403
    del client.environ_base['HTTP_AUTHORIZATION']

class TestUsuarioCRUD:
    ids = {}
    
    @pytest.mark.dependency()
    def test_criar_usuario_para_crud(self, auth_client):
        resp = auth_client.post('/usuarios/', json={
            "nome": "Charlie", "email": "charlie@crud.com", "senha": "password", "cpf": "12345678902"
        })
        assert resp.status_code == 201
        TestUsuarioCRUD.ids['usuario_id'] = resp.get_json()['id']
    
    @pytest.mark.dependency(depends=["TestUsuarioCRUD::test_criar_usuario_para_crud"])
    def test_obter_usuario(self, auth_client):
        usuario_id = TestUsuarioCRUD.ids['usuario_id']
        resp = auth_client.get(f'/usuarios/{usuario_id}')
        assert resp.status_code == 200
        assert resp.get_json()['email'] == "charlie@crud.com"

    @pytest.mark.dependency(depends=["TestUsuarioCRUD::test_criar_usuario_para_crud"])
    def test_obter_usuario_negado_para_nao_superuser(self, client):

        user_data = {"nome": "Dave", "email": "dave@naosuper.com", "senha": "password", "is_superuser": False, "cpf": "12345678903"}
        resp = client.post('/usuarios/', json=user_data)
        assert resp.status_code == 201
        login_data = {"email": user_data['email'], "senha": user_data['senha']}
        resp_login = client.post('/login', json=login_data)
        token = resp_login.get_json()['token']
        client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'
        usuario_id = TestUsuarioCRUD.ids['usuario_id']
        resp = client.get(f'/usuarios/{usuario_id}')
        assert resp.status_code == 403
        del client.environ_base['HTTP_AUTHORIZATION']

    @pytest.mark.dependency(depends=["TestUsuarioCRUD::test_criar_usuario_para_crud"])
    def test_atualizar_usuario(self, auth_client):
        usuario_id = TestUsuarioCRUD.ids['usuario_id']
        headers = {"Authorization": f"Bearer {auth_client._token}"}
        resp = auth_client.put(
            f'/usuarios/{usuario_id}',
            json={"nome": "Charlie Brown", "is_superuser": True},
            headers=headers
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['nome'] == "Charlie Brown"
        assert data['is_superuser'] is True

    @pytest.mark.dependency(depends=["TestUsuarioCRUD::test_criar_usuario_para_crud"])
    def test_atualizar_usuario_negado(self, client):
        user_data = {"nome": "Eve", "email": "eve@naosuper.com", "senha": "password", "is_superuser": False, "cpf": "12345678904"}
        resp = client.post('/usuarios/', json=user_data)
        assert resp.status_code == 201
        login_data = {"email": user_data['email'], "senha": user_data['senha']}
        resp_login = client.post('/login', json=login_data)
        token = resp_login.get_json()['token']
        client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'
        usuario_id = TestUsuarioCRUD.ids['usuario_id']
        resp = client.put(f'/usuarios/{usuario_id}', json={"nome": "Novo Nome"})
        assert resp.status_code == 403
        del client.environ_base['HTTP_AUTHORIZATION']

    @pytest.mark.dependency(depends=["TestUsuarioCRUD::test_criar_usuario_para_crud"])
    def test_deletar_usuario(self, auth_client):
        usuario_id = TestUsuarioCRUD.ids['usuario_id']
        headers = {"Authorization": f"Bearer {auth_client._token}"}
        resp = auth_client.delete(f'/usuarios/{usuario_id}', headers=headers)
        assert resp.status_code == 200

        if 'HTTP_AUTHORIZATION' in auth_client.environ_base:
            del auth_client.environ_base['HTTP_AUTHORIZATION']
        resp = auth_client.get(f'/usuarios/{usuario_id}')
        assert resp.status_code == 401

    @pytest.mark.dependency(depends=["TestUsuarioCRUD::test_criar_usuario_para_crud"])
    def test_deletar_usuario_negado(self, client):
        user_data = {"nome": "Frank", "email": "frank@naosuper.com", "senha": "password", "is_superuser": False, "cpf": "12345678905"}
        resp = client.post('/usuarios/', json=user_data)
        assert resp.status_code == 201
        login_data = {"email": user_data['email'], "senha": "password"}
        resp_login = client.post('/login', json=login_data)
        token = resp_login.get_json()['token']
        client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'
        usuario_id = TestUsuarioCRUD.ids['usuario_id']
        resp = client.delete(f'/usuarios/{usuario_id}')
        assert resp.status_code == 403
        del client.environ_base['HTTP_AUTHORIZATION']

def test_obter_me(auth_client):
    resp = auth_client.get('/usuarios/me')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['email'] == 'test@example.com'
    assert 'senha' not in data 
    assert 'id' in data