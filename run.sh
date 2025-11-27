#!/bin/bash
# 国际新闻获取工具启动脚本

# 切换到脚本所在目录
cd "$(dirname "$0")"

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "虚拟环境不存在，正在创建..."
    python3 -m venv venv

    echo "正在安装依赖..."
    source venv/bin/activate
    pip install -r requirements.txt
    echo "✓ 环境设置完成"
else
    source venv/bin/activate
fi

# 显示帮助信息
show_help() {
    echo "=================================="
    echo "   国际新闻获取工具"
    echo "=================================="
    echo ""
    echo "用法："
    echo "  ./run.sh [选项] [--api-key KEY] [--api-url URL]"
    echo ""
    echo "功能选项："
    echo "  1, --websearch       获取实时新闻（Web Search + 真实来源）⭐ 推荐"
    echo "  2, --openai-sources  快速获取新闻（OpenAI 格式 + 来源标注）"
    echo "  3, --openai          快速获取新闻（OpenAI 格式 - 基础版）"
    echo "  4, --anthropic       快速获取新闻（Anthropic 格式）"
    echo "  5, --compare         快速获取新闻（两种格式对比）"
    echo "  6, --list-models     查看可用模型"
    echo "  7, --test-api        测试 API 端点"
    echo "  8, --test-env        测试环境"
    echo "  -h, --help           显示此帮助信息"
    echo ""
    echo "配置选项："
    echo "  --api-key KEY        设置 API Key"
    echo "  --api-url URL        设置 API Base URL（默认：https://spai.aicoding.sh）"
    echo "  --model MODEL        设置默认模型"
    echo ""
    echo "配置优先级："
    echo "  1. 命令行参数（--api-key）"
    echo "  2. 环境变量（export API_KEY=xxx）"
    echo "  3. .env 配置文件"
    echo "  4. 脚本默认值"
    echo ""
    echo "示例："
    echo "  ./run.sh --websearch --api-key sk-xxx"
    echo "  API_KEY=sk-xxx ./run.sh 1"
    echo "  ./run.sh --api-key sk-xxx --api-url https://api.example.com 1"
    echo ""
    echo "无参数时进入交互式菜单模式"
    echo ""
}

# 执行对应的功能
run_function() {
    local choice=$1
    case $choice in
        1|--websearch)
            echo ""
            echo "正在使用 Web Search 获取实时新闻（带真实来源链接）..."
            echo "注意：需要较长时间（60-90秒）"
            python get_news_with_websearch_final.py
            ;;
        2|--openai-sources)
            echo ""
            echo "使用 OpenAI 格式获取新闻（AI 会标注来源）..."
            python get_news_openai_with_sources.py
            ;;
        3|--openai)
            echo ""
            echo "使用 OpenAI 格式获取新闻（基础版）..."
            python get_news.py
            ;;
        4|--anthropic)
            echo ""
            echo "使用 Anthropic 格式获取新闻..."
            python get_news_final.py --method messages
            ;;
        5|--compare)
            echo ""
            echo "使用两种格式对比获取新闻..."
            python get_news_final.py --method both
            ;;
        6|--list-models)
            echo ""
            python list_models.py
            ;;
        7|--test-api)
            echo ""
            python api_endpoint_test.py
            ;;
        8|--test-env)
            echo ""
            python test_env.py
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "无效的选项: $choice"
            echo "使用 --help 查看帮助信息"
            exit 1
            ;;
    esac
}

# 解析命令行参数
COMMAND=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --api-key)
            export API_KEY="$2"
            shift 2
            ;;
        --api-url)
            export API_BASE_URL="$2"
            shift 2
            ;;
        --model)
            export DEFAULT_MODEL="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            # 保存功能命令
            COMMAND="$1"
            shift
            ;;
    esac
done

# 如果有功能命令，直接执行
if [ ! -z "$COMMAND" ]; then
    run_function "$COMMAND"
    exit 0
fi

# 否则显示交互式菜单
echo "=================================="
echo "   国际新闻获取工具"
echo "=================================="
echo ""
echo "请选择运行方式："
echo ""
echo "1. 获取实时新闻（Web Search + 真实来源）⭐ 推荐"
echo "2. 快速获取新闻（OpenAI 格式 + 来源标注）"
echo "3. 快速获取新闻（OpenAI 格式 - 基础版）"
echo "4. 快速获取新闻（Anthropic 格式）"
echo "5. 快速获取新闻（两种格式对比）"
echo "6. 查看可用模型"
echo "7. 测试 API 端点"
echo "8. 测试环境"
echo "0. 退出"
echo ""
read -p "请输入选项 [0-8]: " choice

case $choice in
    0)
        echo "退出"
        exit 0
        ;;
    *)
        run_function "$choice"
        ;;
esac

echo ""
echo "按回车键退出..."
read
