from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ================= USER MODEL =================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin' or 'student'

# ================= SUBJECT =================
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    topics = db.relationship('Topic', backref='subject', cascade="all, delete")

# ================= TOPIC =================
class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)

    questions = db.relationship('Question', backref='topic', cascade="all, delete")

# ================= QUESTION =================
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)

    question_text = db.Column(db.Text, nullable=False)

    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255), nullable=False)
    option4 = db.Column(db.String(255), nullable=False)

    correct_answer = db.Column(db.String(50), nullable=False)  # option1/option2/etc

    marks = db.Column(db.Integer, default=1)

# ================= QUIZ =================
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)

    title = db.Column(db.String(200), nullable=False)

    duration = db.Column(db.Integer, nullable=False)  # in minutes

    scheduled_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)

    questions = db.relationship('QuizQuestion', backref='quiz', cascade="all, delete")

# ================= QUIZ QUESTION MAPPING =================
class QuizQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

# ================= STUDENT ANSWERS =================
class StudentAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    selected_answer = db.Column(db.String(50))

# ================= RESULT =================
class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)

    total_marks = db.Column(db.Integer)
    obtained_marks = db.Column(db.Integer)

    percentage = db.Column(db.Float)

    status = db.Column(db.String(50))  # Completed / Missed

    created_at = db.Column(db.DateTime, default=datetime.utcnow)