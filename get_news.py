#!/usr/bin/env python3
"""
获取最新的5条国际新闻
使用 OpenAI 兼容的 API
"""

import requests
import json
from datetime import datetime
import time
from config import API_KEY, API_BASE_URL

def try_models(models_to_try=None):
    """尝试不同的模型获取新闻"""
    if models_to_try is None:
        # 使用该 API 支持的 Claude 模型
        models_to_try = [
            "claude-3-5-haiku-20241022",
            "claude-sonnet-4-5-20250929",
            "claude-sonnet-4-20250514"
        ]

    for model in models_to_try:
        print(f"\n尝试使用模型: {model}")
        success = get_international_news(model)
        if success:
            return True
        time.sleep(1)  # 等待1秒后再尝试下一个模型

    return False

def get_international_news(model="claude-3-5-haiku-20241022"):
    """使用 OpenAI API 获取最新的国际新闻"""

    url = f"{API_BASE_URL}/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # 构建请求数据
    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "你是一个国际新闻专家，专门提供准确、简洁的国际新闻摘要。"
            },
            {
                "role": "user",
                "content": "请提供最新的5条重要国际新闻。每条新闻应包括：1) 新闻标题 2) 简要内容（2-3句话描述）3) 涉及的主要国家或地区。请用中文回答，格式清晰。"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }

    try:
        print("正在获取国际新闻...")
        print("-" * 80)

        response = requests.post(url, headers=headers, json=data, timeout=30)

        # 打印响应状态码
        print(f"响应状态码: {response.status_code}")

        # 如果响应不是 200，打印详细信息
        if response.status_code != 200:
            print(f"响应内容: {response.text}")
            return False

        response.raise_for_status()

        result = response.json()

        # 提取回复内容
        if "choices" in result and len(result["choices"]) > 0:
            news_content = result["choices"][0]["message"]["content"]

            print(f"\n📰 最新国际新闻 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            print(news_content)
            print("\n" + "-" * 80)

            # 保存到文件
            with open("international_news.txt", "w", encoding="utf-8") as f:
                f.write(f"最新国际新闻 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                f.write(news_content)

            print("\n✓ 新闻已保存到 international_news.txt")
            return True

        else:
            print("❌ 无法获取新闻内容")
            print(f"完整响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ 解析响应失败: {e}")
        print(f"响应文本: {response.text if 'response' in locals() else 'N/A'}")
        return False
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        return False

if __name__ == "__main__":
    # 尝试使用不同的模型
    success = try_models()

    if not success:
        print("\n❌ 所有模型都失败了，请检查:")
        print("  1. API 密钥是否正确")
        print("  2. API 服务是否可用")
        print("  3. 网络连接是否正常")
