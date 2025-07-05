import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # change if needed
        database="enchanted_library"
    )
    if connection.is_connected():
        print("✅ Connected to MySQL database successfully.")
    connection.close()

except mysql.connector.Error as err:
    print(f"❌ Error: {err}")
