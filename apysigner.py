
__version__ = "2.1.0"


import base64
import datetime
import decimal
import hashlib
import hmac
import json
import six

if six.PY3:
    from urllib.parse import urlparse
else:
    from urlparse import urlparse


__all__ = (
    'Signer',
    'get_signature',
)


def get_signature(private_key, base_url, payload=None):
    """
    A shortcut to sign a url with just one function.

    :param private_key:
        Base 64, url encoded private key string used to sign request.
    :param base_url:
        The 'GET' portion of the URL including parameters if any.
    :param payload:
        The 'POST' parameter data.
        If present must be either a dictionary or an iterable
        of two items, first being key, second being value(s).
    """
    return Signer(private_key).create_signature(base_url, payload)


def is_aware(value):
    """
    Determines if a given datetime.datetime is aware.

    The logic is described in Python's docs:
    http://docs.python.org/library/datetime.html#datetime.tzinfo
    """
    return value.tzinfo is not None and value.tzinfo.utcoffset(value) is not None


class DateJSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time and decimal types.
    Taken from django.core.serializers.DjangoJSONEncoder.
    """
    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            if is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, decimal.Decimal):
            return str(o)
        else:
            return super(DateJSONEncoder, self).default(o)


class Signer(object):
    """
    Creates an HMAC signature for a url and possible POST data payload.

    USAGE:
        signer = Signer(<private_key>)
        signature = signer.create_signature('http://www.google.com?q=hmac+security')
    """
    private_key = None

    def __init__(self, private_key):
        self.private_key = private_key

        if self.private_key is None:
            raise Exception('Private key is required.')

    def create_signature(self, base_url, payload=None):
        """
        Creates unique signature for request.
        Make sure ALL 'GET' and 'POST' data is already included before
        creating the signature or receiver won't be able to re-create it.

        :param base_url:
            The url you'll using for your request.
        :param payload:
            The POST data that you'll be sending.
        """
        url = urlparse(base_url)

        url_to_sign = "{path}?{query}".format(path=url.path, query=url.query)

        converted__payload = self._convert(payload)

        decoded_key = base64.urlsafe_b64decode(self.private_key.encode('utf-8'))
        signature = hmac.new(decoded_key, str.encode(url_to_sign + converted__payload), hashlib.sha256)
        return bytes.decode(base64.urlsafe_b64encode(signature.digest()))

    def _convert(self, payload):
        """
        Converts payload to a string. Complex objects are dumped to json
        """
        if not isinstance(payload, six.string_types):
            payload = json.dumps(payload, cls=DateJSONEncoder, sort_keys=True)
        return str(payload)
