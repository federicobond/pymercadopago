PyMercadoPago
=============

.. image:: https://img.shields.io/pypi/v/pymercadopago.svg
   :target: https://pypi.python.org/pypi/pymercadopago
   :alt: Latest Version

.. image:: https://travis-ci.org/federicobond/pymercadopago.svg?branch=master
   :target: https://travis-ci.org/federicobond/pymercadopago


PyMercadoPago is user-friendly library to interact with the MercadoPago API.

It's compatible with both Python 2 and 3.

To install it from PyPI, simply run::

    pip install pymercadopago

If you haven't done so already, obtain your ``CLIENT_ID`` and ``CLIENT_SECRET`` `here
<https://www.mercadopago.com/mla/account/credentials?type=basic>`_.

Quickstart
----------

Create a new ``mercadopago.Client`` instance and pass it your credentials:

.. code-block:: python

    import mercadopago

    CLIENT_ID = 'XXX'
    CLIENT_SECRET = 'XXX'

    mp = mercadopago.Client(CLIENT_ID, CLIENT_SECRET)


You can navigate the full API from the client methods. Try running the above
code in a Python shell and explore them.

.. code-block:: python

    # Get the invoice with ID 1234
    mp.invoices.get('1234')


.. code-block:: python

    # Get the current user account balance
    mp.users.account_balance()


.. code-block:: python

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
    Update a Customer, include ``ìd`` in your keyword arguments.

``mp.customers.search(**params)``
    Search for customers matching params.

Not all methods are available for all resources, and some additional
convenience methods have been added to some. To learn more, check out the
official docs and/or the code from the ``mercadopago.api`` module.

Nested resources like are usually accessed by following the corresponding
resource paths. For example:

.. code-block:: python

  # GET /v1/customers/:id/cards
  # ----
  mp.customers.cards(id).list()


All methods return a ``Response`` object if successful (HTTP status code in the
2XX range) or raise an instance of ``mercadopago.Error`` otherwise.

Response
--------

Every API call you make will return a ``Response`` instance with the following
attributes:

===============  ==============================================
Attribute        Description
===============  ==============================================
``status_code``  The HTTP status_code returned by the API.
``data``         The decoded JSON response returned by the API.
``url``          The requested URL.
===============  ==============================================

If MercadoPago returns a response with pagination information, a
``PaginatedResponse`` will be returned instead. Paginated responses have the
following additional methods:

``response.total``
    Total amount of records in this collection.

``response.limit``
    Maximum number of records for this page.

``response.offset``
    Number of records skipped to reach this page.

``response.results``
    List of records in this request. This is different from ``.data`` which
    contains the full body of the response, with the pagination info.

``response.has_prev()``
    Whether there are any preceding pages.

``response.has_next()``
    Whether there are any following pages.

``response.prev()``
    Requests the previous page and returns a ``PaginatedResponse``.

``response.next()``
    Requests the next page and returns a ``PaginatedResponse``.

``response.auto_paging_iter()``
    Returns a generator of records that will automatically request new pages
    when necessary.


Error
-----

If there is a connection error or the HTTP response contains a non-2XX status
code, the method will raise an instance of ``mercadopago.Error``.

===============  ==========================================================
Attribute        Description
===============  ==========================================================
``http_status``  The HTTP status_code returned by the API, if applicable.
``code``         The error code returned by the API, if applicable.
``json_data``    The full JSON response returned by the API, if applicable.
===============  ==========================================================

The specific subclass raised depends on the HTTP status code.

====== ==================================
Status Class
====== ==================================
400    ``mercadopago.BadRequestError``
401    ``mercadopago.AuthorizationError``
404    ``mercadopago.NotFoundError``
\*     ``mercadopago.Error``
====== ==================================


Running the tests
-----------------

Make sure tests pass before contributing a bugfix or a new feature.
To run the test suite, execute this in your terminal::

    python setup.py test


This will execute the tests with your default Python interpreter.
Use ``tox`` to run the tests in all supported Python versions.


To Do
-----

* Implement idempotency headers in POST/PUT requests.
* Implement retry request from error.


----------

For more information about the API, refer to the `official docs 
<https://www.mercadopago.com.ar/developers/en/api-docs/>`_.


Author
------

Federico Bond

License
-------

Apache-2.0
