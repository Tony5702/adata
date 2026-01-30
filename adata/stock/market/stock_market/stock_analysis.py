# -*- coding: utf-8 -*-
"""
@desc: 股票数据分析功能
@author: 1nchaos
@time: 2024/01/30
@log: change log
"""

import pandas as pd
import numpy as np
from datetime import datetime


class StockAnalysis:
    """
    股票数据分析类
    """

    def __init__(self) -> None:
        super().__init__()

    def analyze_by_weekday(self, df):
        """
        分析周一到周五每个交易日的平均收益率和平均成交量以及上涨概率
        :param df: 包含trade_date, open, close, volume字段的DataFrame
        :return: DataFrame，行为星期维度，列为统计指标
        """
        # 确保数据包含必要字段
        required_columns = ['trade_date', 'open', 'close', 'volume']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"数据缺少必要字段: {col}")

        # 复制数据避免修改原始数据
        data = df.copy()
        
        # 确保trade_date是datetime类型
        data['trade_date'] = pd.to_datetime(data['trade_date'])
        
        # 计算日收益率
        data = data.sort_values('trade_date')
        data['prev_close'] = data['close'].shift(1)
        data['daily_return'] = data['close'] / data['prev_close'] - 1
        
        # 获取星期几 (0=周一, 1=周二, ..., 4=周五)
        data['weekday'] = data['trade_date'].dt.dayofweek
        data['weekday_name'] = data['trade_date'].dt.day_name()
        
        # 筛选出周一到周五的数据
        data = data[data['weekday'] <= 4]
        
        # 计算上涨标识
        data['is_up'] = data['daily_return'] > 0
        
        # 按星期分组计算统计指标
        result = data.groupby('weekday').agg(
            avg_return=('daily_return', 'mean'),
            avg_volume=('volume', 'mean'),
            up_probability=('is_up', 'mean'),
            weekday_name=('weekday_name', 'first')
        ).reset_index()
        
        # 将星期名称作为索引
        result.set_index('weekday_name', inplace=True)
        
        # 格式化结果
        result['avg_return'] = result['avg_return'].apply(lambda x: f"{x:.4f}")
        result['avg_volume'] = result['avg_volume'].apply(lambda x: f"{x:,.0f}")
        result['up_probability'] = result['up_probability'].apply(lambda x: f"{x:.4f}")
        
        # 重命名列
        result.rename(columns={
            'avg_return': '平均收益率',
            'avg_volume': '平均成交量',
            'up_probability': '上涨概率'
        }, inplace=True)
        
        # 按星期顺序排序
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        result = result.reindex(weekday_order)
        
        # 将星期名称改为中文
        chinese_weekdays = {
            'Monday': '周一',
            'Tuesday': '周二',
            'Wednesday': '周三',
            'Thursday': '周四',
            'Friday': '周五'
        }
        result.index = [chinese_weekdays.get(day, day) for day in result.index]
        
        return result

    def analyze_by_month_period(self, df):
        """
        分析每月月初（1-10），月中（11-20），月末（21-月最后一天）三个区间的平均收益率和平均成交量以及上涨概率
        :param df: 包含trade_date, open, close, volume字段的DataFrame
        :return: DataFrame，行为月份区间维度，列为统计指标
        """
        # 确保数据包含必要字段
        required_columns = ['trade_date', 'open', 'close', 'volume']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"数据缺少必要字段: {col}")

        # 复制数据避免修改原始数据
        data = df.copy()
        
        # 确保trade_date是datetime类型
        data['trade_date'] = pd.to_datetime(data['trade_date'])
        
        # 计算日收益率
        data = data.sort_values('trade_date')
        data['prev_close'] = data['close'].shift(1)
        data['daily_return'] = data['close'] / data['prev_close'] - 1
        
        # 获取日期
        data['day'] = data['trade_date'].dt.day
        
        # 定义月份区间
        def get_month_period(day):
            if 1 <= day <= 10:
                return '月初'
            elif 11 <= day <= 20:
                return '月中'
            else:
                return '月末'
        
        data['month_period'] = data['day'].apply(get_month_period)
        
        # 计算上涨标识
        data['is_up'] = data['daily_return'] > 0
        
        # 按月份区间分组计算统计指标
        result = data.groupby('month_period').agg(
            avg_return=('daily_return', 'mean'),
            avg_volume=('volume', 'mean'),
            up_probability=('is_up', 'mean')
        ).reset_index()
        
        # 将月份区间作为索引
        result.set_index('month_period', inplace=True)
        
        # 格式化结果
        result['avg_return'] = result['avg_return'].apply(lambda x: f"{x:.4f}")
        result['avg_volume'] = result['avg_volume'].apply(lambda x: f"{x:,.0f}")
        result['up_probability'] = result['up_probability'].apply(lambda x: f"{x:.4f}")
        
        # 重命名列
        result.rename(columns={
            'avg_return': '平均收益率',
            'avg_volume': '平均成交量',
            'up_probability': '上涨概率'
        }, inplace=True)
        
        # 按月份区间顺序排序
        period_order = ['月初', '月中', '月末']
        result = result.reindex(period_order)
        
        return result