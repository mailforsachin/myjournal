#!/bin/bash

echo "Setting up MySQL for MyJournal..."

# Create database and user
sudo mysql -e "CREATE DATABASE IF NOT EXISTS myjournal_db;"
sudo mysql -e "CREATE USER IF NOT EXISTS 'myjournal_user'@'localhost' IDENTIFIED BY 'SecurePass123!';"
sudo mysql -e "GRANT ALL PRIVILEGES ON myjournal_db.* TO 'myjournal_user'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

echo "✅ MySQL setup complete!"
echo "Database: myjournal_db"
echo "User: myjournal_user"
