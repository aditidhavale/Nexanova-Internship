from flask import request, jsonify
from db import get_db

def init_app(app):

    # Add Participant (FR-3.1)
    @app.route('/add_participant', methods=['POST'])
    def add_participant():
        data = request.json
        conn = get_db()
        conn.execute("INSERT INTO participants VALUES (NULL,?,?,?)",
                     (data['name'], data['batch'], data['technology']))
        conn.commit()
        return jsonify({"msg": "Participant added"})

    # ✅ View All Participants (IMPORTANT for evaluator)
    @app.route('/view_participants', methods=['GET'])
    def view_participants():
        conn = get_db()
        data = conn.execute("SELECT * FROM participants").fetchall()
        return jsonify([dict(i) for i in data])

    # Assign Evaluator (FR-3.2)
    @app.route('/assign', methods=['POST'])
    def assign():
        data = request.json
        conn = get_db()
        conn.execute("INSERT INTO assignments VALUES (NULL,?,?,?,?)",
                     (data['participant'], data['evaluator'],
                      data['technology'], data['round']))
        conn.commit()
        return jsonify({"msg": "Assigned"})

    # Get Assigned Evaluations (FR-3.3)
    @app.route('/get_assignments/<evaluator>')
    def get_assignments(evaluator):
        conn = get_db()
        data = conn.execute("SELECT * FROM assignments WHERE evaluator=?",
                            (evaluator,)).fetchall()
        return jsonify([dict(i) for i in data])

    # Submit Evaluation (FR-3.4 & 3.5)
    @app.route('/submit_eval', methods=['POST'])
    def submit_eval():
        data = request.json
        conn = get_db()
        conn.execute("INSERT INTO evaluation VALUES (NULL,?,?,?,?,?,?)",
                     (data['participant'], data['evaluator'],
                      data['technology'], data['round'],
                      data['score'], data['feedback']))
        conn.commit()
        return jsonify({"msg": "Submitted"})