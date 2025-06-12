from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Test route
@app.route('/')
def home():
    return jsonify({"message": "MindVault backend is running!"})

# Example route for creating a note (we'll expand this later)
@app.route('/api/notes', methods=['POST'])
def create_note():
    data = request.json
    # Simulate saving to DB
    print(f"Received note: {data}")
    return jsonify({"status": "Note received", "data": data}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)
