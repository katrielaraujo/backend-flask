def test_register(test_client):
    response = test_client.post('/register', json={
        'email': 'teste@example.com',
        'senha': 'senha123'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Usuário registrado com sucesso.'


def test_register_existing_user(test_client):
    test_client.post('/register', json={
        'email': 'teste@example.com',
        'senha': 'senha123'
    })
    response = test_client.post('/register', json={
        'email': 'teste@example.com',
        'senha': 'senha123'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Usuário já registrado.'


def test_login(test_client):
    test_client.post('/register', json={
        'email': 'teste@example.com',
        'senha': 'senha123'
    })
    response = test_client.post('/login', json={
        'email': 'teste@example.com',
        'senha': 'senha123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json


def test_login_invalid_credentials(test_client):
    response = test_client.post('/login', json={
        'email': 'inexistente@example.com',
        'senha': 'senha123'
    })
    assert response.status_code == 401
    assert response.json['message'] == 'Credenciais inválidas.'
