from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500", "http://localhost:5500"])

# In-memory database
schedules = {}  # key = week_id, value = list of slots

# ---------------- CREATE WEEKLY SCHEDULE (MON–FRI) ----------------
@app.route('/api/schedule', methods=['POST'])
def create_schedule():
    data = request.json
    week_id = data.get('week_id')

    if not week_id:
        return jsonify({"message": "week_id required"}), 400

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    times = ["8-11", "11-2", "2-5", "5-8"]

    slots = []
    slot_id = 0
    for day in days:
        for time in times:
            slots.append({
                "slot_id": slot_id,
                "day": day,
                "time": time,
                "course_id": None,
                "course_name": None,
                "module_id": None,
                "module_name": None,
                "trainer_id": None,
                "trainer_name": None
            })
            slot_id += 1

    schedules[week_id] = slots
    return jsonify({"message": f"Weekly schedule '{week_id}' created successfully!", "slots": slots}), 201

# ---------------- ALLOCATE SLOT ----------------
@app.route('/api/schedule/slot/<int:slot_id>', methods=['PUT'])
def allocate_slot(slot_id):
    data = request.json
    week_id = data.get('week_id')

    if not week_id or week_id not in schedules:
        return jsonify({"message": "Invalid or missing week_id"}), 400

    slots = schedules[week_id]

    if slot_id < 0 or slot_id >= len(slots):
        return jsonify({"message": "Invalid slot_id"}), 400

    slot = slots[slot_id]

    # Assign values (only if provided)
    for key in ['course_id', 'course_name', 'module_id', 'module_name', 'trainer_id', 'trainer_name']:
        if key in data:
            slot[key] = data[key]

    return jsonify({"message": f"Slot {slot_id} updated successfully!", "slot": slot}), 200

# ---------------- GET WEEKLY SCHEDULE ----------------
@app.route('/api/schedule/<week_id>', methods=['GET'])
def get_schedule(week_id):
    if week_id not in schedules:
        return jsonify({"message": "Schedule not found"}), 404
    return jsonify(schedules[week_id]), 200

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(port=8002, debug=True)