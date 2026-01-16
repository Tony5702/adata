# -*- coding: utf-8 -*-
"""
测试股票行情数据分析功能
"""
from adata.stock.market import market


def test_analysis_functions():
    """测试分析函数"""
    print("=" * 60)
    print("测试股票行情数据分析功能")
    print("=" * 60)
    
    stock_code = '000001'
    start_date = '2024-01-01'
    end_date = None
    
    print(f"\n1. 获取股票 {stock_code} 的日K数据 ({start_date} 至今)...")
    kline_df = market.get_market(stock_code=stock_code, start_date=start_date, end_date=end_date, k_type=1)
    
    if kline_df.empty:
        print(f"未获取到股票 {stock_code} 的数据")
        return
    
    print(f"成功获取 {len(kline_df)} 条日K数据")
    print("数据预览:")
    print(kline_df[['trade_date', 'open', 'close', 'volume']].head())
    
    print("\n2. 分析周一到周五每个交易日的统计指标...")
    weekday_stats = market.analyze_weekday_stats(kline_df)
    print("\n工作日统计结果:")
    print(weekday_stats)
    
    print("\n3. 分析每月月初、月中、月末三个区间的统计指标...")
    monthly_stats = market.analyze_monthly_period_stats(kline_df)
    print("\n月度区间统计结果:")
    print(monthly_stats)
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == '__main__':
    test_analysis_functions()