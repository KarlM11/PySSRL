# PySSRL - <u>P</u>ython <u>S</u>hadow<u>s</u>ocks <u>R</u>esource <u>L</u>ibrary
Library for prasing / generating Shadowsocks & ShadowsocksR links.

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

## Why names `PySSRL`
I had prefered to name this project as `PySRL`, however, a project with same name has already existed on PyPI.

## License
Apache 2.0