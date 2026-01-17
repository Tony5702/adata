# -*- coding: utf-8 -*-
"""
测试频率限制功能
"""

import time
from adata.common.utils import requests, rate_limiter


def test_rate_limiter():
    print("测试频率限制功能...")
    
    # 设置 eastmoney.com 的频率限制为 5次/10秒
    requests.set_rate_limit('eastmoney.com', max_requests=5, window_seconds=10)
    
    # 设置 baidu.com 的频率限制为 3次/5秒
    requests.set_rate_limit('baidu.com', max_requests=3, window_seconds=5)
    
    print("\n测试 eastmoney.com (5次/10秒):")
    start_time = time.time()
    for i in range(8):
        print(f"请求 {i+1} 开始时间: {time.time() - start_time:.2f}s")
        try:
            res = requests.request('get', 'http://push2his.eastmoney.com/api/qt/stock/kline/get?fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f116&ut=7eea3edcaed734bea9cbfc24409ed989&klt=101&fqt=1&secid=0.000001&beg=20240101&end=20240110')
            print(f"请求 {i+1} 完成, 状态码: {res.status_code}")
        except Exception as e:
            print(f"请求 {i+1} 失败: {e}")
    
    print(f"\n总耗时: {time.time() - start_time:.2f}s")
    
    print("\n测试 baidu.com (3次/5秒):")
    start_time = time.time()
    for i in range(5):
        print(f"请求 {i+1} 开始时间: {time.time() - start_time:.2f}s")
        try:
            res = requests.request('get', 'https://finance.pae.baidu.com/selfselect/getstockquotation?all=1&isIndex=false&isBk=false&isBlock=false&isFutures=false&isStock=true&newFormat=1&group=quotation_kline_ab&finClientType=pc&code=000001&start_time=2024-01-01 00:00:00&ktype=1')
            print(f"请求 {i+1} 完成, 状态码: {res.status_code}")
        except Exception as e:
            print(f"请求 {i+1} 失败: {e}")
    
    print(f"\n总耗时: {time.time() - start_time:.2f}s")
    
    # 重置频率限制
    print("\n重置频率限制...")
    requests.reset_rate_limit()
    
    print("\n测试完成！")


if __name__ == '__main__':
    test_rate_limiter()
