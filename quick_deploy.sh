#!/bin/bash
# Quick deployment script for Docker

set -e

DOMAIN=${DOMAIN:-"localhost"}
PORT=${PORT:-"8000"}
USE_SSL=${USE_SSL:-"false"}

echo "=================================="
echo "cKey API Gateway - Quick Deploy"
echo "=================================="

# 1. Create directory
mkdir -p ckey-api

# 2. Copy files
if [ ! -f "docker-compose.prod.yml" ]; then
    echo "Error: docker-compose.prod.yml not found"
    exit 1
fi

cp docker-compose.prod.yml ckey-api/
cp .env.example ckey-api/.env
cp Dockerfile.prod ckey-api/Dockerfile

# 3. Build and start
cd ckey-api

if docker compose version &>/dev/null; then
    echo "Using docker compose..."
    docker compose -f docker-compose.prod.yml up -d --build
else
    echo "Using docker-compose..."
    docker-compose -f docker-compose.prod.yml up -d --build
fi

# 4. Wait for service to start
echo "Waiting for service to start..."
sleep 5

# 5. Check status
echo ""
echo "Checking service status..."
if curl -f "http://localhost:${PORT}/api/status" &>/dev/null; then
    echo "✅ Service is running!"
    echo ""
    echo "Access points:"
    echo "  - API: http://localhost:${PORT}"
    echo "  - Docs: http://localhost:${PORT}/docs"
    echo "  - Health: http://localhost:${PORT}/api/status"
else
    echo "⚠️  Service is starting, please wait a bit more"
fi

# 6. Show logs
echo ""
echo "Service logs (press Ctrl+C to exit):"
docker compose -f docker-compose.prod.yml logs -f

# Cleanup
echo "=================================="
echo "To stop: docker compose -f docker-compose.prod.yml down"
echo "=================================="