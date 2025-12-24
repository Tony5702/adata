#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
均线突破 + 成交量确认信号检测模块
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import adata


def detect_ma_breakout_signal(
    stock_code: str,
    start_date: str,
    end_date: str
):
    """
    检测均线突破 + 成交量确认信号
    
    参数:
        stock_code: 股票代码
        start_date: 开始日期
        end_date: 结束日期
    
    返回:
        无，直接打印结果和绘制图形
    """
    # 1. 获取市场数据
    print(f"正在获取股票 {stock_code} 的行情数据...")
    df = adata.stock.market.get_market(
        stock_code=stock_code,
        start_date=start_date,
        end_date=end_date,
        k_type=1,  # 日线
        adjust_type=1  # 前复权
    )
    
    if df.empty:
        print("未获取到有效数据，请检查股票代码和日期范围。")
        return
    
    # 2. 计算技术指标
    print("正在计算技术指标...")
    # 计算均线
    df['MA5'] = df['close'].rolling(window=5).mean()
    df['MA10'] = df['close'].rolling(window=10).mean()
    df['MA20'] = df['close'].rolling(window=20).mean()
    # 计算成交量10日均值
    df['VOL_MA10'] = df['volume'].rolling(window=10).mean()
    
    # 3. 检测信号
    print("正在检测信号...")
    # 均线突破条件
    ma_breakout = (df['close'] > df['MA20']) & (df['close'].shift(1) <= df['MA20'].shift(1))
    # 成交量确认条件
    volume_confirm = df['volume'] > df['VOL_MA10']
    # 综合信号
    df['signal'] = ma_breakout & volume_confirm
    
    # 4. 输出信号
    signal_dates = df[df['signal']]
    
    if not signal_dates.empty:
        print("\n检测到有效买入信号：")
        print("------------------------------")
        print(f"共 {len(signal_dates)} 个信号日期")
        print("------------------------------")
        print(signal_dates[['trade_date', 'close', 'volume']].to_string(index=False))
        print("------------------------------")
    else:
        print("\n区间内未检测到有效信号")
        return
    
    # 5. 可视化
    print("\n正在绘制可视化图形...")
    plt.figure(figsize=(12, 8))
    
    # 绘制收盘价
    plt.plot(df['trade_date'], df['close'], label='收盘价', color='blue', linewidth=1)
    
    # 绘制均线
    plt.plot(df['trade_date'], df['MA5'], label='MA5', color='green', linewidth=1)
    plt.plot(df['trade_date'], df['MA10'], label='MA10', color='orange', linewidth=1)
    plt.plot(df['trade_date'], df['MA20'], label='MA20', color='red', linewidth=1)
    
    # 标记信号点
    signal_points = df[df['signal']]
    plt.scatter(signal_points['trade_date'], signal_points['close'], 
                marker='^', color='red', s=100, label='买入信号')
    
    # 设置图形属性
    plt.title(f"股票 {stock_code} 均线突破信号检测 ({start_date} 至 {end_date})")
    plt.xlabel("日期")
    plt.ylabel("价格 (元)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 显示图形
    plt.show()


if __name__ == "__main__":
    # 示例使用
    import sys
    if len(sys.argv) != 4:
        print("使用方法：python ma_breakout_signal.py <股票代码> <开始日期> <结束日期>")
        print("示例：python ma_breakout_signal.py 000001 2024-01-01 2024-12-31")
        sys.exit(1)
    
    stock_code = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    
    detect_ma_breakout_signal(stock_code, start_date, end_date)
