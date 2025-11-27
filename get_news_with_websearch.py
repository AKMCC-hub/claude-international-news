#!/usr/bin/env python3
"""
使用 web_search 工具获取国际新闻
模拟浏览器请求头以避免 Cloudflare 阻断
"""

import requests
import json
from datetime import datetime
from config import API_KEY, API_BASE_URL

def get_news_with_web_search():
    """使用 web_search 工具"""

    url = f"{API_BASE_URL}/v1/messages"

    # 模拟浏览器的完整请求头
    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Origin": "https://spai.aicoding.sh",
        "Referer": "https://spai.aicoding.sh/",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin"
    }

    data = {
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": "What's the weather in NYC?"  # 先测试原始示例
            }
        ],
        "tools": [{
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 5
        }]
    }

    try:
        print("=== 使用 web_search 工具 (带浏览器请求头) ===")
        print(f"URL: {url}")
        print(f"Model: {data['model']}")
        print("-" * 80)

        response = requests.post(url, headers=headers, json=data, timeout=60)

        print(f"状态码: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")

        if response.status_code == 200:
            print("\n✅ 成功！web_search 工具可用！")

            # 检查响应内容
            print(f"Response Content-Type: {response.headers.get('Content-Type')}")
            print(f"Response Encoding: {response.encoding}")
            print(f"Response Content Length: {len(response.content)}")

            # 先保存原始响应
            with open("web_search_raw_response.txt", "wb") as f:
                f.write(response.content)

            print(f"✓ 原始响应已保存到 web_search_raw_response.txt")

            # 尝试解析 JSON
            try:
                result = response.json()
                print(f"\n完整响应预览:")
                print(json.dumps(result, indent=2, ensure_ascii=False)[:1000])

                # 保存 JSON 响应
                with open("web_search_response.json", "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)

                print(f"✓ JSON 响应已保存到 web_search_response.json")

                # 提取内容
                if "content" in result:
                    for item in result["content"]:
                        if item.get("type") == "text":
                            print(f"\n文本内容:\n{item.get('text', '')}")
                            return True

            except json.JSONDecodeError as e:
                print(f"⚠️  JSON 解析失败: {e}")
                print(f"响应文本前500字符: {response.text[:500]}")

            return True

        else:
            print(f"\n❌ 失败: {response.status_code}")
            print(f"错误详情: {response.text}")

            # 尝试不带 web_search 工具
            print("\n尝试不带 web_search 工具...")
            return try_without_tools(headers)

    except Exception as e:
        print(f"❌ 错误: {type(e).__name__}: {e}")
        return False

def try_without_tools(headers):
    """不使用工具参数"""

    url = f"{API_BASE_URL}/v1/messages"

    data = {
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": "请提供5条国际新闻标题"
            }
        ]
        # 不包含 tools 参数
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)

        if response.status_code == 200:
            result = response.json()
            print("\n✅ 不带工具成功")

            if "content" in result:
                for item in result["content"]:
                    if item.get("type") == "text":
                        print(f"\n{item.get('text', '')[:300]}...")
                        return True

        return False

    except Exception as e:
        print(f"不带工具也失败: {e}")
        return False

def test_different_tool_types():
    """测试不同的工具类型"""

    url = f"{API_BASE_URL}/v1/messages"

    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }

    # 不同的工具类型
    tool_types = [
        {
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 5
        },
        {
            "type": "web_search",
            "name": "web_search"
        },
        {
            "name": "web_search",
            "description": "Search the web for information"
        }
    ]

    print("\n=== 测试不同的工具类型 ===\n")

    for i, tool in enumerate(tool_types, 1):
        print(f"测试 {i}: {tool}")

        data = {
            "model": "claude-sonnet-4-5-20250929",
            "max_tokens": 512,
            "messages": [{"role": "user", "content": "Hello"}],
            "tools": [tool]
        }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            print(f"  状态码: {response.status_code}")

            if response.status_code == 200:
                print(f"  ✅ 工具类型 {i} 成功!")
                return True
            else:
                error_msg = response.text[:100] if len(response.text) > 100 else response.text
                print(f"  ❌ 失败: {error_msg}")

        except Exception as e:
            print(f"  ❌ 错误: {e}")

        print()

    return False

if __name__ == "__main__":
    print("=" * 80)
    print("Web Search 工具测试")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80 + "\n")

    # 先测试带 web_search
    success = get_news_with_web_search()

    if not success:
        print("\n" + "=" * 80)
        print("测试不同的工具类型...")
        print("=" * 80)
        test_different_tool_types()

    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)