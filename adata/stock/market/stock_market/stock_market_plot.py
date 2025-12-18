# -*- coding: utf-8 -*-
"""
@desc: 股票行情可视化
@author: 1nchaos
@time: 2025/07/14
@log: change log
"""

import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

# 配置 matplotlib 使用中文字体
plt.rcParams['font.sans-serif'] = ['Hiragino Sans GB', 'PingFang SC', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

from adata.stock.market.stock_market import StockMarket


class StockMarketPlot(object):
    """
    股票行情可视化
    """

    def __init__(self) -> None:
        super().__init__()
        self.stock_market = StockMarket()

    def plot_k_line(self, stock_code: str = '000001', start_date='1990-01-01', end_date=None, 
                    k_type=1, adjust_type: int = 1, title: str = None):
        """
        绘制股票 K 线图
        :param stock_code: 股票代码
        :param start_date: 开始时间
        :param end_date: 结束日期
        :param k_type: k线类型：1.日；2.周；3.月,4季度，5.5min，15.15min，30.30min，60.60min 默认：1 日k
        :param adjust_type: k线复权类型：0.不复权；1.前复权；2.后复权 默认：1 前复权
        :param title: 图表标题
        :return: None
        """
        # 1. 获取股票行情数据
        df = self.stock_market.get_market(stock_code=stock_code, start_date=start_date, 
                                              end_date=end_date, k_type=k_type, adjust_type=adjust_type)
        
        if df.empty:
            print(f"没有找到股票 {stock_code} 的行情数据")
            return
        
        # 2. 处理数据格式
        # 将 trade_date 列转换为 datetime 类型
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        # 设置 trade_date 列为索引
        df.set_index('trade_date', inplace=True)
        # 重命名列，以符合 mplfinance 的要求
        df.rename(columns={
            'open': 'Open',
            'close': 'Close',
            'high': 'High',
            'low': 'Low',
            'volume': 'Volume'
        }, inplace=True)
        
        # 3. 设置图表标题
        if not title:
            title = f"{stock_code} K 线图"
        
        # 4. 配置 mplfinance 使用中文字体
        # 创建自定义样式
        mc = mpf.make_marketcolors(up='red', down='green', inherit=True)
        s = mpf.make_mpf_style(marketcolors=mc, rc={'font.sans-serif': ['Hiragino Sans GB', 'PingFang SC', 'Microsoft YaHei']})
        
        # 绘制 K 线图
        mpf.plot(df, type='candle', title=title, ylabel='价格 (元)', 
                 volume=True, ylabel_lower='成交量', style=s)

    def get_and_plot_k_line(self, stock_code: str = '000001', start_date='1990-01-01', end_date=None, 
                             k_type=1, adjust_type: int = 1):
        """
        获取股票数据并绘制 K 线图
        :param stock_code: 股票代码
        :param start_date: 开始时间
        :param end_date: 结束日期
        :param k_type: k线类型
        :param adjust_type: 复权类型
        :return: 行情数据 DataFrame
        """
        # 获取数据
        df = self.stock_market.get_market(stock_code=stock_code, start_date=start_date, 
                                              end_date=end_date, k_type=k_type, adjust_type=adjust_type)
        
        # 绘制图表
        self.plot_k_line(stock_code=stock_code, start_date=start_date, end_date=end_date, 
                         k_type=k_type, adjust_type=adjust_type)
        
        return df


if __name__ == '__main__':
    # 示例用法
    StockMarketPlot().plot_k_line(stock_code='000001', start_date='2024-07-01', end_date='2024-07-31')
    StockMarketPlot().get_and_plot_k_line(stock_code='002230', start_date='2024-07-01', end_date='2024-07-31')
