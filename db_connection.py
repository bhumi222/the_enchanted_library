import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='enchanted_library',  # Use your database name
            user='root',  # Your MySQL username
            password=''  # Your MySQL password
        )

        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
        else:
            print("Failed to connect to the database")
            return None

    except Error as e:
        print(f"Error: {e}")
        return None

def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("Database connection closed")

def insert_book(title, author, isbn, book_type, status, condition, is_restricted):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """
        INSERT INTO books (title, author, isbn, book_type, status, `condition`, is_restricted)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        values = (title, author, isbn, book_type, status, condition, is_restricted)
        
        try:
            cursor.execute(query, values)
            connection.commit()
            print("Book inserted successfully.")
        except Exception as e:
            print(f"Error inserting book: {e}")
        finally:
            cursor.close()
            close_connection(connection)

def get_books():
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT * FROM books;"
        
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                print(row)
        except Exception as e:
            print(f"Error fetching books: {e}")
        finally:
            cursor.close()
            close_connection(connection)
