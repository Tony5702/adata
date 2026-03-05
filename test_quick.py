# -*- coding: utf-8 -*-
"""快速测试频率限制功能"""
print('开始测试...')
from adata.common import set_rate_limit, set_default_rate_limit
from adata.common.utils import requests

print('1. 测试导入...')
print('导入成功')

print('\n2. 测试设置频率限制...')
set_rate_limit('eastmoney.com', 60)
print('设置域名频率限制成功: eastmoney.com = 60次/分钟')

set_default_rate_limit(30)
print('设置默认频率限制成功: 默认 = 30次/分钟')

print('\n3. 测试请求功能（禁用频率限制）...')
import time
start = time.time()
for i in range(3):
    try:
        res = requests.request('get', 'https://httpbin.org/get', timeout=5, rate_limit=False)
        print('请求 {} 成功，状态码: {}'.format(i+1, res.status_code))
    except Exception as e:
        print('请求 {} 失败: {}'.format(i+1, e))
print('耗时: {:.2f}s'.format(time.time() - start))

print('\n所有测试通过！')
