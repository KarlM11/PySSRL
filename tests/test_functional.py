# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import unittest
from ssrl.functional import b64encode, b64decode, default_encoding


class TestFunctional(unittest.TestCase):

    def test_b64_encode(self):
        input_ = 'breakwa11.moe'
        expected = 'YnJlYWt3YTExLm1vZQ'
        result = b64encode(input_)

        self.assertEqual(result, expected)

    def test_b64_decode(self):
        import base64
        input_ = 'breakwa11.moe'

        # Standard with paddings.
        standard = base64.urlsafe_b64encode(input_.encode(default_encoding))
        no_pad = 'YnJlYWt3YTExLm1vZQ'

        res_std = b64decode(standard.decode(default_encoding))
        res_no_pad = b64decode(no_pad)

        self.assertEqual(input_, res_std)
        self.assertEqual(input_, res_no_pad)