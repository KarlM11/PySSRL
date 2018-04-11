# -*- coding:utf-8 -*-
import sys


def get_env_encoding():
    return sys.getdefaultencoding()


default_encoding = get_env_encoding()
