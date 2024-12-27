import os
from models import User
from app import create_app
import pytest


@pytest.fixture(scope='module')
def test_client():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client

@pytest.fixture(scope='module')
def db_session():
    session = db.session()
    yield session

@pytest.fixture(scope='module')
def valid_user():
    valid_user = User(
            username="test",
            email="test@gmail.com",
            password="test1234"
    )
    return valid_user
