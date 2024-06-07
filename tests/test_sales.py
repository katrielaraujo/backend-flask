def get_token(test_client):
    test_client.post('/register', json={
        'email': 'teste@example.com',
        'senha': 'senha123'
    })
    response = test_client.post('/login', json={
        'email': 'teste@example.com',
        'senha': 'senha123'
    })
    return response.json['access_token']


def test_add_sale(test_client):
    token = get_token(test_client)
    response = test_client.post('/sales', json={
        'nome_cliente': 'Cliente1',
        'produto': 'Produto1',
        'valor': 100.0,
        'data_venda': '01-01-2023'
    }, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    assert response.json['message'] == 'Venda adicionada com sucesso.'


def test_get_sales(test_client):
    token = get_token(test_client)
    test_client.post('/sales', json={
        'nome_cliente': 'Cliente1',
        'produto': 'Produto1',
        'valor': 100.0,
        'data_venda': '01-01-2023'
    }, headers={'Authorization': f'Bearer {token}'})
    response = test_client.get('/sales', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert len(response.json) > 0


def test_edit_sale(test_client):
    token = get_token(test_client)
    test_client.post('/sales', json={
        'nome_cliente': 'Cliente1',
        'produto': 'Produto1',
        'valor': 100.0,
        'data_venda': '01-01-2023'
    }, headers={'Authorization': f'Bearer {token}'})
    response = test_client.put(f'/sales/{1}', json={
        'nome_cliente': 'Cliente Atualizado',
        'produto': 'Produto Atualizado',
        'valor': 150.0,
        'data_venda': '01-02-2023'
    }, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'Venda atualizada com sucesso.'


def test_delete_sale(test_client):
    token = get_token(test_client)
    test_client.post('/sales', json={
        'nome_cliente': 'Cliente1',
        'produto': 'Produto1',
        'valor': 100.0,
        'data_venda': '01-01-2023'
    }, headers={'Authorization': f'Bearer {token}'})
    response = test_client.delete('/sales/1', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'Venda deletada com sucesso.'
