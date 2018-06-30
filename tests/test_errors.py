from __future__ import unicode_literals

import pytest
import requests

from mercadopago import Error
from .util import MockResponse


@pytest.fixture
def res():
    return MockResponse(
        url='https://api.mercadopago.com/v1/payments/1234',
        data={'error': 'not_found', 'message': 'could not find payment with ID = 1234'}
    )


def test_error_init_with_message():
    msg = 'could not find payment'
    assert str(Error(msg)) == msg


def test_error_init_with_httperror(res):
    res.status_code = 404
    http_error = requests.HTTPError(response=res)

    error = Error(http_error)
    assert error.http_status == 404
    assert error.json_body == res.data
    assert error.code == res.data['error']
    assert str(error) == res.data['message']


def test_error_init_with_connectionerror(res):
    connection_error = requests.ConnectionError('unable to connect')

    error = Error(connection_error)
    assert error.http_status == None
    assert error.json_body == None
    assert error.code == None
    assert str(error) == 'unable to connect'
