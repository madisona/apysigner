__version__ = "2.1.0"

import json
import base64
import hashlib
import hmac
import six

if six.PY3:
    from urllib.parse import urlparse
else:
    from urlparse import urlparse


__all__ = (
    'Signer',
    'get_signature',
)


def is_list(v):
    return isinstance(v, (list, tuple))


def sort_vals(vals):
    return sorted(vals) if is_list(vals) else vals


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

        url_to_sign = str(url.path + '?' + url.query)

        unicode_payload = self._convert(payload)
        encoded_payload = str(self._encode_payload(unicode_payload))

        decoded_key = base64.urlsafe_b64decode(self.private_key.encode('utf-8'))
        signature = hmac.new(decoded_key, str.encode(url_to_sign + encoded_payload), hashlib.sha256)
        return bytes.decode(base64.urlsafe_b64encode(signature.digest()))

    def _encode_payload(self, payload):
        """
        json.dumps the payload while sorting the keys to ensure
        that the signature can be reliably recreated.

        :param payload:
            The data to be sent in a POST request.
            Can be a dictionary or it can be an iterable of
            two items, first being key, second being value(s).
        """
        if not payload:
            return ''

        if isinstance(payload, six.text_type):
            return payload

        return json.dumps(payload, sort_keys=True)

    def _convert(self, payload):
        sort_key = {'key': lambda x: x[0]}
        if isinstance(payload, dict):
            return {self._convert(k): self._convert(v) for k, v in dict(sorted(payload.items(), **sort_key)).items()}
        elif isinstance(payload, list):
            return [self._convert(element) for element in payload]
        elif isinstance(payload, str):
            return six.text_type(payload)
        else:
            return payload
