from flask import Blueprint, render_template, session, redirect, url_for, flash
from models import db, Quiz, Result
from utils.auth import login_required, role_required
from datetime import datetime, date

student_bp = Blueprint('student', __name__)

# ================= STUDENT DASHBOARD =================
@student_bp.route('/dashboard')
@login_required
@role_required('student')
def student_dashboard():
    today = date.today()

    # Get today's quizzes only
    quizzes = Quiz.query.filter_by(scheduled_date=today).all()

    return render_template('dashboard.html', quizzes=quizzes)

# ================= START QUIZ =================
@student_bp.route('/start_quiz/<int:quiz_id>')
@login_required
@role_required('student')
def start_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    now = datetime.now()

    # Check date
    if quiz.scheduled_date != now.date():
        flash("Quiz not available today", "error")
        return redirect(url_for('student.student_dashboard'))

    # Check time
    if now.time() < quiz.start_time:
        flash("Quiz has not started yet", "error")
        return redirect(url_for('student.student_dashboard'))

    # Check if already attempted
    existing_result = Result.query.filter_by(
        student_id=session['user_id'],
        quiz_id=quiz_id
    ).first()

    if existing_result:
        flash("You have already attempted this quiz", "error")
        return redirect(url_for('student.student_dashboard'))

    return redirect(url_for('quiz.take_quiz', quiz_id=quiz_id))

# ================= VIEW RESULTS =================
@student_bp.route('/results')
@login_required
@role_required('student')
def view_results():
    student_id = session['user_id']

    results = Result.query.filter_by(student_id=student_id).all()

    # ================= PERFORMANCE CALCULATION =================
    total_quizzes = len(results)

    if total_quizzes > 0:
        avg_score = sum(r.percentage for r in results) / total_quizzes
        best_score = max(r.percentage for r in results)
    else:
        avg_score = 0
        best_score = 0

    return render_template('result.html',
                           results=results,
                           total_quizzes=total_quizzes,
                           avg_score=round(avg_score, 2),
                           best_score=best_score)