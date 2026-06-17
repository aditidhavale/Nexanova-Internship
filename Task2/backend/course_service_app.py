from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500", "http://localhost:5500"])

# ---------------- IN-MEMORY DATABASE ----------------
courses = [
    {"id": 1, "name": "Python Programming", "duration": "3 Months", "day": "Monday"},
    {"id": 2, "name": "Data Science", "duration": "4 Months", "day": "Tuesday"},
    {"id": 3, "name": "Web Development", "duration": "3 Months", "day": "Wednesday"},
    {"id": 4, "name": "Machine Learning", "duration": "4 Months", "day": "Thursday"},
    {"id": 5, "name": "Cloud Computing", "duration": "2 Months", "day": "Friday"}
]

modules = [
    {"id": 1, "name": "Python Basics", "course_id": 1},
    {"id": 2, "name": "OOP in Python", "course_id": 1},
    {"id": 3, "name": "Statistics", "course_id": 2},
    {"id": 4, "name": "Pandas & NumPy", "course_id": 2},
    {"id": 5, "name": "HTML & CSS", "course_id": 3},
    {"id": 6, "name": "JavaScript", "course_id": 3},
    {"id": 7, "name": "Regression", "course_id": 4},
    {"id": 8, "name": "Neural Networks", "course_id": 4},
    {"id": 9, "name": "AWS Basics", "course_id": 5},
    {"id": 10, "name": "Cloud Security", "course_id": 5}
]

# ---------------- GET ALL COURSES ----------------
@app.route('/api/courses', methods=['GET'])
def get_courses():
    return jsonify(courses), 200

# ---------------- GET MODULES OF A COURSE ----------------
@app.route('/api/courses/<int:course_id>/modules', methods=['GET'])
def get_modules(course_id):
    course_modules = [m for m in modules if m['course_id'] == course_id]
    return jsonify(course_modules), 200

# ---------------- ADD NEW COURSE ----------------
@app.route('/api/courses', methods=['POST'])
def add_course():
    data = request.json
    if not data.get("name"):
        return jsonify({"message": "Course name required"}), 400

    new_course = {
        "id": len(courses) + 1,
        "name": data['name'],
        "duration": data.get('duration', 'N/A'),
        "day": data.get('day', 'Not Assigned')  # Can auto-assign later if needed
    }
    courses.append(new_course)
    return jsonify({"message": f"Course '{new_course['name']}' added successfully", "course": new_course}), 201

# ---------------- ADD MODULE TO COURSE ----------------
@app.route('/api/courses/<int:course_id>/modules', methods=['POST'])
def add_module(course_id):
    data = request.json
    if not data.get("name"):
        return jsonify({"message": "Module name required"}), 400

    if not any(c['id'] == course_id for c in courses):
        return jsonify({"message": "Course not found"}), 404

    new_module = {
        "id": len(modules) + 1,
        "name": data['name'],
        "course_id": course_id
    }
    modules.append(new_module)
    return jsonify({"message": f"Module '{new_module['name']}' added to course {course_id}", "module": new_module}), 201

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(port=8001, debug=True)
