# 股票实时行情Web应用

这是一个基于Flask的股票实时行情Web应用，自动显示昨日成交量前十名股票的当前实时行情数据。

## 功能特点

- 自动获取昨日成交量前十的股票
- 实时显示股票行情数据（价格、涨跌幅、成交量、成交额等）
- 简洁美观的卡片式界面设计
- 自动每30秒刷新数据
- 支持响应式布局，适配手机和电脑访问
- 红涨绿跌的配色方案

## 快速开始

### 1. 安装依赖

```bash
pip install flask pandas requests beautifulsoup4
```

### 2. 启动应用

```bash
python3 web_app.py
```

### 3. 访问页面

在浏览器中打开：
- 本地访问：http://127.0.0.1:8000
- 局域网访问：http://172.18.18.102:8000

## 文件说明

- `web_app.py` - Flask后端应用主文件
- `templates/index.html` - 前端页面模板

## API接口

### 获取昨日成交量前十股票的实时行情

**接口地址：** `/api/top_stocks`

**请求方法：** GET

**返回数据格式：**

```json
{
  "success": true,
  "data": [
    {
      "stock_code": "000100",
      "short_name": "股票名称",
      "price": 4.83,
      "change": -0.12,
      "change_pct": -2.42,
      "volume": 703321300,
      "amount": 3419445715.51
    }
  ],
  "update_time": "2026-01-17 16:34:00",
  "from_cache": false
}
```

**字段说明：**
- `stock_code`: 股票代码
- `short_name`: 股票简称
- `price`: 当前价格（元）
- `change`: 涨跌额（元）
- `change_pct`: 涨跌幅（%）
- `volume`: 成交量（股）
- `amount`: 成交额（元）
- `update_time`: 数据更新时间
- `from_cache`: 是否来自缓存

## 技术栈

- **后端：** Flask + Python
- **前端：** HTML5 + CSS3 + JavaScript
- **数据源：** AData股票数据接口

## 注意事项

- 应用运行在开发模式下，不建议用于生产环境
- 默认端口为8000，如需修改请编辑`web_app.py`中的端口号
- 数据每30秒自动刷新一次
- 在市场休市期间会显示最近的历史数据

## 自定义配置

### 修改端口

编辑`web_app.py`文件最后一行：

```python
app.run(host='0.0.0.0', port=8000, debug=True)
```

将`8000`改为你想要的端口号。

### 修改刷新间隔

编辑`templates/index.html`文件，找到以下代码：

```javascript
setInterval(fetchStockData, 30000);
```

将`30000`（30秒）改为你想要的刷新间隔（毫秒）。

## 许可证

MIT License
