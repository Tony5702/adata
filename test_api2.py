# -*- coding: utf-8 -*-
import pandas as pd
from adata.common import requests
from adata.common.utils.code_utils import get_exchange_by_stock_code

stock_codes = [
    {'stock_code': '000001', 'stock_name': '平安银行'},
    {'stock_code': '000002', 'stock_name': '万科A'},
]
codes = [s['stock_code'] for s in stock_codes]
api_url = f'https://qt.gtimg.cn/r=0.5979076524724433&q='
for code in codes:
    api_url += f's_{get_exchange_by_stock_code(code).lower()}{code},'

print('URL:', api_url)
res = requests.request('get', api_url, headers={})
print('Status:', res.status_code)
print('Response:', res.text)
print()

# 解析数据
data_list = res.text.split(';')
print('Data list:', data_list)
print()

data = []
for data_str in data_list:
    print(f'Processing: {repr(data_str)}, len={len(data_str)}')
    if len(data_str) < 8:
        print('  Skipped: too short')
        continue
    code_parts = data_str.split('~')
    print(f'  Split result: {code_parts}, len={len(code_parts)}')
    if len(code_parts) == 11:
        data.append(code_parts[1:8])
        print(f'  Added: {code_parts[1:8]}')

print()
print('Final data:', data)
