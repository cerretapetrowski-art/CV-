# 智能图像识别工具

基于 Vision Transformer (ViT) 模型的图像识别工具，支持识别 1000+ 类别物品。

## 功能特性

-  图片上传识别
-  Top 5 识别结果展示
-  个人识别历史记录
-  响应式设计，支持移动端

## 快速部署到 Railway

1. Fork 或上传本仓库到你的 GitHub

2. 访问 [Railway.app](https://railway.app)，使用 GitHub 登录

3. 点击 "New Project" → "Deploy from GitHub repo"

4. 选择你的仓库

5. Railway 会自动部署，耐心等待首次模型下载（约 1-2 分钟）

6. 部署完成后获取公网访问链接

## 本地运行

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

或使用启动脚本：

```bash
chmod +x start.sh
./start.sh
```

## 技术栈

- **后端**: FastAPI + Python
- **模型**: Hugging Face Transformers (google/vit-base-patch16-224)
- **前端**: 原生 HTML + CSS + JavaScript

## 隐私说明

- 每个人独立的识别记录通过浏览器 LocalStorage 存储的 UUID 实现
- 服务器仅存储识别结果，不存储原始上传图片
- 无需登录，匿名使用
