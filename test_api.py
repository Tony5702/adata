#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from adata.stock.market.stock_market.stock_market_qq import StockMarketQQ
import adata

print("=== 测试腾讯API ===")
qq = StockMarketQQ()
df = qq.list_market_current(code_list=['600519', '000001'])
print('腾讯API结果:')
print(df)
print('列名:', df.columns.tolist())
print('行数:', len(df))

print("\n=== 测试adata主接口 ===")
df2 = adata.stock.market.list_market_current(code_list=['600519', '000001'])
print('adata接口结果:')
print(df2)
print('行数:', len(df2))
