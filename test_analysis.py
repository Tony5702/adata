# -*- coding: utf-8 -*-
"""
测试星期维度和月度区间分析功能
"""
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np


class CalIndex:

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def analyze_weekday_stats(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        df = df.sort_values('trade_date').reset_index(drop=True)
        df['prev_close'] = df['close'].shift(1)
        df['daily_return'] = df['close'] / df['prev_close'] - 1
        df['weekday'] = df['trade_date'].dt.dayofweek
        df['is_up'] = (df['daily_return'] > 0).astype(int)
        
        weekday_names = {0: '周一', 1: '周二', 2: '周三', 3: '周四', 4: '周五', 5: '周六', 6: '周日'}
        
        result = df.groupby('weekday').agg(
            平均收益率=('daily_return', 'mean'),
            平均成交量=('volume', 'mean'),
            上涨概率=('is_up', 'mean'),
            交易天数=('daily_return', 'count')
        ).reset_index()
        
        result['weekday'] = result['weekday'].map(weekday_names)
        result = result.rename(columns={'weekday': '星期'})
        result['平均收益率'] = result['平均收益率'] * 100
        result['上涨概率'] = result['上涨概率'] * 100
        result['平均收益率'] = result['平均收益率'].round(4)
        result['平均成交量'] = result['平均成交量'].round(2)
        result['上涨概率'] = result['上涨概率'].round(2)
        
        return result

    @staticmethod
    def analyze_month_period_stats(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        df = df.sort_values('trade_date').reset_index(drop=True)
        df['prev_close'] = df['close'].shift(1)
        df['daily_return'] = df['close'] / df['prev_close'] - 1
        df['day'] = df['trade_date'].dt.day
        df['is_up'] = (df['daily_return'] > 0).astype(int)
        
        def get_period(day):
            if 1 <= day <= 10:
                return '月初(1-10)'
            elif 11 <= day <= 20:
                return '月中(11-20)'
            else:
                return '月末(21-月底)'
        
        df['period'] = df['day'].apply(get_period)
        
        period_order = ['月初(1-10)', '月中(11-20)', '月末(21-月底)']
        
        result = df.groupby('period').agg(
            平均收益率=('daily_return', 'mean'),
            平均成交量=('volume', 'mean'),
            上涨概率=('is_up', 'mean'),
            交易天数=('daily_return', 'count')
        ).reset_index()
        
        result['period'] = pd.Categorical(result['period'], categories=period_order, ordered=True)
        result = result.sort_values('period').reset_index(drop=True)
        result = result.rename(columns={'period': '月度区间'})
        result['平均收益率'] = result['平均收益率'] * 100
        result['上涨概率'] = result['上涨概率'] * 100
        result['平均收益率'] = result['平均收益率'].round(4)
        result['平均成交量'] = result['平均成交量'].round(2)
        result['上涨概率'] = result['上涨概率'].round(2)
        
        return result


if __name__ == '__main__':
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', '2024-12-31', freq='B')
    n = len(dates)
    test_df = pd.DataFrame({
        'trade_date': dates,
        'open': 10 + np.cumsum(np.random.randn(n) * 0.02),
        'close': 10 + np.cumsum(np.random.randn(n) * 0.02),
        'volume': np.random.randint(1000000, 10000000, n)
    })

    print('=== 测试数据示例 ===')
    print(test_df.head(10))
    print(f'数据行数: {len(test_df)}')

    cal_index = CalIndex()
    print('\n=== 星期维度分析 ===')
    weekday_result = cal_index.analyze_weekday_stats(test_df)
    print(weekday_result.to_string(index=False))

    print('\n=== 月度区间分析 ===')
    month_result = cal_index.analyze_month_period_stats(test_df)
    print(month_result.to_string(index=False))
