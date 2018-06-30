from __future__ import unicode_literals

import pytest

from mercadopago.response import Response, PaginatedResponse
from .util import SpyClient, MockResponse, expect


@pytest.fixture
def c():
    client = SpyClient('XXX', 'XXX')
    client.force_authenticate()
    return client


@pytest.fixture
def res(c):
    return MockResponse(
        url=c.base_url + '/v1/payments/search',
        data={
            'paging': {'total': 20, 'limit': 10, 'offset': 0},
            'results': [{'id': id} for id in range(1, 11)]
        }
    )


def test_response_init(c, res):
    Response(c, res)


def test_response_url(c, res):
    res.url = c.base_url + '/users/me'
    assert Response(c, res).url == c.base_url + '/users/me'


def test_response_status_code(c, res):
    res.status_code = 404
    assert Response(c, res).status_code == 404


def test_response_data(c, res):
    res.data = {'foo': 'bar'}
    assert Response(c, res).data == {'foo': 'bar'}


def test_paginated_response_results(c, res):
    PaginatedResponse(c, res).results == res.data['results']


def test_paginated_response_paging(c, res):
    res.data['paging']['total'] = 20
    res.data['paging']['limit'] = 10
    res.data['paging']['offset'] = 0

    response = PaginatedResponse(c, res)
    assert response.total == 20
    assert response.limit == 10
    assert response.offset == 0


def test_response_has_next_previous(c, res):
    response = PaginatedResponse(c, res)
    assert response.has_next() is True
    assert response.has_previous() is False


def test_response_is_first_page(c, res):
    res.data['paging']['total'] = 100
    res.data['paging']['offset'] = 0

    response = PaginatedResponse(c, res)
    assert response.has_next() is True
    assert response.has_previous() is False


def test_response_is_last_page(c, res):
    res.data['paging']['total'] = 20
    res.data['paging']['limit'] = 10
    res.data['paging']['offset'] = 10

    response = PaginatedResponse(c, res)
    assert response.has_next() is False
    assert response.has_previous() is True


def test_response_next(c, res):
    res.data['paging']['total'] = 100

    response = PaginatedResponse(c, res)

    expect(c, 'GET', '/v1/payments/search', params={'offset': 10})
    response.next()


def test_response_previous(c, res):
    res.data['paging']['total'] = 100
    res.data['paging']['offset'] = 20

    response = PaginatedResponse(c, res)

    expect(c, 'GET', '/v1/payments/search', params={'offset': 10})
    response.previous()


def test_paginated_response_is_iterable(c, res):
    response = PaginatedResponse(c, res)
    assert list(iter(response)) == res.data['results']


def test_paginated_response_auto_paging_iterator(c, res):
    response = PaginatedResponse(c, res)

    res = expect(c, 'GET', '/v1/payments/search', params={'offset': 10})
    res.data = {
        'paging': {'total': 20, 'limit': 10, 'offset': 10},
        'results': [{'id': id} for id in range(11, 21)]
    }
    assert list(response.auto_paging_iter()) == [{'id': id} for id in range(1, 21)]
