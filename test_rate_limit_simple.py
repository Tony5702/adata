# -*- coding: utf-8 -*-
"""
简单测试频率限制功能
"""
import time
from adata.common import set_rate_limit, set_default_rate_limit
from adata.common.utils import requests

print("测试频率限制功能")
print("默认限制：每分钟30次")

url = "https://httpbin.org/get"

start_time = time.time()
for i in range(5):
    try:
        # 测试默认频率限制
        res = requests.request(method='get', url=url, timeout=10)
        print(f"请求 {i+1}: 状态码={res.status_code}, 耗时={time.time() - start_time:.2f}s")
    except Exception as e:
        print(f"请求 {i+1} 出错: {e}")

elapsed = time.time() - start_time
print(f"5次请求总耗时: {elapsed:.2f}s")
print("测试完成")
