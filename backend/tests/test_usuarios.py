import pytest

def test_criar_usuario_publico(client):
    """Testa a rota de criação de usuário, que é pública."""
    resp = client.post('/usuarios/', json={
        "nome": "Alice", "email": "alice@example.com", "senha": "password"
    })
    assert resp.status_code == 201
    assert resp.get_json()['email'] == "alice@example.com"

def test_listar_usuarios(auth_client):
    """Testa a listagem de usuários (requer autenticação)."""
    resp = auth_client.get('/usuarios/')
    assert resp.status_code == 200
    assert len(resp.get_json()) > 0
    assert any(u['email'] == 'test@example.com' for u in resp.get_json())


class TestUsuarioCRUD:
    ids = {}
    
    @pytest.mark.dependency()
    def test_criar_usuario_para_crud(self, auth_client):
        resp = auth_client.post('/usuarios/', json={
            "nome": "Charlie", "email": "charlie@crud.com", "senha": "password"
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
    def test_atualizar_usuario(self, auth_client):
        usuario_id = TestUsuarioCRUD.ids['usuario_id']
        resp = auth_client.put(
            f'/usuarios/{usuario_id}',
            json={"nome": "Charlie Brown", "is_superuser": True}
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['nome'] == "Charlie Brown"
        assert data['is_superuser'] is True

    @pytest.mark.dependency(depends=["TestUsuarioCRUD::test_criar_usuario_para_crud"])
    def test_deletar_usuario(self, auth_client):
        usuario_id = TestUsuarioCRUD.ids['usuario_id']
        resp = auth_client.delete(f'/usuarios/{usuario_id}')
        assert resp.status_code == 200

        resp = auth_client.get(f'/usuarios/{usuario_id}')
        assert resp.status_code == 404