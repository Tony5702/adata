# -*- coding: utf-8 -*-
"""
@desc: 频率限制器测试
@author: 1nchaos
@time: 2023/09/01
@log: 测试频率限制功能
"""

import time
import threading
from adata.common.utils import requests, rate_limiter


def test_default_rate_limit():
    """测试默认频率限制"""
    print("测试默认频率限制（每分钟30次）...")
    start_time = time.time()
    
    # 连续发送5个请求
    for i in range(5):
        print(f"发送请求 {i+1}...")
        try:
            # 使用httpbin.org测试，这是一个用于测试HTTP请求的服务
            response = requests.request('get', 'https://httpbin.org/delay/1', timeout=5)
            print(f"请求 {i+1} 完成，状态码: {response.status_code}")
        except Exception as e:
            print(f"请求 {i+1} 失败: {e}")
    
    end_time = time.time()
    print(f"总耗时: {end_time - start_time:.2f}秒\n")


def test_custom_domain_limit():
    """测试自定义域名频率限制"""
    print("测试自定义域名频率限制（每分钟3次）...")
    
    # 设置httpbin.org域名的限制为每分钟3次
    rate_limiter.set_domain_limit('httpbin.org', 3)
    
    start_time = time.time()
    
    # 连续发送5个请求，应该会有等待时间
    for i in range(5):
        print(f"发送请求 {i+1}...")
        request_start = time.time()
        try:
            response = requests.request('get', 'https://httpbin.org/delay/0', timeout=5)
            request_end = time.time()
            print(f"请求 {i+1} 完成，状态码: {response.status_code}，请求耗时: {request_end - request_start:.2f}秒")
        except Exception as e:
            print(f"请求 {i+1} 失败: {e}")
    
    end_time = time.time()
    print(f"总耗时: {end_time - start_time:.2f}秒\n")


def test_per_request_limit():
    """测试单个请求的临时频率限制"""
    print("测试单个请求的临时频率限制（每分钟2次）...")
    
    start_time = time.time()
    
    # 第一个请求使用临时限制
    print("发送带临时限制的请求 1...")
    try:
        response = requests.request('get', 'https://httpbin.org/delay/0', timeout=5, rate_limit=2)
        print(f"请求 1 完成，状态码: {response.status_code}")
    except Exception as e:
        print(f"请求 1 失败: {e}")
    
    # 第二个请求使用临时限制
    print("发送带临时限制的请求 2...")
    try:
        response = requests.request('get', 'https://httpbin.org/delay/0', timeout=5, rate_limit=2)
        print(f"请求 2 完成，状态码: {response.status_code}")
    except Exception as e:
        print(f"请求 2 失败: {e}")
    
    # 第三个请求不使用临时限制，应该使用默认限制
    print("发送不带临时限制的请求 3...")
    try:
        response = requests.request('get', 'https://httpbin.org/delay/0', timeout=5)
        print(f"请求 3 完成，状态码: {response.status_code}")
    except Exception as e:
        print(f"请求 3 失败: {e}")
    
    end_time = time.time()
    print(f"总耗时: {end_time - start_time:.2f}秒\n")


def test_thread_safety():
    """测试线程安全性"""
    print("测试线程安全性...")
    
    results = []
    
    def worker(worker_id):
        """工作线程函数"""
        start_time = time.time()
        try:
            response = requests.request('get', 'https://httpbin.org/delay/0', timeout=5)
            end_time = time.time()
            results.append({
                'worker_id': worker_id,
                'status_code': response.status_code,
                'duration': end_time - start_time
            })
            print(f"工作线程 {worker_id} 完成，状态码: {response.status_code}，耗时: {end_time - start_time:.2f}秒")
        except Exception as e:
            results.append({
                'worker_id': worker_id,
                'error': str(e)
            })
            print(f"工作线程 {worker_id} 失败: {e}")
    
    # 创建并启动5个线程
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(i+1,))
        threads.append(t)
        t.start()
    
    # 等待所有线程完成
    for t in threads:
        t.join()
    
    print(f"所有线程完成，共处理 {len(results)} 个请求\n")


def test_domain_isolation():
    """测试不同域名的限制隔离"""
    print("测试不同域名的限制隔离...")
    
    # 设置httpbin.org的限制为每分钟2次
    rate_limiter.set_domain_limit('httpbin.org', 2)
    
    start_time = time.time()
    
    # 交替请求不同域名
    domains = ['httpbin.org', 'httpbingo.org']
    for i in range(4):
        domain = domains[i % 2]
        url = f'https://{domain}/delay/0'
        print(f"发送请求到 {domain}...")
        try:
            response = requests.request('get', url, timeout=5)
            print(f"请求到 {domain} 完成，状态码: {response.status_code}")
        except Exception as e:
            print(f"请求到 {domain} 失败: {e}")
    
    end_time = time.time()
    print(f"总耗时: {end_time - start_time:.2f}秒\n")


if __name__ == "__main__":
    print("开始测试频率限制功能...\n")
    
    # 测试默认频率限制
    test_default_rate_limit()
    
    # 测试自定义域名频率限制
    test_custom_domain_limit()
    
    # 测试单个请求的临时频率限制
    test_per_request_limit()
    
    # 测试线程安全性
    test_thread_safety()
    
    # 测试不同域名的限制隔离
    test_domain_isolation()
    
    print("所有测试完成！")