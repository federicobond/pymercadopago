from __future__ import unicode_literals

try:
    # Python 3
    from urllib.parse import urlparse, parse_qs
except ImportError:
    # Python 2
    from urlparse import urlparse, parse_qs


class Response(object):
    """This is the main class for all responses returned by the library.

    Args:
        url: The URL that was requested
        status_code: The HTTP status code of the response
        data: The JSON object returned by the API
    """

    def __init__(self, client, response):
        self._client = client
        self._response = response
        self.url = response.url
        self.status_code = response.status_code
        self.data = response.json()


class PaginatedResponse(Response):

    @property
    def results(self):
        return self.data['results']

    @property
    def total(self):
        return self.data['paging']['total']

    @property
    def limit(self):
        return self.data['paging']['limit']

    @property
    def offset(self):
        return self.data['paging']['offset']

    def has_next(self):
        return self.offset + self.limit < self.total

    def has_previous(self):
        return self.offset > 0

    def next(self):
        offset = min(self.offset + self.limit, self.total)
        return self._request_with_params(offset=offset)

    def previous(self):
        offset = max(0, self.offset - self.limit)
        return self._request_with_params(offset=offset)

    def _request_with_params(self, **params):
        url = urlparse(self.url)
        query = parse_qs(url.query)
        query.update(params)

        return self._client.get(url.path, params=query)

    def __iter__(self):
        return iter(self.results)

    def auto_paging_iter(self):
        req = self

        for result in req:
            yield result

        while req.has_next():
            req = req.next()
            for result in req:
                yield result
