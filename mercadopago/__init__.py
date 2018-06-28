from __future__ import unicode_literals

import requests


__all__ = ['Client', 'Error']


class Error(Exception):
    
    def __init__(self, cause):
        try:
            self.json_body = cause.response.json()
            self.code = self.json_body['error']
            message = self.json_body['message']
        except ValueError:
            self.json_body = None
            self.code = None
            message = 'unknown error'

        super(Error, self).__init__(message)


class API(object):
    base_path = None

    def __init__(self, client):
        self.client = client.with_base_path(self.base_path)


class CardAPI(API):
    base_path = '/v1/customers/{customer_id}/cards'

    def list(self, customer_id):
        return self.client.get('', {'customer_id': customer_id})

    def create(self, data):
        return self.client.post('', data=data)

    def get(self, customer_id, card_id):
        return self.client.get('/{card_id}', {
            'customer_id': customer_id,
            'card_id': card_id
        })

    def update(self, customer_id, card_id, data):
        return self.client.put('/{card_id}', {
            'customer_id': customer_id,
            'card_id': card_id
        }, data=data)

    def delete(self, customer_id, card_id):
        return self.client.delete('/{card_id}', {
            'customer_id': customer_id,
            'card_id': card_id
        })


class CustomerAPI(API):
    base_path = '/v1/customers'

    def create(self, data):
        return self.client.post('', data=data)

    def get(self, customer_id):
        return self.client.get('/{customer_id}', {'customer_id': customer_id})

    def update(self, customer_id, data):
        return self.client.put('/{customer_id}', {'customer_id': customer_id}, data=data)

    def search(self, data):
        return self.client.get('/search', data=data)


class IdentificationTypeAPI(API):
    base_path = '/identification_types'

    def list(self):
        return self.client.get('')


class InvoiceAPI(API):
    base_path = '/merchant_orders'

    def get(self, invoice_id):
        return self.client.get('/{invoice_id}', {'invoice_id': invoice_id})


class MerchantOrderAPI(API):
    base_path = '/merchant_orders'

    def create(self, data):
        return self.client.post('', data=data)

    def get(self, order_id):
        return self.client.get('/{order_id}', {'order_id': order_id})

    def update(self, order_id, data):
        return self.client.put('/{order_id}', {'order_id': order_id}, data=data)
    

class MerchantOrderAPI(API):
    base_path = '/merchant_orders'

    def create(self, data):
        return self.client.post('', data=data)

    def get(self, order_id):
        return self.client.get('/{order_id}', {'order_id': order_id})

    def update(self, order_id, data):
        return self.client.put('/{order_id}', {'order_id': order_id}, data=data)


class PaymentMethodAPI(API):
    base_path = '/v1/payment_methods'

    def list(self):
        return self.client.get('')


class PaymentAPI(API):
    base_path = '/v1/payments'
    
    def get(self, payment_id):
        return self.client.get('/{payment_id}', {'payment_id': payment_id})
    
    def update(self, payment_id, data):
        return self.client.put('/{payment_id}', {'payment_id': payment_id}, data=data)

    def search(self, data):
        return self.client.get('/search', data=data)


class PreferenceAPI(API):
    base_path = '/v1/preferences'

    def list(self):
        return self.client.get('')

    def get(self, preference_id):
        return self.client.get('/{preference_id}', {'preference_id': preference_id})
    
    def update(self, preference_id, data):
        return self.client.put('/{preference_id}', {'preference_id': preference_id}, data=data)



class Client(object):
    base_url = 'https://api.mercadopago.com'

    def __init__(self, client_id=None, client_secret=None, base_path=''):
        self.base_path = base_path
        self.client_id = client_id
        self.client_secret = client_secret
        self._session = requests.Session()
        self._auth = None

    def _build_url(self, path, params):
        return ''.join([
            self.base_url,
            self.base_path,
            path,
            '?access_token=' + self.access_token
        ]).format(**params)

    def is_authenticated(self):
        return bool(self._auth)

    def authenticate(self):
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }

        res = self._session.post(self.base_url + '/oauth/token', data=data)

        if res.status_code != 200:
            raise Exception('invalid credentials')

        self._auth = res.json()

    @property
    def access_token(self):
        if not self.is_authenticated():
            self.authenticate()
        return self._auth['access_token']

    def request(self, method, path, params={}, data={}):
        url = self._build_url(path, params)
        try:
            res = self._session.request(method, url, data=data)
            res.raise_for_status()
            return res
        except (requests.ConnectionError, requests.HTTPError) as e:
            raise Error(cause=e)
            

    def get(self, path, params={}, data={}):
        return self.request('GET', path, params=params, data=data)

    def post(self, path, params={}, data={}):
        return self.request('POST', path, params=params, data=data)

    def put(self, path, params={}, data={}):
        return self.request('PUT', path, params=params, data=data)

    def delete(self, path, params={}, data={}):
        return self.request('DELETE', path, params=params, data=data)

    def with_base_path(self, base_path):
        return Client(
            base_path=base_path,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )

    @property
    def cards(self):
        return CardAPI(self)

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

    def preferences(self):
        return PreferenceAPI(self)
