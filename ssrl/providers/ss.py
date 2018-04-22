# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import six
from .base import BaseProvider
from ssrl.functional import (b64encode, b64decode, quote, unquote, parse_qsl,
                             default_encoding)


class SSProvider(BaseProvider):
    """ URI loader and dumper compeitable with Shadowsocks.
    """
    _scheme = 'ss://'
    _template_sip2 = '{auth}@{server}:{server_port}'
    _template = '{method}:{password}@{server}:{server_port}'

    @classmethod
    def loads(cls, link):
        """ Loads config from given URI.

        Supports original and SIP002 scheme.
        """
        body = link[len(cls._scheme):]
        if '#' in body:
            body, remarks = body.split('#')
            if six.PY2:
                remarks = remarks.encode(default_encoding)
                remarks = unquote(remarks).decode(default_encoding)
            else:
                remarks = unquote(remarks)
        else:
            remarks = None

        if body.endswith('/'):
            body = body[:-1]
        
        if '@' in body:
            _conf = cls._loads_sip002(body)
        else:
            _conf = cls._loads_original(body)

        _conf.update({'remarks': remarks})
        _conf['server_port'] = int(_conf['server_port'])
        return _conf  

    @classmethod
    def dumps(cls, conf, sip002=False):
        """ Dump URIs from config json.
        
        Arguments:
            conf {dict} -- Given config.
        
        Keyword Arguments:
            sip002 {bool} -- Force using SIP002 scheme. (default: {False})
        
        Returns:
            str -- Target URI.
        """
        remarks = conf.pop('remarks', None)
        conf['server_port'] = str(conf['server_port'])

        if 'plugin' in conf or sip002:
            uri =  cls._dump_sip002(**conf)
        else:
            uri = cls._dump_original(**conf)

        if remarks:
            _remarks = '#' + quote(remarks.encode(default_encoding)).lower()
        else:
            _remarks = ''

        uri += _remarks
        return uri

        
    @classmethod
    def _dump_original(cls, server, server_port, method, password, **kwargs):
        """ Dump URIs with original scheme.
        
        Arguments:
            server {str} -- Server Address
            server_port {int} -- Server Port
            method {str} -- Encryption Method
            password {str} -- Shadowsocks Password
        
        Returns:
            str -- Target URI.
        """

        _body = cls._template.format(**{
            'server': server,
            'server_port': server_port,
            'method': method,
            'password': password
        })

        _body = b64encode(_body, False)
        _uri = cls._scheme + _body
        return _uri

    @classmethod
    def _dump_sip002(cls, server, server_port, method, password,
                     plugin=None, plugin_opts='', **remarks):
        """ Dump URIs with SIP002 scheme.
        
        Arguments:
            server {str} -- Server Address
            server_port {int} -- Server Port
            method {str} -- Encryption Method
            password {str} -- Shadowsocks Password            
        
        Keyword Arguments:
            plugin {str} -- Plugin Name (or Path?) (default: {None})
            plugin_opts {str} -- Plugin Params (default: {None})
            remarks {str} -- Remarks (default: {''})
        
        Returns:
            str -- Target URI.
        """
        _auth = b64encode(':'.join((method, password)))
        _body = cls._template_sip2.format(**{
            'auth': _auth,
            'server': server,
            'server_port': server_port
        })

        _uri = cls._scheme + _body
        if not plugin:
            return _uri

        _plugin = ';'.join((plugin, plugin_opts))
        _plugin = '/?plugin=' + quote(_plugin).lower()

        _uri += _plugin
        return _uri

    @classmethod
    def _loads_original(cls, body):
        """ Loads URI in original scheme.
        """

        _parsed = b64decode(body)
        _auth, _server = _parsed.split('@')
        method, password = _auth.split(':', 1)
        server, server_port = _server.rsplit(':', 1)

        return {
            'server': server,
            'server_port': server_port,
            'method': method,
            'password': password,
            'plugin': None,
            'plugin_opts': None
        }

    @classmethod
    def _loads_sip002(cls, body):
        """ Loads URI with SIP002 scheme.
        """
        _auth, _server = body.split('@')
        _auth = b64decode(_auth)
        method, password = _auth.split(':', 1)
        
        params = dict()
        if '?' in _server:
            _server, _param = _server.split('/?')
            _param = dict(parse_qsl(_param))
            _plugin = _param.get('plugin')

            if _plugin:
                plugin, plugin_opts = _plugin.split(';', 1)
                params['plugin'] = plugin
                params['plugin_opts'] = plugin_opts

        server, server_port = _server.rsplit(':', 1)
        _conf = {
            'server': server,
            'server_port': server_port,
            'method': method,
            'password': password
        }
        _conf.update(params)
        return _conf
