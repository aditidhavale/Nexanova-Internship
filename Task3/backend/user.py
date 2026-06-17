from flask import request, jsonify, session
from db import get_db

def init_app(app):

    # FR-2.1 Add User
    @app.route('/add_user', methods=['POST'])
    def add_user():
        data = request.json
        conn = get_db()

        # ✅ clean inputs
        name = data['name'].strip()
        email = data['email'].strip()
        password = data['password'].strip()
        role = data['role'].strip().upper()   # IMPORTANT

        conn.execute(
            "INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)",
            (name, email, password, role)
        )
        conn.commit()

        return jsonify({"msg": "User added"})


    # ✅ LOGIN (FINAL FIX)
    @app.route('/login', methods=['POST'])
    def login():
        data = request.json
        conn = get_db()

        # ✅ clean input (MAIN FIX)
        email = data['email'].strip()
        password = data['password'].strip()

        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()

        # ✅ DEBUG (you can remove later)
        print("LOGIN TRY:", email, password)
        print("USER FOUND:", user)

        if user:
            session['role'] = user['role']
            session['email'] = user['email']

            return jsonify({
                "msg": "Login success",
                "role": user['role']
            })

        return jsonify({"msg": "Invalid"}), 401