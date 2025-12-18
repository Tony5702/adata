#!/usr/bin/env python3
"""
股票数据分析工具
使用 adata 库获取股票行情数据，并计算关键指标和绘制收益曲线
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
from adata.stock.market import StockMarket

# 设置 matplotlib 支持中文显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']  # 用于显示中文
plt.rcParams['axes.unicode_minus'] = False  # 用于显示负号


def calculate_stock_metrics(stock_code: str, start_date: str, end_date: str) -> dict:
    """
    获取指定股票在给定日期区间内的行情数据，并计算关键指标
    
    Args:
        stock_code (str): 股票代码
        start_date (str): 开始日期 (YYYY-MM-DD)
        end_date (str): 结束日期 (YYYY-MM-DD)
    
    Returns:
        dict: 包含股票数据和计算指标的字典
    """
    # 初始化股票行情对象
    stock_market = StockMarket()
    
    # 获取股票行情数据
    print(f"正在获取股票 {stock_code} 从 {start_date} 到 {end_date} 的行情数据...")
    df = stock_market.get_market(
        stock_code=stock_code,
        start_date=start_date,
        end_date=end_date,
        k_type=1  # 日K线
    )
    
    if df.empty:
        print(f"未获取到股票 {stock_code} 的行情数据")
        return None
    
    print(f"成功获取 {len(df)} 条数据")
    
    # 计算指标
    print("正在计算股票指标...")
    
    # 转换为数值类型
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    df['high'] = pd.to_numeric(df['high'], errors='coerce')
    df['low'] = pd.to_numeric(df['low'], errors='coerce')
    
    # 移除缺失值
    df = df.dropna(subset=['close', 'high', 'low'])
    
    # 计算区间涨跌幅
    start_price = df['close'].iloc[0]
    end_price = df['close'].iloc[-1]
    price_change = (end_price / start_price) - 1
    
    # 计算区间最大回撤
    df['cum_max'] = df['close'].cummax()
    df['drawdown'] = (df['close'] / df['cum_max']) - 1
    max_drawdown = df['drawdown'].min()
    
    # 计算区间最高价和最低价
    highest_price = df['high'].max()
    lowest_price = df['low'].min()
    
    # 准备结果
    result = {
        'stock_code': stock_code,
        'start_date': start_date,
        'end_date': end_date,
        'data': df,
        'metrics': {
            'price_change': price_change,
            'max_drawdown': max_drawdown,
            'highest_price': highest_price,
            'lowest_price': lowest_price,
            'start_price': start_price,
            'end_price': end_price
        }
    }
    
    return result


def print_stock_analysis(result: dict) -> None:
    """
    打印股票分析结果
    
    Args:
        result (dict): 包含股票数据和指标的字典
    """
    if not result:
        return
    
    print("\n" + "="*50)
    print(f"股票分析报告: {result['stock_code']}")
    print(f"时间区间: {result['start_date']} 到 {result['end_date']}")
    print("="*50)
    
    metrics = result['metrics']
    print(f"区间涨跌幅: {metrics['price_change']:.2%}")
    print(f"区间最大回撤: {metrics['max_drawdown']:.2%}")
    print(f"区间最高价: {metrics['highest_price']:.2f} 元")
    print(f"区间最低价: {metrics['lowest_price']:.2f} 元")
    print(f"期初价格: {metrics['start_price']:.2f} 元")
    print(f"期末价格: {metrics['end_price']:.2f} 元")
    print("="*50)


def plot_stock_performance(result: dict) -> None:
    """
    绘制股票收益曲线图
    
    Args:
        result (dict): 包含股票数据和指标的字典
    """
    if not result:
        return
    
    df = result['data']
    stock_code = result['stock_code']
    
    # 计算归一化价格
    df['normalized_close'] = df['close'] / df['close'].iloc[0]
    
    # 创建图形
    plt.figure(figsize=(12, 6))
    plt.plot(df['trade_date'], df['normalized_close'], label='归一化收盘价')
    
    plt.title(f'{stock_code} 股票收益曲线 ({result["start_date"]} 到 {result["end_date"]})')
    plt.xlabel('日期')
    plt.ylabel('归一化价格')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    print(f"\n正在显示 {stock_code} 的收益曲线图...")
    plt.show()


def main():
    """
    主函数，处理命令行参数并执行分析
    """
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='股票数据分析工具')
    parser.add_argument('stock_code', type=str, help='股票代码 (如: 000001)')
    parser.add_argument('start_date', type=str, help='开始日期 (YYYY-MM-DD)')
    parser.add_argument('end_date', type=str, help='结束日期 (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    try:
        # 计算股票指标
        result = calculate_stock_metrics(args.stock_code, args.start_date, args.end_date)
        
        if result:
            # 打印分析结果
            print_stock_analysis(result)
            
            # 绘制收益曲线
            plot_stock_performance(result)
        else:
            print("分析失败，未获取到足够的数据")
    
    except Exception as e:
        print(f"分析过程中出现错误: {str(e)}")


if __name__ == '__main__':
    main()
