# 国际新闻获取工具

使用 OpenAI 兼容 API 和 Anthropic Messages API 获取最新国际新闻的 Python 脚本集合。

## 功能特点

- ✅ 支持两种 API 调用方式：OpenAI 格式和 Anthropic 格式
- ✅ **Web Search 功能**：实时搜索网络获取最新新闻
- ✅ 使用 Claude AI 模型进行新闻总结和分析
- ✅ 自动处理 Brotli 压缩响应
- ✅ 详细的错误处理和日志输出
- ✅ 保存新闻到文本文件和 JSON 格式

## 文件说明

### 主要脚本

1. **get_news_with_websearch_final.py** ⭐ **推荐使用**
   - 使用 web_search 工具实时搜索网络
   - 获取真实的最新国际新闻
   - 包含新闻来源链接

2. **get_news_final.py**
   - 支持两种 API 调用方式
   - 基于 AI 知识库生成新闻
   - 包含命令行参数选择

3. **get_news.py**
   - 原始版本，使用 /v1/chat/completions 端点
   - OpenAI 格式调用

4. **get_news_messages_api.py**
   - 使用 /v1/messages 端点
   - Anthropic 格式调用

### 辅助脚本

- **list_models.py** - 查询 API 支持的模型列表
- **api_endpoint_test.py** - 测试不同的 API 端点支持情况
- **curl_simulation.py** - 模拟 curl 命令行为

### 配置文件

- **requirements.txt** - Python 依赖包列表

## 环境设置

### 快速开始（推荐）

使用提供的启动脚本，会自动设置环境：

```bash
./run.sh
```

### 手动设置

如果您的系统是 Python 3.13+（Homebrew 安装），需要使用虚拟环境：

```bash
# 1. 创建虚拟环境（首次运行）
python3 -m venv venv

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt
```

**依赖包：**
- `requests>=2.31.0` - HTTP 请求
- `brotli>=1.0.0` - 解压缩响应数据

**详细说明：** 参见 [SETUP.md](SETUP.md)

## 使用方法

### 方法 1：使用启动脚本（最简单）

```bash
./run.sh
```

提供交互式菜单，选择需要的功能。

### 方法 2：使用 Web Search 获取实时新闻（推荐）

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行脚本
python get_news_with_websearch_final.py
```

**特点：**
- 🔍 实时搜索网络
- 📊 提供新闻来源链接
- 🌐 获取最新国际新闻
- ⏱️ 响应时间较长（约60-90秒）

**输出示例：**
```
🔍 检测到 Web Search 调用
   查询: latest international news today

📊 收到搜索结果
   - Israel attacks Beirut... - ABC News
     https://abcnews.go.com/...

📰 AI 总结:
1. 乌克兰和平谈判取得进展
   来源：CBS News, CNN

2. 尼日利亚被绑架女学生全部获救
   来源：ABC News, Fox News
   ...
```

### 方法 3：使用 AI 知识库（快速）

```bash
# 激活虚拟环境
source venv/bin/activate

# 使用两种方式
python get_news_final.py --method both

# 只使用 OpenAI 格式
python get_news_final.py --method chat

