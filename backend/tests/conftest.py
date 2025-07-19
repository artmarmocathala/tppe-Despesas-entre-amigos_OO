import pytest
from app import create_app
from database import db as _db
from models import Usuario


# instancia de app pros testes
@pytest.fixture(scope='session')
def app():
    # SQLite p testes isolados
    app = create_app('sqlite:///:memory:')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'

    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


# Cliente de testes p http
@pytest.fixture(scope='session')
def client(app):
    with app.test_client() as client:
        yield client


# Cliente p testes logados
@pytest.fixture(scope='class')
def auth_client(app, client):
    with app.app_context():
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()

    user_data = {
        "nome": "Test User",
        "email": "test@example.com",
        "senha": "password123"
    }
    resp_create = client.post('/usuarios/', json=user_data)
    assert resp_create.status_code == 201, "Falha ao criar usuário de teste na fixture."

    login_data = {"email": "test@example.com", "senha": "password123"}
    resp_login = client.post('/login', json=login_data)
    assert resp_login.status_code == 200, "Falha ao fazer login na fixture."

    token = resp_login.get_json()['token']
    client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'

    yield client 
    if 'HTTP_AUTHORIZATION' in client.environ_base:
        del client.environ_base['HTTP_AUTHORIZATION']


