import pytest
from app import create_app
from database import db as _db


# instancia de app pros testes
@pytest.fixture(scope='session')
def app():
    # SQLite p testes isolados
    app = create_app('sqlite:///:memory:')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_ECHO'] = False

    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


# Cliente de testes p http
@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


# Limpar o banco antes dos testes
@pytest.fixture(autouse=True)
def clean_db(app):
    with app.app_context():
        yield
        _db.session.remove()
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()
