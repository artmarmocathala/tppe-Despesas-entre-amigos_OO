import pytest

class TestGrupos:
    ids = {}
    
    @pytest.mark.dependency()
    def test_criar_grupo(self, auth_client):
        resp = auth_client.post('/grupos/', json={"nome": "Viagem de Férias"})        
        assert resp.status_code == 201
        data = resp.get_json()
        TestGrupos.ids['grupo_id'] = resp.get_json()['id']

    @pytest.mark.dependency(depends=["TestGrupos::test_criar_grupo"])
    def test_obter_grupo(self, auth_client):
        grupo_id = TestGrupos.ids['grupo_id']
        resp = auth_client.get(f'/grupos/{grupo_id}')
        assert resp.status_code == 200
        assert resp.get_json()['id'] == grupo_id

    @pytest.mark.dependency(depends=["TestGrupos::test_criar_grupo"])
    def test_atualizar_grupo(self, auth_client):
        grupo_id = TestGrupos.ids['grupo_id']
        resp = auth_client.put(f'/grupos/{grupo_id}', json={"nome": "Viagem de Férias 2025"})
        assert resp.status_code == 200
        assert resp.get_json()['nome'] == "Viagem de Férias 2025"
    
    @pytest.mark.dependency(depends=["TestGrupos::test_criar_grupo"])
    def test_listar_grupos(self, auth_client):
        grupo_id = TestGrupos.ids['grupo_id']
        resp = auth_client.get('/grupos/')
        assert resp.status_code == 200
        assert any(g['id'] == grupo_id for g in resp.get_json())

    @pytest.mark.dependency(depends=["TestGrupos::test_criar_grupo"])
    def test_deletar_grupo(self, auth_client):
        grupo_id = TestGrupos.ids['grupo_id']
        resp = auth_client.delete(f'/grupos/{grupo_id}')
        assert resp.status_code == 200
        
        resp = auth_client.get(f'/grupos/{grupo_id}')
        assert resp.status_code == 404