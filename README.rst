A simple API request signer
===========================

A very simple library to help generate signed requests.

INSTALLATION
------------

::

    pip install apysigner


USAGE
-----

For a **GET** request

::

    >>> import apysigner
    >>> private_key = 'UHJpdmF0ZSBLZXk='
    >>> url = 'http://www.example.com/api-endpoint?q=find+my+thing'
    >>> apysigner.get_signature(private_key, url)
    'zMxf77eY-xuORInBIA0azhxHPg2bzhsjz-huP-OuYKk='

For a **POST** request

::

    >>> import apysigner
    >>> private_key = 'UHJpdmF0ZSBLZXk='
    >>> payload = {'do': 'something', 'name': 'Johnny'}
    >>> url = 'http://www.example.com/api-endpoint'
    >>> apysigner.get_signature(private_key, url, payload)
    'CFNmvPrjW_Z1x5XO-tQzJzhs6GjeJH0k0SxOuuhJ3YA='


Just the basics to create the HMAC signature. You'll need combine this with other things
like actually adding the signature on the URL and making the request, but those responsibilities
intentionally live elsewhere.

See the django-request-signer project for examples if you need the rest.
