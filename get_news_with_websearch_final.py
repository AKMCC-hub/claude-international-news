#!/usr/bin/env python3
"""
使用 web_search 工具获取最新国际新闻
支持 Brotli 解压缩
"""

import requests
import json
from datetime import datetime

# 导入配置模块
try:
    from config import API_KEY, API_BASE_URL, DEFAULT_MODEL
except ImportError:
    # 如果配置模块不存在，从环境变量获取
    import os
    API_KEY = os.environ.get('API_KEY')
    if not API_KEY:
        raise ValueError("API_KEY not found. Please set it in environment variable or .env file")
    API_BASE_URL = os.environ.get('API_BASE_URL', "https://spai.aicoding.sh")
    DEFAULT_MODEL = os.environ.get('DEFAULT_MODEL', "claude-sonnet-4-5-20250929")

def get_news_with_web_search(query="最新国际新闻"):
    """使用 web_search 工具获取新闻"""

    url = f"{API_BASE_URL}/v1/messages"

    # 模拟浏览器请求头
    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/json",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "gzip, deflate, br"  # 告诉服务器支持 brotli
    }

    data = {
        "model": DEFAULT_MODEL,
        "max_tokens": 2048,
        "messages": [
            {
                "role": "user",
                "content": f"请搜索并提供{query}，包括：1) 新闻标题 2) 简要内容 3) 来源。用中文回答。"
            }
        ],
        "tools": [{
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 5
        }]
    }

    try:
        print("=" * 80)
        print(f"使用 Web Search 工具获取: {query}")
        print("=" * 80)

        # 确保 requests 自动处理解压
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=90  # 增加超时时间，因为需要搜索网络
        )

        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            print("✅ 请求成功")

            # 尝试获取 JSON 内容
            try:
                # 如果响应是 brotli 压缩的，requests 会自动解压
                result = response.json()

                print(f"\n响应类型: {result.get('type', 'unknown')}")
                print(f"模型: {result.get('model', 'unknown')}")

                # 解析内容
                if "content" in result:
                    has_web_search = False
                    text_content = []
                    search_results = []

                    for item in result["content"]:
                        item_type = item.get("type", "")

                        if item_type == "server_tool_use" or item_type == "tool_use":
                            # Web search 被调用
                            has_web_search = True
                            print(f"\n🔍 检测到 Web Search 调用")
                            print(f"   查询: {item.get('input', {}).get('query', 'N/A')}")

                        elif item_type == "web_search_tool_result":
                            # Web search 结果
                            print(f"\n📊 收到搜索结果")
                            content = item.get("content", [])
                            for result_item in content:
                                if result_item.get("type") == "web_search_result":
                                    title = result_item.get("title", "")
                                    url_link = result_item.get("url", "")
                                    search_results.append({
                                        "title": title,
                                        "url": url_link
                                    })
                                    print(f"   - {title}")
                                    print(f"     {url_link}")

                        elif item_type == "text":
                            # AI 生成的文本内容
                            text_content.append(item.get("text", ""))

                    # 显示 AI 的总结
                    if text_content:
                        full_text = "\n".join(text_content)
                        print(f"\n📰 AI 总结:\n")
                        print(full_text)
                        print("\n" + "=" * 80)

                        # 保存结果
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"news_websearch_{timestamp}.txt"

                        with open(filename, "w", encoding="utf-8") as f:
                            f.write(f"国际新闻 (Web Search) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                            f.write("=" * 80 + "\n\n")

                            if search_results:
                                f.write("搜索结果来源:\n")
                                for i, sr in enumerate(search_results, 1):
                                    f.write(f"{i}. {sr['title']}\n")
                                    f.write(f"   {sr['url']}\n\n")
                                f.write("=" * 80 + "\n\n")

                            f.write(full_text)

                        print(f"\n✓ 已保存到 {filename}")

                        # 同时保存 JSON
                        json_file = f"news_websearch_{timestamp}.json"
                        with open(json_file, "w", encoding="utf-8") as f:
                            json.dump(result, f, indent=2, ensure_ascii=False)
                        print(f"✓ 完整响应已保存到 {json_file}")

                        return True
                    else:
                        print("⚠️  没有找到文本内容")

                        # 保存原始响应用于调试
                        with open("debug_response.json", "w", encoding="utf-8") as f:
                            json.dump(result, f, indent=2, ensure_ascii=False)
                        print("调试信息已保存到 debug_response.json")

                else:
                    print("❌ 响应中没有 content 字段")

            except json.JSONDecodeError as e:
                print(f"❌ JSON 解析失败: {e}")

                # 检查是否需要手动解压 brotli
                try:
                    import brotli
                    decompressed = brotli.decompress(response.content)
                    result = json.loads(decompressed)
                    print("✓ 使用 brotli 手动解压成功")

                    # 处理解压后的结果（重复上面的逻辑）
                    with open("brotli_decompressed.json", "w", encoding="utf-8") as f:
                        json.dump(result, f, indent=2, ensure_ascii=False)
                    print("解压后的内容已保存到 brotli_decompressed.json")

                except ImportError:
                    print("⚠️  需要安装 brotli: pip install brotli")
                except Exception as e2:
                    print(f"❌ Brotli 解压失败: {e2}")

        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"错误: {response.text[:500]}")

        return False

    except Exception as e:
        print(f"❌ 发生错误: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("国际新闻获取工具 - 使用 Web Search")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80 + "\n")

    # 获取最新的国际新闻
    get_news_with_web_search("最新5条重要国际新闻")

    print("\n" + "=" * 80)
    print("完成")
    print("=" * 80)