from __future__ import unicode_literals

import pytest

from .util import SpyClient, expect


@pytest.fixture
def c():
    return SpyClient('XXX', 'XXX')


def test_card_tokens_get(c):
    c.force_authenticate()

    expect(c, 'GET', '/v1/card_tokens/1234',
           params={'public_key': '6789'})
    c.card_tokens.get('1234', public_key='6789')


def test_card_tokens_update(c):
    c.force_authenticate()

    expect(c, 'PUT', '/v1/card_tokens/1234',
           params={'public_key': '6789'}, json={'foo': 'bar'})
    c.card_tokens.update('1234', public_key='6789', foo='bar')


def test_card_tokens_create(c):
    c.force_authenticate()

    expect(c, 'POST', '/v1/card_tokens/',
           params={'public_key': '6789'}, json={'foo': 'bar'})
    c.card_tokens.create(public_key='6789', foo='bar')


def test_customers(c):
    c.force_authenticate()

    expect(c, 'POST', '/v1/customers', json={'foo': 'bar'})
    c.customers.create(foo='bar')

    expect(c, 'GET', '/v1/customers/1234')
    c.customers.get('1234')

    expect(c, 'PUT', '/v1/customers/1234', json={'foo': 'bar'})
    c.customers.update(id='1234', foo='bar')

    expect(c, 'GET', '/v1/customers/search', params={'field': '1234'})
    c.customers.search(field='1234')


def test_customers_cards(c):
    c.force_authenticate()

    expect(c, 'GET', '/v1/customers/1234/cards')
    c.customers.cards('1234').list()

    expect(c, 'POST', '/v1/customers/1234/cards', json={'foo': 'bar'})
    c.customers.cards('1234').create(foo='bar')

    expect(c, 'GET', '/v1/customers/1234/cards/5678')
    c.customers.cards('1234').get('5678')

    expect(c, 'PUT', '/v1/customers/1234/cards/5678', json={'foo': 'bar'})
    c.customers.cards('1234').update(id='5678', foo='bar')

    expect(c, 'DELETE', '/v1/customers/1234/cards/5678')
    c.customers.cards('1234').delete('5678')


def test_identification_types(c):
    c.force_authenticate()

    expect(c, 'GET', '/identification_types')
    c.identification_types.list()


def test_invoices(c):
    c.force_authenticate()

    expect(c, 'GET', '/v1/invoices/1234')
    c.invoices.get('1234')


def test_merchant_orders(c):
    c.force_authenticate()

    expect(c, 'GET', '/merchant_orders/1234')
    c.merchant_orders.get('1234')

    expect(c, 'POST', '/merchant_orders', json={'foo': 'bar'})
    c.merchant_orders.create(foo='bar')

    expect(c, 'PUT', '/merchant_orders/1234', json={'foo': 'bar'})
    c.merchant_orders.update(id='1234', foo='bar')


def test_payment_methods(c):
    c.force_authenticate()

    expect(c, 'GET', '/v1/payment_methods')
    c.payment_methods.list()

    expect(c, 'GET', '/v1/payment_methods/card_issuers', params={'payment_method_id': 'visa'})
    c.payment_methods.card_issuers('visa')

    expect(c, 'GET', '/v1/payment_methods/installments', params={'foo': 'bar'})
    c.payment_methods.installments(foo='bar')


def test_payments(c):
    c.force_authenticate()

    expect(c, 'GET', '/v1/payments/1234')
    c.payments.get('1234')

    expect(c, 'POST', '/v1/payments', json={'foo': 'bar'})
    c.payments.create(foo='bar')

    expect(c, 'PUT', '/v1/payments/1234', json={'foo': 'bar'})
    c.payments.update(id='1234', foo='bar')

    expect(c, 'GET', '/v1/payments/search', params={'foo': 'bar'})
    c.payments.search(foo='bar')

    expect(c, 'PUT', '/v1/payments/1234', json={'status': 'cancelled'})
    c.payments.cancel('1234')


def test_plans(c):
    c.force_authenticate()

    expect(c, 'GET', '/v1/plans/1234')
    c.plans.get('1234')

    expect(c, 'POST', '/v1/plans', json={'foo': 'bar'})
    c.plans.create(foo='bar')

    expect(c, 'PUT', '/v1/plans/1234', json={'foo': 'bar'})
    c.plans.update(id='1234', foo='bar')


def test_preferences(c):
    c.force_authenticate()

    expect(c, 'GET', '/v1/preferences/1234')
    c.preferences.get('1234')

    expect(c, 'POST', '/v1/preferences', json={'foo': 'bar'})
    c.preferences.create(foo='bar')

    expect(c, 'PUT', '/v1/preferences/1234', json={'foo': 'bar'})
    c.preferences.update(id='1234', foo='bar')

    # TODO: check if there is no search for preferences
    expect(c, 'GET', '/v1/preferences')
    c.preferences.list()


def test_preapprovals(c):
    c.force_authenticate()

    res = expect(c, 'GET', '/preapproval/search', params={'id': '1234'})
    res.data = {'paging': {}, 'results': [{'id': '1234'}]}
    c.preapprovals.get('1234')

    expect(c, 'POST', '/preapproval', json={'foo': 'bar'})
    c.preapprovals.create(foo='bar')

    expect(c, 'PUT', '/preapproval/1234', json={'foo': 'bar'})
    c.preapprovals.update(id='1234', foo='bar')

    expect(c, 'PUT', '/preapproval/1234', json={'status': 'cancelled'})
    c.preapprovals.cancel('1234')

    expect(c, 'PUT', '/preapproval/1234', json={'status': 'paused'})
    c.preapprovals.pause('1234')

    expect(c, 'GET', '/preapproval/search', params={'foo': 'bar'})
    c.preapprovals.search(foo='bar')


def test_users(c):
    c.force_authenticate()

    expect(c, 'GET', '/users/me')
    c.users.me()

    expect(c, 'GET', '/users/1234/mercadopago_account/balance')
    c.users.account_balance('1234')

    res = expect(c, 'GET', '/users/me')
    res.data = {'id': '1234'}
    expect(c, 'GET', '/users/1234/mercadopago_account/balance')
    c.users.account_balance()


def test_bank_reports(c):
    c.force_authenticate()

    expect(c, 'GET', '/v1/account/bank_report')
    c.account.bank_report.list()

    expect(c, 'GET', '/v1/account/bank_report/1234')
    c.account.bank_report.get('1234')

    expect(c, 'POST', '/v1/account/bank_report', json={'foo': 'bar'})
    c.account.bank_report.create(foo='bar')


def test_settlement_report(c):
    c.force_authenticate()

    expect(c, 'GET', '/v1/account/settlement_report/1234')
    c.account.settlement_report.get('1234')

    expect(c, 'GET', '/v1/account/settlement_report/config')
    c.account.settlement_report.config_get()

    expect(c, 'POST', '/v1/account/settlement_report/config', json={'foo': 'bar'})
    c.account.settlement_report.config_new(foo='bar')

    expect(c, 'PUT', '/v1/account/settlement_report/config', json={'foo': 'bar'})
    c.account.settlement_report.config_update(foo='bar')

    expect(c, 'POST', '/v1/account/settlement_report/schedule', json={'foo': 'bar'})
    c.account.settlement_report.schedule_set(foo='bar')

    expect(c, 'DELETE', '/v1/account/settlement_report/schedule')
    c.account.settlement_report.schedule_delete()
