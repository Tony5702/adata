# -*- coding: utf-8 -*-
"""
测试频率限制器修复效果
"""
import time
import threading
from adata.common import set_rate_limit, set_default_rate_limit
from adata.common.utils import requests


def test_timeout_mechanism():
    """测试超时机制"""
    print("=== 测试超时机制 ===")
    
    # 设置非常严格的限制（1次/分钟）
    test_domain = "httpbin.org"
    set_rate_limit(test_domain, 1)
    print(f"设置 {test_domain} 每分钟限制1次请求")
    
    url = "https://httpbin.org/get"
    
    # 第一次请求应该成功
    print("\n1. 第一次请求...")
    start = time.time()
    try:
        res = requests.request('get', url, timeout=5)
        print(f"✓ 请求成功，状态码: {res.status_code}")
    except Exception as e:
        print(f"✗ 请求失败: {e}")
    print(f"耗时: {time.time() - start:.2f}s")
    
    # 第二次请求应该超时（因为限制了1次/分钟）
    print("\n2. 第二次请求（应该超时）...")
    start = time.time()
    try:
        res = requests.request('get', url, timeout=5, max_wait_time=2)
        print(f"✗ 预期应该超时，但请求成功了，状态码: {res.status_code}")
    except Exception as e:
        print(f"✓ 预期的超时异常: {type(e).__name__}")
    print(f"耗时: {time.time() - start:.2f}s")
    print()


def test_concurrent_requests():
    """测试并发请求（验证死锁修复）"""
    print("=== 测试并发请求 ===")
    
    test_domain = "httpbin.org"
    set_rate_limit(test_domain, 5)  # 每分钟5次
    print(f"设置 {test_domain} 每分钟限制5次请求")
    
    url = "https://httpbin.org/get"
    results = []
    
    def worker(i):
        try:
            start = time.time()
            res = requests.request('get', url, timeout=10, max_wait_time=10)
            results.append((i, True, res.status_code, time.time() - start))
        except Exception as e:
            results.append((i, False, str(e), time.time() - start))
    
    # 启动10个并发请求
    threads = []
    for i in range(10):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()
    
    # 等待所有线程完成
    for t in threads:
        t.join()
    
    # 统计结果
    success_count = sum(1 for _, success, _, _ in results if success)
    print(f"\n10个并发请求结果:")
    print(f"成功: {success_count}, 失败: {10 - success_count}")
    
    for i, success, result, duration in results:
        if success:
            print(f"请求 {i}: 成功，状态码={result}，耗时={duration:.2f}s")
        else:
            print(f"请求 {i}: 失败，原因={result}，耗时={duration:.2f}s")
    print()


def test_backoff_strategy():
    """测试指数退避策略"""
    print("=== 测试指数退避策略 ===")
    
    test_domain = "httpbin.org"
    set_rate_limit(test_domain, 2)  # 每分钟2次
    print(f"设置 {test_domain} 每分钟限制2次请求")
    
    url = "https://httpbin.org/get"
    
    # 连续发送3次请求
    for i in range(3):
        start = time.time()
        try:
            res = requests.request('get', url, timeout=10, max_wait_time=5)
            print(f"请求 {i+1}: 成功，状态码={res.status_code}，耗时={time.time() - start:.2f}s")
        except Exception as e:
            print(f"请求 {i+1}: 失败，原因={e}，耗时={time.time() - start:.2f}s")
        time.sleep(0.1)  # 小延迟，避免并发问题
    print()


def test_default_settings():
    """测试默认设置"""
    print("=== 测试默认设置 ===")
    
    # 恢复默认设置
    set_default_rate_limit(30)
    print("恢复默认频率限制：每分钟30次")
    
    url = "https://httpbin.org/get"
    
    # 快速发送5次请求
    start = time.time()
    for i in range(5):
        try:
            res = requests.request('get', url, timeout=5)
            print(f"请求 {i+1}: 成功，状态码={res.status_code}")
        except Exception as e:
            print(f"请求 {i+1}: 失败，原因={e}")
    print(f"5次请求总耗时: {time.time() - start:.2f}s")
    print()


if __name__ == "__main__":
    print("频率限制器修复测试\n")
    
    # 测试1: 超时机制
    test_timeout_mechanism()
    
    # 测试2: 并发请求（验证死锁修复）
    print("注意：接下来的测试会模拟并发请求，验证死锁修复...")
    time.sleep(1)
    test_concurrent_requests()
    
    # 测试3: 指数退避策略
    test_backoff_strategy()
    
    # 测试4: 默认设置
    test_default_settings()
    
    print("=== 所有测试完成 ===")
