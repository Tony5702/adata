# 频率限制功能使用说明

## 功能概述

已为所有通过 `request` 获取数据的接口添加了频率限制功能：
- 同一个域名默认每分钟最多30次请求
- 支持通过方法自定义每个域名的请求次数限制
- 采用滑动窗口算法实现精确的频率控制
- 线程安全的单例模式实现

## 使用方法

### 1. 基本使用（默认限制）

```python
from adata.common.utils import requests

# 默认情况下，每个域名每分钟最多30次请求
response = requests.request('get', 'https://api.example.com/data')
```

### 2. 自定义频率限制

```python
from adata.common.utils import requests

# 设置特定域名的频率限制：每分钟10次
requests.set_rate_limit('api.example.com', 10)

# 后续对该域名的请求将受到限制
for i in range(15):
    response = requests.request('get', 'https://api.example.com/data')
    # 第11次及以后的请求将被限制，等待约60秒后继续
```

### 3. 不同域名独立限制

```python
from adata.common.utils import requests

# 设置不同域名的不同限制
requests.set_rate_limit('api.example.com', 10)  # 每分钟10次
requests.set_rate_limit('api.test.com', 50)     # 每分钟50次

# 对 api.example.com 的请求
response1 = requests.request('get', 'https://api.example.com/data')

# 对 api.test.com 的请求（使用默认30次/分钟或自定义的50次/分钟）
response2 = requests.request('get', 'https://api.test.com/info')
```

## 实现细节

### 核心类

1. **RateLimiter**: 频率限制器单例类
   - 使用滑动窗口算法
   - 线程安全的实现
   - 支持动态设置限制

2. **SunRequests**: 请求工具类
   - 集成了频率限制功能
   - 提供 `set_rate_limit` 方法
   - 自动解析URL域名

### 算法说明

采用滑动窗口算法实现频率限制：
- 维护每个域名的请求时间戳列表
- 每次请求时，移除超过60秒的旧时间戳
- 检查当前窗口内的请求数量是否超过限制
- 超过限制时，自动等待直到可以继续请求

## 注意事项

- 频率限制按域名独立计算
- 设置的限制会在应用运行期间保持
- 应用重启后，限制会重置为默认值（30次/分钟）
- 频率限制检查在请求发起前执行，如果被限制，会自动等待
