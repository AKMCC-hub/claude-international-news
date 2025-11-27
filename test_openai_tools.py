#!/usr/bin/env python3
"""
测试 OpenAI 格式是否支持工具（包括 web_search）
"""

import requests
import json
from datetime import datetime
from config import API_KEY, API_BASE_URL

def test_openai_with_tools():
    """测试 OpenAI 格式 + tools 参数"""

    url = f"{API_BASE_URL}/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # 测试1：OpenAI 格式的 function calling
    data = {
        "model": "claude-3-5-haiku-20241022",
        "messages": [
            {
                "role": "user",
                "content": "What's the weather in NYC?"
            }
        ],
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "web_search",
                    "description": "Search the web for information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query"
                            }
                        },
                        "required": ["query"]
                    }
                }
            }
        ]
    }

    try:
        print("=" * 80)
        print("测试 1: OpenAI 格式 + function calling tools")
        print("=" * 80)

        response = requests.post(url, headers=headers, json=data, timeout=60)
        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("\n✅ 请求成功")
            print(f"\n响应预览:")
            print(json.dumps(result, indent=2, ensure_ascii=False)[:1000])

            # 保存完整响应
            with open("openai_tools_test1.json", "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print("\n✓ 完整响应保存到 openai_tools_test1.json")

        else:
            print(f"\n❌ 失败: {response.status_code}")
            print(f"错误: {response.text}")

    except Exception as e:
        print(f"❌ 错误: {e}")

def test_openai_with_source_prompt():
    """测试通过 prompt 让 AI 返回来源"""

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
                "content": "你是一个新闻助手。在回答时，请明确标注每条新闻的来源，包括来源网站、发布时间等信息。如果无法确定来源，请说明这是基于你的知识库。"
            },
            {
                "role": "user",
                "content": "请提供3条最新的国际新闻，每条必须包含：1) 标题 2) 内容 3) 来源（包括网站名称和链接，如果有的话）"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1500
    }

    try:
        print("\n" + "=" * 80)
        print("测试 2: OpenAI 格式 + 提示词要求来源")
        print("=" * 80)

        response = requests.post(url, headers=headers, json=data, timeout=30)
        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("\n✅ 请求成功")

            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                print(f"\n📰 回复内容:\n")
                print(content)

                # 保存
                with open("openai_source_prompt.txt", "w", encoding="utf-8") as f:
                    f.write(f"OpenAI 格式 + 来源提示词 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 80 + "\n\n")
                    f.write(content)

                print("\n✓ 保存到 openai_source_prompt.txt")

        else:
            print(f"\n❌ 失败: {response.status_code}")
            print(f"错误: {response.text}")

    except Exception as e:
        print(f"❌ 错误: {e}")

def test_openai_anthropic_style_tools():
    """测试 OpenAI 格式 + Anthropic 风格的 tools"""

    url = f"{API_BASE_URL}/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    data = {
        "model": "claude-3-5-haiku-20241022",
        "messages": [
            {
                "role": "user",
                "content": "Search for latest news about Ukraine"
            }
        ],
        "tools": [
            {
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": 3
            }
        ]
    }

    try:
        print("\n" + "=" * 80)
        print("测试 3: OpenAI 格式 + Anthropic 风格 web_search 工具")
        print("=" * 80)

        response = requests.post(url, headers=headers, json=data, timeout=60)
        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("\n✅ 请求成功！OpenAI 格式支持 web_search！")
            print(f"\n响应预览:")
            print(json.dumps(result, indent=2, ensure_ascii=False)[:1000])

            # 保存
            with open("openai_websearch_test.json", "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print("\n✓ 完整响应保存到 openai_websearch_test.json")

        else:
            print(f"\n❌ 失败: {response.status_code}")
            print(f"错误: {response.text[:500]}")

    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == "__main__":
    print("=" * 80)
    print("OpenAI 格式工具支持测试")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    # 测试1：OpenAI function calling
    test_openai_with_tools()

    # 测试2：通过提示词
    test_openai_with_source_prompt()

    # 测试3：OpenAI + Anthropic 工具
    test_openai_anthropic_style_tools()

    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)
