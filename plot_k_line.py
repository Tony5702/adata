#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@desc: 股票 K 线图绘制命令行工具
@author: 1nchaos
@time: 2025/07/14
"""

import argparse
from adata.stock.market import market


def main():
    """
    命令行工具主函数
    """
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='绘制股票 K 线图')
    
    # 添加命令行参数
    parser.add_argument('stock_code', type=str, help='股票代码')
    parser.add_argument('--start_date', type=str, default='1990-01-01', help='开始日期 (格式: YYYY-MM-DD)')
    parser.add_argument('--end_date', type=str, default=None, help='结束日期 (格式: YYYY-MM-DD)')
    parser.add_argument('--k_type', type=int, default=1, help='K 线类型: 1.日; 2.周; 3.月; 4.季度; 5.5分钟; 15.15分钟; 30.30分钟; 60.60分钟')
    parser.add_argument('--adjust_type', type=int, default=1, help='复权类型: 0.不复权; 1.前复权; 2.后复权')
    parser.add_argument('--title', type=str, default=None, help='图表标题')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    try:
        print(f"正在绘制股票 {args.stock_code} 的 K 线图...")
        
        # 调用绘制 K 线图的函数
        market.plot_k_line(
            stock_code=args.stock_code,
            start_date=args.start_date,
            end_date=args.end_date,
            k_type=args.k_type,
            adjust_type=args.adjust_type,
            title=args.title
        )
        
        print("K 线图绘制完成！")
    except Exception as e:
        print(f"绘制 K 线图时发生错误: {str(e)}")


if __name__ == '__main__':
    main()
