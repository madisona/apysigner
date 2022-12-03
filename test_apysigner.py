
import datetime
import decimal
import json
import pytz
from unittest import TestCase, main

from apysigner import Signer, get_signature, DefaultJSONEncoder


class SignatureMakerTests(TestCase):

    def setUp(self):
        self.private_key = 'CoVTr95Xv2Xlu4ZjPo2bWl7u4SnnAMAD7EFFBMS4Dy4='
        self.signature_param = "signature"
        self.signer = Signer(self.private_key)

    def test_create_signature_with_string_does_not_raise(self):
        payload = "hello world!"
        base_url = 'http://www.example.com/accounts/user/add/'
        expected_signature = '1kUGrvPfAj2EuPmBbmO3ebMXmaBM2VyJHpkwKm_Ccr0='
        self.assertEqual(expected_signature, self.signer.create_signature(base_url, payload))

    def test_signs_request_with_data(self):
        data = {'username': 'some tester', 'first_name': 'Mr. Test'}
        signature = self.signer.create_signature('http://www.example.com/accounts/user/add/', data)

        expected_signature = 'cKOHRf5TZpTrrAGHPFq9g6jRVZwUD_YgEpjk1nAncLo='
        self.assertEqual(expected_signature, signature)

    def test_signs_request_with_no_payload(self):
        signature = self.signer.create_signature('http://www.example.com/accounts/?one=1&two=2&two=dos&two=two')
        expected_signature = 'bm9_IDIQtEElubM5r__M0kDMUfdQ__0ZSI-2Bi6DcRo='
        self.assertEqual(expected_signature, signature)

    def test_signs_request_when_private_key_is_unicode(self):
        signer = Signer(str(self.private_key))
        signature = signer.create_signature('http://www.example.com/accounts/user/add/')

        expected_signature = '2ZzgF8AGioIfYzPqedI0FfJKEDG2asRA1LR70q4IOYs='
        self.assertEqual(expected_signature, signature)

    def test_requires_private_key(self):
        with self.assertRaises(Exception) as context:
            Signer(None)

        self.assertEqual(str(context.exception), 'Private key is required.')

    def test_signature_is_same_with_different_blank_payloads(self):
        base_url = 'http://www.example.com/'
        signatures = set([
            get_signature(self.private_key, base_url, None),
            get_signature(self.private_key, base_url, ""),
            get_signature(self.private_key, base_url, {}),
        ])
        self.assertEqual(1, len(signatures))
        # all should be same as the empty string version
        self.assertEqual(get_signature(self.private_key, base_url, ""), signatures.pop())

    def test_get_signature_creates_signature_with_payload_data(self):
        base_url = 'http://www.example.com/accounts/user/add/'
        data = {'username': 'some tester', 'first_name': 'Mr. Test'}
        signature = get_signature(self.private_key, base_url, data)

        expected_signature = 'cKOHRf5TZpTrrAGHPFq9g6jRVZwUD_YgEpjk1nAncLo='
        self.assertEqual(expected_signature, signature)

    def test_get_signature_with_complex_non_unicode_payload(self):
        base_url = 'http://www.example.com/accounts/user/add/'
        data = {'coverages': [{
            'construction_type': u'', 'premium': None, 'fire_class': None, 'optional_coverages': [{
                'construction_type': u'', 'irpms': [], 'fire_class': None, 'deductible_code': u'500',
                'coverage_amount': '100000', 'territory': None, 'rate_code': u'033', 'year_built': None
                }],
            'rate_code': u'005', 'property_id': '6b86b273ff3', 'packages': [], 'year_built': None,
            'coverage_amount': '100000', 'irpms': [], 'deductible_code': u'500', 'territory': None
            }, {
                'construction_type': u'', 'premium': None, 'fire_class': None, 'optional_coverages': [],
                'rate_code': u'015', 'property_id': 'd4735e3a265', 'packages': [{
                    'rate_code': u'017', 'irpms': [], 'construction_type': u'', 'deductible_code': u'500',
                    'fire_class': None, 'rateable_amount': 10000, 'territory': None, 'property_id': '6b86b273ff3'
                }],
                'year_built': None, 'coverage_amount': '100000', 'irpms': [], 'deductible_code': u'500',
                'territory': None
            }, {
                'construction_type': u'', 'premium': None, 'fire_class': None, 'optional_coverages': [{
                    'construction_type': u'', 'irpms': [], 'fire_class': None, 'deductible_code': u'500',
                    'coverage_amount': '100000', 'territory': None, 'rate_code': u'033', 'year_built': None
                }],
                'rate_code': u'002', 'property_id': '4e07408562b', 'packages': [], 'year_built': None,
                'coverage_amount': '100000', 'irpms': [u'RCC'], 'deductible_code': u'500', 'territory': None
            }],
            'producer': u'matt.morrison', 'policy_type': u'FM', 'policy': {
                'effective_date': None, 'path': 'APPS9690', 'apps_key': u'FM', 'discount_a': u'1'
            }, 'company': 9690, 'agency': None, 'policy_id': 1
        }
        signature = get_signature(self.private_key, base_url, data)
        expected_signature = '0WhQvC9ZLTIBsLn_N6cfC25qVmwgfsfFMJYlFEWFj4k='
        self.assertEqual(expected_signature, signature)

    def test_convert_function_will_also_sort_dict_based_on_key(self):
        d = {u'coverages': [{
            u'construction_type': u'', u'premium': None, u'coverage_amount': u'100000', u'territory': None,
            u'irpms': [], u'fire_class': None, u'deductible_code': u'500', u'optional_coverages': [{
                u'construction_type': u'', u'year_built': None, u'coverage_amount': u'100000', u'irpms': [],
                u'fire_class': None, u'deductible_code': u'500', u'territory': None, u'rate_code': u'033'
            }],
            u'packages': [], u'year_built': None, u'rate_code': u'005', u'property_id': u'6b86b273ff3'
            }, {
                u'construction_type': u'', u'premium': None, u'coverage_amount': u'100000', u'territory': None,
                u'irpms': [], u'fire_class': None, u'deductible_code': u'500', u'optional_coverages': [],
                u'packages': [{
                    u'fire_class': None, u'rate_code': u'017', u'irpms': [], u'construction_type': u'',
                    u'deductible_code': u'500', u'rateable_amount': 10000, u'territory': None,
                    u'property_id': u'6b86b273ff3'
                }],
                u'year_built': None, u'rate_code': u'015', u'property_id': u'd4735e3a265'
            }, {
                u'construction_type': u'', u'premium': None, u'coverage_amount': u'100000', u'territory': None,
                u'irpms': [u'RCC'], u'fire_class': None, u'deductible_code': u'500', u'optional_coverages': [{
                    u'construction_type': u'', u'year_built': None, u'coverage_amount': u'100000', u'irpms': [],
                    u'fire_class': None, u'deductible_code': u'500', u'territory': None, u'rate_code': u'033'
                }],
                u'packages': [], u'year_built': None, u'rate_code': u'002', u'property_id': u'4e07408562b'
                }],
            u'producer': u'matt.morrison', u'company': 9690, u'agency': None, u'policy_type': u'FM', u'policy': {
                u'effective_date': None, u'path': u'APPS9690', u'apps_key': u'FM', u'discount_a': u'1'
            },
            u'policy_id': 1
        }
        unicode_payload = self.signer._convert(d)
        d_sig = self.signer.create_signature("http://example.com", d)
        u_sig = self.signer.create_signature("http://example.com", unicode_payload)
        self.assertEqual(d_sig, u_sig)

    def test_get_signature_signs_request_with_no_payload(self):
        signature = get_signature(self.private_key, 'http://www.example.com/accounts/?one=1&two=2&two=dos&two=two')
        expected_signature = 'bm9_IDIQtEElubM5r__M0kDMUfdQ__0ZSI-2Bi6DcRo='
        self.assertEqual(expected_signature, signature)

    def test_convert_returns_string_when_already_string(self):
        d = 'my_value'
        unicode_payload = self.signer._convert(d)
        self.assertEqual(d, unicode_payload)

    def test_converts_every_str_key_and_value_of_dictionary_to_string(self):
        d = {'my_key': 'my_value'}
        unicode_payload = self.signer._convert(d)
        self.assertEqual(unicode_payload, json.dumps(d, sort_keys=True))

    def test_converts_every_str_key_and_value_of_nested_dictionary_to_string(self):
        d = {'my_key': {"one": "two"}}
        unicode_payload = self.signer._convert(d)
        self.assertEqual(unicode_payload, json.dumps(d, sort_keys=True))

    def test_converts_list_item_to_string(self):
        d = ["one", "two"]
        unicode_payload = self.signer._convert(d)
        self.assertEqual(unicode_payload, json.dumps(d, sort_keys=True))

    def test_signs_request_with_date_in_data(self):
        data = {'username': 'tester', 'first_name': 'Mr. Test', 'joined': datetime.datetime(2015, 11, 2)}
        signature = self.signer.create_signature('http://www.example.com/accounts/user/add/', data)
        self.assertEqual('LUPaFQGPy9vEF434BlQtzLgL3fmq7MofictHxy8VCmU=', signature)

    def test_signs_request_with_date_nested_in_data(self):
        data = {'username': 'tester', 'first_name': 'Mr. Test', 'dates': {'joined': datetime.datetime(2015, 11, 2)}}
        signature = self.signer.create_signature('http://www.example.com/accounts/user/add/', data)
        self.assertEqual('K5Zg2RWGFIhK0cxr9AUWraT5twpeKU8zyj0K2xE60fY=', signature)


