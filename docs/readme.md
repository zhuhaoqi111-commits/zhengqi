# 项目文档

## 项目概述

这是一个政企项目，采用Django框架开发。

## 目录结构说明

```
├── app/                    # 应用代码
│   ├── models/            # 数据模型
│   ├── views/             # 视图处理
│   ├── controllers/       # 控制器
│   ├── services/          # 业务逻辑服务
│   ├── utils/             # 工具函数
│   └── config/            # 配置管理
├── migrations/            # 数据库迁移文件
├── tests/                 # 测试代码
│   ├── unit/              # 单元测试
│   ├── integration/       # 集成测试
│   ├── e2e/               # 端到端测试
│   └── fixtures/          # 测试数据
├── static/                # 静态文件
│   ├── css/               # 样式文件
│   ├── js/                # JavaScript文件
│   ├── images/            # 图片资源
│   └── fonts/             # 字体文件
├── templates/             # 模板文件
│   ├── base/              # 基础模板
│   ├── components/        # 组件模板
│   ├── pages/             # 页面模板
│   └── layouts/           # 布局模板
├── docs/                  # 项目文档
├── requirements/          # 依赖管理
│   ├── base.txt           # 基础依赖
│   ├── dev.txt            # 开发环境依赖
│   └── prod.txt           # 生产环境依赖
├── tools/                 # 工具脚本
│   ├── setup.py           # 项目设置脚本
│   └── deploy.py          # 部署脚本
├── envs/                  # 环境配置
│   └── .env.example       # 环境变量示例
└── README.md              # 项目说明
```

## 快速开始

### 1. 环境设置

```bash
# 复制环境配置
cp envs/.env.example .env

# 编辑.env文件，配置您的设置
```

### 2. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements/dev.txt
```

### 3. 数据库设置

```bash
# 运行迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

### 4. 运行开发服务器

```bash
python manage.py runserver
```

## 开发指南

### 代码规范

- 使用Black进行代码格式化
- 使用Flake8进行代码检查
- 使用isort进行导入排序

### 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/unit/

# 生成测试覆盖率报告
pytest --cov=app
```

### 部署

```bash
# 使用部署脚本
python tools/deploy.py
```