import pytest
from flask import g
from flaskr.models import User, Post


def test_user_repr(client):
    with client:
        client.get('/')
        repr_user = repr(g.session.query(User).filter_by(id=1).first())
    assert repr_user.startswith('<User(')
    assert repr_user.endswith(')>')
    assert 'username=test' in repr_user


def test_post_repr(client):
    with client:
        client.get('/')
        repr_post = repr(g.session.query(Post).filter_by(id=1).first())
    assert repr_post.startswith('<Post(')
    assert repr_post.endswith(')>')
    assert 'author=test' in repr_post


def test_rollback(app):
    with pytest.raises(SystemExit):
        with app.test_client() as client:
            client.get('/')
            count = g.session.query(User.id).count()
            g.session.add(User(username='bogus', password='bogus'))
            raise SystemExit(1)
    with app.test_client() as client:
        client.get('/')
        assert count == g.session.query(User.id).count()


def test_missing_session(client):
    with client:
        client.get('/')
        g.pop('session', None)
    #teardown, nothing to assert