# 只使用 Anthropic 格式
python get_news_final.py --method messages
```

**特点：**
- ⚡ 快速响应（10-20秒）
- 📚 基于 AI 知识库
- ⚠️ 知识截止到 2024年4月

### 查询可用模型

```bash
source venv/bin/activate
python list_models.py
```

### 测试 API 端点

```bash
source venv/bin/activate
python api_endpoint_test.py
```

## API 配置

所有脚本中的 API 配置：

```python
API_BASE_URL = "https://spai.aicoding.sh"
API_KEY = "sk-SZVRIyGtmcvXzJqhvUkvgTYd2ZTzct9Kx2IHGhf7r8UbDPCc"
```

## 支持的功能

### API 端点

| 端点 | 格式 | 状态 | 说明 |
|------|------|------|------|
| /v1/chat/completions | OpenAI | ✅ 支持 | 使用 `Authorization: Bearer` |
| /v1/messages | Anthropic | ✅ 支持 | 使用 `x-api-key` header |
| /v1/models | GET | ✅ 支持 | 查询可用模型 |

### 工具支持

| 工具 | 类型 | 状态 | 说明 |
|------|------|------|------|
| web_search | web_search_20250305 | ✅ 支持 | 实时网络搜索 |

### 支持的模型

当前 API 支持以下 Claude 模型：
- `claude-3-5-haiku-20241022` - 快速轻量级模型
- `claude-haiku-4-5-20251001` - Haiku 4.5
- `claude-opus-4-1-20250805` - Opus 4.1
- `claude-sonnet-4-20250514` - Sonnet 4
- `claude-sonnet-4-5-20250929` - Sonnet 4.5（推荐）

## 技术细节

### Web Search 工作流程

1. 发送请求到 `/v1/messages` 端点
2. 包含 `tools` 参数，指定 `web_search_20250305`
3. AI 自动决定搜索查询
4. 服务器执行实际的网络搜索
5. AI 分析搜索结果并生成总结

### 响应处理

- 响应使用 Brotli 压缩 (`Content-Encoding: br`)
- requests 库自动处理解压
- 如果自动解压失败，手动使用 brotli 库

### 请求头配置

```python
headers = {
    "x-api-key": API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json",
    "User-Agent": "Mozilla/5.0...",  # 模拟浏览器
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br"
}
```

## 输出文件

脚本会生成以下文件：

- `news_websearch_YYYYMMDD_HHMMSS.txt` - Web Search 新闻文本
- `news_websearch_YYYYMMDD_HHMMSS.json` - 完整 JSON 响应
- `news_chat_completions_YYYYMMDD_HHMMSS.txt` - Chat 格式新闻
- `news_messages_YYYYMMDD_HHMMSS.txt` - Messages 格式新闻

## 注意事项

1. **网络连接**：需要稳定的互联网连接
2. **API 配额**：确保 API 密钥有足够的配额
3. **响应时间**：Web Search 需要较长时间（60-90秒）
4. **新闻来源**：Web Search 提供真实新闻来源链接
5. **知识截止**：非 Web Search 模式基于 2024年4月的知识

## 故障排除

### 问题：500 错误

**原因：**
- 早期测试中，使用 `web_search` 工具时遇到 500 错误
- 由于未正确处理 Brotli 压缩响应

**解决方案：**
```bash
pip install brotli
```

### 问题：503 错误或"模型不可用"

**解决方案：**
1. 运行 `python3 list_models.py` 查看可用模型
2. 检查 API 密钥是否有效
3. 确认网络连接正常

### 问题：JSON 解析失败

**原因：** 响应被 Brotli 压缩但未正确解压

**解决方案：**
- 确保安装了 `brotli` 库
- 检查 `Accept-Encoding` header 是否正确设置

## 命令行示例

```bash
# 方式1：使用启动脚本（推荐）
./run.sh

# 方式2：手动运行（需先激活虚拟环境）
source venv/bin/activate

# 获取实时新闻（推荐）
python get_news_with_websearch_final.py

# 快速获取新闻（使用 AI 知识库）
python get_news_final.py --method both

# 查看可用模型
python list_models.py

# 测试 API 端点
python api_endpoint_test.py

# 模拟 curl 命令
python curl_simulation.py

# 退出虚拟环境
deactivate
```

## API 使用示例

### 基本 curl 命令

```bash
curl https://spai.aicoding.sh/v1/messages \
    --header "x-api-key: sk-SZVRIyGtmcvXzJqhvUkvgTYd2ZTzct9Kx2IHGhf7r8UbDPCc" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": "请提供最新国际新闻"
            }
        ],
        "tools": [{
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 5
        }]
    }'
```

### Python 请求示例

```python
import requests

url = "https://spai.aicoding.sh/v1/messages"
headers = {
    "x-api-key": "sk-SZVRIyGtmcvXzJqhvUkvgTYd2ZTzct9Kx2IHGhf7r8UbDPCc",
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}
data = {
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "最新新闻"}],
    "tools": [{
        "type": "web_search_20250305",
        "name": "web_search",
        "max_uses": 5
    }]
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
```

## 项目结构

```
international-news/
├── README.md                           # 本文档
├── SETUP.md                            # 环境设置详细指南
├── run.sh                              # 启动脚本（推荐使用）
├── requirements.txt                    # 依赖包
├── venv/                               # 虚拟环境目录
├── get_news_with_websearch_final.py   # ⭐ Web Search 版本
├── get_news_final.py                  # 双格式支持版本
├── get_news.py                        # OpenAI 格式
├── get_news_messages_api.py           # Anthropic 格式
├── list_models.py                     # 模型列表查询
├── api_endpoint_test.py               # API 端点测试
└── curl_simulation.py                 # curl 模拟
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可

MIT License
