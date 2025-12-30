import mysql.connector

def init_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="myjournal_user",  # Use the app user, not root
            password="SecurePassword123!",
            database="myjournal"
        )
        # ... rest of your initialization code ...
    except mysql.connector.Error as e:
        print(f"Error connecting to MariaDB: {e}")
