from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
from functools import wraps
import jwt

from login import add_user, login
from data_retriever import get_user_notebooks
app = Flask(__name__)
SECRET_KEY = "secret_key"
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')  # Get token from headers
        if not token:
            return jsonify({"error": "Token is missing!"}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])  # Decode the token
            current_user = data['username']  # Get the username from the token
        except Exception as e:
            return jsonify({"error": "Token is invalid!"}), 401
        
        return f(current_user, *args, **kwargs)  # Pass the current user to the route
    return decorated

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
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

@app.route('/api/database', methods=['GET'])
def get_database():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM test_table")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(rows)

@app.route('/api/data', methods=['GET'])
def get_data():
    # Sample data to send as a JSON response
    data = {"message": "Hello from your server!"}
    return jsonify(data)

@app.route('/api/data', methods=['POST'])
def post_data():
    new_data = request.json
    return jsonify({"received": new_data}), 201

@app.route('/api/add_user', methods=['POST'])  # New route for adding a user
def api_add_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    if username and password and email:
        result = add_user(username, password, email)  # Call the add_user function
        return jsonify({"message": result}), 201 if result == "User created successfully." else 400
    else:
        return jsonify({"error": "Username, password, and email are required."}), 400

@app.route('/api/login', methods=['POST'])  # New route for login
def api_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username and password:
        result = login(username, password)  # Call the login function
        return jsonify(result), 200 if result["message"] == "Login successful!" else 401
    else:
        return jsonify({"error": "Username and password are required."}), 400
    
@app.route('/api/notebooks', methods=['GET'])  # New route for user notebooks
@token_required  # Protect this route
def api_get_notebooks(current_user):
    notebooks = get_user_notebooks(current_user)  # Use the current user from the token
    if notebooks:
        return jsonify({"notebooks": notebooks}), 200
    else:
        return jsonify({"error": "No notebooks found for this user."}), 404
    
if __name__ == '__main__':
    # Run on all interfaces to allow external access
    app.run(host='0.0.0.0', port=5000)
