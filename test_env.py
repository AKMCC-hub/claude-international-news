#!/usr/bin/env python3
"""
环境测试脚本
检查所有依赖是否正确安装
"""

import sys

def test_environment():
    """测试环境配置"""

    print("=" * 60)
    print("环境测试")
    print("=" * 60)

    # 检查 Python 版本
    print(f"\n✓ Python 版本: {sys.version}")
    print(f"✓ Python 路径: {sys.executable}")

    # 检查依赖包
    print("\n检查依赖包...")

    try:
        import requests
        print(f"✓ requests {requests.__version__} 已安装")
    except ImportError as e:
        print(f"✗ requests 未安装: {e}")
        return False

    try:
        import brotli
        print(f"✓ brotli 已安装")
    except ImportError as e:
        print(f"✗ brotli 未安装: {e}")
        return False

    # 测试 API 连接
    print("\n测试 API 连接...")

    try:
        # 从 config 导入 API 配置
        try:
            from config import API_KEY, API_BASE_URL
        except ImportError:
            print("⚠ 无法导入 config 模块，跳过 API 测试")
            return True

        url = f"{API_BASE_URL}/v1/models"
        headers = {"Authorization": f"Bearer {API_KEY}"}

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            models = response.json().get("data", [])
            print(f"✓ API 连接成功")
            print(f"✓ 可用模型数量: {len(models)}")
        else:
            print(f"✗ API 连接失败: {response.status_code}")
            return False

    except Exception as e:
        print(f"✗ API 测试失败: {e}")
        return False

    print("\n" + "=" * 60)
    print("✓ 所有测试通过！环境配置正确。")
    print("=" * 60)

    print("\n快速开始：")
    print("  ./run.sh                          # 使用启动脚本")
    print("  source venv/bin/activate          # 激活虚拟环境")
    print("  python get_news.py                # 运行脚本")

    return True

if __name__ == "__main__":
    success = test_environment()
    sys.exit(0 if success else 1)
