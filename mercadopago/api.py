from __future__ import unicode_literals

import requests

from . import errors
from .abstract_api import (
    API,
    CreatableAPIResource,
    DeletableAPIResource,
    ListableAPIResource,
    RetrievableAPIResource,
    SearchableAPIResource,
    UpdatableAPIResource,
)
from .client import BaseClient
from .response import Response


class CardAPI(ListableAPIResource, RetrievableAPIResource, CreatableAPIResource,
              UpdatableAPIResource, DeletableAPIResource):
    _base_path = '/v1/customers/{customer_id}/cards'

    def __init__(self, client, customer_id):
        super(CardAPI, self).__init__(
            client, path_args={'customer_id': customer_id})


class CardTokenAPI(API):
    _base_path = '/v1/card_tokens'

    def create(self, public_key, **data):
        return self._client.post('/', params={'public_key': public_key}, json=data)

    def get(self, id, public_key):
        return self._client.get('/{id}', {'id': id}, params={'public_key': public_key})

    def update(self, id, public_key, **data):
        return self._client.put('/{id}', {'id': id}, params={'public_key': public_key}, json=data)


class CustomerAPI(RetrievableAPIResource, CreatableAPIResource,
                  UpdatableAPIResource, DeletableAPIResource,
                  SearchableAPIResource):
    _base_path = '/v1/customers'

    def cards(self, id):
        return CardAPI(self._client, id)


class IdentificationTypeAPI(ListableAPIResource):
    _base_path = '/identification_types'


class InvoiceAPI(RetrievableAPIResource):
    _base_path = '/v1/invoices'


class MerchantOrderAPI(RetrievableAPIResource, CreatableAPIResource,
                       UpdatableAPIResource):
    _base_path = '/merchant_orders'


class PaymentMethodAPI(ListableAPIResource):
    _base_path = '/v1/payment_methods'

    def card_issuers(self, payment_method_id):
        return self._client.get('/card_issuers', params={'payment_method_id': payment_method_id})

    def installments(self, **data):
        return self._client.get('/installments', params=data)


class PaymentAPI(RetrievableAPIResource, CreatableAPIResource,
                 UpdatableAPIResource, SearchableAPIResource):
    _base_path = '/v1/payments'

    def cancel(self, id):
        return self.update(id, status='cancelled')


class PlanAPI(RetrievableAPIResource, CreatableAPIResource,
              UpdatableAPIResource):
    _base_path = '/v1/plans'


class PreferenceAPI(RetrievableAPIResource, CreatableAPIResource,
                    UpdatableAPIResource, ListableAPIResource):
    _base_path = '/v1/preferences'


class PreapprovalAPI(CreatableAPIResource, UpdatableAPIResource,
                     SearchableAPIResource):
    _base_path = '/preapproval'

    def get(self, id):
        # NOTE: this is actually performing a search with ID and mangling
        # the response data to conform to a single object format.
        # There is no method to retrieve a preapproval by ID at the moment.

        res = self.search(id=id)

        if not res.data['results']:
            raise errors.NotFoundError('could not find preapproval with ID = %s' % id)

        res = Response(self._client.client, res._response)  # pylint: disable=protected-access
        res.data = res.data['results'][0]

        return res

    def cancel(self, id):
        return self.update(id, status='cancelled')

    def pause(self, id):
        return self.update(id, status='paused')


class UsersAPI(API):
    _base_path = '/users'

    def me(self):
        return self._client.get('/me')

    def account_balance(self, user_id=None):
        if user_id is None:
            user_id = self.me().data['id']

        return self._client.get('/{user_id}/mercadopago_account/balance', {
            'user_id': user_id
        })


class BankReportAPI(ListableAPIResource):
    _base_path = '/v1/account/bank_report'

    def get(self, file_name):
        return self._client.get('/{file_name}', {'file_name': file_name})

    def create(self, **data):
        return self._client.post(json=data)


class SettlementReportAPI(SearchableAPIResource):
    _base_path = '/v1/account/settlement_report'

    def get(self, file_name):
        return self._client.get('/{file_name}', {'file_name': file_name})

    def config_new(self, **data):
        return self._client.post('/config', json=data)

    def config_update(self, **data):
        return self._client.put('/config', json=data)

    def config_get(self):
        return self._client.get('/config')

    def schedule_set(self, **data):
        return self._client.post('/schedule', json=data)

    def schedule_delete(self):
        return self._client.delete('/schedule')


class AccountAPI(API):
    _base_path = '/v1/account'

    @property
    def bank_report(self):
        return BankReportAPI(self._client)

    @property
    def settlement_report(self):
        return SettlementReportAPI(self._client)


class Client(BaseClient):
    base_url = 'https://api.mercadopago.com'

    def is_authenticated(self):
        return bool(self._auth)

    def authenticate(self):
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }

        try:
            res = self._session.post(self.base_url + '/oauth/token', data=data)
            res.raise_for_status()
        except (requests.HTTPError, requests.ConnectionError) as error:
            self._handle_request_error(error)

        self._auth = res.json()

    @property
    def access_token(self):
        if not self.is_authenticated():
            self.authenticate()
        return self._auth['access_token']

    def request(self, method, path, path_args={}, **kwargs):
        if 'params' not in kwargs:
            kwargs['params'] = {}
        kwargs['params']['access_token'] = self.access_token

        url = self.base_url + path.format(**path_args)

        return self._request(method, url, **kwargs)

    @property
    def card_tokens(self):
        return CardTokenAPI(self)

    @property
    def customers(self):
        return CustomerAPI(self)

    @property
    def identification_types(self):
        return IdentificationTypeAPI(self)

    @property
    def invoices(self):
        return InvoiceAPI(self)

    @property
    def merchant_orders(self):
        return MerchantOrderAPI(self)

    @property
    def payment_methods(self):
        return PaymentMethodAPI(self)

    @property
    def payments(self):
        return PaymentAPI(self)

    @property
    def plans(self):
        return PlanAPI(self)

    @property
    def preapprovals(self):
        return PreapprovalAPI(self)

    @property
    def preferences(self):
        return PreferenceAPI(self)

    @property
    def account(self):
        return AccountAPI(self)

    @property
    def users(self):
        return UsersAPI(self)
