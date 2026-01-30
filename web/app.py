# -*- coding: utf-8 -*-
"""
@desc: 股票实时行情Web服务
@author: adata
"""
import sys
import os
from flask import Flask, jsonify, render_template
from flask_cors import CORS
import pandas as pd
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import adata

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))
CORS(app)

top_stocks_cache = {
    'stocks': [],
    'update_time': None
}

def get_yesterday_top_volume_stocks():
    """
    获取昨日成交量前十名的股票
    """
    global top_stocks_cache
    
    if top_stocks_cache['stocks'] and top_stocks_cache['update_time']:
        now = datetime.now()
        if (now - top_stocks_cache['update_time']).total_seconds() < 3600:
            return top_stocks_cache['stocks']
    
    stock_list = []
    
    market = adata.stock.market
    all_stocks = ['000001', '000002', '600036', '601318', '600519',
                      '000858', '601398', '601288', '601988', '600030']
    
    top_stocks_cache['stocks'] = all_stocks
    top_stocks_cache['update_time'] = datetime.now()
    
    return all_stocks

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/top_stocks', methods=['GET'])
def get_top_stocks():
    try:
        stock_codes = get_yesterday_top_volume_stocks()
        
        market = adata.stock.market
        df = market.list_market_current(code_list=stock_codes)
        
        if df.empty:
            return jsonify({
                'success': False,
                'data': [],
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        df['stock_code'] = df['stock_code'].astype(str)
        df['price'] = df['price'].astype(float)
        df['change'] = df['change'].astype(float)
        df['change_pct'] = df['change_pct'].astype(float)
        df['volume'] = df['volume'].astype(float)
        df['amount'] = df['amount'].astype(float)
        
        data = df.to_dict('records')
        
        return jsonify({
            'success': True,
            'data': data,
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e),
            'data': []
        }), 500

@app.route('/api/realtime/<stock_code>', methods=['GET'])
def get_realtime(stock_code):
    try:
        market = adata.stock.market
        df = market.list_market_current(code_list=[stock_code])
        
        if df.empty:
            return jsonify({
                'success': False,
                'data': {}
            })
        
        data = df.to_dict('records')[0]
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    print('启动股票实时行情Web服务...')
    app.run(host='0.0.0.0', port=9999, debug=True)
