# -*- coding: utf-8 -*-
"""
验证频率限制功能 - 精确测试
"""
import time
import requests as real_requests
from adata.common.utils import requests

# 模拟底层的requests库请求
def mock_request(method='get', url=None, **kwargs):
    return type('MockResponse', (object,), {'status_code': 200})()

real_requests.request = mock_request

def test_precise_rate_limit():
    print("=" * 60)
    print("精确验证频率限制功能")
    print("=" * 60)
    
    # 设置严格的频率限制：每分钟5次
    print("\n设置频率限制: api.example.com 每分钟5次请求")
    requests.set_rate_limit('api.example.com', 5)
    
    print("\n开始发起请求，观察时间间隔...")
    print("-" * 60)
    
    last_request_time = None
    
    # 发起10次请求
    for i in range(10):
        current_time = time.time()
        
        if last_request_time is not None:
            interval = current_time - last_request_time
            print(f"\n请求 {i+1}: 与上次请求间隔 {interval:.2f}秒")
        else:
            print(f"\n请求 {i+1}: 首次请求")
        
        # 发起请求
        start_request = time.time()
        response = requests.request('get', 'https://api.example.com/test')
        end_request = time.time()
        
        request_duration = end_request - start_request
        print(f"  请求处理耗时: {request_duration:.2f}秒")
        
        if request_duration > 1.0:
            print(f"  ✓ 触发频率限制，自动等待 {request_duration:.2f}秒")
        
        last_request_time = end_request
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("\n预期结果：")
    print("  - 前5次请求：快速完成（间隔约0.00秒）")
    print("  - 第6次请求：触发限制，等待约60秒")
    print("  - 第7-10次请求：继续正常处理")
    print("=" * 60)

if __name__ == "__main__":
    test_precise_rate_limit()
