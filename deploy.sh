#!/bin/bash
echo "=== MyJournal Deployment Script ==="

# Go to frontend directory
cd ~/myjournal/myjournal-ui

echo "1. Installing dependencies..."
npm install

echo "2. Building frontend for production..."
npm run build

echo "3. Restarting backend service..."
sudo systemctl restart myjournal

echo "4. Testing API..."
curl -s https://myjournal.omchat.ovh/api/health | jq .

echo "5. Testing frontend..."
curl -I https://myjournal.omchat.ovh/ | head -5

echo ""
echo "=== Deployment Complete ==="
echo "Access your application at: https://myjournal.omchat.ovh"
echo ""
echo "If you encounter issues, check:"
echo "1. Backend logs: sudo journalctl -u myjournal -f"
echo "2. Nginx logs: sudo tail -f /var/log/nginx/myjournal.*.log"
echo "3. Test SSL: curl -I https://myjournal.omchat.ovh"
