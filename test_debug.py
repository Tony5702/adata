#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import pandas as pd

url = "https://qt.gtimg.cn/r=0.5979076524724433&q=s_sh600519,s_sz000001"
res = requests.get(url)
print(f"状态码: {res.status_code}")

# 模拟修复后的解析逻辑
data_list = res.text.split(';')
data = []
for data_str in data_list:
    if len(data_str) < 8:
        continue
    if '"' in data_str:
        data_str = data_str.split('"')[1]
    code = data_str.split('~')
    print(f"解析行: {repr(data_str)}")
    print(f"  分割后长度: {len(code)}")
    print(f"  内容: {code}")
    if len(code) >= 8:
        print(f"  取 code[1:8] = {code[1:8]}")
        data.append(code[1:8])

print(f"\n最终提取的数据: {data}")
data_columns = ['short_name', 'stock_code', 'price', 'change', 'change_pct', 'volume', 'amount']
_MARKET_CURRENT_COLUMNS = ['stock_code', 'short_name', 'price', 'change', 'change_pct', 'volume', 'amount']

if data:
    result_df = pd.DataFrame(data=data, columns=data_columns)
    print(f"\nDataFrame:\n{result_df}")
    mask = result_df['stock_code'].str.startswith(('0', '3', '6', '9'))
    result_df.loc[mask, 'volume'] = result_df['volume'].astype(int) * 100
    result_df.loc[mask, 'amount'] = result_df['amount'].astype(float) * 10000
    print(f"\n转换后:\n{result_df}")
    print(f"\n最终列选择: {_MARKET_CURRENT_COLUMNS}")
    print(f"可用列: {result_df.columns.tolist()}")
    final_df = result_df[_MARKET_CURRENT_COLUMNS]
    print(f"\n最终结果:\n{final_df}")
