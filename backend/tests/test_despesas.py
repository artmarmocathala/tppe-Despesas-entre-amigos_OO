import pytest

class TestCompras:
    ids = {}

    @pytest.mark.dependency()
    def test_criar_compra(self, auth_client):
        grupo_resp = auth_client.post('/grupos/', json={"nome": "Grupo de Compras"})
        assert grupo_resp.status_code == 201
        TestCompras.ids['grupo_id'] = grupo_resp.get_json()['id']

        pessoa_resp = auth_client.post(
            f"/grupos/{TestCompras.ids['grupo_id']}/pessoas", 
            json={"nome": "Comprador", "cpf": "11111111111"}
        )
        assert pessoa_resp.status_code == 201
        TestCompras.ids['pessoa_id'] = pessoa_resp.get_json()['id']

        compra_data = {
            "valor": 125.50, "data": "2025-07-18", "pagador_id": TestCompras.ids['pessoa_id'], 
            "nome_mercado": "Supermercado Teste"
        }
        compra_resp = auth_client.post(f"/grupos/{TestCompras.ids['grupo_id']}/despesas/compras", json=compra_data)
        assert compra_resp.status_code == 201
        TestCompras.ids['compra_id'] = compra_resp.get_json()['id']

    @pytest.mark.dependency(depends=["TestCompras::test_criar_compra"])
    def test_obter_compra(self, auth_client):
        compra_id = TestCompras.ids['compra_id']
        resp = auth_client.get(f'/despesas/compras/{compra_id}')
        assert resp.status_code == 200
        assert resp.get_json()['nome_mercado'] == "Supermercado Teste"

    @pytest.mark.dependency(depends=["TestCompras::test_criar_compra"])
    def test_listar_despesas_do_grupo(self, auth_client):
        grupo_id = TestCompras.ids['grupo_id']
        compra_id = TestCompras.ids['compra_id']
        resp = auth_client.get(f'/grupos/{grupo_id}/despesas')
        assert resp.status_code == 200
        assert any(d['id'] == compra_id for d in resp.get_json())

    @pytest.mark.dependency(depends=["TestCompras::test_criar_compra"])
    def test_deletar_compra(self, auth_client):
        compra_id = TestCompras.ids['compra_id']
        resp = auth_client.delete(f'/despesas/compras/{compra_id}')
        assert resp.status_code == 200
        resp = auth_client.get(f'/despesas/compras/{compra_id}')
        assert resp.status_code == 404

class TestImoveis:
    ids = {}

    @pytest.mark.dependency()
    def test_criar_imovel(self, auth_client):
        grupo_resp = auth_client.post('/grupos/', json={"nome": "Grupo de Imóveis"})
        assert grupo_resp.status_code == 201
        TestImoveis.ids['grupo_id'] = grupo_resp.get_json()['id']

        pessoa_resp = auth_client.post(
            f"/grupos/{TestImoveis.ids['grupo_id']}/pessoas", 
            json={"nome": "Inquilino", "cpf": "22222222222"}
        )
        assert pessoa_resp.status_code == 201
        TestImoveis.ids['pessoa_id'] = pessoa_resp.get_json()['id']

        imovel_data = {
            "valor": 1500.00, "data": "2025-07-18", "pagador_id": TestImoveis.ids['pessoa_id'], 
            "endereco": "Rua dos Testes, 123"
        }
        imovel_resp = auth_client.post(f"/grupos/{TestImoveis.ids['grupo_id']}/despesas/imoveis", json=imovel_data)
        assert imovel_resp.status_code == 201
        TestImoveis.ids['imovel_id'] = imovel_resp.get_json()['id']

    @pytest.mark.dependency(depends=["TestImoveis::test_criar_imovel"])
    def test_obter_imovel(self, auth_client):
        imovel_id = TestImoveis.ids['imovel_id']
        resp = auth_client.get(f'/despesas/imoveis/{imovel_id}')
        assert resp.status_code == 200
        assert resp.get_json()['endereco'] == "Rua dos Testes, 123"

    @pytest.mark.dependency(depends=["TestImoveis::test_criar_imovel"])
    def test_deletar_imovel(self, auth_client):
        imovel_id = TestImoveis.ids['imovel_id']
        resp = auth_client.delete(f'/despesas/imoveis/{imovel_id}')
        assert resp.status_code == 200
        resp = auth_client.get(f'/despesas/imoveis/{imovel_id}')
        assert resp.status_code == 404