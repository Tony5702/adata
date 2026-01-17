# -*- coding: utf-8 -*-
"""
股票行情Web应用
"""

from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adata.stock.market.stock_market.stock_market import StockMarket
from adata.stock.info.stock_code import StockCode

app = Flask(__name__)

stock_market = StockMarket()
stock_code = StockCode()


def get_yesterday_date():
    """获取昨天的日期"""
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')


def get_top_volume_stocks(n=10):
    """获取当前成交量前n的股票"""
    # 获取所有股票代码
    stock_codes = stock_code.all_code()
    
    if stock_codes.empty:
        return []
    
    # 分批获取股票的当前行情
    code_list = stock_codes['stock_code'].tolist()
    batch_size = 100
    all_stocks = []
    
    for i in range(0, 100, batch_size):
        batch = code_list[i:i+batch_size]
        try:
            # 批量获取当前行情
            df = stock_market.list_market_current(code_list=batch)
            
            if not df.empty:
                for _, row in df.iterrows():
                    all_stocks.append({
                        'code': row['stock_code'],
                        'name': row['short_name'],
                        'volume': float(row['volume']) if row['volume'] else 0
                    })
        except Exception as e:
            print(f"Error fetching batch {i//batch_size + 1}: {e}")
            continue
    
    # 按成交量排序并返回前n只
    all_stocks.sort(key=lambda x: x['volume'], reverse=True)
    
    return all_stocks[:n]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/stocks')
def get_stocks():
    try:
        # 获取昨日成交量前10的股票
        top_stocks = get_top_volume_stocks(10)
        
        if not top_stocks:
            return jsonify([])
        
        # 获取这些股票的实时行情
        code_list = [stock['code'] for stock in top_stocks]
        current_df = stock_market.list_market_current(code_list=code_list)
        
        if current_df.empty:
            return jsonify([])
        
        # 获取每个股票的最高最低价
        stock_list = []
        for stock in top_stocks:
            code = stock['code']
            
            # 获取今日的最高最低价
            df = stock_market.get_market_min(stock_code=code)
            
            high = 0
            low = 0
            if not df.empty and 'high' in df.columns and 'low' in df.columns:
                high = df['high'].max()
                low = df['low'].min()
            
            # 查找当前行情
            current_row = current_df[current_df['stock_code'] == code]
            if not current_row.empty:
                current_row = current_row.iloc[0]
                stock_list.append({
                    'code': code,
                    'name': stock['name'],
                    'price': float(current_row['price']),
                    'change_percent': float(current_row['change_pct']),
                    'volume': float(current_row['volume']),
                    'amount': float(current_row['amount']),
                    'high': float(high) if high > 0 else float(current_row['price']),
                    'low': float(low) if low > 0 else float(current_row['price'])
                })
        
        return jsonify(stock_list)
    except Exception as e:
        print(f"Error in get_stocks: {e}")
        return jsonify([])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)