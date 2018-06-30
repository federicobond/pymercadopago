from __future__ import unicode_literals


class API(object):
    _base_path = None

    def __init__(self, client, path_args={}):
        self._client = client.for_base_path(self._base_path, path_args)

    def __repr__(self):
        return '<{} at {}>'.format(self.__class__.__name__, self._base_path)


class RetrievableAPIResource(API):

    def get(self, id):
        return self._client.get('/{id}', {'id': id})


class CreatableAPIResource(API):

    def create(self, **data):
        return self._client.post(json=data)


class UpdatableAPIResource(API):

    def update(self, id, **data):
        return self._client.put('/{id}', {'id': id}, json=data)


class DeletableAPIResource(API):

    def delete(self, id):
        return self._client.delete('/{id}', {'id': id})


class ListableAPIResource(API):

    def list(self, **params):
        return self._client.get(params=params)


class SearchableAPIResource(API):

    def search(self, **params):
        return self._client.get('/search', params=params)
