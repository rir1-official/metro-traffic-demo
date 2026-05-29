@echo off
docker run -d --name metro-demo-redis -p 6379:6379 redis
pause
