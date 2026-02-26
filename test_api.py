# -*- coding: utf-8 -*-
import pandas as pd
from adata.common import requests
from adata.common.headers import sina_headers
from adata.common.utils import code_utils

code_list = ['000001', '600519', '002594']
api_url = f'https://hq.sinajs.cn/list='
for code in code_list:
    api_url += f's_{code_utils.get_exchange_by_stock_code(code).lower()}{code},'

res = requests.request('get', api_url, headers=sina_headers.c_headers)
print('Response text:', repr(res.text))
print()

# 解析数据
data_list = res.text.split(';')
print('Data list:', data_list)
print()

data = []
_MARKET_CURRENT_COLUMNS = ['stock_code', 'short_name', 'price', 'change', 'change_pct', 'volume', 'amount']

for data_str in data_list:
    print(f'Processing: {repr(data_str)}, len={len(data_str)}')
    if len(data_str) < 8:
        continue
    idx = data_str.index('=')
    code = [data_str[idx - 6:idx]]
    code.extend(data_str[idx + 2:-1].split(','))
    print(f'  Code extracted: {code}, len={len(code)}')
    if len(code) == 7:
        data.append(code)

print()
print('Final data:', data)
result_df = pd.DataFrame(data=data, columns=_MARKET_CURRENT_COLUMNS)
print(result_df)
