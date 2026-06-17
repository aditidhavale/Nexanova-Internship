from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models import db, Quiz, QuizQuestion, Question, StudentAnswer, Result
from utils.auth import login_required, role_required
from datetime import datetime

quiz_bp = Blueprint('quiz', __name__)

# ================= TAKE QUIZ =================
@quiz_bp.route('/take_quiz/<int:quiz_id>')
@login_required
@role_required('student')
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    # Get all questions for this quiz
    quiz_questions = QuizQuestion.query.filter_by(quiz_id=quiz_id).all()
    questions = [Question.query.get(q.question_id) for q in quiz_questions]

    # Store start time in session
    session['quiz_start_time'] = datetime.now().timestamp()

    return render_template('quiz.html',
                           quiz=quiz,
                           questions=questions)

# ================= SAVE ANSWER =================
@quiz_bp.route('/save_answer', methods=['POST'])
@login_required
@role_required('student')
def save_answer():
    student_id = session['user_id']
    quiz_id = request.form['quiz_id']
    question_id = request.form['question_id']
    selected_answer = request.form.get('selected_answer')

    answer = StudentAnswer.query.filter_by(
        student_id=student_id,
        quiz_id=quiz_id,
        question_id=question_id
    ).first()

    if answer:
        answer.selected_answer = selected_answer
    else:
        answer = StudentAnswer(
            student_id=student_id,
            quiz_id=quiz_id,
            question_id=question_id,
            selected_answer=selected_answer
        )
        db.session.add(answer)

    db.session.commit()

    return "Saved"

# ================= SUBMIT QUIZ =================
@quiz_bp.route('/submit_quiz/<int:quiz_id>', methods=['POST'])
@login_required
@role_required('student')
def submit_quiz(quiz_id):
    student_id = session['user_id']

    quiz = Quiz.query.get_or_404(quiz_id)
    quiz_questions = QuizQuestion.query.filter_by(quiz_id=quiz_id).all()

    total_marks = 0
    obtained_marks = 0

    for qq in quiz_questions:
        question = Question.query.get(qq.question_id)
        total_marks += question.marks

        answer = StudentAnswer.query.filter_by(
            student_id=student_id,
            quiz_id=quiz_id,
            question_id=question.id
        ).first()

        if answer and answer.selected_answer == question.correct_answer:
            obtained_marks += question.marks

    percentage = (obtained_marks / total_marks) * 100 if total_marks > 0 else 0

    result = Result(
        student_id=student_id,
        quiz_id=quiz_id,
        total_marks=total_marks,
        obtained_marks=obtained_marks,
        percentage=percentage,
        status="Completed"
    )

    db.session.add(result)
    db.session.commit()

    flash("Quiz submitted successfully!", "success")
    return redirect(url_for('student.view_results'))

# ================= GET ANSWER STATUS =================
@quiz_bp.route('/get_status/<int:quiz_id>')
@login_required
@role_required('student')
def get_status(quiz_id):
    student_id = session['user_id']

    answers = StudentAnswer.query.filter_by(
        student_id=student_id,
        quiz_id=quiz_id
    ).all()

    status = {}

    for ans in answers:
        status[ans.question_id] = ans.selected_answer

    return status