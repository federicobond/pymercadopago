PyMercadoPago
=============

.. image:: https://img.shields.io/pypi/v/pymercadopago.svg
   :target: https://pypi.python.org/pypi/pymercadopago
   :alt: Latest Version

.. image:: https://travis-ci.org/federicobond/pymercadopago.svg?branch=master
   :target: https://travis-ci.org/federicobond/pymercadopago


PyMercadoPago is user-friendly library to interact with the MercadoPago API.

It's compatible with Python 2 and 3.

To install it from PyPI, simply run::

    pip install pymercadopago

If you haven't done so already, obtain your ``CLIENT_ID`` and ``CLIENT_SECRET`` `here
<https://www.mercadopago.com/mla/account/credentials?type=basic>`_.

Quickstart
----------

Create a new ``mercadopago.Client`` instance and pass it your credentials:

.. highlight:: python

::

    import mercadopago

    CLIENT_ID = 'XXX'
    CLIENT_SECRET = 'XXX'

    mp = mercadopago.Client(CLIENT_ID, CLIENT_SECRET)


You can navigate the full API from the client methods. Try running the above
code in a Python shell and explore them.

::

    # Get the invoice with ID 1234
    mp.invoices.get('1234')


::

    # Get the current user account balance
    mp.users.account_balance()


::

    # Create a new customer instance
    mp.customers.create(
      first_name='Federico'
      last_name='Bond',
      # ...
    )


In general, assuming ``mp`` is a ``mercadopago.Client`` instance and there is
an endpoint documented at (for example) ``/customers`` or ``/v1/customers``,
you can do:

``mp.customers.list()``
    List all customers. Pass pagination parameters via keyword arguments.

``mp.customers.create(**data)``
    Create a new Customer.

``mp.customers.delete(id)``
    Delete a Customer.

``mp.customers.update(**data)``
    Update a Customer, include ``ìd`` in your keword arguments.

``mp.customers.search(**params)``
    Search for customers matching params.

Not all methods are available for all resources, and some additional methods
are provided for convenience. To learn more, check out the official docs and
the code from the ``mercadopago.api`` module.

Nested resources like ``/v1/customers/:id/cards`` are usually accessed by
following the resource paths: ``mp.customers.cards(id).list()``

All methods return a ``mercadopago.response.Response`` object if successful
(HTTP status code in the 2XX range) or raise a ``mercadopago.errors.Error`` or
one of its subclasses otherwise.

Response
--------

Attributes
    :url The requested URL.
    :status_code: The HTTP status_code returned by the API.
    :data: The JSON response returned by the API, as a standard Python dict/list.


If MercadoPago returns a response with pagination information, a
``mercadopago.response.PaginatedResponse`` will be returned instead.

Error
-----

Attributes
    :http_status: The HTTP status_code returned by the API, if applicable.
    :code: The error code returned by the API, if applicable.
    :json_data: The full JSON response returned by the API, if applicable.


The library will raise specific subclasses of ``mercadopago.errors.Error``
according to the HTTP status code returned:

:400: ``mercadopago.errors.BadRequestError``
:401: ``mercadopago.errors.AuthorizationError``
:404: ``mercadopago.errors.NotFoundError``


Running the tests
-----------------

Make sure tests pass before contributing a bugfix or a new feature.
To run the test suite, execute this in your terminal:

::

    python setup.py test


This will execute the tests with your default Python interpreter.
Use ``tox`` to run the tests in all supported Python versions.


----------

For more information about the API, refer to the `official docs 
<https://www.mercadopago.com.ar/developers/en/api-docs/>`_.


Author
------

Federico Bond

License
-------

Apache-2.0
