# -*- coding:utf-8 -*-


class BaseProvider(object):

    @staticmethod
    def loads(link_url):
        raise NotImplementedError("Implemetion required.")

    @staticmethod
    def dumps(conf):
        raise NotImplementedError("Implemetion required.")
