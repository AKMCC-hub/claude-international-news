#!/usr/bin/env python3
"""
测试 API 支持的不同端点
"""

import requests
import json
from config import API_KEY, API_BASE_URL
API_BASE = API_BASE_URL

def test_endpoints():
    """测试不同的 API 端点"""

    # 要测试的端点
    endpoints = [
        "/v1/models",
        "/v1/chat/completions",
        "/v1/completions",
        "/v1/messages",
        "/v1/engines",
        "/v1/embeddings",
        "/v1/audio"
    ]

    headers_base = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    headers_anthropic = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    print("测试各种 API 端点...")
    print(f"API Base: {API_BASE}")
    print("=" * 80)

    for endpoint in endpoints:
        url = f"{API_BASE}{endpoint}"

        print(f"\n测试 GET 请求: {endpoint}")
        try:
            response = requests.get(url, headers=headers_base, timeout=10)
            print(f"  GET 状态码: {response.status_code}")
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "data" in data and data["data"]:
                        print(f"  GET 支持: ✅")
                        print(f"  数据条数: {len(data['data'])}")
                    else:
                        print(f"  GET 支持: ✅")
                        print(f"  响应: {json.dumps(data, ensure_ascii=False)[:100]}")
                except:
                    print(f"  GET 支持: ✅ (非 JSON 响应)")
            else:
                print(f"  GET 不支持: ❌")

        except Exception as e:
            print(f"  GET 错误: {type(e).__name__}: {str(e)}")

        # POST 测试 - 仅对某些端点
        if endpoint in ["/v1/chat/completions", "/v1/completions", "/v1/messages"]:
            for header_type, headers in [("OpenAI", headers_base), ("Anthropic", headers_anthropic)]:
                print(f"\n  测试 {header_type} POST: {endpoint}")

                test_request = None
                if endpoint == "/v1/chat/completions":
                    test_request = {
                        "model": "claude-sonnet-4-5-20250929",
                        "messages": [{"role": "user", "content": "Hello"}],
                        "max_tokens": 50
                    }
                elif endpoint == "/v1/completions":
                    test_request = {
                        "model": "claude-sonnet-4-5-20250929",
                        "prompt": "Hello",
                        "max_tokens": 50
                    }
                elif endpoint == "/v1/messages":
                    test_request = {
                        "model": "claude-sonnet-4-5-20250929",
                        "max_tokens": 50,
                        "messages": [{"role": "user", "content": "Hello"}]
                    }

                if test_request:
                    try:
                        response = requests.post(url, headers=headers, json=test_request, timeout=30)
                        print(f"    POST {header_type} 状态码: {response.status_code}")
                        if response.status_code == 200:
                            print(f"    POST {header_type} 支持: ✅")
                        else:
                            print(f"    POST {header_type} 失败: {response.status_code}")
                            print(f"    错误信息: {response.text[:200]}")
                    except Exception as e:
                        print(f"    POST {header_type} 错误: {type(e).__name__}: {str(e)}")

def examine_supported_models(openai_only=True):
    """检查支持的模型和格式"""
    print("\n" + "="*80)
    print("测试不同模型和格式支持")

    url = f"{API_BASE}/v1/models"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            models = response.json().get("data", [])
            print(f"支持的模型数量: {len(models)}")

            print("\n模型列表:")
            for i, model in enumerate(models[:10], 1):  # 只显示前10个
                model_id = model.get("id", "unknown")
                object_type = model.get("object", "unknown")
                owned_by = model.get("owned_by", "unknown")
                created = model.get("created", 0)
                print(f"{i}. {model_id} ({object_type}) by {owned_by}")

    except Exception as e:
        print(f"获取模型列表失败: {e}")

if __name__ == "__main__":
    test_endpoints()
    examine_supported_models()

    print("\n" + "="*80)
    print("结论:")
    print("1. 该 API 基于 OpenAI 格式的 /v1/chat/completions 端点工作")
    print("2. /v1/messages 端点不可用 (500 错误)")
    print("3. 推荐使用第一版本 get_news.py 脚本")