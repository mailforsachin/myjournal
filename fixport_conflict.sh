#!/bin/bash

PORT="8011"

echo "🔧 Checking port $PORT conflict..."

# Check what's using the port
PID=$(sudo lsof -ti:$PORT)
if [ -z "$PID" ]; then
    echo "✅ Port $PORT is free"
    exit 0
fi

echo "⚠️  Port $PORT is used by PID: $PID"
echo "Process info:"
ps -p $PID -o pid,user,cmd

echo -e "\nOptions:"
echo "1. Kill the process"
echo "2. Change MyJournal port"
echo "3. Do nothing"
echo -n "Choose option [1-3]: "
read choice

case $choice in
    1)
        echo "Killing process $PID..."
        sudo kill -9 $PID
        echo "✅ Process killed"
        ;;
    2)
        echo -n "Enter new port (default: 8012): "
        read new_port
        new_port=${new_port:-8012}
        
        # Update config.py
        sed -i "s/PORT = .*/PORT = $new_port/" config.py 2>/dev/null || echo "Could not update config.py"
        
        # Update systemd service
        sudo sed -i "s/--port $PORT/--port $new_port/" /etc/systemd/system/myjournal.service 2>/dev/null
        
        # Update deploy.sh for future runs
        sed -i "s/PORT=\"$PORT\"/PORT=\"$new_port\"/" deploy.sh 2>/dev/null
        
        echo "✅ Port changed to $new_port"
        echo "Restart service with: sudo systemctl restart myjournal.service"
        ;;
    3)
        echo "⚠️  Leaving port conflict unresolved"
        ;;
    *)
        echo "❌ Invalid option"
        ;;
esac
