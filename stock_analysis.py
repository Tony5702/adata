#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票数据分析工具
功能：
1. 获取指定股票在给定日期区间内的日行情数据
2. 计算区间涨跌幅、最大回撤、最高价、最低价等指标
3. 打印输出结果
4. 绘制收益曲线图
"""

import pandas as pd
import matplotlib.pyplot as plt
from adata.stock.market.stock_market.stock_market import StockMarket


def calculate_stock_indicators(stock_code: str, start_date: str, end_date: str):
    """
    计算指定股票在给定日期区间内的各项指标
    :param stock_code: 股票代码
    :param start_date: 开始日期，格式 'YYYY-MM-DD'
    :param end_date: 结束日期，格式 'YYYY-MM-DD'
    :return: 包含指标的字典和行情数据
    """
    # 1. 获取行情数据
    market = StockMarket()
    df = market.get_market(stock_code=stock_code, start_date=start_date, end_date=end_date)
    
    if df.empty:
        print(f"未获取到股票 {stock_code} 在 {start_date} 至 {end_date} 期间的行情数据")
        return None, None
    
    # 2. 计算各项指标
    indicators = {}
    
    # 区间涨跌幅
    start_price = df['close'].iloc[0]
    end_price = df['close'].iloc[-1]
    indicators['涨跌幅'] = (end_price / start_price - 1) * 100
    
    # 区间最高价
    indicators['最高价'] = df['high'].max()
    
    # 区间最低价
    indicators['最低价'] = df['low'].min()
    
    # 区间最大回撤
    df['cum_max'] = df['close'].cummax()
    df['drawdown'] = (df['close'] / df['cum_max'] - 1) * 100
    indicators['最大回撤'] = df['drawdown'].min()
    
    return indicators, df


def print_indicators(stock_code: str, start_date: str, end_date: str, indicators: dict):
    """
    打印输出股票分析指标
    :param stock_code: 股票代码
    :param start_date: 开始日期
    :param end_date: 结束日期
    :param indicators: 指标字典
    """
    print("=" * 60)
    print(f"股票分析报告: {stock_code}")
    print(f"日期区间: {start_date} 至 {end_date}")
    print("=" * 60)
    print(f"区间涨跌幅: {indicators['涨跌幅']:.2f}%")
    print(f"区间最大回撤: {indicators['最大回撤']:.2f}%")
    print(f"区间最高价: {indicators['最高价']:.2f} 元")
    print(f"区间最低价: {indicators['最低价']:.2f} 元")
    print("=" * 60)


def plot_returns(df: pd.DataFrame, stock_code: str):
    """
    绘制股票收益曲线图
    :param df: 行情数据
    :param stock_code: 股票代码
    """
    # 归一化价格
    normalized_price = (df['close'] / df['close'].iloc[0]) * 100
    
    plt.figure(figsize=(12, 6))
    plt.plot(df['trade_date'], normalized_price, label='归一化收盘价')
    plt.title(f'{stock_code} 收益曲线')
    plt.xlabel('日期')
    plt.ylabel('归一化价格 (基准=100)')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # 示例用法
    import argparse
    
    parser = argparse.ArgumentParser(description='股票数据分析工具')
    parser.add_argument('stock_code', type=str, help='股票代码，例如 000001')
    parser.add_argument('start_date', type=str, help='开始日期，格式 YYYY-MM-DD')
    parser.add_argument('end_date', type=str, help='结束日期，格式 YYYY-MM-DD')
    
    args = parser.parse_args()
    
    # 计算指标
    indicators, df = calculate_stock_indicators(args.stock_code, args.start_date, args.end_date)
    
    if indicators and not df.empty:
        # 打印结果
        print_indicators(args.stock_code, args.start_date, args.end_date, indicators)
        
        # 绘制收益曲线
        plot_returns(df, args.stock_code)
