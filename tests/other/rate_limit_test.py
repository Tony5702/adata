# -*- coding: utf-8 -*-
"""
@desc: 频率限制测试
@author: 1nchaos
@time: 2026/2/26
@log: 
"""
import time
from adata.common.utils import requests


def test_rate_limit():
    """测试频率限制功能"""
    # 测试1: 检查默认限制
    print("=== 测试1: 默认频率限制 ===")
    default_limit = requests.get_rate_limit("www.example.com")
    print(f"默认限制: {default_limit}次/分钟")
    assert default_limit == 30, "默认限制应该是30次/分钟"
    
    # 测试2: 设置自定义限制
    print("\n=== 测试2: 设置自定义限制 ===")
    requests.set_rate_limit("www.test.com", 5)
    custom_limit = requests.get_rate_limit("www.test.com")
    print(f"自定义限制: {custom_limit}次/分钟")
    assert custom_limit == 5, "自定义限制应该是5次/分钟"
    
    # 测试3: 使用URL设置限制
    print("\n=== 测试3: 使用URL设置限制 ===")
    requests.set_rate_limit("http://www.example2.com/path", 10)
    url_limit = requests.get_rate_limit("www.example2.com")
    print(f"通过URL设置的限制: {url_limit}次/分钟")
    assert url_limit == 10, "通过URL设置的限制应该是10次/分钟"
    
    # 测试4: 频率限制实际效果测试（模拟快速请求）
    print("\n=== 测试4: 频率限制实际效果测试 ===")
    test_domain = "httpbin.org"
    requests.set_rate_limit(test_domain, 2)  # 设置为每分钟2次，方便测试
    
    start_time = time.time()
    
    # 发送3次请求
    for i in range(3):
        req_start = time.time()
        try:
            res = requests.request('get', f'https://{test_domain}/get', timeout=10)
            print(f"请求{i+1}: 状态码={res.status_code}, 耗时={time.time()-req_start:.2f}秒")
        except Exception as e:
            print(f"请求{i+1}: 失败 - {e}")
    
    total_time = time.time() - start_time
    print(f"总耗时: {total_time:.2f}秒")
    print("如果频率限制生效，3次请求应该花费至少60秒（因为限制是2次/分钟）")
    
    print("\n=== 所有测试完成 ===")


if __name__ == '__main__':
    test_rate_limit()
