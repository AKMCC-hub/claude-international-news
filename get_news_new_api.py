#!/usr/bin/env python3
"""
获取最新的5条国际新闻
使用新的 API 端点和 Anthropic 格式
支持 web_search 工具
"""

import requests
import json
from datetime import datetime
import os

# API 配置 - 根据提供的 curl 命令修改
API_BASE_URL = "https://api.anthropic.com"  # 这是 Anthropic 的主 API
API_KEY = os.environ.get('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY not found. Please set it in environment variable or .env file")

def get_international_news_new():
    """使用新 API 获取国际新闻"""

    url = f"{API_BASE_URL}/v1/messages"

    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    data = {
        "model": "claude-sonnet-4-5-20250929",  # 使用可用的模型
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": "请提供最新的5条重要国际新闻。每条新闻包括：1) 标题 2) 简要内容 3) 涉及国家/地区。用中文回答。"
            }
        ],
        "tools": [{
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 5
        }]
    }

    try:
        print("正在获国际新闻...")
        print("URL:", url)
        print("-" * 80)

        response = requests.post(url, headers=headers, json=data, timeout=60)
        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"响应成功!")

            # 解析响应
            if "content" in result:
                news_content = ""
                for item in result["content"]:
                    if item.get("type") == "text":
                        news_content = item.get("text", "")
                        break

                if news_content:
                    print(f"\n📰 新闻内容:\n")
                    print(news_content)
                    print("\n" + "=" * 80)

                    # 保存到文件
                    with open("international_news_new_api.txt", "w", encoding="utf-8") as f:
                        f.write(f"国际新闻 (新 API) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write("=" * 80 + "\n\n")
                        f.write(news_content)

                    print("\n✓ 保存到 international_news_new_api.txt")
                    return True

        else:
            print(f"❌ 错误详情: {response.text}")
            return False

    except Exception as e:
        print(f"❌ 异: {e}")
        return False

if __name__ == "__main__":
    print("=== 新 API 国际新闻获取工具 ===\n")
    get_international_news_new()