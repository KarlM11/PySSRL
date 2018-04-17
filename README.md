# PySSRL - <u>P</u>ython <u>S</u>hadow<u>s</u>ocks <u>R</u>esource <u>L</u>ibrary
Library for prasing / generating Shadowsocks & ShadowsocksR links.

[![Build Status](https://travis-ci.org/AspirinGeyer/PySSRL.svg?branch=master)](https://travis-ci.org/AspirinGeyer/PySSRL)
[![codecov](https://codecov.io/gh/AspirinGeyer/PySSRL/branch/master/graph/badge.svg)](https://codecov.io/gh/AspirinGeyer/PySSRL)

## Usage
```python
import ssrl

# Parse configuration from link.
# Returns dict.
ssrl.load_ss(ss_link)
ssrl.load_ssr(ssr_link)

# Generate link from configuration.
# Returns str.
ssrl.dump_ss(conf_dict)
ssrl.dump_ssr(conf_dict)
```

## SSR Config Dictionary
According to [this document](https://github.com/shadowsocksrr/shadowsocks-rss/wiki/SSR-QRcode-scheme), loader and dumper use data structure like below. 

### Config Fields
| Key | Base64 Encode | Type | Required | Description |
|:---:|:-------------:|:----:|:--------:|:-----------:|
|`server`| False | str | True | Server Address, IPv4 or IPv6 |
|`server_port`| False | str | True | Server Port |
|`method`| False | str | True | SSR Encryption Method |
|`password`| True | str | True | SSR Password |
|`protocol`| False | str | True | SSR Protocol |
|`obfs`| False | str | True | SSR Obfs Method |
|`params`| False | dict | False | Additional Params |

### Params Fields
| Key | Base64 Encode | Type | Required | Description |
|:---:|:-------------:|:----:|:--------:|:-----------:|
|`obfsparam`| True | str | False | Obfs Param |
|`protoparam`| True | str | False | Protocol Param |
|`remarks`| True | str | False | Remark |
|`group`| True | str | False | Group Name |
|`udpport`| False | int | False | NaN, only supported by C\# client |
|`uot`| False | int | False | NaN, only supported by C\# client |


### Example
```python
conf = {
    'server': '127.0.0.1',
    'server_port': '1234',
    'password': 'aaabbb',
    'method': 'aes-128-cfb',
    'protocol': 'auth_aes128_md5',
    'obfs': 'tls1.2_ticket_auth',
    'params': {
        "obfsparam": 'breakwa11.moe',
        'remarks': '测试中文'
    }
}
```

## Why names `PySSRL`
I had prefered to name this project as `PySRL`, however, a project with same name has already existed on PyPI.

## License
Apache 2.0