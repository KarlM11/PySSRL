# -*- coding:utf-8 -*-
import sys
import locale
import base64
import six

def get_env_encoding():
    _, enc = locale.getdefaultlocale()
    if enc:
        return enc.lower()

    if six.PY2:
        # Force using UTF-8 in Python 2.
        return 'utf-8'  
    else:
        return sys.getdefaultencoding()


default_encoding = get_env_encoding()

if six.PY2:
    from six.moves.urllib.parse import parse_qsl, urlencode, quote, unquote
else:
    from urllib.parse import parse_qsl, urlencode, quote, unquote


def b64encode(input_, no_padding=True):
    input_ = input_.encode(default_encoding)
    _encoded = base64.urlsafe_b64encode(input_) \
                        .decode(default_encoding)

    if no_padding:
        _encoded = _encoded.replace('=', '')  # Remove padding
    return _encoded


def b64decode(input_):
    input_ = input_.encode(default_encoding)
    length = len(input_)
    pad_len = length % 4

    # Base64 library accepts extra paddings.
    pad = b'=' * pad_len
    input_ += pad
    return base64.urlsafe_b64decode(input_).decode(default_encoding)
