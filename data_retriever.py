# implement a get_notebooks function that returns all notebooks for a user
from connection import create_connection

db,cursor = create_connection()

def get_user_notebooks(username):
    # cursor.execute("SELECT title, content FROM Notebooks WHERE user_id = %s", (username,))
    print("Returning "+str(username)+"'s notebooks")
    return True

def get_user_info(username):
    cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
    return cursor.fetchone()