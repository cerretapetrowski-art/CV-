#!/bin/bash

echo "========================================"
echo "  智能图像识别工具 - 本地启动脚本"
echo "========================================"
echo ""

echo "正在安装依赖..."
pip install -r requirements.txt

echo ""
echo "正在启动服务..."
echo "访问地址: http://localhost:8000"
echo "按 Ctrl+C 停止服务"
echo ""

uvicorn app:app --host 0.0.0.0 --port 8000 --reload
