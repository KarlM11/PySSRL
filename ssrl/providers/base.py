# -*- coding:utf-8 -*-
from typing import Dict


class BaseProvider(object):

    @staticmethod
    def loads(link_url: str) -> dict:
        raise NotImplementedError("Implemetion required.")

    @staticmethod
    def dumps(conf: Dict) -> str:
        raise NotImplementedError("Implemetion required.")
