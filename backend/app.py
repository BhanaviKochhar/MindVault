from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from dotenv import load_dotenv
import os
from datetime import datetime  # Added for timestamp formatting

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
CORS(app)

# DB connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    return conn

# Test route
@app.route('/')
def home():
    return jsonify({"message": "MindVault backend is running!"})

# Route: Create a note
@app.route('/api/notes', methods=['POST'])
def create_note():
    data = request.json
    user_id = data.get('user_id')
    content = data.get('content')
    tags = data.get('tags', '')
    timestamp = datetime.utcnow()

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO notes (user_id, content, timestamp, tags) VALUES (%s, %s, %s, %s)",
            (user_id, content, timestamp, tags)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "success", "message": "Note created!"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Route: Get all notes
@app.route('/api/notes', methods=['GET'])
def get_notes():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, user_id, content, timestamp, tags FROM notes ORDER BY timestamp DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        notes = [
            {
                "id": row[0],
                "user_id": row[1],
                "content": row[2],
                "timestamp": row[3].isoformat(),
                "tags": row[4]
            }
            for row in rows
        ]
        return jsonify(notes), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
