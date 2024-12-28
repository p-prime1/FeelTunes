from app import create_app
import os

def test_home_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        assert b"Welcome to FeelTune" in response.data
        assert b"Get Started" in response.data

def test_home_page_with_fixture(test_client):
    response = test_client.get('/')
    assert response.status_code == 200


def test_about_page_with_fixture(test_client):
    response = test_client.get('/about/')
    assert response.status_code == 200
    assert b"About FeelTune" in response.data
    assert b"Get Started Now" in response.data


def test_about_page_post_with_fixture(test_client):
    response = test_client.post('/about/')
    assert response.status_code == 405
    assert b"About FeelTune" not in response.data


def test_home_page_post_with_fixture(test_client):
    response = test_client.post('/')
    assert response.status_code == 405
    assert b"Welcome to FeelTune" not in response.data
