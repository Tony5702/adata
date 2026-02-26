# -*- coding: utf-8 -*-
"""
@desc: 股票实时行情Web应用
@author: AI Assistant
@time: 2026/2/26
"""

import json
import re
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify
import pandas as pd

# 直接使用腾讯接口获取数据
from adata.common import requests
from adata.common.utils.code_utils import get_exchange_by_stock_code

app = Flask(__name__)

# 默认热门股票列表（通常是成交量较大的股票）
DEFAULT_HOT_STOCKS = [
    {'stock_code': '000001', 'stock_name': '平安银行'},
    {'stock_code': '000002', 'stock_name': '万科A'},
    {'stock_code': '000858', 'stock_name': '五粮液'},
    {'stock_code': '002594', 'stock_name': '比亚迪'},
    {'stock_code': '300750', 'stock_name': '宁德时代'},
    {'stock_code': '600000', 'stock_name': '浦发银行'},
    {'stock_code': '600519', 'stock_name': '贵州茅台'},
    {'stock_code': '600036', 'stock_name': '招商银行'},
    {'stock_code': '601318', 'stock_name': '中国平安'},
    {'stock_code': '601398', 'stock_name': '工商银行'},
]


def get_current_market(stock_codes):
    """获取股票实时行情（使用腾讯接口）"""
    if not stock_codes:
        return []

    try:
        codes = [s['stock_code'] for s in stock_codes]
        api_url = f"https://qt.gtimg.cn/r=0.5979076524724433&q="
        for code in codes:
            api_url += f's_{get_exchange_by_stock_code(code).lower()}{code},'

        res = requests.request('get', api_url, headers={})

        if len(res.text) < 1 or res.status_code != 200:
            return []

        # 解析数据 v_s_sz000001="51~平安银行~000001~10.83~-0.03~-0.28~442494~47973~~2101.66~GP-A~";
        data_list = res.text.split(';')
        data = []
        for data_str in data_list:
            if len(data_str) < 8:
                continue
            # 使用正则表达式提取引号内的内容
            match = re.search(r'"([^"]*)"', data_str)
            if match:
                content = match.group(1)
                code_parts = content.split('~')
                if len(code_parts) >= 8:
                    # 提取: 市场代码, 名称, 代码, 价格, 涨跌额, 涨跌幅, 成交量(手), 成交额(万元)
                    data.append(code_parts[1:8])

        if not data:
            return []

        # 封装数据
        result = []
        for row in data:
            stock_code = row[1]
            stock_name = row[0]
            
            # 查找对应的股票名称
            for s in stock_codes:
                if s['stock_code'] == stock_code:
                    stock_name = s['stock_name']
                    break

            # 单位转换：手->股，万元->元
            volume = int(row[5]) * 100 if stock_code.startswith(('0', '3', '6', '9')) else int(row[5])
            amount = float(row[6]) * 10000 if stock_code.startswith(('0', '3', '6', '9')) else float(row[6])

            result.append({
                'stock_code': stock_code,
                'stock_name': stock_name,
                'price': float(row[2]),
                'change': float(row[3]),
                'change_pct': float(row[4]),
                'volume': volume,
                'amount': amount,
            })

        return result
    except Exception as e:
        print(f"Error getting current market: {e}")
        import traceback
        traceback.print_exc()
        return []


@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


@app.route('/api/top-volume-stocks')
def api_top_volume_stocks():
    """API: 获取热门股票的实时行情，按成交量排序"""
    try:
        current_data = get_current_market(DEFAULT_HOT_STOCKS)

        # 按成交量排序（模拟昨日成交量前十）
        current_data.sort(key=lambda x: x['volume'], reverse=True)

        return jsonify({
            'success': True,
            'data': current_data,
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'data': [],
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })


if __name__ == '__main__':
    print("Starting stock market web server...")
    print("Please visit: http://127.0.0.1:8888")
    app.run(host='0.0.0.0', port=8888, debug=False)
