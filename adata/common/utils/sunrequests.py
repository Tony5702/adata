# -*- coding: utf-8 -*-
"""
代理:https://jahttp.zhimaruanjian.com/getapi/

@desc: adata 请求工具类
@author: 1nchaos
@time:2023/3/30
@log: 封装请求次数；添加频率限制
"""

import threading
import time
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
    _instance_lock = threading.Lock()
    _rate_limits = {}
    _rate_limit_locks = threading.Lock()
    
    def __new__(cls):
        if not hasattr(RateLimiter, "_instance"):
            with RateLimiter._instance_lock:
                if not hasattr(RateLimiter, "_instance"):
                    RateLimiter._instance = object.__new__(cls)
        return RateLimiter._instance
    
    def __init__(self):
        self.default_requests_per_minute = 30
    
    def set_rate_limit(self, domain, requests_per_minute):
        with self._rate_limit_locks:
            if domain in self._rate_limits:
                _, timestamps = self._rate_limits[domain]
                self._rate_limits[domain] = (requests_per_minute, timestamps)
            else:
                self._rate_limits[domain] = (requests_per_minute, [])
    
    def check_rate_limit(self, domain):
        current_time = time.time()
        
        with self._rate_limit_locks:
            if domain in self._rate_limits:
                limit, timestamps = self._rate_limits[domain]
            else:
                limit = self.default_requests_per_minute
                timestamps = []
                self._rate_limits[domain] = (limit, timestamps)
            
            timestamps = [t for t in timestamps if current_time - t < 60]
            
            if len(timestamps) >= limit:
                oldest_time = timestamps[0]
                wait_time = (oldest_time + 60) - current_time
                if wait_time > 0:
                    return False, wait_time
            
            timestamps.append(current_time)
            self._rate_limits[domain] = (limit, timestamps)
            return True, 0


class SunRequests(object):
    def __init__(self, sun_proxy: SunProxy = None) -> None:
        super().__init__()
        self.sun_proxy = sun_proxy
        self.rate_limiter = RateLimiter()
    
    def set_rate_limit(self, domain, requests_per_minute):
        self.rate_limiter.set_rate_limit(domain, requests_per_minute)
    
    def _get_domain(self, url):
        parsed = urlparse(url)
        return parsed.netloc

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
        # 1. 频率限制检查
        domain = self._get_domain(url)
        allowed, wait_time_needed = self.rate_limiter.check_rate_limit(domain)
        if not allowed:
            print(f"频率限制触发: {domain} 等待 {wait_time_needed:.2f}秒")
            time.sleep(wait_time_needed)
        
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
