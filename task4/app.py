from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from models import db, User
from utils.auth import logout_user
from routes.admin_routes import admin_bp
from routes.student_routes import student_bp
from routes.quiz_routes import quiz_bp

# ================= INIT APP =================
app = Flask(__name__)
app.config.from_object(Config)

# ================= INIT DB =================
db.init_app(app)

# ================= REGISTER BLUEPRINTS =================
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(student_bp, url_prefix='/student')
app.register_blueprint(quiz_bp, url_prefix='/quiz')

# ================= CREATE DB =================
with app.app_context():
    db.create_all()

    # Create default admin if not exists
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", password="admin123", role="admin")
        db.session.add(admin)
        db.session.commit()

# ================= LOGIN =================
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role

            # Redirect based on role
            if user.role == "admin":
                return redirect(url_for('admin.admin_dashboard'))
            else:
                return redirect(url_for('student.student_dashboard'))
        else:
            flash("Invalid credentials", "error")

    return render_template('login.html')

# ================= LOGOUT =================
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# ================= RUN =================
if __name__ == '__main__':
    app.run(debug=True)