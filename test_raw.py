#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests

url = "https://qt.gtimg.cn/r=0.5979076524724433&q=s_sh600519,s_sz000001"
res = requests.get(url)
print(f"状态码: {res.status_code}")
print(f"响应长度: {len(res.text)}")
print(f"原始内容: {repr(res.text)}")
print(f"\n解析后:")
for line in res.text.split(';'):
    print(f"  行: {repr(line)}")
    if len(line) > 8 and '~' in line:
        parts = line.split('~')
        print(f"  拆分数组长度: {len(parts)}")
        print(f"  内容: {parts}")
