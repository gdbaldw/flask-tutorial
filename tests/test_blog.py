import pytest
from flask import g
from flaskr.models import User, Post


def test_index(client, auth):
    response = client.get('/')
    assert b'Sign In' in response.data
    assert b'Sign Up' in response.data

    auth.login()
    response = client.get('/')
    assert b'Sign Out' in response.data
    assert b'test title' in response.data
    assert b'on 2018-01-01' in response.data
    assert b'test\nbody' in response.data
    assert b'href="/1/update"' in response.data


@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'].startswith('http://localhost/auth/login')


def test_author_required(app, client, auth):
    with client:
        client.get('/')
        g.session.query(Post).filter_by(id=1).first().author_id = 2

    auth.login()
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    assert b'href="/1/update"' not in client.get('/').data


@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    auth.login()
    assert client.get('/create').status_code == 200

    with client:
        client.post('/create', data={'title': 'created', 'body': ''})
        assert g.session.query(Post.id).count() == 2


def test_update(client, auth, app):
    auth.login()
    assert client.get('/1/update').status_code == 200

    with client:
        client.post('/1/update', data={'title': 'updated', 'body': ''})
        assert g.session.query(Post).filter_by(id=1).first().title == 'updated'
        response = client.post('/1/update', data={'delete': True})
    assert response.headers['Location'] == 'http://localhost/1/delete'


def test_delete(client, auth, app):
    auth.login()

    with client:
        client.get('/1/delete')
        assert g.session.query(Post).filter_by(id=1).first()
        response = client.post('/1/delete', data={'delete': True})
        assert not g.session.query(Post).filter_by(id=1).first()
    assert response.headers['Location'] == 'http://localhost/'
