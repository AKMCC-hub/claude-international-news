#!/usr/bin/env python3
"""
获取最新的5条国际新闻
使用 Anthropic 风格的 API 调用
模拟您提供的 curl 命令格式
"""

import requests
import json
from datetime import datetime
from config import API_KEY, API_BASE_URL

def get_news_claude_style():
    """使用 Anthropic 风格的 API，支持 web search 工具"""

    url = f"{API_BASE_URL}/v1/messages"  # 使用 messages 端点

    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",  # 使用提供的版本
        "content-type": "application/json"
    }

    data = {
        "model": "claude-sonnet-4-5-20250929",  # 使用确认的可用模型
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": "请提供最新的5条重要国际新闻。请使用中文回答。"
            }
        ],
        "tools": [{
            "type": "web_search_20250305",  # 您提供的工具类型
            "name": "web_search",
            "max_uses": 5
        }]
    }

    try:
        print("使用 Claude 风格 API 获取新闻...")
        print("URL:", url)
        print("Headers:", {k:v for k,v in headers.items() if k != "x-api-key"})
        print("-" * 80)

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60
        )

        print(f"状态码: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")

        if response.status_code == 200:
            try:
                result = response.json()
                print("\n=== 原始响应 ===")
                print(json.dumps(result, indent=2, ensure_ascii=False)[:1000])

                # 尝试提取内容
                if "content" in result:
                    text_content = ""
                    for item in result["content"]:
                        if item.get("type") == "text":
                            text_content = item.get("text", "")
                            break

                    if text_content:
                        display_news(text_content)
                        save_news(text_content, "web_search")
                        return True

                print("找不到预期的内容结构")

            except json.JSONDecodeError:
                print("无法解析为 JSON")
                print("原始响应:")
                print(response.text[:500])

        else:
            print(f"请求失败: {response.status_code}")
            print(f"失败原因: {response.text[:500]}")

        return False

    except Exception as e:
        print(f"错误: {type(e).__name__}: {e}")
        return False

def display_news(content):
    """显示新闻内容"""
    print(f"\n📰 最新国际新闻 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    print(content)
    print("\n" + "-="*40)

def save_news(content, source="claude-style"):
    """保存新闻到文件"""
    filename = f"international_news_{source}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"国际新闻 ({source}) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        f.write(content)
    print(f"已保存到 {filename}")

def test_simple_request():
    """使用简单的消息格式"""
    url = f"{API_BASE_URL}/v1/messages"

    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    data = {
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 512,
        "messages": [
            {
                "role": "user",
                "content": "请给我3条最新的国际新闻标题"
            }
        ]
    }

    print("\n测试简单请求...")
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        print(f"简单请求状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            content_text = ""
            for item in result.get("content", []):
                if item.get("type") == "text":
                    content_text = item.get("text", "")
                    break

            if content_text:
                print(f"\n响应内容:\n{content_text}")
                save_news(content_text, "simple")
        else:
            print(f"简单请求失败: {response.text[:300]}")

    except Exception as e:
        print(f"简单请求错误: {e}")

if __name__ == "__main__":
    print("=== Claude 风格 API 国际新闻获取 ===")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API: {API_BASE_URL}")
    print("-" * 80)

    # 先用包含 web search 的方式
    success = get_news_claude_style()

    if not success:
        print("\n原始 web search 方式失败，尝试简单消息方式...")
        test_simple_request()

    print("\n=== 作完成 ===")