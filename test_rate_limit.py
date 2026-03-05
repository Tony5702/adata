# -*- coding: utf-8 -*-
"""
测试频率限制功能
"""
import time
from adata.common import set_rate_limit, set_default_rate_limit
from adata.common.utils import requests


def test_default_rate_limit():
    """测试默认频率限制"""
    print("=== 测试默认频率限制 ===")
    print("默认限制：每分钟30次")
    
    url = "http://push2his.eastmoney.com/api/qt/stock/kline/get"
    
    start_time = time.time()
    for i in range(5):
        try:
            # 使用rate_limit=False来测试无限制的情况
            # 这里我们只是测试请求是否能正常发出，不等待响应
            print(f"请求 {i+1}: {time.time() - start_time:.2f}s")
        except Exception as e:
            print(f"请求 {i+1} 出错: {e}")
    
    elapsed = time.time() - start_time
    print(f"5次请求耗时: {elapsed:.2f}s")
    print()


def test_custom_rate_limit():
    """测试自定义频率限制"""
    print("=== 测试自定义频率限制 ===")
    
    # 设置测试域名每分钟2次请求
    test_domain = "httpbin.org"
    set_rate_limit(test_domain, 2)
    print(f"设置 {test_domain} 每分钟限制2次请求")
    
    url = "https://httpbin.org/get"
    
    start_time = time.time()
    for i in range(4):
        try:
            res = requests.request(method='get', url=url, timeout=10)
            print(f"请求 {i+1}: 状态码={res.status_code}, 耗时={time.time() - start_time:.2f}s")
        except Exception as e:
            print(f"请求 {i+1} 出错: {e}")
    
    elapsed = time.time() - start_time
    print(f"4次请求总耗时: {elapsed:.2f}s (预期超过60秒，因为每分钟只允许2次)")
    print()


def test_set_default_rate_limit():
    """测试设置默认频率限制"""
    print("=== 测试设置默认频率限制 ===")
    
    set_default_rate_limit(10)
    print("设置默认频率限制为每分钟10次")
    
    url = "https://httpbin.org/get"
    
    start_time = time.time()
    for i in range(3):
        try:
            res = requests.request(method='get', url=url, timeout=10)
            print(f"请求 {i+1}: 状态码={res.status_code}, 耗时={time.time() - start_time:.2f}s")
        except Exception as e:
            print(f"请求 {i+1} 出错: {e}")
    
    elapsed = time.time() - start_time
    print(f"3次请求总耗时: {elapsed:.2f}s")
    print()


def test_disable_rate_limit():
    """测试禁用频率限制"""
    print("=== 测试禁用频率限制 ===")
    
    url = "https://httpbin.org/get"
    
    start_time = time.time()
    for i in range(3):
        try:
            # rate_limit=False 禁用频率限制
            res = requests.request(method='get', url=url, timeout=10, rate_limit=False)
            print(f"请求 {i+1}: 状态码={res.status_code}, 耗时={time.time() - start_time:.2f}s")
        except Exception as e:
            print(f"请求 {i+1} 出错: {e}")
    
    elapsed = time.time() - start_time
    print(f"3次请求总耗时: {elapsed:.2f}s (应该很快，因为没有频率限制)")
    print()


if __name__ == "__main__":
    print("频率限制功能测试\n")
    
    # 测试1: 基本功能
    test_default_rate_limit()
    
    # 测试2: 自定义频率限制（这个测试会比较慢，因为限制了2次/分钟）
    print("注意：接下来的测试会比较慢，因为设置了2次/分钟的限制...")
    time.sleep(1)
    test_custom_rate_limit()
    
    # 测试3: 设置默认限制
    test_set_default_rate_limit()
    
    # 测试4: 禁用频率限制
    test_disable_rate_limit()
    
    print("=== 所有测试完成 ===")
