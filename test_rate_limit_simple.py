#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试频率限制功能
"""

import sys
import time

# 添加项目根目录到Python路径
sys.path.insert(0, 'd:\\Repo\\adata')

from adata.common.utils.sunrequests import SunRequests


def test_rate_limit_simple():
    """
    简单测试频率限制功能
    """
    try:
        print("开始测试频率限制功能...")
        
        # 创建SunRequests实例
        requests = SunRequests()
        
        # 设置测试域名的限制为3次/分钟
        test_domain = "test.example.com"
        requests.set_domain_limit(test_domain, 3)
        
        print(f"设置 {test_domain} 的限制为3次/分钟")
        
        # 模拟发送4次请求，应该在第4次时触发等待
        start_time = time.time()
        for i in range(4):
            request_start = time.time()
            print(f"\n模拟第{i+1}次请求...")
            # 直接调用_check_rate_limit方法
            requests._check_rate_limit(f"https://{test_domain}/test")
            request_end = time.time()
            print(f"处理耗时: {request_end - request_start:.2f}秒")
        
        total_time = time.time() - start_time
        print(f"\n总耗时: {total_time:.2f}秒")
        print("如果第4次请求耗时明显增加，说明频率限制功能正常工作")
    except Exception as e:
        print(f"测试出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_rate_limit_simple()
