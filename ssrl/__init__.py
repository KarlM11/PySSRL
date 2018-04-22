# -*- coding:utf-8 -*-
from .providers import ss, ssr


load_ss = ss.SSProvider.loads
load_ssr = ssr.SSRProvider.loads

dump_ss = ss.SSProvider.dumps
dump_ssr = ssr.SSRProvider.dumps
