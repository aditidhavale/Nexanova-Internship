from flask import request, jsonify
from db import get_db
import csv

def init_app(app):

    # Filtered Report (FR-4.1)
    @app.route('/report', methods=['POST'])
    def report():
        data = request.json
        conn = get_db()
        rows = conn.execute("""
            SELECT * FROM evaluation
            WHERE technology=?""",
            (data['technology'],)).fetchall()
        return jsonify([dict(i) for i in rows])

    # Avg per round (FR-4.2)
    @app.route('/average', methods=['POST'])
    def average():
        data = request.json
        conn = get_db()
        avg = conn.execute("""
            SELECT round, AVG(score) as avg_score
            FROM evaluation
            WHERE technology=?
            GROUP BY round
        """, (data['technology'],)).fetchall()
        return jsonify([dict(i) for i in avg])

    # Export CSV (FR-4.3)
    @app.route('/export')
    def export():
        conn = get_db()
        rows = conn.execute("SELECT * FROM evaluation").fetchall()

        with open("report.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Participant","Score"])
            for r in rows:
                writer.writerow([r["participant"], r["score"]])

        return jsonify({"msg": "CSV exported"})