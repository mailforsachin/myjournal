import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="myjournal",
        password="SecurePassword123!",
        database="myjournal"
    )
    print("✅ Successfully connected to MariaDB!")
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"MariaDB version: {version[0]}")
    conn.close()
except mysql.connector.Error as e:
    print(f"❌ Error connecting to MariaDB: {e}")
