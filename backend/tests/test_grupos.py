import pytest


class TestGrupos:
    ids = {}

    @pytest.mark.dependency()
    def test_criar_grupo(self, auth_client):
        resp = auth_client.post('/grupos/',
                                json={"nome": "Viagem de Férias"})     
        assert resp.status_code == 201
        data = resp.get_json()
        TestGrupos.ids['grupo_id'] = data['id']

    @pytest.mark.dependency(depends=["TestGrupos::test_criar_grupo"])
    def test_obter_grupo(self, auth_client):
        grupo_id = TestGrupos.ids['grupo_id']
        resp = auth_client.get(f'/grupos/{grupo_id}')
        assert resp.status_code == 200
        assert resp.get_json()['id'] == grupo_id

    @pytest.mark.dependency(depends=["TestGrupos::test_criar_grupo"])
    def test_atualizar_grupo(self, auth_client):
        grupo_id = TestGrupos.ids['grupo_id']
        resp = auth_client.put(f'/grupos/{grupo_id}',
                               json={"nome": "Viagem de Férias 2025"})
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


class TestGrupoPermissions:
    ids = {}

    @pytest.mark.dependency()
    def test_setup_cenario_permissoes(self, auth_client, auth_client_B):
        # Usuário A cria seu grupo
        resp_A = auth_client.post('/grupos/',
                                  json={"nome": "Grupo do Usuário A"})
        assert resp_A.status_code == 201
        TestGrupoPermissions.ids['grupo_id_A'] = resp_A.get_json()['id']
        
        # Usuário B cria seu grupo
        resp_B = auth_client_B.post('/grupos/',
                                    json={"nome": "Grupo do Usuário B"})
        assert resp_B.status_code == 201
        TestGrupoPermissions.ids['grupo_id_B'] = resp_B.get_json()['id']

    @pytest.mark.dependency(depends=["TestGrupoPermissions::test_setup_cenario_permissoes"])
    def test_outro_usuario_nao_pode_obter_grupo(self, auth_client_B):
        grupo_id = TestGrupoPermissions.ids['grupo_id_A']
        resp = auth_client_B.get(f'/grupos/{grupo_id}')
        assert resp.status_code == 403 # Proibido

    @pytest.mark.dependency(depends=["TestGrupoPermissions::test_setup_cenario_permissoes"])
    def test_outro_usuario_nao_pode_atualizar_grupo(self, auth_client_B):
        grupo_id = TestGrupoPermissions.ids['grupo_id_A']
        resp = auth_client_B.put(f'/grupos/{grupo_id}',
                                 json={"nome": "Invasão"})
        assert resp.status_code == 403

    @pytest.mark.dependency(depends=["TestGrupoPermissions::test_setup_cenario_permissoes"])
    def test_outro_usuario_nao_pode_deletar_grupo(self, auth_client_B):
        grupo_id = TestGrupoPermissions.ids['grupo_id_A']
        resp = auth_client_B.delete(f'/grupos/{grupo_id}')
        assert resp.status_code == 403
    
    @pytest.mark.dependency(depends=["TestGrupoPermissions::test_setup_cenario_permissoes"])
    def test_listar_grupos_mostra_apenas_os_seus(self, auth_client_B):
        grupo_id_A = TestGrupoPermissions.ids['grupo_id_A']
        grupo_id_B = TestGrupoPermissions.ids['grupo_id_B']

        resp_B = auth_client_B.get('/grupos/')
        assert resp_B.status_code == 200
        
        lista_grupos_B = resp_B.get_json()
        
        # Verifica que a lista do Usuário B tem exatamente 1 grupo
        assert len(lista_grupos_B) == 1
        # Verifica que o grupo na lista é o dele
        assert lista_grupos_B[0]['id'] == grupo_id_B
        # Verifica que o grupo do Usuário A NÃO está na lista dele
        assert not any(g['id'] == grupo_id_A for g in lista_grupos_B)
        