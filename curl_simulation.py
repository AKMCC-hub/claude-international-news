#!/usr/bin/env python3
"""
模拟完整的 curl 命令行为
使用 requests 库模拟 curl 命令
"""

import subprocess
import json
from datetime import datetime
from config import API_KEY, API_BASE_URL

def run_curl_news():
    """模拟获取国际新闻的 curl 命令"""

    # 构建 curl 命令 (替换 API 地址)
    curl_command = [
        'curl',
        f'{API_BASE_URL}/v1/messages',
        '--header', f'x-api-key: {API_KEY}',
        '--header', 'anthropic-version: 2023-06-01',
        '--header', 'content-type: application/json',
        '--data', json.dumps({
            "model": "claude-sonnet-4-5-20250929",
            "max_tokens": 1024,
            "messages": [
                {
                    "role": "user",
                    "content": "请提供最新的5条重要国际新闻"
                }
            ],
            "tools": [{
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": 5
            }]
        }),
        '--connect-timeout', '30',
        '--max-time', '60'
    ]

    print("执行模拟 curl 命令...")
    print("命令: curl", " ".join([f"'{arg}'" if " " in arg else arg for arg in curl_command]))
    print("-" * 80)

    try:
        # 执行命令
        result = subprocess.run(
            curl_command,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )

        print(f"返回码: {result.returncode}")

        if result.returncode == 0:
            # 成功情况
            try:
                response_data = json.loads(result.stdout)
                print("响应数据:")
                print(json.dumps(response_data, indent=2, ensure_ascii=False)[:1000])

                # 保存结果
                with open("curl_response.json", "w", encoding="utf-8") as f:
                    f.write(json.dumps(response_data, indent=2, ensure_ascii=False))

                print("\n✓ 响应已保存到 curl_response.json")

            except json.JSONDecodeError:
                print("原始响应(非 JSON):")
                print(result.stdout)

        else:
            # 错误情况
            print(f"curl 错误输出: {result.stderr}")
            print(f"curl 标准输出: {result.stdout}")

        return result.returncode == 0

    except subprocess.TimeoutExpired:
        print("❌ curl 命令超时")
        return False
    except FileNotFoundError:
        print("❌ 没有找到 curl 命令")
        return False
    except Exception as e:
        print(f"❌ 执行 curl 失败: {e}")
        return False

def run_python_requests_curl():
    """用纯 Python 模拟 curl 行为"""

    import requests

    print("\n=== 用 Python 模拟 curl 行为 ===")

    url = f"{API_BASE_URL}/v1/messages"

    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
        "User-Agent": "curl/7.68.0",  # 模拟 curl User-Agent
        "Accept": "*/*"
    }

    data = {
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": "请提供最新的5条重要国际新闻"
            }
        ],
        "tools": [{
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 5
        }]
    }

    try:
        print(f"请求: {url}")
        print(f"Headers: {headers}")
        print(f"Data: {json.dumps(data, ensure_ascii=False)}")
        print("-" * 80)

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60,
            allow_redirects=True  # curl 默认跟随重定向
        )

        print(f"Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")

        # 保存详细响应
        print(f"\n=== 完整响应预览 ===")
        content_preview = response.text[:500] if len(response.text) > 500 else response.text
        print(f"Response Body: {content_preview}")

        # 保存到文件
        with open("curl_simulation_response.txt", "w", encoding="utf-8") as f:
            f.write(f"=== Curl 模拟请求 ===\n")
            f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"URL: {url}\n")
            f.write(f"Status: {response.status_code}\n\n")
            f.write("=== Headers ===\n")
            for k, v in dict(response.headers).items():
                f.write(f"{k}: {v}\n")
            f.write("\n=== Response Body ===\n")
            f.write(response.text)

        print(f"\n✓ 详细响应已保存到 curl_simulation_response.txt")

        return response.status_code == 200

    except Exception as e:
        print(f"Python 模拟 curl 失败: {e}")
        return False

if __name__ == "__main__":
    print("=== curl 命令模拟器 ===")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 80)

    # 先尝试 Python 版本的 curl 模拟
    success = run_python_requests_curl()

    if not success:
        print("\nPython 版本失败，尝试真实 curl 命令...")
        run_curl_news()

    print("\n=== 测试完成 ===")