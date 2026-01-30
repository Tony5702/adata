# -*- coding: utf-8 -*-
"""
@desc: 请求频率限制器
@author: 1nchaos
@time: 2023/09/01
@log: 实现按域名限制请求频率功能
"""

import threading
import time
from collections import defaultdict
from urllib.parse import urlparse


class RateLimiter:
    """
    请求频率限制器，支持按域名限制请求频率
    """

    _instance = None
    _instance_lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init()
        return cls._instance
    
    def _init(self):
        # 初始化实例变量
        self._domain_counters = defaultdict(list)  # 存储每个域名的请求时间戳
        self._domain_limits = {}  # 存储每个域名的请求限制
        self._default_limit = 30  # 默认每分钟30次请求
        self._time_window = 60  # 时间窗口为60秒
        self._lock = threading.Lock()  # 用于线程安全的锁

    def set_domain_limit(self, domain, limit):
        """
        设置特定域名的请求限制
        :param domain: 域名
        :param limit: 每分钟请求次数限制
        """
        with self._lock:
            self._domain_limits[domain] = limit

    def set_default_limit(self, limit):
        """
        设置默认的请求限制
        :param limit: 每分钟请求次数限制
        """
        with self._lock:
            self._default_limit = limit

    def get_domain_limit(self, domain):
        """
        获取域名的请求限制
        :param domain: 域名
        :return: 每分钟请求次数限制
        """
        with self._lock:
            return self._domain_limits.get(domain, self._default_limit)

    def _extract_domain(self, url):
        """
        从URL中提取域名
        :param url: 请求URL
        :return: 域名
        """
        try:
            parsed_url = urlparse(url)
            return parsed_url.netloc
        except Exception:
            return "unknown"

    def _clean_old_requests(self, domain, current_time):
        """
        清理过期的请求记录
        :param domain: 域名
        :param current_time: 当前时间戳
        """
        # 保留时间窗口内的请求记录
        self._domain_counters[domain] = [
            timestamp for timestamp in self._domain_counters[domain]
            if current_time - timestamp < self._time_window
        ]

    def wait_if_needed(self, url):
        """
        如果需要，等待直到可以发起请求
        :param url: 请求URL
        """
        domain = self._extract_domain(url)
        limit = self.get_domain_limit(domain)
        
        with self._lock:
            current_time = time.time()
            
            # 清理过期的请求记录
            self._clean_old_requests(domain, current_time)
            
            # 检查是否超过限制
            if len(self._domain_counters[domain]) >= limit:
                # 计算需要等待的时间
                oldest_request = min(self._domain_counters[domain])
                wait_time = self._time_window - (current_time - oldest_request)
                
                if wait_time > 0:
                    # 释放锁，然后等待
                    self._lock.release()
                    time.sleep(wait_time)
                    # 重新获取锁
                    self._lock.acquire()
                    # 更新当前时间
                    current_time = time.time()
                    # 再次清理过期请求
                    self._clean_old_requests(domain, current_time)
            
            # 记录当前请求
            self._domain_counters[domain].append(current_time)


# 创建全局单例
rate_limiter = RateLimiter()