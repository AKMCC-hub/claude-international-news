#!/usr/bin/env python3
"""
使用 /v1/messages 端点获取国际新闻
使用 Anthropic API 格式 (不包含 web_search 工具)
"""

import requests
import json
from datetime import datetime
from config import API_KEY, API_BASE_URL

def get_news_with_messages_api():
    """使用 /v1/messages 端点获取新闻"""

    url = f"{API_BASE_URL}/v1/messages"

    # 使用 Anthropic 风格的 headers
    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    # 不使用 tools 参数
    data = {
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": "请提供最新的5条重要国际新闻。每条新闻包括：1) 新闻标题 2) 简要内容（2-3句话）3) 涉及的国家或地区。请用中文回答，格式清晰。"
            }
        ]
    }

    try:
        print("=== 使用 /v1/messages 端点 (Anthropic 格式) ===")
        print(f"URL: {url}")
        print(f"Model: {data['model']}")
        print("-" * 80)

        response = requests.post(url, headers=headers, json=data, timeout=60)

        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()

            print("\n✅ 请求成功！")
            print(f"响应类型: {result.get('type', 'unknown')}")
            print(f"模型: {result.get('model', 'unknown')}")
            print(f"Role: {result.get('role', 'unknown')}")

            # 提取内容
            if "content" in result and isinstance(result["content"], list):
                text_content = ""
                for item in result["content"]:
                    if item.get("type") == "text":
                        text_content = item.get("text", "")
                        break

                if text_content:
                    print(f"\n📰 最新国际新闻 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    print(text_content)
                    print("\n" + "=" * 80)

                    # 保存到文件
                    filename = "international_news_messages_api.txt"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(f"国际新闻 (Messages API) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write("=" * 80 + "\n\n")
                        f.write(text_content)

                    print(f"\n✓ 已保存到 {filename}")

                    # 同时保存 JSON 响应
                    with open("messages_api_response.json", "w", encoding="utf-8") as f:
                        json.dump(result, f, indent=2, ensure_ascii=False)
                    print(f"✓ 完整响应已保存到 messages_api_response.json")

                    return True
                else:
                    print("❌ 未找到文本内容")
                    print(f"内容结构: {result.get('content', [])}")
                    return False
            else:
                print("❌ 响应格式不符合预期")
                print(f"完整响应: {json.dumps(result, indent=2, ensure_ascii=False)[:500]}")
                return False

        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"错误详情: {response.text}")
            return False

    except Exception as e:
        print(f"❌ 发生错误: {type(e).__name__}: {e}")
        return False

def get_news_with_openai_headers():
    """使用 /v1/messages 端点，但用 OpenAI 风格的 headers"""

    url = f"{API_BASE_URL}/v1/messages"

    # 使用 OpenAI 风格的 headers
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": "请提供最新的5条重要国际新闻。每条新闻包括：1) 标题 2) 简要内容 3) 涉及国家。用中文。"
            }
        ]
    }

    try:
        print("\n=== 使用 /v1/messages 端点 (OpenAI 风格 headers) ===")
        print(f"URL: {url}")
        print("-" * 80)

        response = requests.post(url, headers=headers, json=data, timeout=60)

        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("✅ OpenAI 风格也成功！")

            # 解析内容
            if "content" in result:
                for item in result["content"]:
                    if item.get("type") == "text":
                        text = item.get("text", "")
                        print(f"\n{text[:200]}...")
                        return True

        else:
            print(f"❌ OpenAI 风格失败: {response.text[:200]}")
            return False

    except Exception as e:
        print(f"❌ OpenAI 风格错误: {e}")
        return False

if __name__ == "__main__":
    print("=== Messages API 国际新闻获取工具 ===")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API: {API_BASE_URL}")
    print("=" * 80 + "\n")

    # 先用 Anthropic 格式
    success = get_news_with_messages_api()

    if success:
        print("\n测试 OpenAI 风格 headers...")
        get_news_with_openai_headers()

    print("\n=== 完成 ===")