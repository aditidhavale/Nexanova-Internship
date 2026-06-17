from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import jwt, datetime
import csv

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500", "http://localhost:5500"])  # Enable CORS for frontend
app.config['SECRET_KEY'] = 'supersecretkey'

# In-memory database
users = []  # store users in memory

# ---------------- JWT HELPER ----------------
def generate_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

# ---------------- REGISTER ----------------
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    if not data.get("email") or not data.get("password") or not data.get("name") or not data.get("role"):
        return jsonify({"message": "All fields required"}), 400
    
    # Check if email already exists
    if any(u['email'] == data['email'] for u in users):
        return jsonify({"message": "User already exists"}), 400

    hashed_password = generate_password_hash(data['password'], method='sha256')
    user = {
        "id": len(users)+1,
        "name": data['name'],
        "email": data['email'],
        "password": hashed_password,
        "role": data['role']
    }
    users.append(user)

    # Role-based registration message
    if data['role'] == "Admin":
        message = f"Admin {data['name']} registered successfully!"
    elif data['role'] == "Trainer":
        message = f"Trainer {data['name']} registered successfully!"
    elif data['role'] == "Student":
        message = f"Student {data['name']} registered successfully!"
    else:
        message = "User registered successfully!"

    return jsonify({"message": message}), 201

# ---------------- LOGIN ----------------
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    user = next((u for u in users if u['email']==data['email']), None)
    if not user or not check_password_hash(user['password'], data['password']):
        return jsonify({"message":"Invalid credentials"}), 401

    token = generate_token(user['id'], user['role'])
    return jsonify({"token": token})

# ---------------- FORGOT PASSWORD ----------------
@app.route('/api/auth/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    user = next((u for u in users if u['email']==data['email']), None)
    if not user:
        return jsonify({"message":"Email not found"}),404
    return jsonify({"message":"Password reset link sent to email"}),200

# ---------------- BULK UPLOAD ----------------
@app.route('/api/users/bulk-upload', methods=['POST'])
def bulk_upload():
    if 'file' not in request.files:
        return jsonify({"message":"CSV file required"}), 400
    
    file = request.files['file']
    csv_reader = csv.DictReader(file.stream.read().decode('utf-8').splitlines())
    for row in csv_reader:
        hashed_password = generate_password_hash(row['password'], method='sha256')
        user = {
            "id": len(users)+1,
            "name": row['name'],
            "email": row['email'],
            "password": hashed_password,
            "role": row['role']
        }
        users.append(user)
    return jsonify({"message":"Bulk upload successful"}),201

# ---------------- GET TRAINERS ----------------
@app.route('/api/users/trainers', methods=['GET'])
def get_trainers():
    trainers = [u for u in users if u['role']=="Trainer"]
    return jsonify(trainers)

# ---------------- GET STUDENTS ----------------
@app.route('/api/users/students', methods=['GET'])
def get_students():
    students = [u for u in users if u['role']=="Student"]
    return jsonify(students)

# ---------------- RUN APP ----------------
if __name__=="__main__":
    app.run(port=8000, debug=True)