class DefaultJsonEncoderTests(TestCase):

    def setUp(self):
        self.sut = DefaultJSONEncoder

    def test_subclasses_JsonDecoder(self):
        self.assertTrue(issubclass(self.sut, json.JSONEncoder))

    def test_returns_iso_format_for_datetime_object(self):
        obj = datetime.datetime(2016, 1, 1, 14, 35, 7)
        prepared = self.sut().default(obj)
        self.assertEqual("2016-01-01T14:35:07", prepared)

    def test_returns_iso_format_for_datetime_object_with_microseconds(self):
        obj = datetime.datetime(2016, 1, 1, 14, 35, 7, microsecond=441069)
        prepared = self.sut().default(obj)
        self.assertEqual("2016-01-01T14:35:07.441069", prepared)

    def test_returns_iso_format_for_timezone_aware_datetime_objects(self):
        central = pytz.timezone("America/Chicago")
        obj = datetime.datetime(2016, 1, 1, 14, 35, 7, microsecond=441069, tzinfo=central)
        prepared = self.sut().default(obj)
        self.assertEqual("2016-01-01T14:35:07.441069-05:51", prepared)

    def test_returns_iso_format_for_timezone_aware_datetime_objects_when_utc(self):
        obj = datetime.datetime(2016, 1, 1, 14, 35, 7, microsecond=441069, tzinfo=pytz.utc)
        prepared = self.sut().default(obj)
        self.assertEqual("2016-01-01T14:35:07.441069+00:00", prepared)

    def test_returns_iso_format_for_date_object(self):
        obj = datetime.date(2016, 1, 1)
        prepared = self.sut().default(obj)
        self.assertEqual("2016-01-01", prepared)

    def test_returns_iso_format_for_time_object(self):
        obj = datetime.time(16, 23, 32)
        prepared = self.sut().default(obj)
        self.assertEqual("16:23:32", prepared)

    def test_returns_iso_format_for_time_object_with_microseconds(self):
        obj = datetime.time(16, 23, 32, 553521)
        prepared = self.sut().default(obj)
        self.assertEqual("16:23:32.553521", prepared)

    def test_returns_string_format_when_decimal_object(self):
        obj = decimal.Decimal("32.25")
        prepared = self.sut().default(obj)
        self.assertEqual("32.25", prepared)


if __name__ == '__main__':
    main()
