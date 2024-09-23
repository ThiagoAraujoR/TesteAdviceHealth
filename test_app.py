import pytest
from flask import Flask
from models.car_owner import db, Owner, Car
from app import app # Altera o nome da importação

@pytest.fixture
def app_init():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Usar banco de dados em memória para testes
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app_init):
    return app_init.test_client()  # Ajusta para usar app_init

def test_add_owner(client):
    response = client.post('/add_owner', json={"name": "Test", "is_sale_opportunity": True})
    assert response.status_code == 200
    assert b"Success" in response.data

def test_add_car(client):
    owner_id = 1
    response = client.post('/add_car', json={"color": "blue", "model": "sedan", "owner_id": owner_id})
    assert response.status_code == 200
    assert b"select a valid owner" in response.data

def test_get_owners(client):
    client.post('/add_owner', json={"name": "Test", "is_sale_opportunity": True})
    response = client.get('/owners')
    assert response.status_code == 200
    assert len(response.json) > 0

def test_get_owner_cars(client):
    owner_id = 1
    client.post('/add_car', json={"color": "blue", "model": "sedan", "owner_id": owner_id})
    
    response = client.get(f'/get_owner_cars/{owner_id}')
    assert response.status_code == 404

def test_update_owner_sale_opportunity(client):
    owner_id = 1
    
    response = client.patch(f'/update_owner/{owner_id}', json={"is_sale_opportunity": False})
    assert response.status_code == 404
    assert b'404 Not Found' in response.data

def test_delete_car(client):
    car_id = 1

    response = client.delete(f'/delete_car/{car_id}')
    assert response.status_code == 404
    assert b'404 Not Found' in response.data

    response = client.get(f'/get_car/{car_id}')
    assert response.status_code == 404

def test_get_owner_info(client):
    owner_id = 1

    response = client.get(f'/get_owner_info/{owner_id}')
    assert response.status_code == 404
    assert b'404 Not Found' in response.data