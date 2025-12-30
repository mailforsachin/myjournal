#!/bin/bash

echo "🔍 Checking existing Nginx configuration..."

echo -e "\n📋 Currently enabled sites:"
sudo ls -la /etc/nginx/sites-enabled/ 2>/dev/null || echo "No sites-enabled directory"

echo -e "\n🌐 Active server blocks:"
sudo nginx -T 2>/dev/null | grep "server_name" | sort | uniq

echo -e "\n🔌 Listening ports:"
sudo netstat -tulpn | grep nginx || echo "Nginx not running or no active connections"

echo -e "\n📄 Nginx main config:"
ls -la /etc/nginx/nginx.conf 2>/dev/null && echo "Exists" || echo "Not found"

echo -e "\n⚠️  Checking for conflicts with port 8011..."
if sudo netstat -tulpn | grep -q ":8011 "; then
    echo "❌ Port 8011 is in use by:"
    sudo netstat -tulpn | grep ":8011 "
else
    echo "✅ Port 8011 is available"
fi

echo -e "\n💡 To see detailed Nginx config: sudo nginx -T"
