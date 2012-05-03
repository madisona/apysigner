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

    import apysigner

    signature = apysigner.get_signature('my_private_key', 'http://www.example.com/api-endpoint?q=find+my+thing')

For a **POST** request

::

    import apysigner
    payload = {'do': 'something', 'name': 'Johnny'}
    signature = apysigner.get_signature('my_private_key', 'http://www.example.com/api-endpoint', payload)


Just the basics to create the HMAC signature. You'll need combine this with other things
like actually adding the signature on the URL and making the request, but those responsibilities
intentionally live elsewhere.

See the django-request-signer project for examples if you need the rest.
