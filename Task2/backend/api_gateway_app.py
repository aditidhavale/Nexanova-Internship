from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import jwt

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500", "http://localhost:5500"])

SECRET_KEY = "supersecretkey"  # must match auth service

# ---------------- HELPER ----------------
def validate_token():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None, "Missing token"
    try:
        payload = jwt.decode(auth_header, SECRET_KEY, algorithms=["HS256"])
        return payload, None
    except Exception as e:
        return None, str(e)

def proxy_request(method, url, json_data=None, files=None, headers=None):
    if method == "GET":
        resp = requests.get(url, headers=headers)
    elif method == "POST":
        if files:
            resp = requests.post(url, files=files)
        else:
            resp = requests.post(url, json=json_data, headers=headers)
    elif method == "PUT":
        resp = requests.put(url, json=json_data, headers=headers)
    else:
        return None, 405
    return resp, resp.status_code

# ---------------- AUTH ROUTES ----------------
@app.route("/api/auth/<path:path>", methods=["POST"])
def auth_proxy(path):
    resp = requests.post(f"http://127.0.0.1:8000/api/auth/{path}", json=request.get_json())
    return jsonify(resp.json()), resp.status_code

@app.route("/api/users/<path:path>", methods=["GET","POST"])
def users_proxy(path):
    payload, err = validate_token()
    if not payload:
        return jsonify({"message":"Unauthorized: "+err}), 401

    if request.method == "GET":
        resp, status = proxy_request("GET", f"http://127.0.0.1:8000/api/users/{path}")
    else:
        # POST (bulk upload)
        resp, status = proxy_request("POST", f"http://127.0.0.1:8000/api/users/{path}", files=request.files)
    return jsonify(resp.json()), status

# ---------------- COURSE ROUTES ----------------
@app.route("/api/courses", methods=["GET","POST"])
@app.route("/api/courses/<path:path>", methods=["GET","POST"])
def courses_proxy(path=""):
    payload, err = validate_token()
    if not payload:
        return jsonify({"message":"Unauthorized: "+err}), 401

    url = f"http://127.0.0.1:8001/api/courses"
    if path:
        url += f"/{path}"
    resp, status = proxy_request(request.method, url, json_data=request.get_json())
    return jsonify(resp.json()), status

# ---------------- SCHEDULE ROUTES ----------------
@app.route("/api/schedule", methods=["GET","POST"])
@app.route("/api/schedule/<path:path>", methods=["GET","POST","PUT"])
def schedule_proxy(path=""):
    payload, err = validate_token()
    if not payload:
        return jsonify({"message":"Unauthorized: "+err}), 401

    url = f"http://127.0.0.1:8002/api/schedule"
    if path:
        url += f"/{path}"
    resp, status = proxy_request(request.method, url, json_data=request.get_json())
    return jsonify(resp.json()), status

# ---------------- ENROLLMENT ROUTES ----------------
@app.route("/api/enrollments", methods=["GET","POST"])
@app.route("/api/enrollments/<path:path>", methods=["GET","POST"])
def enrollments_proxy(path=""):
    payload, err = validate_token()
    if not payload:
        return jsonify({"message":"Unauthorized: "+err}), 401

    url = f"http://127.0.0.1:8003/api/enrollments"
    if path:
        url += f"/{path}"
    resp, status = proxy_request(request.method, url, json_data=request.get_json())
    return jsonify(resp.json()), status

# ---------------- TIMETABLE ROUTES ----------------
@app.route("/api/timetable/<path:path>", methods=["GET"])
def timetable_proxy(path):
    payload, err = validate_token()
    if not payload:
        return jsonify({"message":"Unauthorized: "+err}), 401

    resp, status = proxy_request("GET", f"http://127.0.0.1:8004/api/timetable/{path}")
    return jsonify(resp.json()), status

# ---------------- RUN GATEWAY ----------------
if __name__ == "__main__":
    app.run(port=8005, debug=True)
