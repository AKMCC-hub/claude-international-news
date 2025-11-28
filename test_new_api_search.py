import anthropic
import json
import uuid
import os
from datetime import datetime

def test_new_api_search():
    """测试新API地址的联网搜索功能"""

    # 生成唯一的追踪ID，方便在日志中查找
    trace_id = f"TRACE-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8].upper()}"
    print(f"=== 测试新API地址联网搜索 ===")
    print(f"🔍 追踪ID: {trace_id}")
    print(f"请在日志中搜索此ID: {trace_id}\n")

    # 使用自定义API端点的Anthropic客户端，修复base_url配置
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("请设置环境变量 ANTHROPIC_API_KEY")

    client = anthropic.Anthropic(
        api_key=api_key,
        base_url="https://spai.aicoding.sh",  # 不包含/v1，SDK会自动添加
        default_headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            # "Accept-Encoding": "gzip, deflate, br",  # 移除压缩编码，避免SDK无法正确处理gzip响应
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "X-Trace-ID": trace_id,  # 自定义追踪ID，方便在日志中查找
            "X-Test-Type": "API-SEARCH-TEST"  # 测试类型标识
        }
    )

    # 测试1: 基础对话（无搜索）
    print("\n1. 测试基础对话...")
    try:
        response1 = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=100,
            temperature=0.1,
            messages=[
                {"role": "user", "content": f"[{trace_id}] 你好，请简单回答"}
            ]
        )
        print("[OK] 基础对话成功!")
        if response1.content:
            for content in response1.content:
                if hasattr(content, 'text'):
                    print(f"回复: {content.text[:100]}...")
    except Exception as e:
        print(f"[ERROR] 基础对话异常: {e}")

    # 测试2: 联网搜索香港火灾新闻（强制使用工具）
    print("\n2. 测试联网搜索香港火灾新闻（强制使用web_search工具）...")
    try:
        response2 = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            temperature=0.1,
            messages=[
                {"role": "user", "content": f"[{trace_id}] 搜索香港火灾2025年11月的最新消息"}
            ],
            tools=[{
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": 3  # 增加使用次数
            }],
            tool_choice={"type": "tool", "name": "web_search"}  # 强制必须使用web_search工具
        )
        print("[OK] 联网搜索请求成功!")

        # 分析响应
        tool_calls = []
        server_tool_calls = []
        tool_results = []
        text_responses = []
        if response2.content:
            for content in response2.content:
                if hasattr(content, 'type'):
                    if content.type == 'tool_use':
                        tool_calls.append(content)
                    elif content.type == 'server_tool_use':
                        server_tool_calls.append(content)
                    elif content.type == 'web_search_tool_result':
                        tool_results.append(content)
                    elif content.type == 'text':
                        text_responses.append(content)

        print(f"客户端工具调用数量: {len(tool_calls)}")
        print(f"服务器端工具调用数量: {len(server_tool_calls)}")
        print(f"搜索结果数量: {len(tool_results)}")
        print(f"文本响应数量: {len(text_responses)}")

        # 详细输出完整响应结构
        print(f"\n完整响应内容块数量: {len(response2.content) if response2.content else 0}")

        # 显示服务器端工具调用（web_search 是服务器端工具）
        if server_tool_calls:
            print("\n✅ 服务器端工具调用详情:")
            for i, tool in enumerate(server_tool_calls, 1):
                print(f"  {i}. 工具类型: server_tool_use")
                if hasattr(tool, 'name'):
                    print(f"     工具名: {tool.name}")
                if hasattr(tool, 'id'):
                    print(f"     工具ID: {tool.id}")
                if hasattr(tool, 'input'):
                    print(f"     工具输入: {json.dumps(tool.input, ensure_ascii=False, indent=6)}")
                # 尝试获取所有属性
                print(f"     完整对象: {tool}")

        # 显示搜索结果
        if tool_results:
            print("\n🔍 Web搜索结果:")
            for i, result in enumerate(tool_results, 1):
                print(f"  {i}. 结果类型: {result.type}")
                if hasattr(result, 'search_results'):
                    print(f"     搜索结果数: {len(result.search_results)}")
                    for idx, sr in enumerate(result.search_results[:3], 1):  # 只显示前3个
                        print(f"       - 结果{idx}: {sr if isinstance(sr, str) else json.dumps(sr, ensure_ascii=False)[:100]}")
                # 显示完整对象
                result_str = str(result)[:500]
                print(f"     结果摘要: {result_str}...")

        if tool_calls:
            print("\n✅ 客户端工具调用详情:")
            for i, tool in enumerate(tool_calls, 1):
                print(f"  {i}. 工具名: {tool.name}")
                print(f"     工具ID: {tool.id if hasattr(tool, 'id') else 'N/A'}")
                print(f"     工具输入: {json.dumps(tool.input if hasattr(tool, 'input') else {}, ensure_ascii=False, indent=6)}")

        if not tool_calls and not server_tool_calls:
            print("\n⚠️  没有检测到任何工具调用！")
            print("     这不应该发生，因为我们使用了 tool_choice 强制调用")

        if text_responses:
            print("\nAI文本回复:")
            for i, text in enumerate(text_responses, 1):
                print(f"  {i}. {text.text[:300]}...")

    except Exception as e:
        print(f"[ERROR] 联网搜索异常: {e}")
        import traceback
        traceback.print_exc()

    # 测试3: 简单的联网搜索（测试工具是否可用）
    print("\n3. 测试简单搜索查询...")
    try:
        response3 = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            temperature=0.1,
            messages=[
                {"role": "user", "content": f"[{trace_id}] 今天的天气"}
            ],
            tools=[{
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": 1
            }],
            tool_choice={"type": "tool", "name": "web_search"}
        )
        print("[OK] 简单搜索请求成功!")

        # 检查响应
        has_tool_use = any(hasattr(c, 'type') and c.type == 'tool_use' for c in response3.content) if response3.content else False
        print(f"包含工具调用: {has_tool_use}")

        if response3.content:
            for idx, block in enumerate(response3.content):
                print(f"  内容块 {idx}: {block.type if hasattr(block, 'type') else 'unknown'}")
                if hasattr(block, 'type') and block.type == 'tool_use':
                    print(f"    ✅ 工具: {block.name}, 输入: {block.input if hasattr(block, 'input') else {}}")
    except Exception as e:
        print(f"[ERROR] 简单搜索异常: {e}")
        import traceback
        traceback.print_exc()

    # 测试4: 检查API可达性 (保留requests用于简单的健康检查)
    print("\n4. 测试API可达性...")
    try:
        import requests
        health_response = requests.get("https://spai.aicoding.sh/", timeout=5)
        print(f"基础URL状态码: {health_response.status_code}")

        v1_response = requests.get("https://spai.aicoding.sh/v1/", timeout=5)
        print(f"v1端点状态码: {v1_response.status_code}")
    except Exception as e:
        print(f"[ERROR] API可达性测试失败: {e}")

if __name__ == "__main__":
    test_new_api_search()