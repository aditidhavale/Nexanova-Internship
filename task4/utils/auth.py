from flask import session, redirect, url_for, flash
from functools import wraps

# ================= LOGIN REQUIRED DECORATOR =================
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please login first", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

# ================= ROLE BASED ACCESS =================
def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'role' not in session:
                flash("Unauthorized access", "error")
                return redirect(url_for('login'))

            if session['role'] != role:
                flash("Access denied", "error")
                return redirect(url_for('login'))

            return f(*args, **kwargs)
        return wrapper
    return decorator

# ================= CURRENT USER =================
def get_current_user():
    return {
        "user_id": session.get("user_id"),
        "username": session.get("username"),
        "role": session.get("role")
    }

# ================= LOGOUT =================
def logout_user():
    session.clear()