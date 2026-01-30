# -*- coding: utf-8 -*-
"""
@desc: 股票分析功能测试
@author: 1nchaos
@time: 2024/01/30
@log: change log
"""

import pandas as pd
from adata.stock.market.stock_market import StockMarket


def test_weekday_analysis():
    """测试星期分析功能"""
    print("测试星期分析功能...")
    
    # 创建股票市场对象
    stock_market = StockMarket()
    
    # 获取股票数据
    stock_code = '000001'  # 平安银行
    start_date = '2023-01-01'
    end_date = '2023-12-31'
    
    # 调用星期分析功能
    result = stock_market.analyze_by_weekday(
        stock_code=stock_code,
        start_date=start_date,
        end_date=end_date
    )
    
    print(f"股票代码: {stock_code}")
    print(f"分析时间段: {start_date} 至 {end_date}")
    print("星期分析结果:")
    print(result)
    print("\n" + "="*50 + "\n")


def test_month_period_analysis():
    """测试月份区间分析功能"""
    print("测试月份区间分析功能...")
    
    # 创建股票市场对象
    stock_market = StockMarket()
    
    # 获取股票数据
    stock_code = '000001'  # 平安银行
    start_date = '2023-01-01'
    end_date = '2023-12-31'
    
    # 调用月份区间分析功能
    result = stock_market.analyze_by_month_period(
        stock_code=stock_code,
        start_date=start_date,
        end_date=end_date
    )
    
    print(f"股票代码: {stock_code}")
    print(f"分析时间段: {start_date} 至 {end_date}")
    print("月份区间分析结果:")
    print(result)
    print("\n" + "="*50 + "\n")


def test_multiple_stocks():
    """测试多只股票的分析"""
    print("测试多只股票的分析...")
    
    # 创建股票市场对象
    stock_market = StockMarket()
    
    # 股票列表
    stock_list = ['000001', '000002', '600000']  # 平安银行、万科A、浦发银行
    start_date = '2023-01-01'
    end_date = '2023-12-31'
    
    for stock_code in stock_list:
        print(f"分析股票: {stock_code}")
        
        # 星期分析
        weekday_result = stock_market.analyze_by_weekday(
            stock_code=stock_code,
            start_date=start_date,
            end_date=end_date
        )
        print("星期分析结果:")
        print(weekday_result)
        
        # 月份区间分析
        month_period_result = stock_market.analyze_by_month_period(
            stock_code=stock_code,
            start_date=start_date,
            end_date=end_date
        )
        print("月份区间分析结果:")
        print(month_period_result)
        
        print("\n" + "="*50 + "\n")


if __name__ == '__main__':
    # 测试星期分析
    test_weekday_analysis()
    
    # 测试月份区间分析
    test_month_period_analysis()
    
    # 测试多只股票分析
    test_multiple_stocks()