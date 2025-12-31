#!/bin/bash
echo "=== MyJournal Production Deployment ==="

# Stop any running vite processes
echo "1. Stopping development servers..."
pkill -f vite 2>/dev/null || true

# Go to frontend directory
cd ~/myjournal/myjournal-ui

echo "2. Building frontend..."
rm -rf dist node_modules/.vite
npm run build

echo "3. Fixing permissions..."
sudo chown -R ubuntu:ubuntu dist/
sudo chmod -R 755 dist/

echo "4. Restarting backend..."
sudo systemctl restart myjournal
sleep 2
sudo systemctl status myjournal --no-pager

echo "5. Reloading Nginx..."
sudo nginx -t && sudo systemctl reload nginx

echo ""
echo "=== Testing Deployment ==="
echo "Testing frontend:"
if curl -s -o /dev/null -w "%{http_code}" https://myjournal.omchat.ovh/ | grep -q "200\|304"; then
    echo "✅ Frontend is working!"
else
    echo "❌ Frontend check failed"
    curl -I https://myjournal.omchat.ovh/
fi

echo ""
echo "Testing API:"
API_RESPONSE=$(curl -s https://myjournal.omchat.ovh/api/health)
if echo "$API_RESPONSE" | grep -q "healthy"; then
    echo "✅ API is working: $API_RESPONSE"
else
    echo "❌ API check failed: $API_RESPONSE"
fi

echo ""
echo "=== Deployment Complete ==="
echo "Access your application at: https://myjournal.omchat.ovh"
echo ""
echo "For debugging:"
echo "1. Frontend logs: sudo tail -f /var/log/nginx/myjournal.access.log"
echo "2. Backend logs: sudo journalctl -u myjournal -f"
echo "3. Check build: ls -la ~/myjournal/myjournal-ui/dist/"
