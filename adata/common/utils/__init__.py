# -*- coding: utf-8 -*-
"""
@desc: readme
@author: 1nchaos
@time: 2023/3/29
@log: change log
"""
from .snowflake import worker
from .sunrequests import sun_requests as requests


def set_rate_limit(domain: str, requests_per_minute: int):
    """
    设置指定域名的请求频率限制
    :param domain: 域名，如 'eastmoney.com' 或 'push2his.eastmoney.com'
    :param requests_per_minute: 每分钟最大请求数
    
    示例:
        >>> from adata.common import set_rate_limit
        >>> set_rate_limit('eastmoney.com', 60)  # 东方财富每分钟60次
        >>> set_rate_limit('10jqka.com.cn', 20)  # 同花顺每分钟20次
    """
    requests.set_rate_limit(domain, requests_per_minute)


def set_default_rate_limit(requests_per_minute: int):
    """
    设置默认的请求频率限制（对所有未单独设置的域名生效）
    :param requests_per_minute: 每分钟最大请求数，默认30
    
    示例:
        >>> from adata.common import set_default_rate_limit
        >>> set_default_rate_limit(50)  # 所有域名默认每分钟50次
    """
    requests.set_default_rate_limit(requests_per_minute)


