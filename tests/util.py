from __future__ import unicode_literals

import requests

from mercadopago import Client


class MockHTTPError(requests.HTTPError):

    def __init__(self, response):
        super(MockHTTPError, self).__init__()
        self.response = response


class MockResponse(dict):

    def __init__(self, **kwargs):
        self.status_code = 200
        self.data = {}

        for key, value in kwargs.items():
            self[key] = value

    def __getattr__(self, value):
        return self.get(value)

    def __setattr__(self, key, value):
        self[key] = value

    def raise_for_status(self):
        if self.status_code >= 400:
            raise MockHTTPError(self)

    def json(self):
        return self.data


class SpySession(object):

    def __init__(self):
        self.expected = []
        self.returned = []

    def expect(self, *args, **kwargs):
        self.expected.append((args, kwargs))
        res = MockResponse(url=args[1])
        self.returned.append(res)
        return res

    def get(self, *args, **kwargs):
        return self.request('GET', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.request('POST', *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.request('PUT', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.request('DELETE', *args, **kwargs)

    def request(self, *args, **kwargs):
        if not self.expected:
            raise ValueError('did not expect any requests, received %s, %s' % (args, kwargs))

        exp = self.expected.pop(0)
        res = self.returned.pop(0)

        if exp != (args, kwargs):
            raise ValueError('expected:\n  %s\nreceived:\n  %s' % (exp, (args, kwargs)))

        return res


class SpyClient(Client):

    def __init__(self, *args, **kwargs):
        super(SpyClient, self).__init__(*args, **kwargs)
        self._session = SpySession()

    def force_authenticate(self):
        # just fill the _auth variable with something that has an access token
        self._auth = {'access_token': 'XXX'}


def expect(client, *args, **kwargs):
    # add implicit access_token if we are given an authenticated client
    if client._auth:
        if 'params' not in kwargs:
            kwargs['params'] = {}
        kwargs['params']['access_token'] = 'XXX'

    # mangle url so that we can write relative paths but compare against
    # the absolute  url
    url = client.base_url + args[1]
    args = (args[0], url) + args[2:]

    return client._session.expect(*args, **kwargs)
