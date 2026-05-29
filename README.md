# Metro Traffic Realtime Demo

A Django and WebSocket demo for real-time metro passenger-flow monitoring. The
application simulates traffic updates, stores the latest status in Redis, and
pushes live updates to the browser through WebSocket.

## Features

- Django web page and API endpoint
- Redis-backed latest passenger-flow state
- WebSocket push updates with Django Channels
- Simple browser dashboard for simulated metro station flow

## Tech Stack

- Python
- Django
- Django Channels
- Redis
- HTML, CSS, and JavaScript

## Project Structure

```text
manage.py
metro_demo/       # Django project settings and routing
demo/             # Demo app, views, consumers, and URLs
templates/        # Browser dashboard
static/           # Static assets
requirements.txt
```

## Run Locally

Start Redis first:

```powershell
docker run -d --name metro-demo-redis -p 6379:6379 redis
```

Install and run the Django app:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Environment

Optional environment variables:

```text
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

## Compliance Notes

This repository contains only source code and minimal configuration needed to run
the demo. Local databases, virtual environments, generated caches, and course
documents are intentionally excluded.
