#!/bin/bash
# Деплой cKey API Gateway на VPS
# Запускается от имени root

set -e

# Конфигурация
DOMAIN="yourdomain.com"
EMAIL="your@email.com"
APP_USER="ckey"
APP_DIR="/opt/ckey-api"
SERVICE_NAME="ckey-api.service"

echo "=================================="
echo "cKey API Gateway - Деплой на VPS"
echo "=================================="

# 1. Обновление системы
echo "📦 Обновление системы..."
apt-get update
apt-get upgrade -y

# 2. Установка зависимостей
echo "🔧 Установка зависимостей..."
apt-get install -y \
    python3.11 \
    python3-pip \
    python3-venv \
    nginx \
    gcc \
    curl \
    fail2ban \
    certbot \
    certbot-python \
    logrotate

# 3. Создание пользователя
if ! id "$APP_USER" &>/dev/null; then
    echo "👤 Создание пользователя $APP_USER..."
    useradd -m -s /bin/bash $APP_USER
fi

# 4. Установка Docker (опционально)
echo "🐳 Установка Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
usermod -aG docker $APP_USER
rm get-docker.sh

# 5. Создание директории приложения
echo "📁 Создание директории приложения..."
mkdir -p $APP_DIR
mkdir -p $APP_DIR/logs
mkdir -p $APP_DIR/backups
chown -R $APP_USER:$APP_USER $APP_DIR

# 6. Клонирование/копирование приложения
if [ -f "docker-compose.prod.yml" ]; then
    echo "📋 Копирование Docker файлов..."
    cp docker-compose.prod.yml $APP_DIR/
    cp Dockerfile.prod $APP_DIR/
    cp nginx.conf $APP_DIR/
    cp system.service $APP_DIR/
fi

# 7. Виртуальное окружение Python
echo "🐍 Установка Python зависимостей..."
cd $APP_DIR
sudo -u $APP_USER python3 -m venv .venv
sudo -u $APP_USER .venv/bin/pip install --upgrade pip
sudo -u $APP_USER .venv/bin/pip install -r requirements.txt

# 8. Systemd service
echo "⚙️  Запись Systemd сервиса..."
cp $APP_DIR/system.service /etc/systemd/system/$SERVICE_NAME
systemctl daemon-reload

# 9. Firewall
echo "🔴 Настройка Firewall..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# 10. Nginx configuration
echo "🚀 Настройка Nginx..."
cat > /etc/nginx/sites-available/$SERVICE_NAME <<EOF
server {
    listen 80;
    server_name $DOMAIN;
    
    location / {
        return 301 https://\$server_name\$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name $DOMAIN;
    
    ssl_certificate /etc/letsencrypt/live/\$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/\$DOMAIN/privkey.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
    
    location /healthy {
        access_log off;
        proxy_pass http://localhost:8000/health;
    }
}
EOF

ln -sf /etc/nginx/sites-available/$SERVICE_NAME /etc/nginx/sites-enabled/
php -pctl conf
nginx -t
systemctl enable nginx
systemctl restart nginx

# 11. Certbot SSL
echo "🔒 Получение SSL сертификата..."
if [ ! -f "/etc/letsencrypt/live/\$DOMAIN/fullchain.pem" ]; then
    certbot certonly --nginx -d $DOMAIN --email $EMAIL --agree-tos --non-interactive
fi

# 12. Установка Docker Compose (если не установлен)
if ! command -v docker-compose &> /dev/null; then
    echo "📥 Доставка Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# 13. Fail2ban
echo "🛡️  Настройка Fail2ban..."
cat > /etc/fail2ban/jail.local <<EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 10
action = iptables-multiport[name=nginx, port="http,https", protocol=tcp]
EOF

systemctl restart fail2ban
systemctl enable fail2ban

# 14. Cron для daily SSL renewal
echo "🔄 Добавление cron для SSL renewal..."
echo "0 0,12 * * * certbot renew --quiet --post-hook 'systemctl reload nginx'" | crontab -

# 15. Backups
echo "💾 Создание бэкап crons..."
echo "0 2 * * * tar -czf $APP_DIR/backups/backup-\$(date +\%Y\%m\%d).tar.gz $APP_DIR --exclude=logs --exclude=backups" | crontab -
echo "30 2 * * * find $APP_DIR/backups/ -name 'backup-*.tar.gz' -mtime +30 -delete" | crontab -

echo "=================================="
echo "✅ Деплой завершен!"
echo "=================================="
echo ""
echo "URL: https://$DOMAIN"
echo "API Docs: https://$DOMAIN/docs"
echo ""
echo "Доступные команды:"
echo "  docker-compose -f $APP_DIR/docker-compose.prod.yml up -d"
echo "  systemctl start ckey-api"
echo "  systemctl status ckey-api"
echo "  journalctl -u ckey-api -f"
echo ""
echo "Отредактируйте конфигурацию"
echo "  DOMAIN='$DOMAIN'"
echo "  EMAIL='$EMAIL'"
echo "  APP_USER='$APP_USER'"
echo "  APP_DIR='$APP_DIR'"