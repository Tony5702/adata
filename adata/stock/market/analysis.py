# -*- coding: utf-8 -*-
"""
@desc: 股票市场分析工具
@author: 1nchaos
@time: 2026/01/16
@log: change log
"""

import pandas as pd


class StockAnalysis(object):
    """
    股票市场分析工具类
    提供基于日K数据的分析功能
    """

    def __init__(self) -> None:
        super().__init__()

    def weekday_analysis(self, kline_df: pd.DataFrame) -> pd.DataFrame:
        """
        分析周一到周五每个交易日的平均收益率、平均成交量以及上涨概率
        
        Args:
            kline_df: 包含日K数据的DataFrame，必须包含字段：trade_date, open, close, volume
            
        Returns:
            DataFrame: 行为星期维度，列为统计指标（平均收益率、平均成交量、上涨概率）
        """
        # 检查必要字段
        required_cols = ['trade_date', 'open', 'close', 'volume']
        if not all(col in kline_df.columns for col in required_cols):
            raise ValueError(f"DataFrame must contain columns: {required_cols}")
        
        # 复制数据以避免修改原始数据
        df = kline_df.copy()
        
        # 计算日收益率: daily_return = close / prev_close - 1
        df['daily_return'] = df['close'] / df['close'].shift(1) - 1
        
        # 计算是否上涨
        df['is_rise'] = (df['daily_return'] > 0).astype(int)
        
        # 将trade_date转换为日期类型
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        
        # 获取星期几 (0=周一, 4=周五)
        df['weekday'] = df['trade_date'].dt.weekday
        
        # 定义星期几的映射
        weekday_map = {
            0: '周一',
            1: '周二',
            2: '周三',
            3: '周四',
            4: '周五'
        }
        
        # 分组统计
        result_df = df.groupby('weekday').agg({
            'daily_return': ['mean'],
            'volume': ['mean'],
            'is_rise': ['mean']
        }).round(4)
        
        # 重命名列
        result_df.columns = ['平均收益率', '平均成交量', '上涨概率']
        
        # 应用星期几的映射
        result_df.index = result_df.index.map(weekday_map)
        
        # 按周一到周五排序
        result_df = result_df.reindex(['周一', '周二', '周三', '周四', '周五'])
        
        # 将收益率转换为百分比
        result_df['平均收益率'] = result_df['平均收益率'].apply(lambda x: f"{x*100:.2f}%")
        result_df['上涨概率'] = result_df['上涨概率'].apply(lambda x: f"{x*100:.2f}%")
        
        return result_df

    def monthly_interval_analysis(self, kline_df: pd.DataFrame) -> pd.DataFrame:
        """
        分析每月月初（1-10）、月中（11-20）、月末（21-月最后一天）三个区间的
        平均收益率、平均成交量以及上涨概率
        
        Args:
            kline_df: 包含日K数据的DataFrame，必须包含字段：trade_date, open, close, volume
            
        Returns:
            DataFrame: 行为时间区间维度，列为统计指标（平均收益率、平均成交量、上涨概率）
        """
        # 检查必要字段
        required_cols = ['trade_date', 'open', 'close', 'volume']
        if not all(col in kline_df.columns for col in required_cols):
            raise ValueError(f"DataFrame must contain columns: {required_cols}")
        
        # 复制数据以避免修改原始数据
        df = kline_df.copy()
        
        # 计算日收益率: daily_return = close / prev_close - 1
        df['daily_return'] = df['close'] / df['close'].shift(1) - 1
        
        # 计算是否上涨
        df['is_rise'] = (df['daily_return'] > 0).astype(int)
        
        # 将trade_date转换为日期类型
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        
        # 获取日期的日部分
        df['day'] = df['trade_date'].dt.day
        
        # 定义区间函数
        def get_interval(day):
            if 1 <= day <= 10:
                return '月初(1-10日)'
            elif 11 <= day <= 20:
                return '月中(11-20日)'
            else:
                return '月末(21日-月底)'
        
        # 应用区间函数
        df['interval'] = df['day'].apply(get_interval)
        
        # 分组统计
        result_df = df.groupby('interval').agg({
            'daily_return': ['mean'],
            'volume': ['mean'],
            'is_rise': ['mean']
        }).round(4)
        
        # 重命名列
        result_df.columns = ['平均收益率', '平均成交量', '上涨概率']
        
        # 按月初、月中、月末排序
        result_df = result_df.reindex(['月初(1-10日)', '月中(11-20日)', '月末(21日-月底)'])
        
        # 将收益率转换为百分比
        result_df['平均收益率'] = result_df['平均收益率'].apply(lambda x: f"{x*100:.2f}%")
        result_df['上涨概率'] = result_df['上涨概率'].apply(lambda x: f"{x*100:.2f}%")
        
        return result_df


if __name__ == '__main__':
    import sys
    import os
    
    # 添加项目根目录到Python路径
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    
    # 导入股票行情类
    from adata.stock.market.stock_market.stock_market import StockMarket
    
    # 获取示例数据
    stock_market = StockMarket()
    kline_df = stock_market.get_market(stock_code='000001', start_date='2023-01-01', end_date='2024-12-31')
    
    print("获取到的日K数据前5行:")
    print(kline_df[['trade_date', 'open', 'close', 'volume']].head())
    print("\n" + "="*60 + "\n")
    
    # 创建分析实例
    analysis = StockAnalysis()
    
    # 1. 星期维度分析
    print("【星期维度分析】")
    weekday_result = analysis.weekday_analysis(kline_df)
    print(weekday_result)
    print("\n" + "="*60 + "\n")
    
    # 2. 月份区间分析
    print("【月份区间分析】")
    monthly_result = analysis.monthly_interval_analysis(kline_df)
    print(monthly_result)
