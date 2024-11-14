from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    # Sample data to send as a JSON response
    data = {"message": "Hello from your server!"}
    return jsonify(data)

@app.route('/api/data', methods=['POST'])
def post_data():
    new_data = request.json
    return jsonify({"received": new_data}), 201

if __name__ == '__main__':
    # Run on all interfaces to allow external access
    app.run(host='0.0.0.0', port=5000)
