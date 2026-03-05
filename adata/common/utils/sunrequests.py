# -*- coding: utf-8 -*-
"""
代理:https://jahttp.zhimaruanjian.com/getapi/

@desc: adata 请求工具类
@author: 1nchaos
@time:2023/3/30
@log: 封装请求次数
"""

import threading
import time
from collections import defaultdict
from urllib.parse import urlparse

import requests


class RateLimiter:
    """
    基于域名的频率限制器
    默认每分钟每个域名30次请求，可通过方法自定义
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init()
        return cls._instance
    
    def _init(self):
        # 默认限制：每分钟30次
        self._default_limit = 30
        self._window_size = 60  # 时间窗口：60秒
        # 域名特定限制：域名 -> 每分钟最大请求数
        self._domain_limits = {}
        # 请求记录：域名 -> [(timestamp, count), ...]
        self._request_records = defaultdict(list)
        self._records_lock = threading.Lock()
    
    def set_limit(self, domain: str, requests_per_minute: int):
        """
        设置指定域名的频率限制
        :param domain: 域名，如 'eastmoney.com'
        :param requests_per_minute: 每分钟最大请求数
        """
        self._domain_limits[domain] = requests_per_minute
    
    def set_default_limit(self, requests_per_minute: int):
        """
        设置默认的频率限制（对所有未单独设置的域名生效）
        :param requests_per_minute: 每分钟最大请求数
        """
        self._default_limit = requests_per_minute
    
    def get_limit(self, domain: str) -> int:
        """获取指定域名的频率限制"""
        return self._domain_limits.get(domain, self._default_limit)
    
    def _clean_old_records(self, domain: str, current_time: float):
        """清理过期的请求记录"""
        cutoff_time = current_time - self._window_size
        with self._records_lock:
            records = self._request_records.get(domain, [])
            self._request_records[domain] = [
                (t, c) for t, c in records if t > cutoff_time
            ]
    
    def _get_request_count(self, domain: str, current_time: float) -> int:
        """获取当前时间窗口内的请求次数"""
        cutoff_time = current_time - self._window_size
        with self._records_lock:
            records = self._request_records.get(domain, [])
            return sum(c for t, c in records if t > cutoff_time)
    
    def acquire(self, url: str, max_wait_time: float = 30.0):
        """
        请求频率限制，如果超过限制则等待
        :param url: 请求的URL
        :param max_wait_time: 最大等待时间（秒），默认30秒
        :raises TimeoutError: 当超过最大等待时间仍无法获取请求权限时
        """
        domain = self._extract_domain(url)
        limit = self.get_limit(domain)
        start_time = time.time()
        retry_count = 0
        max_retry_backoff = 2.0  # 最大退避时间（秒）
        
        while time.time() - start_time < max_wait_time:
            current_time = time.time()
            self._clean_old_records(domain, current_time)
            current_count = self._get_request_count(domain, current_time)
            
            if current_count < limit:
                # 可以请求，记录本次请求
                with self._records_lock:
                    self._request_records[domain].append((current_time, 1))
                return
            else:
                # 超过限制，等待后重试
                # 计算需要等待的时间（直到最早的一条记录过期）
                with self._records_lock:
                    records = self._request_records.get(domain, [])
                    if records:
                        oldest_time = min(t for t, c in records)
                        wait_time = oldest_time + self._window_size - current_time
                        if wait_time > 0:
                            # 计算指数退避时间（最大不超过max_retry_backoff）
                            backoff_time = min(0.1 * (2 ** min(retry_count, 8)), max_retry_backoff)
                            actual_wait = min(wait_time, backoff_time)
                            time.sleep(actual_wait)
                        else:
                            time.sleep(0.1)
                    else:
                        time.sleep(0.1)
                
                retry_count += 1
        
        # 超过最大等待时间
        raise TimeoutError(f"请求频率限制超时：{url}，已等待 {max_wait_time:.1f} 秒")
    
    def _extract_domain(self, url: str) -> str:
        """从URL中提取域名"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            # 移除端口
            if ':' in domain:
                domain = domain.split(':')[0]
            return domain
        except Exception:
            return url


class SunProxy(object):
    _data = {}
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(SunProxy, "_instance"):
            with SunProxy._instance_lock:
                if not hasattr(SunProxy, "_instance"):
                    SunProxy._instance = object.__new__(cls)

    @classmethod
    def set(cls, key, value):
        cls._data[key] = value

    @classmethod
    def get(cls, key):
        return cls._data.get(key)

    @classmethod
    def delete(cls, key):
        if key in cls._data:
            del cls._data[key]


class SunRequests(object):
    def __init__(self, sun_proxy: SunProxy = None) -> None:
        super().__init__()
        self.sun_proxy = sun_proxy
        self._rate_limiter = RateLimiter()

    def request(self, method='get', url=None, times=3, retry_wait_time=1588, proxies=None, wait_time=None, 
                rate_limit=True, max_wait_time: float = 30.0, **kwargs):
        """
        简单封装的请求，参考requests，增加循环次数和次数之间的等待时间
        :param proxies: 代理配置
        :param method: 请求方法： get；post
        :param url: url
        :param times: 次数，int
        :param retry_wait_time: 重试等待时间，毫秒
        :param wait_time: 等待时间：毫秒；表示每个请求的间隔时间，在请求之前等待sleep，主要用于防止请求太频繁的限制。
        :param rate_limit: 是否启用频率限制，默认True
        :param max_wait_time: 频率限制最大等待时间（秒），默认30秒
        :param kwargs: 其它 requests 参数，用法相同
        :return: res
        """
        # 1. 频率限制检查
        if rate_limit and url:
            try:
                self._rate_limiter.acquire(url, max_wait_time)
            except TimeoutError as e:
                # 频率限制超时，记录日志并继续执行（使用原始requests）
                import logging
                logging.warning(f"频率限制超时: {e}")
        
        # 2. 获取设置代理
        proxies = self.__get_proxies(proxies)
        # 3. 请求数据结果
        res = None
        for i in range(times):
            if wait_time:
                time.sleep(wait_time / 1000)
            res = requests.request(method=method, url=url, proxies=proxies, **kwargs)
            if res.status_code in (200, 404):
                return res
            time.sleep(retry_wait_time / 1000)
            if i == times - 1:
                return res
        return res
    
    def set_rate_limit(self, domain: str, requests_per_minute: int):
        """
        设置指定域名的频率限制
        :param domain: 域名，如 'eastmoney.com' 或 'push2his.eastmoney.com'
        :param requests_per_minute: 每分钟最大请求数
        """
        self._rate_limiter.set_limit(domain, requests_per_minute)
    
    def set_default_rate_limit(self, requests_per_minute: int):
        """
        设置默认的频率限制（对所有未单独设置的域名生效）
        :param requests_per_minute: 每分钟最大请求数，默认30
        """
        self._rate_limiter.set_default_limit(requests_per_minute)

    def __get_proxies(self, proxies):
        """
        获取代理配置
        """
        if proxies is None:
            proxies = {}
        is_proxy = SunProxy.get('is_proxy')
        ip = SunProxy.get('ip')
        proxy_url = SunProxy.get('proxy_url')
        if not ip and is_proxy and proxy_url:
            ip = requests.get(url=proxy_url).text.replace('\r\n', '') \
                .replace('\r', '').replace('\n', '').replace('\t', '')
        if is_proxy and ip:
            proxies = {'https': f"http://{ip}", 'http': f"http://{ip}"}
        return proxies


sun_requests = SunRequests()
