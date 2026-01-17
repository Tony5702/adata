# -*- coding: utf-8 -*-
"""
测试新浪行情API
"""
import sys
sys.path.insert(0, '/Users/mars/disk/test_back/adata_a1')

from adata.stock.market.stock_market.stock_market_sina import StockMarketSina

# 测试新浪行情
sina_market = StockMarketSina()
df = sina_market.list_market_current(code_list=['000001', '600001', '000795', '872925', '920445'])

print("\n新浪行情数据:")
print(df)
print(f"\n数据行数: {len(df)}")
print(f"列名: {list(df.columns)}")