import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "myjournal_user",
    "password": "SecurePass123!",
    "database": "myjournal_db",
    "port": 3306,
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)
