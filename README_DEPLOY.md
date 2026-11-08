# Deployment Guide - cKey API Gateway Service

Deploy your cKey API Gateway service on production servers.

## Table of Contents

- [Quick Deployment (Docker)](#quick-deployment-docker)
- [VPS Deployment (Linux)](#vps-deployment-linux)
- [Windows Server Deployment](#windows-server-deployment)
- [Production Checklist](#production-checklist)
- [Troubleshooting](#troubleshooting)

---

## Quick Deployment (Docker)

### Run with Docker Compose

```bash
# Copy files to server
scp -r . username@server:/opt/ckey-api/

# SSH to server
ssh username@server

# Navigate to directory
cd /opt/ckey-api

# Set up environment
cp .env.example .env
nano .env  # Edit configuration if needed

# Build and start
docker-compose -f docker-compose.prod.yml up -d --build

# Check logs
docker-compose -f docker-compose.prod.yml logs -f

# Test
curl http://your-server-ip:8000/api/status
curl -X POST http://your-server-ip:8000/api/license/generate \
  -H "Content-Type: application/json" \
  -d '{"product":"PC","name":"Test"}'
```

### Access the API

- Main API: `http://your-server:8000`
- Swagger Docs: `http://your-server:8000/docs`
- Health Check: `http://your-server:8000/api/status`

---

## VPS Deployment (Linux)

### Option 1: Using deployment script (Recommended)

```bash
# On your local machine
scp deploy.sh username@your-vps:/tmp/

# SSH to VPS
ssh username@your-vps

# Make executable and run
chmod +x /tmp/deploy.sh
sudo /tmp/deploy.sh
```

The script will:
- Install all dependencies (Python, Docker, Nginx, Certbot)
- Set up automated SSL certificates
- Configure firewall rules
- Create auto-restart service
- Enable SSL renewal daily cron job

### Option 2: Manual Deployment

#### 1. Update System
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

#### 2. Install Dependencies
```bash
sudo apt-get install -y python3.11 python3-pip python3-venv \
    nginx curl gcc fail2ban certbot
```

#### 3. Create User and Directory
```bash
sudo useradd -m -s /bin/bash ckey
sudo mkdir -p /opt/ckey-api
sudo mkdir -p /opt/ckey-api/logs
sudo mkdir -p /opt/ckey-api/backups
sudo chown -R ckey:ckey /opt/ckey-api
```

#### 4. Install Python Dependencies
```bash
cd /opt/ckey-api
sudo -u ckey python3 -m venv .venv
sudo -u ckey .venv/bin/pip install --upgrade pip
sudo -u ckey .venv/bin/pip install -r requirements.txt
```

#### 5. Copy Application Files
```bash
# Copy these files from local machine:
# - ckey_api.py
# - ckey_service.py
# - requirements.txt
# - .env (or .env.example)

docker-compose -f docker-compose.prod.yml up -d --build
```

#### 6. Configure Nginx
```bash
# Stop default Nginx site
sudo rm /etc/nginx/sites-enabled/default

# Configure new site
sudo nano /etc/nginx/sites-available/ckey-api
```

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/ckey-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 7. SSL Certificate (Let's Encrypt)
```bash
sudo certbot certonly --nginx -d api.yourdomain.com --email your@email.com --agree-tos --non-interactive
```

#### 8. Database (Optional)
```bash
# Install PostgreSQL
sudo apt-get install -y postgresql postgresql-contrib

# Create database
sudo -u postgres psql -c "CREATE DATABASE ckey_api;"
sudo -u postgres psql -c "CREATE USER ckey_user WITH PASSWORD 'your_password';"
printf '\nc1SECRET;UPDATE\n' | sudo -u postgres psql ckey_api
```

#### 9. Start Service
```bash
sudo systemctl enable ckey-api
sudo systemctl start ckey-api
sudo systemctl status ckey-api
```

---

## Windows Server Deployment

### 1. Install Dependencies
```powershell
# Install Python
winget install Python.Python.3.11

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Nginx (using nginx-windows)
1. Download nginx from http://nginx.org/en/download.html
2. Extract to `C:\nginx\`
3. Configure `conf\nginx.conf`:
```nginx
events {
    worker_connections 1024;
}

http {
    server {
        listen 80;
        server_name api.yourdomain.com;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### 3. Run as Windows Service

```cmd
# Add GiRAPI
sc create ckey-api type= own binPath= "C:\Python311\python.exe C:\ckey-api\ckey_api.py"
sc config ckey-api start= auto
sc start ckey-api
```

### 4. SSL Certificate
```cmd
# Download Win32OpenSSL
https://slproweb.com/products/Win32OpenSSL.html

# Run certbot manually with OpenSSL
```

### 5. Launch
```cmd
# Create scheduled task
schtasks /Create /TN "cKey API Service" /TR "C:\Python311\python.exe C:\ckey-api\ckey_api.py" /SC STARTUP
```

---

## Production Checklist

### Basic Setup
- [ ] Install dependencies (Python 3.11+, pip)
- [ ] Create dedicated user for service
- [ ] Configure firewall (ports 80, 443, 8000)
- [ ] Set up environment variables (.env file)

### Security Hardening
- [ ] Enable SSL certificate (Let's Encrypt)
- [ ] Configure Nginx reverse proxy
- [ ] Enable fail2ban
- [ ] Set up rate limiting
- [ ] Configure security headers
- [ ] Regular SSL certificate renewal
- [ ] Backup configuration

### Monitoring
- [ ] Configure logging (systemd journal or file)
- [ ] Set up file rotation (logrotate)
- [ ] Enable monitoring (Prometheus/Grafana optional)
- [ ] Set up alerts (Sentry/PagerDuty)
- [ ] Keep-alive configuration
- [ ] Timeout settings

### Performance
- [ ] Set appropriate worker count
- [ ] Configure resource limits
- [ ] Enable caching
- [ ] Database optimization (if used)
- [ ] CDN for static files (optional)

### Maintenance
- [ ] Automated backups
- [ ] Update strategy
- [ ] Rollback plan
- [ ] Documentation ready
- [ ] Troubleshooting guide

---

## Troubleshooting

### Service won't start
```bash
# Check logs
journalctl -u ckey-api -n 50 --no-pager
docker-compose -f docker-compose.prod.yml logs

# Test Python dependencies
python -c "import fastapi; print('OK')"

# Check permissions
ls -la /opt/ckey-api/
```

### Nginx connection refused
```bash
# Check if Python service running
curl http://localhost:8000/api/status

# If not, start it
sudo systemctl start ckey-api

# Check Nginx config
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### SSL certificate issues
```bash
# Renew certificate manually
sudo certbot renew --dry-run

# Check certificate details
sudo certbot certificates

# Force renewal
sudo certbot renew --force-renewal
```

### High memory usage
```bash
# Reduce Docker workers
# Add to Dockerfile.env:
# API_LIMITS_MEM=128M

# Or rebuild Docker image
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build --no-cache
```

### Database connection failed
```bash
# Test connection
telnet localhost 5432

# Check PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-15-main.log

# Verify credentials in .env
```

### Rate limiting too aggressive
```bash
# Edit nginx.conf
# Modify rate limits in:
# limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
```

---

## Performance Tuning

### Docker Performance
```bash
# Add to docker-compose.prod.yml:
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 512M
```

### System Performance
```bash
# Edit sysctl.conf
cat >> /etc/sysctl.conf <<EOF
vm.swappiness=1
net.core.somaxconn=65535
net.ipv4.tcp_max_tw_buckets=100000
EOF

sysctl -p
```

### Database Performance
```sql
-- Connection pool settings
CREATE SCHEMA IF NOT EXISTS ckey;

-- Add appropriate indexes for your queries
```

---

## Complete Deployment Workflow

```bash
# 1. Build locally
docker-compose -f docker-compose.prod.yml build

# 2. Test locally
docker-compose -f docker-compose.prod.yml up
curl http://localhost:8000/api/status

# 3. Push images to registry (if using Docker registry)

# 4. Deploy to server
scp -Dockerfile.prod -docker-compose.prod.yml -system.service username@server:/opt/ckey-api/
ssh username@server

# 5. Deploy on server
systemctl restart ckey-api
sudo systemctl enable ckey-api

# 6. Configure Nginx
sudo nano /etc/nginx/sites-enabled/ckey-api
sudo systemctl restart nginx

# 7. Get SSL
sudo certbot certonly --nginx -d api.yourdomain.com

# 8. Monitoring
journalctl -u ckey-api -f
```

---

## Resources

- **Docker Hub**: https://hub.docker.com/
- **Python GIRA**: https://docs.python.org/3.11/
- **FastAPI**: https://fastapi.tiangolo.com/
- **Nginx**: https://nginx.org/en/docs/
- **Certbot**: https://certbot.eff.org/

---

Next steps: test thoroughly, deploy to staging first, then production!
