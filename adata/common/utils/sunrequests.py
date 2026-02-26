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


class RateLimiter:
    """
    频率限制器，按域名控制请求频率
    默认每分钟每个域名30次请求
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
        # 每个域名的请求时间戳列表
        self._domain_requests = defaultdict(list)
        # 每个域名的限制次数，默认30次/分钟
        self._domain_limits = defaultdict(lambda: 30)
        # 时间窗口，默认60秒
        self._window_size = 60
        self._lock = threading.Lock()

    def set_limit(self, domain: str, limit: int):
        """
        设置指定域名的频率限制
        :param domain: 域名，如 'www.iwencai.com'
        :param limit: 每分钟最大请求次数
        """
        with self._lock:
            self._domain_limits[domain] = limit

    def get_limit(self, domain: str) -> int:
        """
        获取指定域名的频率限制
        :param domain: 域名
        :return: 每分钟最大请求次数
        """
        return self._domain_limits[domain]

    def wait_if_needed(self, url: str):
        """
        根据URL检查是否需要等待以满足频率限制
        :param url: 请求的URL
        """
        domain = self._extract_domain(url)
        limit = self._domain_limits[domain]
        
        with self._lock:
            now = time.time()
            # 清理窗口外的旧记录
            cutoff = now - self._window_size
            self._domain_requests[domain] = [
                ts for ts in self._domain_requests[domain] if ts > cutoff
            ]
            
            # 如果当前请求数已达限制，等待直到可以发送
            if len(self._domain_requests[domain]) >= limit:
                # 计算需要等待的时间
                oldest = min(self._domain_requests[domain])
                wait_time = self._window_size - (now - oldest)
                if wait_time > 0:
                    time.sleep(wait_time)
                    now = time.time()
                    # 再次清理
                    cutoff = now - self._window_size
                    self._domain_requests[domain] = [
                        ts for ts in self._domain_requests[domain] if ts > cutoff
                    ]
            
            # 记录本次请求
            self._domain_requests[domain].append(now)

    def _extract_domain(self, url: str) -> str:
        """
        从URL中提取域名
        :param url: URL
        :return: 域名
        """
        try:
            parsed = urlparse(url)
            return parsed.netloc.lower()
        except Exception:
            return url.lower()


class SunRequests(object):
    def __init__(self, sun_proxy: SunProxy = None) -> None:
        super().__init__()
        self.sun_proxy = sun_proxy
        self._rate_limiter = RateLimiter()

    def set_rate_limit(self, domain: str, limit: int):
        """
        设置指定域名的请求频率限制
        :param domain: 域名，如 'www.iwencai.com' 或 'http://www.iwencai.com'
        :param limit: 每分钟最大请求次数
        """
        # 如果传入的是URL，提取域名
        if '://' in domain or '/' in domain:
            domain = self._rate_limiter._extract_domain(domain)
        self._rate_limiter.set_limit(domain, limit)

    def get_rate_limit(self, domain: str) -> int:
        """
        获取指定域名的请求频率限制
        :param domain: 域名或URL
        :return: 每分钟最大请求次数
        """
        if '://' in domain or '/' in domain:
            domain = self._rate_limiter._extract_domain(domain)
        return self._rate_limiter.get_limit(domain)

    def request(self, method='get', url=None, times=3, retry_wait_time=1588, proxies=None, wait_time=None, **kwargs):
        """
        简单封装的请求，参考requests，增加循环次数和次数之间的等待时间
        :param proxies: 代理配置
        :param method: 请求方法： get；post
        :param url: url
        :param times: 次数，int
        :param retry_wait_time: 重试等待时间，毫秒
        :param wait_time: 等待时间：毫秒；表示每个请求的间隔时间，在请求之前等待sleep，主要用于防止请求太频繁的限制。
        :param kwargs: 其它 requests 参数，用法相同
        :return: res
        """
        # 0. 频率限制检查
        if url:
            self._rate_limiter.wait_if_needed(url)
        
        # 1. 获取设置代理
        proxies = self.__get_proxies(proxies)
        # 2. 请求数据结果
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
