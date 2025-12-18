# -*- coding: utf-8 -*-
"""
@desc: 股票K线图可视化
@author: AI Assistant
@time: 2025/01/27
"""

import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd

# 配置中文字体
plt.rcParams['font.sans-serif'] = ['Hiragino Sans GB', 'PingFang SC', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

from adata.stock.market.stock_market import StockMarket


class StockMarketPlot(object):
    """股票行情可视化类"""

    def __init__(self) -> None:
        super().__init__()
        self.stock_market = StockMarket()

    def plot_k_line(self, stock_code: str = '000001', start_date='2024-01-01', end_date=None, k_type=1):
        """
        绘制股票K线图
        :param stock_code: 股票代码
        :param start_date: 开始日期
        :param end_date: 结束日期
        :param k_type: K线类型
        :return: None
        """
        # 获取股票行情数据
        df = self.stock_market.get_market(stock_code=stock_code, start_date=start_date, end_date=end_date, k_type=k_type)

        if df.empty:
            print(f"没有找到股票 {stock_code} 的数据")
            return

        # 处理数据，确保列名符合mplfinance要求
        # 假设数据列包含: trade_date, open, close, high, low, volume
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        df.set_index('trade_date', inplace=True)

        # 重命名列名以符合mplfinance要求
        df.rename(columns={
            'open': 'Open',
            'close': 'Close',
            'high': 'High',
            'low': 'Low',
            'volume': 'Volume'
        }, inplace=True)

        # 创建自定义样式，解决中文字体问题
        mc = mpf.make_marketcolors(
            up='red', down='green', edge='i', wick='i', volume='in'
        )
        s = mpf.make_mpf_style(
            base_mpf_style='yahoo',
            marketcolors=mc,
            rc={
                'font.sans-serif': ['Hiragino Sans GB', 'PingFang SC', 'Microsoft YaHei'],
                'axes.unicode_minus': False
            }
        )

        # 绘制K线图
        mpf.plot(
            df,
            type='candle',
            volume=True,
            title=f'{stock_code} 股票K线图',
            ylabel='价格 (元)',
            ylabel_lower='成交量',
            style=s
        )

    def get_and_plot_k_line(self, stock_code: str = '000001', start_date='2024-01-01', end_date=None, k_type=1):
        """
        获取并绘制股票K线图
        :param stock_code: 股票代码
        :param start_date: 开始日期
        :param end_date: 结束日期
        :param k_type: K线类型
        :return: 股票数据DataFrame
        """
        # 获取股票行情数据
        df = self.stock_market.get_market(stock_code=stock_code, start_date=start_date, end_date=end_date, k_type=k_type)

        if not df.empty:
            self.plot_k_line(stock_code=stock_code, start_date=start_date, end_date=end_date, k_type=k_type)

        return df


if __name__ == '__main__':
    # 示例用法
    plotter = StockMarketPlot()
    plotter.plot_k_line(stock_code='000001', start_date='2024-07-01', end_date='2024-07-31')
