# 配置说明

本项目支持多种方式配置 API Key 和其他参数。

## 配置优先级

配置参数会按照以下优先级读取（从高到低）：

1. **命令行参数** - 最高优先级
2. **环境变量** - 临时配置
3. **.env 文件** - 持久化配置
4. **默认值** - 代码中的硬编码值

## 方法 1：命令行参数（推荐用于临时测试）

```bash
# 使用 --api-key 参数
./run.sh --websearch --api-key sk-your-api-key-here

# 同时设置多个参数
./run.sh --api-key sk-xxx --api-url https://api.example.com --model claude-3-sonnet 1

# 查看帮助
./run.sh --help
```

## 方法 2：环境变量（推荐用于临时使用）

```bash
# 设置环境变量后运行
export API_KEY="sk-your-api-key-here"
./run.sh --websearch

# 或者在同一行运行
API_KEY="sk-your-api-key-here" ./run.sh 1

# 设置多个环境变量
export API_KEY="sk-your-api-key-here"
export API_BASE_URL="https://api.example.com"
export DEFAULT_MODEL="claude-3-sonnet"
./run.sh --websearch
```

## 方法 3：.env 文件（推荐用于持久化配置）

1. 复制示例文件：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件：
```bash
# API 配置
API_BASE_URL=https://spai.aicoding.sh
API_KEY=sk-your-actual-api-key-here
DEFAULT_MODEL=claude-sonnet-4-5-20250929
```

3. 运行脚本（会自动读取 .env 配置）：
```bash
./run.sh --websearch
```

## 可配置参数

| 参数 | 命令行 | 环境变量 | 说明 |
|------|--------|----------|------|
| API Key | `--api-key KEY` | `API_KEY` | API 密钥（必填） |
| API URL | `--api-url URL` | `API_BASE_URL` | API 基础地址 |
| 模型 | `--model MODEL` | `DEFAULT_MODEL` | 默认使用的模型 |

## 使用示例

### 示例 1：使用 .env 文件
```bash
# 创建 .env 文件
cat > .env << EOF
API_KEY=sk-your-api-key-here
API_BASE_URL=https://spai.aicoding.sh
DEFAULT_MODEL=claude-sonnet-4-5-20250929
EOF

# 直接运行
./run.sh --websearch
```

### 示例 2：环境变量覆盖 .env
```bash
# .env 中有默认配置，但临时使用不同的 key
API_KEY=sk-another-key ./run.sh 1
```

### 示例 3：命令行参数最高优先级
```bash
# 即使有 .env 和环境变量，命令行参数优先级最高
./run.sh --api-key sk-override-key --websearch
```

### 示例 4：直接调用 Python 脚本
```bash
# Python 脚本也会自动读取配置
source venv/bin/activate

# 使用 .env 文件中的配置
python get_news_with_websearch_final.py

# 使用环境变量
API_KEY=sk-xxx python get_news_with_websearch_final.py
```

## 安全建议

1. **不要提交 .env 文件到 Git**
   - `.env` 文件包含敏感信息，已在 `.gitignore` 中排除
   - 只提交 `.env.example` 作为模板

2. **使用环境变量管理密钥**
   - 生产环境推荐使用环境变量而非 .env 文件
   - 可以使用密钥管理服务（如 AWS Secrets Manager）

3. **定期轮换 API Key**
   - 定期更新 API Key 以提高安全性
   - 发现密钥泄露立即撤销并更新

## 故障排除

### 问题：API 请求失败，401 未授权
检查 API Key 是否正确：
```bash
# 查看当前使用的 API Key（仅显示前后几位）
python -c "from config import API_KEY; print(f'Using API_KEY: {API_KEY[:8]}...{API_KEY[-4:]}')"
```

### 问题：不知道使用了哪个配置
添加调试信息：
```bash
# 在脚本开头添加
echo "API_KEY: ${API_KEY:0:8}...${API_KEY: -4}"
echo "API_BASE_URL: $API_BASE_URL"
```

### 问题：.env 文件不生效
检查文件格式：
```bash
# 查看 .env 文件内容
cat .env

# 确保没有多余的空格和引号
# 正确：API_KEY=sk-xxx
# 错误：API_KEY = "sk-xxx"
```
