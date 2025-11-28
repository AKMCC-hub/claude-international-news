#!/usr/bin/env python3
"""
使用 Anthropic SDK 测试 API 调用
用于对比测试是否会被 Cloudflare 拦截
"""

import anthropic
from config import API_KEY, API_BASE_URL
import sys

def test_anthropic_sdk():
    """使用 Anthropic SDK 进行测试"""

    print("=" * 80)
    print("使用 Anthropic SDK 测试 API 调用")
    print("=" * 80)
    print(f"\nAPI Base URL: {API_BASE_URL}")
    print(f"API Key: {API_KEY[:10]}...{API_KEY[-4:]}")
    print()

    try:
        # 创建 Anthropic 客户端
        print("正在创建 Anthropic 客户端...")
        client = anthropic.Anthropic(
            api_key=API_KEY,
            base_url=API_BASE_URL
        )
        print("✅ 客户端创建成功")

        # 测试简单的消息请求
        print("\n正在发送测试消息...")
        print("-" * 80)

        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello! Please respond with a simple greeting."
                }
            ]
        )

        print("✅ 请求成功!")
        print("\n响应信息:")
        print(f"  Model: {message.model}")
        print(f"  Role: {message.role}")
        print(f"  Stop Reason: {message.stop_reason}")
        print(f"\n内容:")
        print("-" * 80)
        for content_block in message.content:
            if hasattr(content_block, 'text'):
                print(content_block.text)
        print("-" * 80)

        return True

    except anthropic.APIConnectionError as e:
        print(f"\n❌ API 连接错误:")
        print(f"   错误类型: APIConnectionError")
        print(f"   错误信息: {e}")
        print(f"\n可能原因:")
        print("   - 被 Cloudflare 拦截")
        print("   - 网络连接问题")
        print("   - API Base URL 不正确")
        return False

    except anthropic.APIStatusError as e:
        print(f"\n❌ API 状态错误:")
        print(f"   HTTP 状态码: {e.status_code}")
        print(f"   错误信息: {e.message}")
        print(f"   响应: {e.response}")
        return False

    except anthropic.AuthenticationError as e:
        print(f"\n❌ 认证错误:")
        print(f"   错误信息: {e}")
        print(f"\n可能原因:")
        print("   - API Key 不正确")
        print("   - API Key 已过期")
        return False

    except Exception as e:
        print(f"\n❌ 未知错误:")
        print(f"   错误类型: {type(e).__name__}")
        print(f"   错误信息: {e}")
        return False

def test_with_streaming():
    """测试流式响应"""

    print("\n" + "=" * 80)
    print("测试流式响应")
    print("=" * 80)

    try:
        client = anthropic.Anthropic(
            api_key=API_KEY,
            base_url=API_BASE_URL
        )

        print("\n正在发送流式请求...")
        print("-" * 80)

        with client.messages.stream(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Count from 1 to 5, with a brief comment for each number."
                }
            ]
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)

        print("\n" + "-" * 80)
        print("✅ 流式请求成功!")
        return True

    except Exception as e:
        print(f"\n❌ 流式请求失败:")
        print(f"   错误类型: {type(e).__name__}")
        print(f"   错误信息: {e}")
        return False

def compare_with_requests():
    """对比使用 requests 库的请求"""
    import requests

    print("\n" + "=" * 80)
    print("对比测试: 使用 requests 库直接请求")
    print("=" * 80)

    url = f"{API_BASE_URL}/v1/messages"
    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    payload = {
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": "Hello! Please respond with a simple greeting."
            }
        ]
    }

    try:
        print(f"\n正在发送请求到: {url}")
        print(f"Headers: {headers}")
        response = requests.post(url, headers=headers, json=payload, timeout=30)

        print(f"\n响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")

        if response.status_code == 200:
            print("✅ requests 请求成功!")
            data = response.json()
            print(f"\n响应内容 (前 200 字符):")
            print(str(data)[:200])
        else:
            print(f"❌ requests 请求失败")
            print(f"响应内容: {response.text[:500]}")

        return response.status_code == 200

    except Exception as e:
        print(f"\n❌ requests 请求错误:")
        print(f"   错误类型: {type(e).__name__}")
        print(f"   错误信息: {e}")
        return False

def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("Anthropic SDK vs Cloudflare 拦截测试")
    print("=" * 80)
    print("\n这个脚本将测试:")
    print("1. 使用 Anthropic 官方 SDK 的标准请求")
    print("2. 使用 Anthropic SDK 的流式请求")
    print("3. 使用 requests 库的直接 HTTP 请求")
    print("\n通过对比这三种方式,我们可以判断:")
    print("- 是否被 Cloudflare 拦截")
    print("- 哪种请求方式更可靠")
    print("- 不同请求方式的 User-Agent 和 Headers 差异")

    input("\n按回车键开始测试...")

    # 测试 1: 标准请求
    result1 = test_anthropic_sdk()

    # 测试 2: 流式请求
    result2 = test_with_streaming()

    # 测试 3: requests 对比
    result3 = compare_with_requests()

    # 总结
    print("\n" + "=" * 80)
    print("测试总结")
    print("=" * 80)
    print(f"1. Anthropic SDK 标准请求: {'✅ 成功' if result1 else '❌ 失败'}")
    print(f"2. Anthropic SDK 流式请求: {'✅ 成功' if result2 else '❌ 失败'}")
    print(f"3. requests 库直接请求:    {'✅ 成功' if result3 else '❌ 失败'}")

    print("\n结论:")
    if result1 and result2 and result3:
        print("✅ 所有测试都通过,API 工作正常,没有被 Cloudflare 拦截")
    elif result1 or result2:
        print("⚠️  Anthropic SDK 可以工作,但 requests 可能被拦截")
        print("   建议: 使用 Anthropic SDK 而不是直接 HTTP 请求")
    elif result3:
        print("⚠️  requests 可以工作,但 Anthropic SDK 失败")
        print("   可能原因: SDK 版本问题或 API 端点不兼容")
    else:
        print("❌ 所有测试都失败,可能被 Cloudflare 拦截或 API 配置错误")
        print("   请检查:")
        print("   1. API Base URL 是否正确")
        print("   2. API Key 是否有效")
        print("   3. 是否被 Cloudflare 或防火墙拦截")

    return 0 if (result1 or result2 or result3) else 1

if __name__ == "__main__":
    sys.exit(main())
