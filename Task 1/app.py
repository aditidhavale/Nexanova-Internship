from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ----------------- DATABASE MODELS -----------------

class Trainer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.id'))

# ----------------- CREATE DATABASE -----------------
with app.app_context():
    db.create_all()

# ----------------- ROUTES -----------------

@app.route('/')
def index():
    trainers = Trainer.query.all()
    subjects = Subject.query.all()
    return render_template('index.html', trainers=trainers, subjects=subjects)

# 1. Add trainer
@app.route('/add_trainer', methods=['POST'])
def add_trainer():
    name = request.form.get('trainer_name')
    new_trainer = Trainer(name=name)
    db.session.add(new_trainer)
    db.session.commit()
    return redirect('/')

# 2. Get all trainers (API)
@app.route('/trainer', methods=['GET'])
def get_trainers():
    trainers = Trainer.query.all()
    return {"trainers": [{"id": t.id, "name": t.name} for t in trainers]}

# 3. Delete specific trainer (API + UI)
@app.route('/trainer/<int:id>/delete', methods=['GET', 'POST'])
def delete_trainer(id):
    trainer = Trainer.query.get_or_404(id)

    # Find all subjects taught by this trainer
    subjects = Subject.query.filter_by(trainer_id=id).all()

    # Remove trainer from subjects
    for subject in subjects:
        subject.trainer_id = None

    # Delete trainer
    db.session.delete(trainer)
    db.session.commit()

    return redirect('/')

# 4. Get info of specific trainer (API + UI)
@app.route('/trainer/<int:id>', methods=['GET'])
def trainer_info(id):
    trainer = Trainer.query.get_or_404(id)
    return {"id": trainer.id, "name": trainer.name}

# 5. Get info of trainer(s) teaching specific subject (API)
@app.route('/trainer/<subject_name>/topic', methods=['GET'])
def trainer_by_subject(subject_name):
    subject = Subject.query.filter_by(name=subject_name).first()
    if not subject:
        return {"error": "No such subject found"}
    trainer = Trainer.query.get(subject.trainer_id)
    return {"subject": subject.name, "trainer": trainer.name}

# 6. Add new subject
@app.route('/add_subject', methods=['POST'])
def add_subject():
    name = request.form.get('subject_name')
    trainer_id = request.form.get('trainer_id')
    new_subject = Subject(name=name, trainer_id=trainer_id)
    db.session.add(new_subject)
    db.session.commit()
    return redirect('/')

# 7. Get all subjects (API)
@app.route('/subject', methods=['GET'])
def get_subjects():
    subjects = Subject.query.all()
    return {"subjects": [{"id": s.id, "name": s.name, "trainer_id": s.trainer_id} for s in subjects]}

# 8. Get subjects with trainer info (API)
@app.route('/subject/<int:id>', methods=['GET'])
def subject_info(id):
    subject = Subject.query.get_or_404(id)
    trainer = Trainer.query.get(subject.trainer_id)
    return {
        "subject": subject.name,
        "trainer": {"id": trainer.id, "name": trainer.name}
    }

# ----------------- RUN APP -----------------
if __name__ == '__main__':
    app.run(debug=True)
