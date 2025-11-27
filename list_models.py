#!/usr/bin/env python3
"""
列出 API 支持的所有模型
"""

import requests
import json
from config import API_KEY, API_BASE_URL

def list_models():
    """获取可用的模型列表"""

    url = f"{API_BASE_URL}/v1/models"

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    try:
        print("正在获取可用模型列表...")
        print("-" * 80)

        response = requests.get(url, headers=headers, timeout=30)

        print(f"响应状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()

            if "data" in result:
                models = result["data"]
                print(f"\n找到 {len(models)} 个可用模型:\n")

                for i, model in enumerate(models, 1):
                    model_id = model.get("id", "N/A")
                    print(f"{i}. {model_id}")

                # 保存到文件
                with open("available_models.json", "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)

                print(f"\n✓ 完整模型信息已保存到 available_models.json")
            else:
                print("响应中没有找到模型数据")
                print(f"完整响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"请求失败，响应内容: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ 解析响应失败: {e}")
    except Exception as e:
        print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    list_models()
