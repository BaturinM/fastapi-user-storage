def test_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    assert response.json()[0]['email'] == 'fake@test.com'
