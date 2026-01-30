# -*- coding: utf-8 -*-
"""
@desc: 股票分析功能使用示例
@author: 1nchaos
@time: 2024/01/30
@log: change log
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adata.stock.market.stock_market import StockMarket


def example_weekday_analysis():
    """星期分析示例"""
    print("=== 星期分析示例 ===")
    
    # 创建股票市场对象
    stock_market = StockMarket()
    
    # 设置分析参数
    stock_code = '000001'  # 平安银行
    start_date = '2023-01-01'
    end_date = '2023-12-31'
    
    # 调用星期分析功能
    result = stock_market.analyze_by_weekday(
        stock_code=stock_code,
        start_date=start_date,
        end_date=end_date
    )
    
    # 打印结果
    print(f"股票代码: {stock_code}")
    print(f"分析时间段: {start_date} 至 {end_date}")
    print("\n星期分析结果:")
    print(result)
    
    return result


def example_month_period_analysis():
    """月份区间分析示例"""
    print("\n=== 月份区间分析示例 ===")
    
    # 创建股票市场对象
    stock_market = StockMarket()
    
    # 设置分析参数
    stock_code = '000001'  # 平安银行
    start_date = '2023-01-01'
    end_date = '2023-12-31'
    
    # 调用月份区间分析功能
    result = stock_market.analyze_by_month_period(
        stock_code=stock_code,
        start_date=start_date,
        end_date=end_date
    )
    
    # 打印结果
    print(f"股票代码: {stock_code}")
    print(f"分析时间段: {start_date} 至 {end_date}")
    print("\n月份区间分析结果:")
    print(result)
    
    return result


if __name__ == '__main__':
    # 执行示例
    weekday_result = example_weekday_analysis()
    month_period_result = example_month_period_analysis()
    
    # 保存结果到CSV文件
    if not weekday_result.empty:
        weekday_result.to_csv('weekday_analysis_result.csv')
        print("\n星期分析结果已保存到 weekday_analysis_result.csv")
    
    if not month_period_result.empty:
        month_period_result.to_csv('month_period_analysis_result.csv')
        print("月份区间分析结果已保存到 month_period_analysis_result.csv")