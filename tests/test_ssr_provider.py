# -*- coding:utf-8 -*-
from unittest import TestCase
from ssrl.providers.ssr import SSRProvider


class TestSSRProvider(TestCase):

    def test_b64_encode(self):
        input_ = b'breakwa11.moe'
        expected = b'YnJlYWt3YTExLm1vZQ'
        result = SSRProvider.b64encode(input_)

        self.assertEqual(result, expected)

    def test_b64_decode(self):
        import base64
        input_ = b'breakwa11.moe'
        standard = base64.urlsafe_b64encode(input_)  # Standard with paddings.
        no_pad = b'YnJlYWt3YTExLm1vZQ'

        res_std = SSRProvider.b64decode(standard)
        res_no_pad = SSRProvider.b64decode(no_pad)

        self.assertEqual(input_, res_std)
        self.assertEqual(input_, res_no_pad)

        input_bad = b'YnJlYWt3YTExLm1vZQa'
        self.assertRaises(ValueError, SSRProvider.b64decode, input_bad)
