# -*- coding: utf-8 -*-
"""简单测试频率限制器修复"""
print('开始测试...')

# 测试导入
from adata.common import set_rate_limit, set_default_rate_limit
from adata.common.utils import requests
print('导入成功')

# 测试设置频率限制
set_rate_limit('httpbin.org', 2)
print('设置 httpbin.org 每分钟限制2次请求')

# 测试请求
url = 'https://httpbin.org/get'

print('\n第一次请求...')
try:
    res = requests.request('get', url, timeout=5)
    print(f'成功，状态码: {res.status_code}')
except Exception as e:
    print(f'失败: {e}')

print('\n第二次请求...')
try:
    res = requests.request('get', url, timeout=5)
    print(f'成功，状态码: {res.status_code}')
except Exception as e:
    print(f'失败: {e}')

print('\n第三次请求（应该等待或超时）...')
try:
    res = requests.request('get', url, timeout=5, max_wait_time=2)
    print(f'成功，状态码: {res.status_code}')
except Exception as e:
    print(f'预期的超时: {e}')

print('\n测试完成！')
