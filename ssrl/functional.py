# -*- coding:utf-8 -*-
import sys
import locale
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
    from six.moves.urllib.parse import parse_qsl, urlencode
else:
    from urllib.parse import parse_qsl, urlencode
