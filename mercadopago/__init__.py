from __future__ import unicode_literals

from .api import Client
from .errors import (
    Error,
    AuthenticationError,
    NotFoundError,
    BadRequestError
)

__version__ = '0.1.4'
