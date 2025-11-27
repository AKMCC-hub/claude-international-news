#!/usr/bin/env python3
"""
国际新闻获取工具 - 最终版本
支持两种 API 端点：
1. /v1/chat/completions (OpenAI 格式)
2. /v1/messages (Anthropic 格式)
"""

import requests
import json
from datetime import datetime
import argparse
from config import API_KEY, API_BASE_URL

def get_news_chat_completions():
    """使用 /v1/chat/completions 端点 (OpenAI 格式)"""

    url = f"{API_BASE_URL}/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    data = {
        "model": "claude-3-5-haiku-20241022",
        "messages": [
            {
                "role": "system",
                "content": "你是一个国际新闻专家。"
            },
            {
                "role": "user",
                "content": "请基于你的知识库，提供5条重要的国际新闻事件。每条包括：标题、内容摘要、涉及国家。用中文回答。"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }

    try:
        print("=== 方式 1: /v1/chat/completions (OpenAI 格式) ===")
        print(f"URL: {url}")
        print("-" * 80)

        response = requests.post(url, headers=headers, json=data, timeout=30)

        if response.status_code == 200:
            result = response.json()

            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]

                print(f"\n📰 国际新闻\n")
                print(content)
                print("\n" + "=" * 80)

                save_to_file(content, "chat_completions")
                return True

        print(f"❌ 失败: {response.status_code} - {response.text[:200]}")
        return False

    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def get_news_messages():
    """使用 /v1/messages 端点 (Anthropic 格式)"""

    url = f"{API_BASE_URL}/v1/messages"

    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    data = {
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": "请基于你的知识库，提供5条重要的国际新闻事件。每条包括：标题、内容摘要、涉及国家。用中文回答。"
            }
        ]
    }

    try:
        print("=== 方式 2: /v1/messages (Anthropic 格式) ===")
        print(f"URL: {url}")
        print("-" * 80)

        response = requests.post(url, headers=headers, json=data, timeout=60)

        if response.status_code == 200:
            result = response.json()

            if "content" in result:
                text_content = ""
                for item in result["content"]:
                    if item.get("type") == "text":
                        text_content = item.get("text", "")
                        break

                if text_content:
                    print(f"\n📰 国际新闻\n")
                    print(text_content)
                    print("\n" + "=" * 80)

                    save_to_file(text_content, "messages")
                    return True

        print(f"❌ 失败: {response.status_code} - {response.text[:200]}")
        return False

    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def save_to_file(content, method):
    """保存新闻到文件"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    filename = f"news_{method}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"国际新闻 ({method}) - {timestamp}\n")
        f.write("=" * 80 + "\n\n")
        f.write(content)

    print(f"\n✓ 已保存到 {filename}")

def main():
    parser = argparse.ArgumentParser(description="国际新闻获取工具")
    parser.add_argument(
        "--method",
        choices=["chat", "messages", "both"],
        default="both",
        help="选择 API 调用方式: chat (OpenAI), messages (Anthropic), both (两种都试)"
    )

    args = parser.parse_args()

    print("=" * 80)
    print("国际新闻获取工具")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API: {API_BASE_URL}")
    print("=" * 80 + "\n")

    if args.method == "chat" or args.method == "both":
        success = get_news_chat_completions()
        if success and args.method == "chat":
            return

    if args.method == "messages" or args.method == "both":
        print("\n")
        get_news_messages()

    print("\n" + "=" * 80)
    print("完成")

if __name__ == "__main__":
    main()