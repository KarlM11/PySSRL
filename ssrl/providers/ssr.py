# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import base64
import six
from ssrl.functional import default_encoding, urlencode, parse_qsl
from .base import BaseProvider


class SSRProvider(BaseProvider):

    _scheme = 'ssr://'
    _template = '{server}:{server_port}:{protocol}:{method}:{obfs}:{password}/'

    # Defines config fields.
    # All of them are required.
    # fields -> name, is_encode, type
    _conf_fields = (
        ('server', False, six.text_type),
        ('server_port', False, six.text_type),
        ('method', False, six.text_type),
        ('password', True, six.text_type),
        ('protocol', False, six.text_type),
        ('obfs', False, six.text_type)
    )

    # Defines param fields.
    # Neither of them is required.
    # fields -> name, is_encode, type
    _param_fields = (
        ('group', True, six.text_type),
        ('obfsparam', True, six.text_type),
        ('protoparam', True, six.text_type),
        ('remarks', True, six.text_type),
        ('udpport', False, int),
        ('uot', False, int)
    )

    @classmethod
    def _clean_input(cls, data, fields, strict=True):
        _out = dict()
        for k, e, t in fields:
            _v = data.get(k, '')
            if not _v:
                if strict:
                    raise KeyError('Key %s missing.' % k)
                else:
                    continue

            if e:
                _v = cls.b64encode(_v)

            _out[k] = t(_v)
        
        return _out

    @classmethod
    def dumps(cls, conf):
        params = conf.pop('params', None)
        _conf = cls._clean_input(conf, cls._conf_fields, True)

        body = cls._template.format(**_conf)

        if params:
            _params = cls._clean_input(params, cls._param_fields, False)
            _qs = urlencode(_params)
            if _qs:
                body = '?'.join((body, _qs))

        body = cls.b64encode(body)
        return cls._scheme + body        

    @classmethod
    def loads(cls, link):
        if not link.lower().startswith(cls._scheme):
            raise ValueError('Bad link.')

        body = link[len(cls._scheme):]
        body = cls.b64decode(body)

        try:
            base, extra = body.split('/?')  # Split body and params.
        except IndexError:
            extra = None
            base = body

            if body.endswith('/'):
                base = base[:-1]

        # Use `rsplit in order to handle IPv6 address.`
        host, port, proto, method, obfs, pass_en = base.rsplit(':', 5)
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

        if not extra:
            conf['params'] = None
            return conf

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
    def b64encode(input_):
        input_ = input_.encode(default_encoding)
        _encoded = base64.urlsafe_b64encode(input_) \
                         .decode(default_encoding)

        _encoded = _encoded.replace('=', '')  # Remove padding
        return _encoded
    @staticmethod
    def b64decode(input_):
        input_ = input_.encode(default_encoding)
        length = len(input_)
        pad_len = length % 4

        # Base64 library accepts extra paddings.
        pad = b'=' * pad_len
        input_ += pad
        return base64.urlsafe_b64decode(input_).decode(default_encoding)
