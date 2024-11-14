import jwt
import datetime
import bcrypt
import mysql.connector
from mysql.connector import Error
from connection import create_connection
SECRET_KEY = "secret_key"


def hash_password(plain_password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed_password

def add_user(username, plain_password, email):
    try:
        hashed_password = hash_password(plain_password)
        # check if user already exists
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        if cursor.fetchone():
            return "Username already exists."
        # Insert into the Users table
        cursor.execute("INSERT INTO Users (username, password_hash, email) VALUES (%s, %s, %s)", 
                       (username, hashed_password, email))
        db.commit()
        return "User created successfully."
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()
        return "Failed to create user."
    
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def login(username, plain_password):
    cursor.execute("SELECT password_hash FROM Users WHERE username = %s", (username,))
    result = cursor.fetchone()
    
    if result and verify_password(plain_password, result[0]):
        # user_info = get_user_info(username)  # Fetch user info
        # Generate JWT
        token = jwt.encode({
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
        }, SECRET_KEY, algorithm='HS256')
        return {"message": "Login successful!", "token": token, "user": username}
    else:
        return {"message": "Invalid username or password."}
def get_user_id(username):
    cursor.execute("SELECT id FROM Users WHERE username = %s", (username,))
    result = cursor.fetchone()
    return result[0] if result else None


db,cursor = create_connection()

# create_user("testuser", "testpassword", "test@example.com")
# login("testuser", "testpassword")