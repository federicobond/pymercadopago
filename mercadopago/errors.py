from __future__ import unicode_literals
from builtins import str


class Error(Exception):

    def __init__(self, cause_or_message):
        if isinstance(cause_or_message, str):
            super(Error, self).__init__(cause_or_message)
            return

        cause = cause_or_message

        self.http_status = None
        self.json_body = None
        self.code = None

        res = cause.response
        if res:
            try:
                self.http_status = res.status_code
                self.json_body = res.json()
                self.code = self.json_body['error']
                message = self.json_body['message']
            except (KeyError, ValueError):
                message = str(cause)
        else:
            message = str(cause)

        super(Error, self).__init__(message)


class AuthenticationError(Error):
    pass


class NotFoundError(Error):
    pass


class BadRequestError(Error):
    pass
