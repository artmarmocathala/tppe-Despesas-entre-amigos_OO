def test_adicionar_listar_pessoa(client):
    resp = client.post(
        '/grupos', json={"nome": "Grupo Pessoas", "max_pessoas": 2}
    )
    grupo_id = resp.get_json()['id']
    resp = client.post(
        f'/grupos/{grupo_id}/pessoas',
        json={"nome": "Maria", "cpf": "12345678901"}
    )
    assert resp.status_code == 201
    pessoa_id = resp.get_json()['id']
    resp = client.get(f'/grupos/{grupo_id}/pessoas')
    pessoas = resp.get_json()
    assert any(p['id'] == pessoa_id for p in pessoas)

    resp = client.get(f'/pessoas/{pessoa_id}')
    assert resp.status_code == 200
    pessoa = resp.get_json()
    assert pessoa['id'] == pessoa_id
    assert pessoa['nome'] == "Maria"
    assert pessoa['cpf'] == "12345678901"


def test_deletar_pessoa(client):
    resp = client.post('/grupos', json={"nome": "Grupo Del"})
    grupo_id = resp.get_json()['id']
    pessoa = client.post(
        f'/grupos/{grupo_id}/pessoas',
        json={"nome": "Ana", "cpf": "11122233344"}
    ).get_json()
    pessoa_id = pessoa['id']
    resp = client.delete(f'/pessoas/{pessoa_id}')
    assert resp.status_code == 200
