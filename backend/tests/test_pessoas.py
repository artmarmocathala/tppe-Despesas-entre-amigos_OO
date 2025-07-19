import pytest

class TestPessoas:
    
    ids = {}
    
    @pytest.mark.dependency()
    def test_adicionar_pessoa(self, auth_client):
        grupo_resp = auth_client.post('/grupos/', json={"nome": "Grupo com Pessoas"})
        assert grupo_resp.status_code == 201
        TestPessoas.ids['grupo_id'] = grupo_resp.get_json()['id']
        grupo_id = TestPessoas.ids['grupo_id']
        resp = auth_client.post(
            f'/grupos/{grupo_id}/pessoas',
            json={"nome": "Fulano", "cpf": "11122233344"}
        )
        assert resp.status_code == 201
        TestPessoas.ids['pessoa_id'] = resp.get_json()['id']

    @pytest.mark.dependency(depends=["TestPessoas::test_adicionar_pessoa"])
    def test_listar_pessoas_do_grupo(self, auth_client):
        pessoa_id = TestPessoas.ids['pessoa_id']
        grupo_id = TestPessoas.ids['grupo_id']
        resp = auth_client.get(f'/grupos/{grupo_id}/pessoas')
        assert resp.status_code == 200
        assert any(p['id'] == pessoa_id for p in resp.get_json())

    @pytest.mark.dependency(depends=["TestPessoas::test_adicionar_pessoa"])
    def test_obter_pessoa(self, auth_client):
        pessoa_id = TestPessoas.ids['pessoa_id']
        resp = auth_client.get(f'/pessoas/{pessoa_id}')
        assert resp.status_code == 200
        assert resp.get_json()['id'] == pessoa_id

    @pytest.mark.dependency(depends=["TestPessoas::test_adicionar_pessoa"])
    def test_deletar_pessoa(self, auth_client):
        pessoa_id = TestPessoas.ids['pessoa_id']
        resp = auth_client.delete(f'/pessoas/{pessoa_id}')
        assert resp.status_code == 200
        resp = auth_client.get(f'/pessoas/{pessoa_id}')
        assert resp.status_code == 404