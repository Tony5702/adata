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
from collections import defaultdict, deque
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


class RateLimiter(object):
    _instance_lock = threading.Lock()

    def __init__(self, default_max_requests=30, default_window_seconds=60):
        self._request_times = defaultdict(deque)
        self._limits = defaultdict(lambda: (default_max_requests, default_window_seconds))
        self._default_max_requests = default_max_requests
        self._default_window_seconds = default_window_seconds
        self._lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(RateLimiter, "_instance"):
            with RateLimiter._instance_lock:
                if not hasattr(RateLimiter, "_instance"):
                    RateLimiter._instance = object.__new__(cls)
        return RateLimiter._instance

    def set_rate_limit(self, domain, max_requests=None, window_seconds=None):
        with self._lock:
            if max_requests is None:
                max_requests = self._default_max_requests
            if window_seconds is None:
                window_seconds = self._default_window_seconds
            self._limits[domain] = (max_requests, window_seconds)

    def _get_domain(self, url):
        parsed = urlparse(url)
        return parsed.netloc

    def _clean_old_requests(self, domain, current_time, window_seconds):
        request_times = self._request_times[domain]
        while request_times and current_time - request_times[0] > window_seconds:
            request_times.popleft()

    def acquire(self, url):
        domain = self._get_domain(url)
        max_requests, window_seconds = self._limits[domain]
        current_time = time.time()

        with self._lock:
            self._clean_old_requests(domain, current_time, window_seconds)
            request_times = self._request_times[domain]

            if len(request_times) >= max_requests:
                sleep_time = window_seconds - (current_time - request_times[0])
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    self._clean_old_requests(domain, time.time(), window_seconds)

            self._request_times[domain].append(time.time())

    def reset(self, domain=None):
        with self._lock:
            if domain:
                self._request_times[domain].clear()
            else:
                self._request_times.clear()
                self._limits.clear()


rate_limiter = RateLimiter()


class SunRequests(object):
    def __init__(self, sun_proxy: SunProxy = None) -> None:
        super().__init__()
        self.sun_proxy = sun_proxy

    @staticmethod
    def set_rate_limit(domain, max_requests=None, window_seconds=None):
        """
        设置指定域名的请求频率限制
        :param domain: 域名，如 'eastmoney.com' 或 'baidu.com'
        :param max_requests: 最大请求数，默认为30
        :param window_seconds: 时间窗口（秒），默认为60
        """
        rate_limiter.set_rate_limit(domain, max_requests, window_seconds)

    @staticmethod
    def reset_rate_limit(domain=None):
        """
        重置频率限制器
        :param domain: 指定域名，如果为None则重置所有
        """
        rate_limiter.reset(domain)

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
        # 1. 频率限制
        if url:
            rate_limiter.acquire(url)
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
