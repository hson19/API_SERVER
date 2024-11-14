import requests

# Configuration
BASE_URL = "http://localhost:5000/api"  # Change this if your server is running on a different host/port
USERNAME = "testuser"  # Replace with the username you want to test
PASSWORD = "testpassword"  # Replace with the corresponding password

def login(username, password):
    """Log in the user and return the JWT token."""
    url = f"{BASE_URL}/login"
    response = requests.post(url, json={"username": username, "password": password})
    if response.status_code == 200:
        data = response.json()
        print("Login successful!")
        print(data)
        print("Token:", data['token'])
        return data['token']
    else:
        print("Login failed:", response.json())
        return None

def get_notebooks(token):
    """Get the user's notebooks using the provided JWT token."""
    url = f"{BASE_URL}/notebooks"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        notebooks = response.json()
        print("Notebooks retrieved successfully!")
        print(notebooks)
    else:
        print("Failed to retrieve notebooks:", response.json())

if __name__ == "__main__":
    # Step 1: Log in to get the token
    token = login(USERNAME, PASSWORD)
    
    # Step 2: If login was successful, get the user's notebooks
    if token:
        get_notebooks(token)
