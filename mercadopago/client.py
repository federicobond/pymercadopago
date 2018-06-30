from __future__ import unicode_literals

import requests

from . import errors, response


class BaseClient(object):
    base_url = None

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self._session = requests.Session()
        self._auth = None

    def _request(self, method, url, **kwargs):
        try:
            res = self._session.request(method, url, **kwargs)
            res.raise_for_status()
        except (requests.ConnectionError, requests.HTTPError) as error:
            self._handle_request_error(error)

        try:
            data = res.json()
            if 'paging' in data:
                return response.PaginatedResponse(self, res)
        except ValueError:
            pass

        return response.Response(self, res)

    def request(self, method, path, path_args={}, **kwargs):
        url = self.base_url + path.format(**path_args)
        return self._request(method, url, **kwargs)

    def _handle_request_error(self, error):
        if isinstance(error, requests.HTTPError):
            status = error.response.status_code

            if status == 400:
                raise errors.BadRequestError(error)
            elif status == 401:
                raise errors.AuthenticationError(error)
            elif status == 404:
                raise errors.NotFoundError(error)

        raise errors.Error(error)

    def get(self, path, path_args={}, **kwargs):
        return self.request('GET', path, path_args=path_args, **kwargs)

    def post(self, path, path_args={}, **kwargs):
        return self.request('POST', path, path_args=path_args, **kwargs)

    def put(self, path, path_args={}, **kwargs):
        return self.request('PUT', path, path_args=path_args, **kwargs)

    def delete(self, path, path_args={}, **kwargs):
        return self.request('DELETE', path, path_args=path_args, **kwargs)

    def for_base_path(self, base_path, path_args={}):
        return ClientProxy(self, base_path, path_args)


class ClientProxy(object):

    def __init__(self, client, base_path, path_args={}):
        self.client = client
        self.base_path = base_path
        self.path_args = path_args

    def for_base_path(self, base_path, path_args={}):
        return ClientProxy(self.client, base_path, path_args)

    def _merge_path_args(self, path_args):
        args = {}
        args.update(**self.path_args)
        args.update(**path_args)
        return args

    def get(self, path='', path_args={}, **kwargs):
        return self.client.get(
            self.base_path + path,
            self._merge_path_args(path_args),
            **kwargs
        )

    def post(self, path='', path_args={}, **kwargs):
        return self.client.post(
            self.base_path + path,
            self._merge_path_args(path_args),
            **kwargs
        )

    def put(self, path='', path_args={}, **kwargs):
        return self.client.put(
            self.base_path + path,
            self._merge_path_args(path_args),
            **kwargs
        )

    def delete(self, path='', path_args={}, **kwargs):
        return self.client.delete(
            self.base_path + path,
            self._merge_path_args(path_args),
            **kwargs
        )
