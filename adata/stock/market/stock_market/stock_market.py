# -*- coding: utf-8 -*-
"""
@desc: 股票行情
@author: 1nchaos
@time: 2023/3/29
@log: change log
TODO 数据返回类型转换
"""

import concurrent.futures
from functools import wraps

import pandas as pd

from adata.stock.market.stock_market.stock_market_baidu import StockMarketBaiDu
from adata.stock.market.stock_market.stock_market_east import StockMarketEast
from adata.stock.market.stock_market.stock_market_qq import StockMarketQQ
from adata.stock.market.stock_market.stock_market_sina import StockMarketSina


def multi_thread_get_market(max_workers=5):
    """
    多线程获取多个股票行情数据的装饰器
    :param max_workers: 最大线程数，默认5个线程
    :return: 装饰器函数
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, stock_code, *args, **kwargs):
            # 如果传入的是列表，则使用多线程并发获取
            if isinstance(stock_code, list):
                if not stock_code:
                    return pd.DataFrame()
                
                results = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                    # 提交所有任务
                    future_to_code = {
                        executor.submit(func, self, code, *args, **kwargs): code 
                        for code in stock_code
                    }
                    # 收集结果
                    for future in concurrent.futures.as_completed(future_to_code):
                        code = future_to_code[future]
                        try:
                            df = future.result()
                            if not df.empty:
                                results.append(df)
                        except Exception as e:
                            print(f"获取股票 {code} 数据失败: {e}")
                
                # 合并所有结果
                if results:
                    return pd.concat(results, ignore_index=True)
                return pd.DataFrame()
            else:
                # 单个股票代码，直接调用原函数
                return func(self, stock_code, *args, **kwargs)
        return wrapper
    return decorator


class StockMarket(object):
    """
    股票行情
    """

    def __init__(self) -> None:
        super().__init__()
        self.sina_market = StockMarketSina()
        self.qq_market = StockMarketQQ()
        self.baidu_market = StockMarketBaiDu()
        self.east_market = StockMarketEast()

    @multi_thread_get_market(max_workers=5)
    def get_market(self, stock_code: str = '000001', start_date='1990-01-01', end_date=None, k_type=1,
                   adjust_type: int = 1):
        """
        获取单个股票的行情，支持传入列表多线程并发获取多个股票
        :param stock_code: 股票代码或股票代码列表，例如：'000001' 或 ['000001', '000002']
        :param start_date: 开始时间
        :param end_date: 结束日期
        :param k_type: k线类型：1.日；2.周；3.月,4季度，5.5min，15.15min，30.30min，60.60min 默认：1 日k
        :param adjust_type: k线复权类型：0.不复权；1.前复权；2.后复权 默认：1 前复权 （目前：只有前复权,作为股票交易已经可用）
        :return: k线行情数据，传入列表时返回合并后的DataFrame
        """
        df = self.east_market.get_market(stock_code=stock_code, start_date=start_date, end_date=end_date,
                                         k_type=k_type, adjust_type=adjust_type)
        return df

    def get_market_min(self, stock_code: str = '000001'):
        """
        获取单个股票的今日分时行情
        :param stock_code: 股票代码
        :return: 当日分钟行情数据
        """
        df = self.east_market.get_market_min(stock_code=stock_code)
        if df.empty:
            return self.baidu_market.get_market_min(stock_code=stock_code)
        return df

    def list_market_current(self, code_list=None):
        """
        获取多个股票最新行情信息
        :param code_list: 股票代码
        :return: 当前最新的行情价格信息
        stock_code: 股票代码
        short_name: 股票简称
        price: 当前价格（元）
        change: 涨跌额（元）
        change_pct: 涨跌幅（%）
        volume: 成交量（股）
        amount: 成交金额（元）
        """
        if code_list is None:
            return pd.DataFrame()
        # 1. 先查询新浪
        df = self.sina_market.list_market_current(code_list=code_list)
        # 2. 然后腾讯
        if df.empty:
            df = self.qq_market.list_market_current(code_list=code_list)
        return df

    def get_market_five(self, stock_code: str = '000001'):
        """
        获取单个股票的5档行情
        其中：百度的接口数据更精准，精确到了股。腾讯的精确到手
        :param stock_code: 股票代码
        :return: 最新的五档行情
        """
        res_df = self.qq_market.get_market_five(stock_code=stock_code)
        if res_df.empty:
            res_df = self.baidu_market.get_market_five(stock_code=stock_code)
        return res_df

    def get_market_bar(self, stock_code: str = '000001'):
        """
        获取单个股票的分时成交
        :param stock_code: 股票代码
        :return: 最新当天的分时成交
        """
        res_df = self.baidu_market.get_market_bar(stock_code=stock_code)
        if res_df.empty:
            res_df = self.qq_market.get_market_bar(stock_code=stock_code)
        return res_df


if __name__ == '__main__':
    import time
    
    sm = StockMarket()
    
    # 测试1：单股票获取（原有功能）
    print("=" * 50)
    print("测试1：单股票获取")
    print("=" * 50)
    df_single = sm.get_market(stock_code='000001', start_date='2024-07-22', k_type=1)
    print(f"单股票数据条数: {len(df_single)}")
    print(df_single.head())
    
    # 测试2：多股票并发获取（新增功能）
    print("\n" + "=" * 50)
    print("测试2：多股票并发获取")
    print("=" * 50)
    stock_list = ['000001', '000002', '600001']
    start_time = time.time()
    df_multi = sm.get_market(stock_code=stock_list, start_date='2024-07-22', k_type=1)
    end_time = time.time()
    print(f"股票列表: {stock_list}")
    print(f"并发获取耗时: {end_time - start_time:.2f}秒")
    print(f"总数据条数: {len(df_multi)}")
    if not df_multi.empty and 'stock_code' in df_multi.columns:
        print(f"包含股票: {df_multi['stock_code'].unique().tolist()}")
    print(df_multi.head(10))
    
    # 测试3：空列表测试
    print("\n" + "=" * 50)
    print("测试3：空列表测试")
    print("=" * 50)
    df_empty = sm.get_market(stock_code=[], start_date='2024-07-22', k_type=1)
    print(f"空列表返回结果: {df_empty}")
    
    # 测试4：其他原有功能
    print("\n" + "=" * 50)
    print("测试4：其他原有功能")
    print("=" * 50)
    print("分时行情:")
    print(sm.get_market_min(stock_code='000001'))
    print("\n当前行情:")
    print(sm.list_market_current(code_list=['000001', '600001', '000795', '872925']))
    print("\n五档行情:")
    print(sm.get_market_five(stock_code='000001'))
    print("\n分时成交:")
    print(sm.get_market_bar(stock_code='000001'))

