#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@desc: 启动股票实时行情Web服务
@author: adata
"""
import sys
import os

web_dir = os.path.join(os.path.dirname(__file__), 'web')
sys.path.insert(0, web_dir)

from web.app import app

if __name__ == '__main__':
    print('=' * 50)
    print('股票实时行情 Web 服务')
    print('=' * 50)
    print('服务地址: http://localhost:9999')
    print('按 Ctrl+C 停止服务')
    print('=' * 50)
    app.run(host='0.0.0.0', port=9999, debug=True)
