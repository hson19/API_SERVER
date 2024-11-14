import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="my_user",
            password="my_password",
            database="my_database"
        )
        if connection.is_connected():
            print("Successfully connected to the database")
        return connection, connection.cursor()
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None
