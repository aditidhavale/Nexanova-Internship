from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500", "http://localhost:5500"])

COURSE_SERVICE = "http://127.0.0.1:8001/api"

# In-memory database
enrollments = []

# ---------------- ENROLL SINGLE STUDENT ----------------
@app.route('/api/enrollments', methods=['POST'])
def enroll_student():
    data = request.json

    if not data.get('student_id') or not data.get('course_id'):
        return jsonify({"message": "student_id and course_id are required"}), 400

    # 🔥 FIX: convert IDs to int
    student_id = int(data['student_id'])
    course_id = int(data['course_id'])

    # Fetch course info
    courses = requests.get(f"{COURSE_SERVICE}/courses").json()
    course_info = next((c for c in courses if c["id"] == course_id), None)

    if not course_info:
        return jsonify({"message": "Course not found"}), 404

    enrollment = {
        "student_id": student_id,
        "student_name": data.get('student_name', f"Student {student_id}"),
        "course_id": course_id,
        "course_name": course_info["name"],
        "course_day": course_info["day"]
    }

    enrollments.append(enrollment)

    return jsonify({
        "message": f"Student enrolled in {course_info['name']}",
        "enrollment": enrollment
    }), 201


# ---------------- GET COURSES OF A STUDENT ----------------
@app.route('/api/enrollments/student/<int:student_id>/courses', methods=['GET'])
def student_courses(student_id):
    student_courses = [e for e in enrollments if e['student_id'] == student_id]
    return jsonify(student_courses), 200


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(port=8003, debug=True)
