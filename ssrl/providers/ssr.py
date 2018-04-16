# -*- coding:utf-8 -*-
import base64
import six
from typing import Dict
from urllib.parse import parse_qsl
from ssrl.functional import default_encoding
from .base import BaseProvider


class SSRProvider(BaseProvider):

    _scheme = 'ssr://'
    _template = '{}'

    # Defines param fields.
    # Neither of them is required.
    # fields -> name, is_encode, type
    _param_fields = (
        ('group', True, str),
        ('obfs_param', True, str),
        ('protoparam', True, str),
        ('remarks', True, str),
        ('udpport', False, int),
        ('uot', False, int)
    )
    
    @staticmethod
    def dumps(conf: Dict) -> str:
        pass

    @classmethod
    def loads(cls, link: str) -> dict:
        if not link.lower().startswith(cls._scheme):
            raise ValueError('Bad link.')

        body = link[len(cls._scheme):]
        body = cls.b64decode(body)
        base, extra = body.split('/?')  # Split body and params.

        host, port, proto, method, obfs, pass_en = base.split(':')
        params = dict(parse_qsl(extra))  # Cast parsed params to dict.
        passwd = cls.b64decode(pass_en)

        conf = {
            'server': host,
            'server_port': port,
            'method': method,
            'password': passwd,
            'protocol': proto,
            'obfs': obfs
        }

        parsed_params = dict()
        for k, e, t in cls._param_fields:
            v = params.get(k, None)
            if not v:
                parsed_params[k] = "" if t is str else None
                continue

            if e:
                v = cls.b64decode(v)

            parsed_params[k] = t(v)
            
        conf['params'] = parsed_params
        return conf

    @staticmethod
    def b64encode(input_: str) -> str:
        input_ = input_.encode(default_encoding)
        _encoded = base64.urlsafe_b64encode(input_) \
                         .decode(default_encoding)

        _encoded = _encoded.replace('==', '')  # Remove padding
        return _encoded
    @staticmethod
    def b64decode(input_: str) -> str:
        input_ = input_.encode(default_encoding)
        length = len(input_)
        pad_len = length % 4

        # Base64 library accepts extra paddings.
        pad = b'=' * pad_len
        input_ += pad
        return base64.urlsafe_b64decode(input_).decode(default_encoding)
