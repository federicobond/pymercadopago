from __future__ import unicode_literals

import pytest

from mercadopago import Client, errors
from .util import SpyClient, expect


@pytest.fixture
def c():
    return SpyClient('XXX', 'XXX')


def test_client_init_with_credentials():
    Client('XXX', 'XXX')


def test_client_authentication(c):
    assert c.is_authenticated() is False

    res = expect(c, 'POST', '/oauth/token',
                 data={'client_id': 'XXX', 'client_secret': 'XXX', 'grant_type': 'client_credentials'})

    res.status_code = 200
    res.data = {'access_token': 'YYY'}

    c.authenticate()
    assert c.is_authenticated() is True


def test_access_token(c):
    res = expect(c, 'POST', '/oauth/token',
                 data={'client_id': 'XXX', 'client_secret': 'XXX', 'grant_type': 'client_credentials'})

    res.status_code = 200
    res.data = {'access_token': 'YYY'}

    assert c.access_token == 'YYY'


def test_http_verbs(c):
    c.force_authenticate()

    expect(c, 'GET', '/payments')
    c.get('/payments')

    expect(c, 'POST', '/payments')
    c.post('/payments')

    expect(c, 'PUT', '/payments')
    c.put('/payments')

    expect(c, 'DELETE', '/payments')
    c.delete('/payments')


def test_error_handling(c):
    c.force_authenticate()

    res = expect(c, 'GET', '/payments')
    res.status_code = 400

    with pytest.raises(errors.BadRequestError):
        c.get('/payments')

    res = expect(c, 'GET', '/payments')
    res.status_code = 401

    with pytest.raises(errors.AuthenticationError):
        c.get('/payments')

    res = expect(c, 'GET', '/payments')
    res.status_code = 404

    with pytest.raises(errors.NotFoundError):
        c.get('/payments')

    res = expect(c, 'GET', '/payments')
    res.status_code = 500

    with pytest.raises(errors.Error):
        c.get('/payments')
