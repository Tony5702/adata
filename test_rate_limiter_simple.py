# -*- coding: utf-8 -*-
"""
@desc: 简单频率限制器测试
@author: 1nchaos
@time: 2023/09/01
@log: 简单测试频率限制功能
"""

import time
from adata.common.utils import requests, rate_limiter


def test_rate_limit_visual():
    """可视化测试频率限制"""
    print("可视化测试频率限制功能...")
    
    # 设置httpbin.org域名的限制为每分钟3次
    rate_limiter.set_domain_limit('httpbin.org', 3)
    
    print("发送5个连续请求，限制为每分钟3次...")
    print("时间戳\t\t请求序号\t状态")
    print("-" * 40)
    
    for i in range(5):
        start_time = time.time()
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        
        try:
            # 使用快速响应的API
            response = requests.request('get', 'https://httpbin.org/get', timeout=10)
            status = "成功"
        except Exception as e:
            status = f"失败: {str(e)[:20]}..."
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        print(f"{timestamp}\t请求 {i+1}\t{status} (耗时: {elapsed:.2f}s)")
    
    print("\n测试完成！可以看到请求3之后有明显的等待时间。")


def test_domain_isolation():
    """测试不同域名的限制隔离"""
    print("\n测试不同域名的限制隔离...")
    
    # 设置httpbin.org的限制为每分钟2次
    rate_limiter.set_domain_limit('httpbin.org', 2)
    
    print("交替请求两个不同域名，httpbin.org限制为每分钟2次，httpbingo.org无限制...")
    print("时间戳\t\t域名\t\t\t请求序号\t状态")
    print("-" * 60)
    
    domains = ['httpbin.org', 'httpbingo.org']
    for i in range(4):
        domain = domains[i % 2]
        url = f'https://{domain}/get'
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        
        try:
            response = requests.request('get', url, timeout=10)
            status = "成功"
        except Exception as e:
            status = f"失败: {str(e)[:20]}..."
        
        print(f"{timestamp}\t{domain.ljust(15)}\t请求 {i+1}\t{status}")
    
    print("\n测试完成！可以看到httpbin.org的请求有等待，而httpbingo.org没有。")


if __name__ == "__main__":
    print("开始简单测试频率限制功能...\n")
    
    # 测试频率限制
    test_rate_limit_visual()
    
    # 测试域名隔离
    test_domain_isolation()
    
    print("\n所有测试完成！")