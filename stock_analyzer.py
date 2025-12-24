#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@desc: 股票分析工具
@author: 1nchaos
@time: 2025-12-24
"""

import pandas as pd
import matplotlib.pyplot as plt
from adata.stock.market.stock_market.stock_market import StockMarket


def calculate_max_drawdown(prices):
    """
    计算最大回撤
    :param prices: 价格序列
    :return: 最大回撤值
    """
    if len(prices) < 2:
        return 0.0
    
    max_price = prices[0]
    max_drawdown = 0.0
    
    for price in prices:
        if price > max_price:
            max_price = price
        else:
            drawdown = (max_price - price) / max_price
            if drawdown > max_drawdown:
                max_drawdown = drawdown
    
    return max_drawdown


def analyze_stock(stock_code, start_date, end_date):
    """
    分析指定股票在给定日期区间内的行情数据
    :param stock_code: 股票代码
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return: 分析结果
    """
    # 1. 获取行情数据
    stock_market = StockMarket()
    df = stock_market.get_market(stock_code=stock_code, start_date=start_date, end_date=end_date, k_type=1)
    
    if df.empty:
        print("未获取到行情数据，请检查股票代码和日期范围。")
        return None
    
    # 2. 计算指标
    close_prices = df['close'].astype(float).tolist()
    
    # 区间涨跌幅
    if len(close_prices) >= 2:
        start_price = close_prices[0]
        end_price = close_prices[-1]
        change_pct = (end_price / start_price - 1) * 100
    else:
        change_pct = 0.0
    
    # 区间最大回撤
    max_drawdown = calculate_max_drawdown(close_prices) * 100
    
    # 区间最高价
    max_price = df['high'].astype(float).max()
    
    # 区间最低价
    min_price = df['low'].astype(float).min()
    
    # 3. 准备结果
    result = {
        'stock_code': stock_code,
        'start_date': start_date,
        'end_date': end_date,
        'start_price': start_price if len(close_prices) >= 2 else None,
        'end_price': end_price if len(close_prices) >= 2 else None,
        'change_pct': change_pct,
        'max_drawdown': max_drawdown,
        'max_price': max_price,
        'min_price': min_price,
        'data': df
    }
    
    return result


def print_analysis_result(result):
    """
    打印分析结果
    :param result: 分析结果
    """
    if not result:
        return
    
    print("=" * 50)
    print("股票分析结果")
    print("=" * 50)
    print(f"股票代码: {result['stock_code']}")
    print(f"日期区间: {result['start_date']} 至 {result['end_date']}")
    print(f"期初价格: {result['start_price']:.2f} 元")
    print(f"期末价格: {result['end_price']:.2f} 元")
    print(f"区间涨跌幅: {result['change_pct']:.2f}%")
    print(f"区间最大回撤: {result['max_drawdown']:.2f}%")
    print(f"区间最高价: {result['max_price']:.2f} 元")
    print(f"区间最低价: {result['min_price']:.2f} 元")
    print("=" * 50)


def plot_profit_curve(result):
    """
    绘制收益曲线图
    :param result: 分析结果
    """
    if not result or result['data'].empty:
        return
    
    df = result['data']
    dates = pd.to_datetime(df['trade_date'])
    close_prices = df['close'].astype(float)
    
    # 归一化价格
    normalized_prices = close_prices / close_prices.iloc[0] * 100
    
    plt.figure(figsize=(12, 6))
    plt.plot(dates, normalized_prices, label='归一化收益', color='blue')
    plt.title(f'{result["stock_code"]} 收益曲线（归一化）')
    plt.xlabel('日期')
    plt.ylabel('归一化价格（期初=100）')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) != 4:
        print("用法: python stock_analyzer.py <股票代码> <开始日期> <结束日期>")
        print("示例: python stock_analyzer.py 000001 2025-01-01 2025-12-24")
        sys.exit(1)
    
    stock_code = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    
    # 执行分析
    result = analyze_stock(stock_code, start_date, end_date)
    
    # 打印结果
    print_analysis_result(result)
    
    # 绘制收益曲线
    if result:
        plot_profit_curve(result)