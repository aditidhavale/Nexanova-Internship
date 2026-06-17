from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Subject, Topic, Question, Quiz, QuizQuestion, User
from utils.auth import login_required, role_required
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

# ================= ADMIN DASHBOARD =================
@admin_bp.route('/dashboard')
@login_required
@role_required('admin')
def admin_dashboard():
    subjects = Subject.query.all()
    quizzes = Quiz.query.all()
    students = User.query.filter_by(role="student").all()

    return render_template('admin_dashboard.html',
                           subjects=subjects,
                           quizzes=quizzes,
                           students=students)

# ================= ADD SUBJECT =================
@admin_bp.route('/add_subject', methods=['POST'])
@login_required
@role_required('admin')
def add_subject():
    name = request.form['name']
    subject = Subject(name=name)

    db.session.add(subject)
    db.session.commit()

    flash("Subject added successfully", "success")
    return redirect(url_for('admin.admin_dashboard'))

# ================= ADD TOPIC =================
@admin_bp.route('/add_topic', methods=['POST'])
@login_required
@role_required('admin')
def add_topic():
    name = request.form['name']
    subject_id = request.form['subject_id']

    topic = Topic(name=name, subject_id=subject_id)

    db.session.add(topic)
    db.session.commit()

    flash("Topic added successfully", "success")
    return redirect(url_for('admin.admin_dashboard'))

# ================= ADD QUESTION =================
@admin_bp.route('/add_question', methods=['POST'])
@login_required
@role_required('admin')
def add_question():
    data = request.form

    question = Question(
        subject_id=data['subject_id'],
        topic_id=data['topic_id'],
        question_text=data['question_text'],
        option1=data['option1'],
        option2=data['option2'],
        option3=data['option3'],
        option4=data['option4'],
        correct_answer=data['correct_answer'],
        marks=1
    )

    db.session.add(question)
    db.session.commit()

    flash("Question added successfully", "success")
    return redirect(url_for('admin.admin_dashboard'))

# ================= CREATE QUIZ =================
@admin_bp.route('/create_quiz', methods=['POST'])
@login_required
@role_required('admin')
def create_quiz():
    title = request.form['title']
    subject_id = request.form['subject_id']
    topic_id = request.form['topic_id']
    duration = request.form['duration']

    scheduled_date = request.form['scheduled_date']
    start_time = request.form['start_time']

    quiz = Quiz(
        title=title,
        subject_id=subject_id,
        topic_id=topic_id,
        duration=duration,
        scheduled_date=datetime.strptime(scheduled_date, "%Y-%m-%d").date(),
        start_time=datetime.strptime(start_time, "%H:%M").time()
    )

    db.session.add(quiz)
    db.session.commit()

    # Add selected questions
    question_ids = request.form.getlist('question_ids')

    for qid in question_ids:
        qq = QuizQuestion(quiz_id=quiz.id, question_id=qid)
        db.session.add(qq)

    db.session.commit()

    flash("Quiz created successfully", "success")
    return redirect(url_for('admin.admin_dashboard'))

# ================= ADD STUDENT =================
@admin_bp.route('/add_student', methods=['POST'])
@login_required
@role_required('admin')
def add_student():
    username = request.form['username']
    password = request.form['password']

    student = User(username=username, password=password, role="student")

    db.session.add(student)
    db.session.commit()

    flash("Student added successfully", "success")
    return redirect(url_for('admin.admin_dashboard'))

# ================= RESET PASSWORD =================
@admin_bp.route('/reset_password/<int:user_id>', methods=['POST'])
@login_required
@role_required('admin')
def reset_password(user_id):
    user = User.query.get(user_id)
    new_password = request.form['new_password']

    user.password = new_password
    db.session.commit()

    flash("Password updated", "success")
    return redirect(url_for('admin.admin_dashboard'))