#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试频率限制功能
"""

import sys
import time

# 添加项目根目录到Python路径
sys.path.insert(0, 'd:\\Repo\\adata')

from adata.common.utils.sunrequests import sun_requests


def test_rate_limit():
    """
    测试频率限制功能
    """
    try:
        print("开始测试频率限制功能...")
        
        # 设置测试域名的限制为5次/分钟
        test_domain = "api.github.com"
        sun_requests.set_domain_limit(test_domain, 5)
        
        print(f"设置 {test_domain} 的限制为5次/分钟")
        
        # 发送6次请求，应该在第6次时触发等待
        start_time = time.time()
        for i in range(6):
            request_start = time.time()
            print(f"\n发送第{i+1}次请求...")
            response = sun_requests.request('get', f'https://{test_domain}/repos/octocat/hello-world')
            request_end = time.time()
            print(f"请求耗时: {request_end - request_start:.2f}秒, 状态码: {response.status_code if response else 'None'}")
        
        total_time = time.time() - start_time
        print(f"\n总耗时: {total_time:.2f}秒")
        print("如果第6次请求耗时明显增加，说明频率限制功能正常工作")
    except Exception as e:
        print(f"测试出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_rate_limit()
