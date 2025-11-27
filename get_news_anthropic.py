#!/usr/bin/env python3
"""
获取最新的5条国际新闻
使用 Anthropic API 格式 (messages endpoint)
支持 web_search 工具
"""

import requests
import json
from datetime import datetime
from config import API_KEY, API_BASE_URL

def get_international_news_anthropic():
    """使用 Anthropic API 格式获取国际新闻"""

    url = f"{API_BASE_URL}/v1/messages"

    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    # 构建请求数据 - 使用 Anthropic 格式
    data = {
        "model": "claude-sonnet-4-5-20250929",  # 使用 API 支持的模型
        "max_tokens": 2048,
        "messages": [
            {
                "role": "user",
                "content": "请提供最新的5条重要国际新闻。每条新闻包括：1) 标题 2) 简要内容 3) 涉及国家/地区。请用中文回答。"
            }
        ],
        "tools": [{
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 5
        }]
    }

    try:
        print("正在使用 Anthropic API 格式获取国际新闻...")
        print("-" * 80)

        response = requests.post(url, headers=headers, json=data, timeout=60)

        # 打印响应状态码和头信息
        print(f"响应状态码: {response.status_code}")
        print(f"响应头: content-type={response.headers.get('content-type', 'N/A')}")

        if response.status_code == 200:
            result = response.json()

            print(f"\n完整响应结构预览:")
            print(json.dumps(result, indent=2, ensure_ascii=False)[:500] + "...")

            # 解析响应内容
            if "content" in result:
                # Anthropic 格式的响应结构
                content_text = ""
                for item in result["content"]:
                    if item.get("type") == "text":
                        content_text = item.get("text", "")
                        break
                    elif item.get("type") == "tool_use":
                        print(f"检测到工具调用: {item.get('name')}")
                        if "input" in item:
                            print(f"工具输入: {item['input']}")

                if content_text:
                    print(f"\n📰 最新国际新闻 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    print(content_text)
                    print("\n" + "-" * 80)

                    # 保存到文件
                    with open("international_news_anthropic.txt", "w", encoding="utf-8") as f:
                        f.write(f"国际新闻 (Anthropic API) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write("=" * 80 + "\n\n")
                        f.write(content_text)

                    print("\n✓ 新闻已保存到 international_news_anthropic.txt")
                    return True
                else:
                    print("❌ 无法提取文本内容")
                    return False
            else:
                print("❌ 响应中没有找到 'content' 字段")
                return False

        else:
            print(f"❌ 请求失败")
            print(f"错误信息: {response.text}")

            # 尝试解析错误详情
            try:
                error_data = response.json()
                if "error" in error_data:
                    print(f"错误类型: {error_data['error'].get('type', 'unknown')}")
                    print(f"错误描述: {error_data['error'].get('message', 'unknown')}")
            except:
                pass
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

def get_weather_test():
    """测试用天气查询"""

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
                "content": "What's the weather in NYC?"
            }
        ],
        "tools": [{
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 5
        }]
    }

    try:
        print("测试天气查询...")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        print(f"天气查询状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("天气查询响应:")
            print(json.dumps(result, indent=2, ensure_ascii=False)[:300] + "...")
            return True
        else:
            print(f"天气查询失败: {response.text}")
            return False

    except Exception as e:
        print(f"天气测试失败: {e}")
        return False

if __name__ == "__main__":
    print("=== Anthropic API 国际新闻获取工具 ===\n")

    # 先尝试获取新闻
    success = get_international_news_anthropic()

    if not success:
        print("新闻获取失败，尝试天气测试...")
        get_weather_test()

    print("\n=== 操作完成 ===")
    print("如需查看模型列表，请运行: python3 list_models.py")