# -*- coding: utf-8 -*-
"""
@desc: 股票行情数据分析
@author: 1nchaos
@time: 2024/1/16
"""
import pandas as pd


class StockMarketAnalysis(object):
    """
    股票行情数据分析
    基于日K数据进行统计分析
    """

    def __init__(self):
        self.weekday_map = {
            0: '周一',
            1: '周二',
            2: '周三',
            3: '周四',
            4: '周五'
        }

    def analyze_weekday_stats(self, kline_df: pd.DataFrame):
        """
        分析周一到周五每个交易日的平均收益率、平均成交量和上涨概率
        :param kline_df: 日K数据DataFrame，必须包含 trade_date, open, close, volume 字段
        :return: DataFrame，行为星期维度，列为统计指标
        """
        if kline_df is None or kline_df.empty:
            return pd.DataFrame()

        required_cols = ['trade_date', 'close', 'volume']
        if not all(col in kline_df.columns for col in required_cols):
            raise ValueError(f"数据必须包含以下字段: {required_cols}")

        df = kline_df.copy()
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        df['prev_close'] = df['close'].shift(1)
        df['daily_return'] = df['close'] / df['prev_close'] - 1
        df['is_rise'] = (df['daily_return'] > 0).astype(int)
        df['weekday'] = df['trade_date'].dt.weekday
        df['weekday_name'] = df['weekday'].map(self.weekday_map)

        weekday_stats = df.groupby('weekday_name').agg(
            avg_return=('daily_return', 'mean'),
            avg_volume=('volume', 'mean'),
            rise_probability=('is_rise', 'mean')
        ).reset_index()

        weekday_stats = weekday_stats.sort_values('weekday_name', key=lambda x: x.map({'周一': 0, '周二': 1, '周三': 2, '周四': 3, '周五': 4}))
        weekday_stats.set_index('weekday_name', inplace=True)
        weekday_stats['avg_return'] = weekday_stats['avg_return'] * 100
        weekday_stats['rise_probability'] = weekday_stats['rise_probability'] * 100
        weekday_stats = weekday_stats.round(4)

        return weekday_stats

    def analyze_monthly_period_stats(self, kline_df: pd.DataFrame):
        """
        分析每月月初、月中、月末三个区间的平均收益率、平均成交量和上涨概率
        :param kline_df: 日K数据DataFrame，必须包含 trade_date, open, close, volume 字段
        :return: DataFrame，行为月份区间维度，列为统计指标
        """
        if kline_df is None or kline_df.empty:
            return pd.DataFrame()

        required_cols = ['trade_date', 'close', 'volume']
        if not all(col in kline_df.columns for col in required_cols):
            raise ValueError(f"数据必须包含以下字段: {required_cols}")

        df = kline_df.copy()
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        df['prev_close'] = df['close'].shift(1)
        df['daily_return'] = df['close'] / df['prev_close'] - 1
        df['is_rise'] = (df['daily_return'] > 0).astype(int)
        df['day_of_month'] = df['trade_date'].dt.day

        df['month_period'] = pd.cut(df['day_of_month'],
                                    bins=[0, 10, 20, 31],
                                    labels=['月初', '月中', '月末'])

        period_stats = df.groupby('month_period').agg(
            avg_return=('daily_return', 'mean'),
            avg_volume=('volume', 'mean'),
            rise_probability=('is_rise', 'mean')
        ).reset_index()

        period_stats.set_index('month_period', inplace=True)
        period_stats['avg_return'] = period_stats['avg_return'] * 100
        period_stats['rise_probability'] = period_stats['rise_probability'] * 100
        period_stats = period_stats.round(4)

        return period_stats
