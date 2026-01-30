# Web服务说明

## 功能说明
展示昨日成交量前十名的股票的实时行情数据。

## 安装依赖

```bash
pip install -r requirements.txt
```

或单独安装Web依赖：
```bash
pip install flask flask-cors
```

## 启动服务

### 方式一：直接运行启动脚本
```bash
cd /path/to/adata_scp
python run_web.py
```

### 方式二：直接运行Web应用
```bash
cd /path/to/adata_scp
python -m web.app
```

## 访问地址

启动成功后，在浏览器中访问：
```
http://localhost:5000
```

## 功能特性

1. **自动刷新**：页面每5秒自动刷新数据
2. **响应式设计**：支持桌面端和移动端
3. **实时行情**：显示股票代码、名称、当前价格、涨跌幅
4. **成交量信息**：显示成交量和成交额
5. **视觉效果**：涨红跌绿，直观易懂

## API接口

### 获取Top股票实时行情
```
GET /api/top_stocks
```

响应示例：
```json
{
  "success": true,
  "data": [
    {
      "stock_code": "000001",
      "short_name": "平安银行",
      "price": 12.50,
      "change": 0.25,
      "change_pct": 2.04,
      "volume": 100000000,
      "amount": 1250000000
    }
  ],
  "update_time": "2024-01-30 15:30:00"
}
```

### 获取单个股票实时行情
```
GET /api/realtime/<stock_code>
```

例如：
```
GET /api/realtime/000001
```

## 项目结构

```
adata_scp/
├── web/
│   ├── __init__.py
│   ├── app.py              # Flask Web应用
│   ├── templates/
│   │   └── index.html      # 前端页面
│   └── static/             # 静态资源目录
└── run_web.py              # 启动脚本
```

## 注意事项

1. 确保网络连接正常，以便获取实时行情数据
2. 服务默认端口为5000，如需修改请编辑 `web/app.py`
3. 开发模式下启用了 `debug=True`，生产环境请设置为 `False`
