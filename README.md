# Metro Traffic Realtime Demo / 地铁客流实时监测演示

## English

A Django and WebSocket demo for real-time metro passenger-flow monitoring. The
application simulates traffic updates, stores the latest status in Redis, and
pushes live updates to the browser through WebSocket.

### Features

- Django web page and API endpoint
- Redis-backed latest passenger-flow state
- WebSocket push updates with Django Channels
- Browser dashboard for simulated metro station flow

### Tech Stack

- Python
- Django
- Django Channels
- Redis
- HTML, CSS, and JavaScript

### Run Locally

Start Redis:

```powershell
docker run -d --name metro-demo-redis -p 6379:6379 redis
```

Install dependencies and run Django:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

### Environment

```text
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

### Compliance

This repository contains source code and minimal configuration only. Local
databases, virtual environments, generated caches, and course documents are
excluded.

---

## 中文

这是一个基于 Django、Redis 和 WebSocket 的地铁客流实时监测演示项目。
项目会模拟客流状态更新，将最新状态写入 Redis，并通过 WebSocket 实时推送到
浏览器页面。

### 功能

- Django 页面和接口
- 使用 Redis 缓存最新客流状态
- 使用 Django Channels 实现 WebSocket 实时推送
- 前端页面展示模拟地铁站客流变化

### 技术栈

- Python
- Django
- Django Channels
- Redis
- HTML / CSS / JavaScript

### 本地运行

先启动 Redis：

```powershell
docker run -d --name metro-demo-redis -p 6379:6379 redis
```

安装依赖并启动 Django：

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

打开 `http://127.0.0.1:8000/`。

### 环境变量

```text
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

### 合规说明

仓库只包含运行演示所需的源代码和最小配置。已排除本地数据库、虚拟环境、
生成缓存和课程文档。
