# -*- coding: utf-8 -*-
"""
测试频率限制功能
"""
import time
import requests as real_requests
from adata.common.utils import requests

# 保存原始的requests库引用
real_requests_request = real_requests.request

def mock_real_request(method='get', url=None, **kwargs):
    print(f"  模拟请求: {method} {url}")
    return type('MockResponse', (object,), {'status_code': 200})()

# 替换底层的requests库，而不是替换SunRequests的request方法
real_requests.request = mock_real_request

def test_rate_limit():
    print("测试频率限制功能...")
    
    # 设置自定义频率限制：每分钟10次
    requests.set_rate_limit('api.example.com', 10)
    
    start_time = time.time()
    
    # 发起15次请求，观察是否被限制
    for i in range(15):
        print(f"发起请求 {i+1}...")
        # 使用模拟URL测试
        requests.request('get', 'https://api.example.com/test')
        elapsed = time.time() - start_time
        print(f"请求 {i+1} 完成 (累计耗时: {elapsed:.2f}秒)")
        
        # 检查是否触发了频率限制
        if elapsed > 0.1 and i < 14:
            print(f"注意：请求 {i+1} 可能被频率限制了")
        
        # 每次请求后短暂延迟，便于观察频率限制效果
        time.sleep(0.1)
    
    end_time = time.time()
    print(f"\n总耗时: {end_time - start_time:.2f} 秒")
    print("如果频率限制生效，总耗时应该接近或超过60秒")
    
    # 测试默认频率限制（30次/分钟）
    print("\n\n测试默认频率限制（30次/分钟）...")
    start_time2 = time.time()
    
    for i in range(35):
        print(f"发起请求 {i+1}...")
        requests.request('get', 'https://default.example.com/test')
        elapsed = time.time() - start_time2
        print(f"请求 {i+1} 完成 (累计耗时: {elapsed:.2f}秒)")
        
        # 每次请求后短暂延迟
        time.sleep(0.1)
    
    end_time2 = time.time()
    print(f"\n总耗时: {end_time2 - start_time2:.2f} 秒")
    print("如果默认频率限制生效，总耗时应该接近或超过60秒")

if __name__ == "__main__":
    test_rate_limit()