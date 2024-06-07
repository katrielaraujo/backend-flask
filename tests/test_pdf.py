from tests.test_sales import get_token


def test_generate_sales_pdf(test_client):
    token = get_token(test_client)
    test_client.post('/sales', json={
        'nome_cliente': 'Cliente1',
        'produto': 'Produto1',
        'valor': 100.0,
        'data_venda': '01-01-2023'
    }, headers={'Authorization': f'Bearer {token}'})
    response = test_client.get('/sales/pdf?start_date=01-01-2023&end_date=31-12-2023',
                               headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/pdf'

