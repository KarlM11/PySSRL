# -*- coding:utf-8 -*-
import base64
from typing import Dict
from ssrl.functional import default_encoding
from .base import BaseProvider


class SSRProvider(BaseProvider):
    
    @staticmethod
    def dumps(conf: Dict) -> str:
        pass

    @staticmethod
    def loads(link: str) -> dict:
        link_ = link.encode(default_encoding)  # Convert to bytes.
        pass

    @staticmethod
    def b64encode(input_: bytes) -> bytes:
        _encoded = base64.urlsafe_b64encode(input_)
        _encoded = _encoded.replace(b'==', b'')  # Remove padding
        return _encoded

    @staticmethod
    def b64decode(input_: bytes) -> bytes:
        length = len(input_)
        pad_len = length % 4
        if pad_len == 3:
            raise ValueError("Bad input encoded string.")

        pad = b'=' * pad_len
        input_ += pad
        return base64.urlsafe_b64decode(input_)
