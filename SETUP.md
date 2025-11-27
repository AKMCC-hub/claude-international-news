# 环境设置指南

## 问题说明

系统存在多个 Python 版本：
- `python3` → Python 3.13.4
- `/usr/local/opt/python@3.9/bin/python3.9` → Python 3.9

Python 3.13 是通过 Homebrew 安装的受管理环境，需要使用虚拟环境。

## 解决方案

我们已经创建了虚拟环境来隔离依赖，确保环境一致性。

## 快速开始

### 方法1：使用启动脚本（推荐）

```bash
./run.sh
```

启动脚本会自动：
1. 检查并创建虚拟环境（如果不存在）
2. 安装所需依赖
3. 显示交互式菜单
4. 运行选择的功能

### 方法2：手动激活虚拟环境

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行脚本
python get_news_with_websearch_final.py

# 退出虚拟环境
deactivate
```

## 虚拟环境说明

### 什么是虚拟环境？

虚拟环境是 Python 的独立运行环境，包含：
- 独立的 Python 解释器
- 独立的包安装目录
- 不会影响系统 Python

### 虚拟环境位置

```
international-news/
└── venv/                    # 虚拟环境目录
    ├── bin/                 # 可执行文件
    │   ├── python           # Python 解释器
    │   ├── pip              # 包管理器
    │   └── activate         # 激活脚本
    └── lib/                 # 安装的包
```

### 已安装的包

在虚拟环境中安装了：
- `requests>=2.31.0` - HTTP 请求库
- `brotli>=1.0.0` - Brotli 解压缩库

## 完整设置流程（已完成）

如果需要重新设置，执行以下步骤：

```bash
# 1. 删除旧的虚拟环境（如果存在）
rm -rf venv

# 2. 创建新的虚拟环境
python3 -m venv venv

# 3. 激活虚拟环境
source venv/bin/activate

# 4. 升级 pip（可选）
pip install --upgrade pip

# 5. 安装依赖
pip install -r requirements.txt

# 6. 测试安装
python -c "import requests, brotli; print('✓ 所有依赖已安装')"
```

## 使用示例

### 示例1：获取实时新闻

```bash
source venv/bin/activate
python get_news_with_websearch_final.py
```

### 示例2：快速获取新闻

```bash
source venv/bin/activate
python get_news_final.py --method both
```

### 示例3：查看可用模型

```bash
source venv/bin/activate
python list_models.py
```

## IDE 配置

### VS Code

1. 打开项目文件夹
2. 按 `Cmd+Shift+P`
3. 输入 "Python: Select Interpreter"
4. 选择 `./venv/bin/python`

### PyCharm

1. 打开项目
2. Settings → Project → Python Interpreter
3. 点击齿轮图标 → Add
4. 选择 Existing Environment
5. 选择 `venv/bin/python`

## 常见问题

### Q: 为什么需要虚拟环境？

A: Python 3.13+ 遵循 PEP 668，系统 Python 被标记为"外部管理"，不允许直接安装包。虚拟环境是推荐的最佳实践。

### Q: 虚拟环境会占用多少空间？

A: 约 10-20 MB，包含 Python 解释器和依赖包。

### Q: 可以删除虚拟环境吗？

A: 可以。删除 `venv` 目录即可，不会影响系统。需要时重新运行 `python3 -m venv venv` 创建。

### Q: 忘记激活虚拟环境怎么办？

A: 会看到 `ModuleNotFoundError: No module named 'requests'` 错误。运行 `source venv/bin/activate` 激活即可。

### Q: 如何在虚拟环境中安装新包？

A:
```bash
source venv/bin/activate
pip install 包名
```

### Q: 多个项目可以共享虚拟环境吗？

A: 不推荐。每个项目应该有独立的虚拟环境，确保依赖隔离。

## 故障排除

### 问题：`python3 -m venv venv` 失败

**解决：**
```bash
# 确保安装了 python3-venv
brew install python@3.13

# 或使用系统 Python
/usr/bin/python3 -m venv venv
```

### 问题：激活虚拟环境后仍然找不到模块

**检查：**
```bash
# 确认使用的是虚拟环境的 Python
which python
# 应该显示: /Users/admin/linux.do/international-news/venv/bin/python

# 检查已安装的包
pip list
```

**解决：**
```bash
# 重新安装依赖
pip install -r requirements.txt
```

### 问题：权限错误

**解决：**
```bash
# 设置正确的权限
chmod +x run.sh
chmod -R u+w venv
```

## 清理和重置

### 完全重置环境

```bash
# 1. 停用虚拟环境（如果已激活）
deactivate

# 2. 删除虚拟环境
rm -rf venv

# 3. 删除生成的文件（可选）
rm -f *.txt *.json

# 4. 重新创建
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 生产环境部署

如果要在服务器上部署：

```bash
# 1. 克隆或上传项目
cd /path/to/international-news

# 2. 创建虚拟环境
python3 -m venv venv

# 3. 激活并安装
source venv/bin/activate
pip install -r requirements.txt

# 4. 测试
python get_news.py

# 5. 设置定时任务（可选）
crontab -e
# 添加：0 8 * * * cd /path/to/international-news && source venv/bin/activate && python get_news_with_websearch_final.py
```

## 参考资料

- [Python 虚拟环境官方文档](https://docs.python.org/3/library/venv.html)
- [PEP 668 - 外部管理环境](https://peps.python.org/pep-0668/)
- [Homebrew Python 说明](https://docs.brew.sh/Homebrew-and-Python)
