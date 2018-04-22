# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import copy
from unittest import TestCase
from ssrl.functional import default_encoding
from ssrl.providers.ss import SSProvider


class TestSSProvider(TestCase):

    def test_ss_parse(self):
        _in_sip2 = 'ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpRYVp3U3g@127.0.0.1:8388/?plugin=simple-obfs%3bbreakwa11.moe#%e6%b5%8b%e8%af%95%e4%b8%ad%e6%96%87'
        _in_original = 'ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpRYVp3U3hAMTI3LjAuMC4xOjgzODg=#%e6%b5%8b%e8%af%95%e4%b8%ad%e6%96%87'

        conf = {
            "server": "127.0.0.1",
            "server_port": 8388,
            "password": "QaZwSx",
            "method": "chacha20-ietf-poly1305",
            "remarks": "测试中文"
        }

        params = {
            "plugin": "simple-obfs",
            "plugin_opts": "breakwa11.moe"
        }

        _conf_original = SSProvider.loads(_in_original)
        _conf_sip2 = SSProvider.loads(_in_sip2)

        for k, v in conf.items():
            self.assertEqual(v, _conf_original[k])
            self.assertEqual(v, _conf_sip2[k])

        for k, v in params.items():
            self.assertEqual(v, _conf_sip2[k])

    def test_ss_dump_sip2(self):
        conf = {
            "server": "127.0.0.1",
            "server_port": 8388,
            "password": "QaZwSx",
            "method": "chacha20-ietf-poly1305",
            "plugin": "simple-obfs",
            "plugin_opts": "breakwa11.moe",
            "remarks": "测试中文",
            "timeout": 5
        }

        _link = SSProvider.dumps(conf)
        _link_expected = 'ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpRYVp3U3g@127.0.0.1:8388/?plugin=simple-obfs%3bbreakwa11.moe#%e6%b5%8b%e8%af%95%e4%b8%ad%e6%96%87'
        self.assertEqual(_link_expected, _link, 'Generated link does not match.')

    def test_ss_dump_original(self):
        conf = {
            "server": "127.0.0.1",
            "server_port": 8388,
            "password": "QaZwSx",
            "method": "chacha20-ietf-poly1305",
            "remarks": "测试中文",
            "timeout": 5
        }

        _link = SSProvider.dumps(conf)
        _link_expected = 'ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpRYVp3U3hAMTI3LjAuMC4xOjgzODg=#%e6%b5%8b%e8%af%95%e4%b8%ad%e6%96%87'
        self.assertEqual(_link_expected, _link)
