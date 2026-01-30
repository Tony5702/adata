# -*- coding: utf-8 -*-
"""
@desc: 频率限制器使用示例
@author: 1nchaos
@time: 2023/09/01
@log: 演示如何使用频率限制功能
"""

from adata.common.utils import requests, rate_limiter

# 示例1：使用默认频率限制（每分钟30次）
def example_default_rate_limit():
    """使用默认频率限制的示例"""
    # 这将使用默认的每分钟30次请求限制
    response = requests.request('get', 'https://api.example.com/data')
    return response

# 示例2：为特定域名设置自定义频率限制
def example_custom_domain_limit():
    """为特定域名设置自定义频率限制的示例"""
    # 为特定域名设置每分钟10次请求的限制
    rate_limiter.set_domain_limit('api.example.com', 10)
    
    # 这些请求将受到每分钟10次的限制
    response1 = requests.request('get', 'https://api.example.com/data1')
    response2 = requests.request('get', 'https://api.example.com/data2')
    
    return response1, response2

# 示例3：为单个请求设置临时频率限制
def example_per_request_limit():
    """为单个请求设置临时频率限制的示例"""
    # 这个请求将使用每分钟5次的临时限制
    response = requests.request('get', 'https://api.example.com/data', rate_limit=5)
    
    # 其他请求仍使用默认限制或域名特定限制
    other_response = requests.request('get', 'https://api.example.com/other')
    
    return response, other_response

# 示例4：设置全局默认频率限制
def example_global_default_limit():
    """设置全局默认频率限制的示例"""
    # 将全局默认限制改为每分钟60次
    rate_limiter.set_default_limit(60)
    
    # 所有未设置特定限制的域名都将使用这个新限制
    response = requests.request('get', 'https://api.example.com/data')
    
    return response