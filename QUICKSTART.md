# 快速开始指南

## 问题解决总结

✅ **已解决的问题：**
- Python 版本不一致（python3 → 3.13, pip3 → 3.9）
- 依赖包找不到（ModuleNotFoundError）
- Homebrew Python 受管理环境限制

✅ **解决方案：**
- 创建了独立的虚拟环境 (venv)
- 在虚拟环境中安装所有依赖
- 提供了便捷的启动脚本

## 三种使用方式

### 方式 1：启动脚本（最简单）⭐

```bash
cd /Users/admin/linux.do/international-news
./run.sh
```

提供交互式菜单，自动处理环境激活。

### 方式 2：命令行（灵活）

```bash
cd /Users/admin/linux.do/international-news

# 激活虚拟环境
source venv/bin/activate

# 运行脚本
python get_news_with_websearch_final.py

# 完成后退出
deactivate
```

### 方式 3：一行命令

```bash
cd /Users/admin/linux.do/international-news && source venv/bin/activate && python get_news_with_websearch_final.py
```

## 常用命令

```bash
# 测试环境
source venv/bin/activate && python test_env.py

# 获取实时新闻（Web Search）
source venv/bin/activate && python get_news_with_websearch_final.py

# 快速获取新闻
source venv/bin/activate && python get_news.py

# 查看可用模型
source venv/bin/activate && python list_models.py

# 测试 API
source venv/bin/activate && python api_endpoint_test.py
```

## 环境状态检查

```bash
# 查看当前 Python
which python3
python3 --version

# 检查虚拟环境
ls -la venv/

# 激活后检查
source venv/bin/activate
which python      # 应显示 venv/bin/python
pip list          # 查看已安装的包
```

## 脚本说明

| 脚本 | 功能 | 推荐度 |
|------|------|--------|
| get_news_with_websearch_final.py | 实时搜索网络获取新闻 | ⭐⭐⭐⭐⭐ |
| get_news_final.py | 双格式支持，命令行参数 | ⭐⭐⭐⭐ |
| get_news.py | OpenAI 格式，快速 | ⭐⭐⭐ |
| get_news_messages_api.py | Anthropic 格式 | ⭐⭐⭐ |
| list_models.py | 查询可用模型 | ⭐⭐⭐⭐ |
| api_endpoint_test.py | 测试 API 端点 | ⭐⭐⭐ |
| test_env.py | 环境测试 | ⭐⭐⭐⭐ |
| run.sh | 启动脚本 | ⭐⭐⭐⭐⭐ |

## 典型工作流程

### 场景 1：获取最新新闻

```bash
./run.sh
# 选择 1 (获取实时新闻)
```

### 场景 2：开发调试

```bash
# 启动时激活虚拟环境
source venv/bin/activate

# 开发和测试
python test_env.py
python get_news.py

# 工作完成后
deactivate
```

### 场景 3：定时任务

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天早上8点）
0 8 * * * cd /Users/admin/linux.do/international-news && source venv/bin/activate && python get_news_with_websearch_final.py >> /tmp/news.log 2>&1
```

## 输出文件位置

所有生成的文件在项目根目录：

```
international-news/
├── news_websearch_YYYYMMDD_HHMMSS.txt      # Web Search 新闻
├── news_websearch_YYYYMMDD_HHMMSS.json     # 完整响应
├── news_chat_completions_*.txt             # Chat 格式新闻
├── news_messages_*.txt                     # Messages 格式新闻
└── international_news.txt                  # 通用输出
```

## 环境变量（可选）

如果需要修改 API 配置，可以设置环境变量：

```bash
export NEWS_API_BASE="https://spai.aicoding.sh"
export NEWS_API_KEY="your-api-key"

# 或者创建 .env 文件
cat > .env <<EOF
NEWS_API_BASE=https://spai.aicoding.sh
NEWS_API_KEY=sk-SZVRIyGtmcvXzJqhvUkvgTYd2ZTzct9Kx2IHGhf7r8UbDPCc
EOF
```

## 故障排除快速参考

| 问题 | 解决方案 |
|------|----------|
| ModuleNotFoundError | `source venv/bin/activate` |
| Permission denied | `chmod +x run.sh` |
| venv 不存在 | `python3 -m venv venv` |
| 依赖未安装 | `source venv/bin/activate && pip install -r requirements.txt` |
| API 错误 | `python test_env.py` |

## 重置环境

如果遇到问题，可以完全重置：

```bash
# 1. 删除虚拟环境
rm -rf venv

# 2. 重新创建
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. 测试
python test_env.py
```

## 获取帮助

- 查看详细设置说明：`cat SETUP.md`
- 查看项目文档：`cat README.md`
- 测试环境：`source venv/bin/activate && python test_env.py`
- 运行启动脚本：`./run.sh`

## 成功标志

当您看到以下输出时，说明环境配置成功：

```
✓ Python 版本: 3.13.4
✓ requests 2.32.5 已安装
✓ brotli 已安装
✓ API 连接成功
✓ 可用模型数量: 5
✓ 所有测试通过！环境配置正确。
```

## 下一步

1. 运行 `./run.sh` 尝试获取新闻
2. 查看生成的文件
3. 根据需要修改脚本参数
4. 设置定时任务（可选）

祝使用愉快！🎉
