#!/bin/bash

echo "🚀 Deploying MyJournal to myjournal.omchat.ovh (Safe Mode)..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
DOMAIN="myjournal.omchat.ovh"
PORT="8011"
APP_DIR="/home/$USER/myjournal"
SERVICE_NAME="myjournal"
NGINX_CONFIG="/etc/nginx/sites-available/$SERVICE_NAME"
NGINX_ENABLED="/etc/nginx/sites-enabled/$SERVICE_NAME"

# Function to check if port is in use
check_port() {
    if sudo netstat -tulpn | grep -q ":$1 "; then
        echo -e "  ⚠️  Port $1 is already in use by:"
        sudo netstat -tulpn | grep ":$1 "
        return 1
    else
        echo -e "  ✅ Port $1 is available"
        return 0
    fi
}

# Function to check if domain config exists
check_domain_config() {
    if [ -f "/etc/nginx/sites-available/$1" ] || sudo nginx -T 2>/dev/null | grep -q "server_name $1"; then
        echo -e "  ⚠️  Nginx configuration for $1 already exists"
        return 1
    else
        echo -e "  ✅ No existing Nginx config for $1"
        return 0
    fi
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${YELLOW}Note: Running as non-root user${NC}"
fi

echo -e "\n${YELLOW}=== Pre-deployment Checks ===${NC}"

# Check port availability
echo -e "\n${YELLOW}Checking ports...${NC}"
if ! check_port $PORT; then
    echo -e "${RED}❌ Port $PORT is already in use. Choose a different port or stop the existing service.${NC}"
    exit 1
fi

# Check domain configuration
echo -e "\n${YELLOW}Checking domain configuration...${NC}"
if ! check_domain_config $DOMAIN; then
    echo -e "${YELLOW}⚠️  Domain $DOMAIN already configured in Nginx. We'll add our config safely.${NC}"
fi

# Check existing Nginx sites
echo -e "\n${YELLOW}Existing Nginx sites:${NC}"
sudo ls -la /etc/nginx/sites-enabled/ 2>/dev/null || echo "No sites-enabled directory"
echo ""

# Update system
echo -e "\n${YELLOW}Updating system packages...${NC}"
sudo apt update && sudo apt upgrade -y

# Install required packages (only if missing)
echo -e "\n${YELLOW}Checking/installing system dependencies...${NC}"

check_and_install() {
    if ! dpkg -l | grep -q "^ii  $1 "; then
        echo "Installing $1..."
        sudo apt install -y $1
    else
        echo "$1 is already installed"
    fi
}

check_and_install python3-pip
check_and_install python3-venv
check_and_install mysql-server
check_and_install mysql-client

# Check if Nginx is installed
if ! dpkg -l | grep -q "^ii  nginx "; then
    echo -e "${YELLOW}Nginx is not installed. Installing...${NC}"
    sudo apt install -y nginx
else
    echo "Nginx is already installed"
fi

# Start MySQL service
echo -e "\n${YELLOW}Starting MySQL service...${NC}"
sudo systemctl start mysql
sudo systemctl enable mysql

# Create project directory
echo -e "\n${YELLOW}Setting up project directory...${NC}"
mkdir -p $APP_DIR
cd $APP_DIR

echo -e "\n${YELLOW}Current directory:${NC} $(pwd)"
echo -e "${YELLOW}App directory:${NC} $APP_DIR"

# Setup MySQL database and user
echo -e "\n${YELLOW}Setting up MySQL database...${NC}"
sudo mysql -e "CREATE DATABASE IF NOT EXISTS myjournal_db;" 2>/dev/null || echo "Database might already exist"
sudo mysql -e "CREATE USER IF NOT EXISTS 'myjournal_user'@'localhost' IDENTIFIED BY 'SecurePass123!';" 2>/dev/null || echo "User might already exist"
sudo mysql -e "GRANT ALL PRIVILEGES ON myjournal_db.* TO 'myjournal_user'@'localhost';" 2>/dev/null || echo "Privileges might already be set"
sudo mysql -e "FLUSH PRIVILEGES;" 2>/dev/null || echo "Could not flush privileges"

# Create virtual environment
echo -e "\n${YELLOW}Creating Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo -e "\n${YELLOW}Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database
echo -e "\n${YELLOW}Initializing database...${NC}"
if [ -f "init_db.py" ]; then
    python init_db.py
else
    echo -e "${YELLOW}⚠️  init_db.py not found. Creating basic tables...${NC}"
    python -c "
import mysql.connector
import bcrypt

conn = mysql.connector.connect(
    host='localhost',
    user='myjournal_user',
    password='SecurePass123!',
    database='myjournal_db'
)
cursor = conn.cursor()

# Create tables if not exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    transaction_date DATE NOT NULL,
    description TEXT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    type ENUM('income', 'expense', 'transfer') NOT NULL,
    auto_category VARCHAR(100),
    manual_category VARCHAR(100),
    confirmed BOOLEAN DEFAULT FALSE,
    source_file VARCHAR(255),
    raw_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create default user
hashed = bcrypt.hashpw('Welcome@2026!'.encode(), bcrypt.gensalt())
cursor.execute('''
    INSERT IGNORE INTO users (username, hashed_password) 
    VALUES (%s, %s)
''', ('sachin', hashed.decode()))

conn.commit()
cursor.close()
conn.close()
print('✅ Basic tables created')
"
fi

# Create systemd service
echo -e "\n${YELLOW}Creating systemd service...${NC}"
sudo tee /etc/systemd/system/$SERVICE_NAME.service > /dev/null << EOF
[Unit]
Description=MyJournal FastAPI Application
After=network.target mysql.service
Wants=mysql.service

[Service]
User=$USER
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port $PORT
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal

# Security
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=$APP_DIR

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start service
echo -e "\n${YELLOW}Starting MyJournal service...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME.service
sudo systemctl start $SERVICE_NAME.service

# Wait for service to start
sleep 3

# Check if service is running
if sudo systemctl is-active --quiet $SERVICE_NAME.service; then
    echo -e "  ✅ Service started successfully"
else
    echo -e "  ❌ Service failed to start. Checking logs..."
    sudo journalctl -u $SERVICE_NAME.service -n 10 --no-pager
    echo -e "${YELLOW}⚠️  Continuing with deployment...${NC}"
fi

# Configure Nginx as reverse proxy (SAFE - only if config doesn't exist)
echo -e "\n${YELLOW}Configuring Nginx (safe mode)...${NC}"

# Backup existing Nginx config if it exists
if [ -f "$NGINX_CONFIG" ]; then
    BACKUP_FILE="$NGINX_CONFIG.backup.$(date +%Y%m%d_%H%M%S)"
    echo "  Backing up existing config to $BACKUP_FILE"
    sudo cp "$NGINX_CONFIG" "$BACKUP_FILE"
fi

# Create new Nginx config
sudo tee "$NGINX_CONFIG" > /dev/null << EOF
# MyJournal Application - Auto-generated
# This config should not interfere with existing sites
server {
    listen 80;
    server_name $DOMAIN;
    
    # Don't interfere with main domain
    if (\$host != $DOMAIN) {
        return 444;  # Close connection for non-matching hosts
    }
    
    location / {
        proxy_pass http://127.0.0.1:$PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Static files
    location /static {
        alias $APP_DIR/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # API documentation
    location /docs {
        proxy_pass http://127.0.0.1:$PORT/docs;
        proxy_set_header Host \$host;
    }
    
    location /redoc {
        proxy_pass http://127.0.0.1:$PORT/redoc;
        proxy_set_header Host \$host;
    }
    
    # Health check endpoint
    location /api/health {
        proxy_pass http://127.0.0.1:$PORT/api/health;
        proxy_set_header Host \$host;
    }
    
    # Block sensitive paths
    location ~* /(\.git|\.env|config\.py|venv|__pycache__) {
        deny all;
        return 404;
    }
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
EOF

# Enable the site (but don't disable others)
if [ -L "$NGINX_ENABLED" ]; then
    echo "  Site already enabled in Nginx"
else
    sudo ln -s "$NGINX_CONFIG" "$NGINX_ENABLED"
    echo "  Site enabled in Nginx"
fi

# Test Nginx configuration
echo -e "\n${YELLOW}Testing Nginx configuration...${NC}"
if sudo nginx -t; then
    echo -e "  ✅ Nginx configuration test passed"
    
    # Reload Nginx (not restart, to avoid downtime)
    echo -e "\n${YELLOW}Reloading Nginx...${NC}"
    if sudo systemctl reload nginx; then
        echo -e "  ✅ Nginx reloaded successfully"
    else
        echo -e "  ⚠️  Nginx reload failed, trying restart..."
        sudo systemctl restart nginx
    fi
else
    echo -e "  ❌ Nginx configuration test failed"
    echo -e "${YELLOW}⚠️  Nginx config error. Your existing sites might be affected.${NC}"
    echo -e "${YELLOW}Check /etc/nginx/sites-available/$SERVICE_NAME and fix issues.${NC}"
    
    # Disable our config if it breaks things
    sudo rm -f "$NGINX_ENABLED"
    sudo systemctl restart nginx
    echo -e "${YELLOW}⚠️  Our Nginx config has been disabled to prevent breaking existing sites.${NC}"
    echo -e "${YELLOW}You can access MyJournal directly on port $PORT.${NC}"
fi

# Configure firewall (only if ufw is enabled)
echo -e "\n${YELLOW}Configuring firewall...${NC}"
if command -v ufw &> /dev/null && sudo ufw status | grep -q "Status: active"; then
    echo "UFW is active. Adding rules..."
    sudo ufw allow $PORT/tcp comment "MyJournal app port"
    sudo ufw reload
    echo "  ✅ Firewall configured"
else
    echo "  ⚠️  UFW not active or not installed"
fi

# Check service status
echo -e "\n${YELLOW}=== Deployment Status ===${NC}"

echo -e "\n${YELLOW}MyJournal service:${NC}"
if sudo systemctl is-active --quiet $SERVICE_NAME.service; then
    echo -e "  ✅ ${GREEN}ACTIVE${NC}"
    echo -e "  Access: http://127.0.0.1:$PORT"
else
    echo -e "  ❌ ${RED}INACTIVE${NC}"
    echo -e "  Check logs: sudo journalctl -u $SERVICE_NAME.service"
fi

echo -e "\n${YELLOW}Nginx status:${NC}"
if sudo systemctl is-active --quiet nginx; then
    echo -e "  ✅ ${GREEN}ACTIVE${NC}"
    echo -e "  Config: /etc/nginx/sites-available/$SERVICE_NAME"
else
    echo -e "  ❌ ${RED}INACTIVE${NC}"
fi

echo -e "\n${YELLOW}Database status:${NC}"
if mysql -u myjournal_user -pSecurePass123! -e "USE myjournal_db; SELECT 'Connected'" &> /dev/null; then
    echo -e "  ✅ ${GREEN}CONNECTED${NC}"
else
    echo -e "  ❌ ${RED}CONNECTION FAILED${NC}"
fi

# DNS information
echo -e "\n${YELLOW}=== DNS Configuration Required ===${NC}"
echo "To access via $DOMAIN, add this A record in your DNS:"
echo ""
echo "Type: A"
echo "Name: myjournal"
echo "Value: $(curl -s ifconfig.me || hostname -I | awk '{print $1}')"
echo "TTL: 3600"
echo ""
echo "Or test locally by adding to /etc/hosts:"
echo "$(hostname -I | awk '{print $1}') $DOMAIN"
echo ""

# Alternative access methods
echo -e "\n${YELLOW}=== Access Methods ===${NC}"
echo "1. Direct access (immediate): http://$(curl -s ifconfig.me || hostname -I | awk '{print $1}'):$PORT"
echo "2. Via Nginx (after DNS): http://$DOMAIN"
echo "3. Local access: http://127.0.0.1:$PORT"
echo "4. API Docs: Add /docs to any URL above"

# Management commands
echo -e "\n${YELLOW}=== Management Commands ===${NC}"
echo "View logs:         sudo journalctl -u $SERVICE_NAME.service -f"
echo "Restart app:       sudo systemctl restart $SERVICE_NAME.service"
echo "Check app status:  sudo systemctl status $SERVICE_NAME.service"
echo "Check Nginx logs:  sudo tail -f /var/log/nginx/access.log"
echo "Test API:          curl http://127.0.0.1:$PORT/api/health"

# Warning about existing Nginx sites
echo -e "\n${YELLOW}=== Important Notes ===${NC}"
echo "⚠️  This deployment tries to be safe with existing Nginx configuration."
echo "⚠️  If you have issues with existing websites:"
echo "    1. Check /etc/nginx/sites-available/$SERVICE_NAME"
echo "    2. Check Nginx error logs: sudo tail -f /var/log/nginx/error.log"
echo "    3. To disable MyJournal Nginx config: sudo rm $NGINX_ENABLED && sudo systemctl reload nginx"
echo "    4. You can still access MyJournal directly on port $PORT"

echo -e "\n${GREEN}✅ Deployment complete!${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Add DNS A record for $DOMAIN"
echo "2. Test access: curl http://127.0.0.1:$PORT/api/health"
echo "3. Login at http://127.0.0.1:$PORT with username: sachin, password: Welcome@2026!"
