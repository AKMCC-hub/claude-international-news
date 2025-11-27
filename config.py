#!/usr/bin/env python3
"""
配置管理模块
支持从环境变量、.env 文件或默认值读取配置
"""

import os

def get_api_key():
    """
    获取 API Key，优先级：
    1. 环境变量 API_KEY
    2. .env 文件中的 API_KEY
    3. 硬编码的默认值
    """
    # 1. 首先尝试从环境变量获取
    api_key = os.environ.get('API_KEY')
    if api_key:
        return api_key

    # 2. 尝试从 .env 文件读取
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if key.strip() == 'API_KEY':
                        return value.strip()

    # 3. 如果没有找到，返回 None 或抛出错误
    raise ValueError("API_KEY not found. Please set it in environment variable or .env file")

def get_api_base_url():
    """获取 API Base URL"""
    # 从环境变量获取
    url = os.environ.get('API_BASE_URL')
    if url:
        return url

    # 从 .env 文件读取
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if key.strip() == 'API_BASE_URL':
                        return value.strip()

    # 默认值
    return "https://spai.aicoding.sh"

def get_default_model():
    """获取默认模型"""
    model = os.environ.get('DEFAULT_MODEL')
    if model:
        return model

    # 从 .env 文件读取
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if key.strip() == 'DEFAULT_MODEL':
                        return value.strip()

    # 默认值
    return "claude-sonnet-4-5-20250929"

# 导出配置
API_KEY = get_api_key()
API_BASE_URL = get_api_base_url()
DEFAULT_MODEL = get_default_model()
