import pytest
from flask import g
from flaskr.models import User
from flask_login import current_user


def test_register(client):
    assert client.get('/auth/register').status_code == 200
    with client:
        response = client.post(
            'auth/register',
            data={'username': 'a', 'password': 'a', 'password2': 'a'}
        )
        assert g.session.query(User).filter_by(username = 'a').first()
    assert 'http://localhost/auth/login' == response.headers['Location']


def test_register_validate_input(client):
    response = client.post(
        '/auth/register',
        data={'username': 'test', 'password': 'test', 'password2': 'test'}
    )
    assert b'Please use a different username' in response.data


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    with client:
        response = auth.login()
        assert current_user.username == 'test'
    assert 'http://localhost/' == response.headers['Location']
    

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Invalid Username or Password'),
    ('test', 'a', b'Invalid Username or Password'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    with client:
        auth.login()
        assert current_user.username == 'test'
        auth.logout()
        assert current_user.is_anonymous


def test_is_safe_url(client):
    response = client.post(
            '/auth/login?next=http://www.example.com/',
        data={'username': 'test', 'password': 'test'}
    )
    assert response.status_code == 400


def test_is_authenticated(client, auth):
    auth.login()
    response = client.get('/auth/register')
    assert 'http://localhost/' == response.headers['Location']
    response = client.get('/auth/login')
    assert 'http://localhost/' == response.headers['Location']
