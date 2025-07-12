def test_criar_listar_obter_atualizar_deletar_usuario(client):
    resp = client.post(
        '/usuarios',
        json={
            "nome": "Alice",
            "email": "alice@example.com",
            "senha": "123456",
            "is_superuser": True
        }
    )
    assert resp.status_code == 201
    usuario = resp.get_json()
    usuario_id = usuario['id']
    assert usuario['nome'] == "Alice"
    assert usuario['is_superuser'] is True

    resp = client.get('/usuarios')
    assert resp.status_code == 200
    usuarios = resp.get_json()
    assert any(u['id'] == usuario_id for u in usuarios)

    resp = client.get(f'/usuarios/{usuario_id}')
    assert resp.status_code == 200
    usuario = resp.get_json()
    assert usuario['email'] == "alice@example.com"

    resp = client.put(
        f'/usuarios/{usuario_id}',
        json={"nome": "Alice Nova", "is_superuser": False}
    )
    assert resp.status_code == 200
    usuario = resp.get_json()
    assert usuario['nome'] == "Alice Nova"
    assert usuario['is_superuser'] is False

    resp = client.delete(f'/usuarios/{usuario_id}')
    assert resp.status_code == 200
    resp = client.get(f'/usuarios/{usuario_id}')
    assert resp.status_code == 404
