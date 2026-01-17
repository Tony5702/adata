# -*- coding: utf-8 -*-
"""
测试频率限制功能 - 更严格的测试
"""

import time
from adata.common.utils import rate_limiter


def test_rate_limiter_strict():
    print("测试频率限制功能（严格模式）...")
    
    # 设置测试域名的频率限制为 3次/5秒
    rate_limiter.set_rate_limit('example.com', max_requests=3, window_seconds=5)
    
    print("\n测试 example.com (3次/5秒):")
    print("前3次请求应该立即执行，第4次请求应该等待约2秒")
    
    start_time = time.time()
    for i in range(5):
        print(f"请求 {i+1} 开始时间: {time.time() - start_time:.2f}s")
        rate_limiter.acquire('http://example.com/test')
        print(f"请求 {i+1} 完成, 当前时间: {time.time() - start_time:.2f}s")
    
    print(f"\n总耗时: {time.time() - start_time:.2f}s")
    print("预期: 前3次请求耗时很短，第4次请求会等待约2秒")
    
    # 重置频率限制
    print("\n重置频率限制...")
    rate_limiter.reset()
    
    print("\n测试完成！")


if __name__ == '__main__':
    test_rate_limiter_strict()
