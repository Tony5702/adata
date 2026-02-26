import adata
import pandas as pd
from flask import Flask, render_template, jsonify

app = Flask(__name__)


FIXED_TOP_STOCKS = [
    '600519', '000858', '601318', '000001', '600036',
    '000333', '600276', '601899', '601398', '601288'
]

print(f"固定Top10股票: {FIXED_TOP_STOCKS}")


@app.route('/')
def index():
    return render_template('index.html')


def safe_float(value, default=0):
    if pd.isna(value) or value == '':
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


@app.route('/api/top_stocks')
def api_top_stocks():
    code_list = FIXED_TOP_STOCKS
    
    try:
        df = adata.stock.market.list_market_current(code_list=code_list)
        
        if df.empty:
            return jsonify([])
        
        result = []
        for _, row in df.iterrows():
            change_pct = safe_float(row.get('change_pct', 0))
            price = safe_float(row.get('price', 0))
            change = safe_float(row.get('change', 0))
            volume = safe_float(row.get('volume', 0))
            amount = safe_float(row.get('amount', 0))
            
            result.append({
                'stock_code': str(row.get('stock_code', '')),
                'short_name': str(row.get('short_name', '')),
                'price': f"{price:.2f}",
                'change': f"{change:+.2f}",
                'change_pct': f"{change_pct:+.2f}%",
                'volume': f"{volume / 10000:.0f}万",
                'amount': f"{amount / 100000000:.2f}亿",
                'change_class': 'up' if change_pct > 0 else 'down' if change_pct < 0 else 'flat'
            })
        
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"获取行情数据异常: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("启动股票行情Web服务...")
    print("访问地址: http://localhost:8081")
    app.run(host='0.0.0.0', port=8081, debug=True)
