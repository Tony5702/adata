# -*- coding: utf-8 -*-
"""
测试 RateLimiter 类的功能
"""
import time
from adata.common.utils.sunrequests import RateLimiter

print("测试 RateLimiter 类")

# 创建 RateLimiter 实例
limiter = RateLimiter()

# 测试默认限制（每分钟30次）
print("默认限制：每分钟30次")

url = "https://httpbin.org/get"

start_time = time.time()
for i in range(5):
    try:
        # 测试默认频率限制
        limiter.acquire(url)
        print(f"请求 {i+1}: 成功，耗时={time.time() - start_time:.2f}s")
    except Exception as e:
        print(f"请求 {i+1} 出错: {e}")

elapsed = time.time() - start_time
print(f"5次请求总耗时: {elapsed:.2f}s")
print("测试完成")
