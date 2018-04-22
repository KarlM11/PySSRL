# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import copy
from unittest import TestCase
from ssrl.functional import default_encoding
from ssrl.providers.ssr import SSRProvider


class TestSSRProvider(TestCase):

    def test_ssr_parse(self):
        _in = 'ssr://MTI3LjAuMC4xOjEyMzQ6YXV0aF9hZXMxMjhfbWQ1OmFlcy0xMjgtY2ZiOnRsczEuMl90aWNrZXRfYXV0aDpZV0ZoWW1KaS8_b2Jmc3BhcmFtPVluSmxZV3QzWVRFeExtMXZaUQ'
        _in_remark = 'ssr://MTI3LjAuMC4xOjEyMzQ6YXV0aF9hZXMxMjhfbWQ1OmFlcy0xMjgtY2ZiOnRsczEuMl90aWNrZXRfYXV0aDpZV0ZoWW1KaS8_b2Jmc3BhcmFtPVluSmxZV3QzWVRFeExtMXZaUSZyZW1hcmtzPTVyV0w2Sy1WNUxpdDVwYUg'

        expected = {
            'server': '127.0.0.1',
            'server_port': '1234',
            'password': 'aaabbb',
            'method': 'aes-128-cfb',
            'protocol': 'auth_aes128_md5',
            'obfs': 'tls1.2_ticket_auth'
        }

        params_expected = {
            "obfsparam": "breakwa11.moe",
            "remarks": "测试中文"
        }

        res = SSRProvider.loads(_in)
        res_remark = SSRProvider.loads(_in_remark)

        for k, v in expected.items():
            _v = res[k]
            _vr = res_remark[k]
            self.assertEqual(v, _v, k)
            self.assertEqual(v, _vr, '[Remark] %s' % k)

        params = res_remark['params']
        for k, v in params_expected.items():
            _v = params[k]
            self.assertEqual(v, _v, '[Param] %s' % k)

    def test_ssr_dump(self):
        conf = {
            'server': '127.0.0.1',
            'server_port': '1234',
            'password': 'aaabbb',
            'method': 'aes-128-cfb',
            'protocol': 'auth_aes128_md5',
            'obfs': 'tls1.2_ticket_auth'
        }

        params = {
            "obfsparam": "breakwa11.moe"
        }

        _conf = copy.copy(conf)
        _conf['params'] = copy.copy(params)

        _link = SSRProvider.dumps(_conf)
        _link_expected = 'ssr://MTI3LjAuMC4xOjEyMzQ6YXV0aF9hZXMxMjhfbWQ1OmFlcy0xMjgtY2ZiOnRsczEuMl90aWNrZXRfYXV0aDpZV0ZoWW1KaS8_b2Jmc3BhcmFtPVluSmxZV3QzWVRFeExtMXZaUQ'
        self.assertEqual(_link_expected, _link, 'Generated link does not match.')

    def test_ssr_parse_v6(self):
        _link = 'ssr://MjAwMTowZGI4OjAwMDA6MDA0MjowMDAwOjhhMmU6MDM3MDo3MzM0OjEwMDE6YXV0aF9jaGFpbl9iOmFlcy0yNTYtY2ZiOnBsYWluOlVXRmFkMU40Lz9vYmZzcGFyYW09JnJlbWFya3M9U1ZCMk5pQlVaWE4wJmdyb3VwPVFuSmhkbThoSVE'

        _expected = {
            'server': '2001:0db8:0000:0042:0000:8a2e:0370:7334',
            'server_port': '1001',
            'password': 'QaZwSx',
            'method': 'aes-256-cfb',
            'protocol': 'auth_chain_b',
            'obfs': 'plain'
        }

        _expected_params  = {
                'remarks': 'IPv6 Test',
                'group': 'Bravo!!'
        }

        _parsed = SSRProvider.loads(_link)
        _parsed_params = _parsed.pop('params')

        for k, v in _expected.items():
            self.assertEqual(v, _parsed[k])

        for k, v in _expected_params.items():
            self.assertEqual(v, _expected_params[k])
