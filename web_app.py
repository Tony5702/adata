# -*- coding: utf-8 -*-
"""
@desc: 股票实时行情Web服务
@author: 1nchaos
@time: 2025/01/17
"""

import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template
from adata.stock.market.stock_market.stock_market import StockMarket

app = Flask(__name__)
stock_market = StockMarket()

cache = {
    'data': None,
    'update_time': None,
    'last_fetch': None
}

def get_yesterday_top_volume_stocks():
    """
    获取昨日成交量前十的股票
    """
    try:
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        today = datetime.now().strftime('%Y-%m-%d')
        
        all_stocks = pd.read_csv('adata/stock/cache/code.csv', dtype={'stock_code': str})
        if all_stocks.empty:
            return []
        
        code_list = all_stocks['stock_code'].tolist()[:100]
        
        top_stocks = []
        for code in code_list:
            try:
                df = stock_market.get_market(stock_code=code, start_date=yesterday, end_date=today, k_type=1)
                if not df.empty:
                    volume = df.iloc[-1]['volume']
                    top_stocks.append({
                        'stock_code': code,
                        'volume': volume
                    })
            except Exception as e:
                continue
        
        top_stocks.sort(key=lambda x: x['volume'], reverse=True)
        return [stock['stock_code'] for stock in top_stocks[:10]]
    except Exception as e:
        print(f"Error getting top volume stocks: {e}")
        return []

def get_stock_historical_data(stock_code, start_date, end_date):
    """
    获取股票历史数据作为实时行情的替代
    """
    try:
        df = stock_market.get_market(stock_code=stock_code, start_date=start_date, end_date=end_date, k_type=1)
        if not df.empty:
            last_row = df.iloc[-1]
            return {
                'stock_code': stock_code,
                'short_name': last_row.get('short_name', ''),
                'price': float(last_row['close']),
                'change': float(last_row.get('change', 0)),
                'change_pct': float(last_row.get('change_pct', 0)),
                'volume': int(last_row['volume']),
                'amount': float(last_row['amount'])
            }
    except Exception as e:
        print(f"Error getting historical data for {stock_code}: {e}")
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/top_stocks')
def get_top_stocks():
    """
    获取昨日成交量前十股票的实时行情
    """
    global cache
    
    try:
        now = datetime.now()
        
        if cache['data'] and cache['last_fetch']:
            time_since_last_fetch = (now - cache['last_fetch']).total_seconds()
            if time_since_last_fetch < 30:
                return jsonify({
                    'success': True,
                    'data': cache['data'],
                    'update_time': cache['update_time'],
                    'from_cache': True
                })
        
        top_codes = get_yesterday_top_volume_stocks()
        
        if not top_codes:
            if cache['data']:
                return jsonify({
                    'success': True,
                    'data': cache['data'],
                    'update_time': cache['update_time'],
                    'from_cache': True
                })
            return jsonify({'error': '无法获取股票数据', 'data': []})
        
        df = stock_market.list_market_current(code_list=top_codes)
        
        data = []
        
        if df.empty:
            yesterday = (now - timedelta(days=1)).strftime('%Y-%m-%d')
            today = now.strftime('%Y-%m-%d')
            
            for code in top_codes:
                stock_data = get_stock_historical_data(code, yesterday, today)
                if stock_data:
                    data.append(stock_data)
        else:
            for _, row in df.iterrows():
                data.append({
                    'stock_code': row['stock_code'],
                    'short_name': row['short_name'],
                    'price': float(row['price']),
                    'change': float(row['change']),
                    'change_pct': float(row['change_pct']),
                    'volume': int(row['volume']),
                    'amount': float(row['amount'])
                })
        
        if data:
            cache['data'] = data
            cache['update_time'] = now.strftime('%Y-%m-%d %H:%M:%S')
            cache['last_fetch'] = now
            
            return jsonify({
                'success': True,
                'data': data,
                'update_time': cache['update_time'],
                'from_cache': False
            })
        elif cache['data']:
            return jsonify({
                'success': True,
                'data': cache['data'],
                'update_time': cache['update_time'],
                'from_cache': True
            })
        else:
            return jsonify({'error': '无法获取行情数据', 'data': []})
    except Exception as e:
        print(f"Error in get_top_stocks: {e}")
        if cache['data']:
            return jsonify({
                'success': True,
                'data': cache['data'],
                'update_time': cache['update_time'],
                'from_cache': True,
                'error': str(e)
            })
        return jsonify({'error': str(e), 'data': []})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
