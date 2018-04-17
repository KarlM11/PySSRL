# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import copy
from unittest import TestCase
from ssrl.functional import default_encoding
from ssrl.providers.ssr import SSRProvider


class TestSSRProvider(TestCase):

    def test_b64_encode(self):
        input_ = 'breakwa11.moe'
        expected = 'YnJlYWt3YTExLm1vZQ'
        result = SSRProvider.b64encode(input_)

        self.assertEqual(result, expected)

    def test_b64_decode(self):
        import base64
        input_ = 'breakwa11.moe'

        # Standard with paddings.
        standard = base64.urlsafe_b64encode(input_.encode(default_encoding))
        no_pad = 'YnJlYWt3YTExLm1vZQ'

        res_std = SSRProvider.b64decode(standard.decode(default_encoding))
        res_no_pad = SSRProvider.b64decode(no_pad)

        self.assertEqual(input_, res_std)
        self.assertEqual(input_, res_no_pad)

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