from flask import Flask, render_template, session
import os
from db import init_db

# App configuration
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'static')
)

# ✅ Required for session (login role handling)
app.secret_key = "secret123"

# Initialize DB
init_db()

# Import modules
import configuration
import user
import evaluation
import reporting

# Register modules
configuration.init_app(app)
user.init_app(app)
evaluation.init_app(app)
reporting.init_app(app)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    role = session.get('role')  # ✅ role from login
    return render_template('dashboard.html', role=role)

# ✅ FIXED: pass role here also
@app.route('/evaluation_page')
def evaluation_page():
    role = session.get('role')
    return render_template('evaluation.html', role=role)

@app.route('/report_page')
def report_page():
    return render_template('report.html')


if __name__ == "__main__":
    app.run(debug=True)