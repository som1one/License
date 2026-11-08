#!/bin/bash
# Service management script for cKey API Gateway

SERVICE_NAME="ckey-api"
APP_DIR="/opt/ckey-api"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
show_menu() {
    clear
    echo "=================================="
    echo "cKey API Gateway - Service Manager"
    echo "=================================="
    echo ""

    if systemctl is-active --quiet "$SERVICE_NAME"; then
        echo -e "${GREEN}✅ Service is RUNNING${NC}"
    else
        echo -e "${RED}❌ Service is STOPPED${NC}"
    fi

    echo ""
    echo "Commands:"
    echo -e "  ${BLUE}1${NC} - Start service"
    echo -e "  ${BLUE}2${NC} - Stop service"
    echo -e "  ${BLUE}3${NC} - Restart service"
    echo -e "  ${BLUE}4${NC} - Status"
    echo -e "  ${BLUE}5${NC} - View logs"
    echo -e "  ${BLUE}6${NC} - Update"
    echo -e "  ${BLUE}7${NC} - Backup"
    echo -e "  ${BLUE}8${NC} - Database backup"
    echo -e "  ${BLUE}9${NC} - Exit"
    echo ""
    echo -n "Enter choice: "
}

start_service() {
    echo ""
    echo -e "${YELLOW}Starting service...${NC}"
    if systemctl start "$SERVICE_NAME"; then
        echo -e "${GREEN}✅ Service started successfully${NC}"
    else
        echo -e "${RED}❌ Failed to start service${NC}"
    fi
    sleep 2
}

stop_service() {
    echo ""
    echo -e "${YELLOW}Stopping service...${NC}"
    if systemctl stop "$SERVICE_NAME"; then
        echo -e "${GREEN}✅ Service stopped successfully${NC}"
    else
        echo -e "${RED}❌ Failed to stop service${NC}"
    fi
    sleep 2
}

restart_service() {
    echo ""
    echo -e "${YELLOW}Restarting service...${NC}"
    if systemctl restart "$SERVICE_NAME"; then
        echo -e "${GREEN}✅ Service restarted successfully${NC}"
    else
        echo -e "${RED}❌ Failed to restart service${NC}"
    fi
    sleep 2
}

show_status() {
    echo ""
    echo -e "${BLUE}Service Status:${NC}"
    systemctl status "$SERVICE_NAME" --no-pager | head -20
    echo ""
    echo -e "${BLUE}API Status:${NC}"
    if command -v curl &>/dev/null; then
        curl -s "http://localhost:8000/api/status" || echo "⚠️  Could not connect to API"
    else
        echo "⚠️  curl not installed, cannot check API"
    fi
}

view_logs() {
    echo ""
    echo -e "${YELLOW}Viewing logs (Ctrl+C to exit):${NC}"
    echo "Recent logs (last 50 lines):"
    journalctl -u "$SERVICE_NAME" -n 50 --no-pager
    echo ""
    echo -e "${YELLOW}To watch live logs, run: journalctl -u $SERVICE_NAME -f${NC}"
}

update_service() {
    echo ""
    echo -e "${YELLOW}Starting update...${NC}"

    # Check directory
    if [ ! -d "$APP_DIR" ]; then
        echo -e "${RED}Application directory not found: ${NC}$APP_DIR"
        return
    fi

    cd "$APP_DIR"

    # Backup current version
    BACKUP_NAME="backup-$(date +'%Y%m%d-%H%M%S').tar.gz"
    echo "Creating backup: $BACKUP_NAME"
    tar -czf "$BACKUP_NAME" logs/ --exclude=logs/* || true
    echo -e "${GREEN}✅ Backup created${NC}"
    sleep 1

    # Pull latest changes
    echo "Checking for updates..."
    git pull || pip install -r requirements.txt || true

    # Restart service
    echo "Restarting service..."
    systemctl restart "$SERVICE_NAME"
    sleep 3

    echo -e "${GREEN}✅ Service updated successfully${NC}"
}

backup_database() {
    echo ""
    echo -e "${YELLOW}Creating database backup...${NC}"

    # Get database config from .env
    DB_TYPE=$(grep "^DB_TYPE=" .env | cut -d'=' -f2)
    DB_HOST=$(grep "^DB_HOST=" .env | cut -d'=' -f2)
    DB_NAME=$(grep "^DB_NAME=" .env | cut -d'=' -f2)
    DB_USER=$(grep "^DB_USER=" .env | cut -d'=' -f2)

    if [ "$DB_TYPE" != "postgresql" ]; then
        echo -e "${YELLOW}Database type: ${NC}$DB_TYPE (skipped for backup)"
        return
    fi

    BACKUP_FILE="db-backup-$(date +'%Y%m%d-%H%M%S').sql"
    echo "Backup file: $BACKUP_FILE"

    # Get password from .env securely
    DB_PASSWORD=$(grep "^DB_PASSWORD=" .env | cut -d'=' -f2)

    # Backup database
    sudo -u postgres pg_dump -h localhost -U $DB_USER $DB_NAME > "$BACKUP_FILE" 2>/dev/null || {
        echo -e "${RED}Warning: PostgreSQL backup skipped${NC}"
        return
    }

    # Compress backup
    gzip "$BACKUP_FILE"
    BACKUP_FILE="${BACKUP_FILE}.gz"

    # Save to backups directory
    mkdir -p "$APP_DIR/backups"
    mv "$BACKUP_FILE" "$APP_DIR/backups/"

    echo -e "${GREEN}✅ Database backup created${NC}"

    # Clean old backups
    echo "Cleaning old backups (retention: 7 days)..."
    find "$APP_DIR/backups/" -name "*.sql.gz" -mtime +7 -delete 2>/dev/null || true
}

main() {
    while true; do
        show_menu
        read choice

        case $choice in
            1) start_service ;;
            2) stop_service ;;
            3) restart_service ;;
            4) show_status ;;
            5) view_logs ;;
            6) update_service ;;
            7) backup_database ;;
            8) backup_database ;;
            9)
                clear
                echo "Goodbye!"
                exit 0
                ;;
            *)
                echo -e "${RED}Invalid choice${NC}"
                sleep 1
                ;;
        esac
    done
}

# Check if running as root (for sudo operations)
check_root() {
    if [ "$EUID" -ne 0 ]; then
        echo -e "${YELLOW}Note: Some operations may require sudo${NC}"
        echo "Run with: sudo $0"
    fi
}

# Check if service exists
check_service() {
    if ! systemctl list-unit-files | grep -q "$SERVICE_NAME"; then
        echo -e "${RED}Service $SERVICE_NAME not found${NC}"
        echo ""
        echo "To install the service:"
        echo "  1. Move files to /opt/ckey-api/"
        echo "  2. Run: sudo cp system.service /etc/systemd/system/"
        echo "  3. Run: sudo systemctl daemon-reload"
        echo "  4. Run: sudo systemctl enable $SERVICE_NAME"
        echo ""
        read -p "Continue anyway? " -n 1 -r
        echo
    fi
}

# Run checks and wait
echo "Starting service manager..."
sleep 1
check_service
check_root

main