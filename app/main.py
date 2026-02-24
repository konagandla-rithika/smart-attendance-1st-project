from flask import Flask, request, jsonify, send_from_directory
import cv2
import numpy as np
import csv
import os
from datetime import datetime
from .face_recog import recognize_face

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(APP_ROOT)
STATIC_FOLDER = os.path.join(APP_ROOT, "static")
app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path="")

ATTENDANCE_FILE = os.path.join(PROJECT_ROOT, "attendance.csv")

# Create attendance file
if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Date", "Time"])


def mark_attendance(name):
    """Mark attendance; skip if already marked today."""
    today = datetime.now().strftime("%Y-%m-%d")
    with open(ATTENDANCE_FILE, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
    for row in rows[1:]:  # skip header
        if len(row) >= 2 and row[0] == name and row[1] == today:
            return False  # already marked today
    now = datetime.now()
    with open(ATTENDANCE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")])
    return True


def get_attendance_list(limit=50):
    """Return recent attendance records."""
    if not os.path.exists(ATTENDANCE_FILE):
        return []
    with open(ATTENDANCE_FILE, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if len(rows) <= 1:
        return []
    header = rows[0]
    records = [dict(zip(header, row)) for row in reversed(rows[1:])]
    return records[:limit]


# --- API (must be before catch-all route) ---
@app.route("/api/recognize", methods=["POST"])
def api_recognize():
    """Accept image (file or base64), run face recognition, mark attendance if known."""
    try:
        raw = None
        if request.files and "image" in request.files:
            file = request.files["image"]
            if file.filename:
                raw = file.read()
        if raw is None and request.json and "image" in request.json:
            import base64
            raw = base64.b64decode(request.json["image"].split(",", 1)[-1])
        if raw is None:
            return jsonify({"error": "No image provided"}), 400
        arr = np.frombuffer(raw, dtype=np.uint8)
        frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if frame is None:
            return jsonify({"error": "Invalid image"}), 400
        name = recognize_face(frame)
        marked = False
        if name != "Unknown":
            marked = mark_attendance(name)
        return jsonify({"name": name, "marked": marked})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/attendance", methods=["GET"])
def api_attendance():
    """Return recent attendance records."""
    limit = request.args.get("limit", 50, type=int)
    return jsonify(get_attendance_list(limit=limit))


@app.route("/start")
def start():
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        name = recognize_face(frame)
        cv2.putText(frame, name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Smart Attendance System", frame)
        if name != "Unknown":
            mark_attendance(name)
            break
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cam.release()
    cv2.destroyAllWindows()
    return "Attendance Completed"


# --- Web UI: serve static files (index.html and assets); must be last ---
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)


if __name__ == "__main__":
    print("Starting Flask Server...")
    print("Open http://127.0.0.1:5000 or http://localhost:5000 in your browser.")
    app.run(host="0.0.0.0", port=5000, debug=True)
