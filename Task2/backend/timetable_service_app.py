from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500", "http://localhost:5500"])

# ---------------- SERVICE URL ----------------
ENROLLMENT_SERVICE = "http://127.0.0.1:8003/api"

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# ---------------- STUDENT TIMETABLE ----------------
@app.route('/api/timetable/student/<int:student_id>', methods=['GET'])
def get_student_timetable(student_id):
    try:
        #  Fetch enrollments
        enroll_resp = requests.get(
            f"{ENROLLMENT_SERVICE}/enrollments/student/{student_id}/courses"
        )
        enrollments = enroll_resp.json()

        #  Initialize timetable
        timetable = {day: [] for day in DAYS}

        #  Fill timetable USING course_day directly ✅
        for e in enrollments:
            day = e.get("course_day")
            name = e.get("course_name")

            if day in timetable:
                timetable[day].append(name)

        #  Handle empty days
        for day in DAYS:
            if not timetable[day]:
                timetable[day] = ["No Courses"]

        return jsonify(timetable), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(port=8004, debug=True)
