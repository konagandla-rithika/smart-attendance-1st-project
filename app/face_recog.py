import face_recognition
import cv2
import os

# Store known faces
known_faces = []
known_names = []

# Dataset folder (project root / dataset when run from project root)
_here = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_here)
dataset_path = os.path.join(_project_root, "dataset")

# Load all images from dataset
if not os.path.isdir(dataset_path):
    os.makedirs(dataset_path, exist_ok=True)
for filename in os.listdir(dataset_path):

    if filename.lower().endswith((".jpg", ".jpeg", ".png")):

        image_path = os.path.join(dataset_path, filename)

        img = face_recognition.load_image_file(image_path)

        encodings = face_recognition.face_encodings(img)

        if len(encodings) > 0:

            known_faces.append(encodings[0])

            name = os.path.splitext(filename)[0]

            known_names.append(name)

print("Loaded faces:", known_names)


# Recognize face function
def recognize_face(frame):

    global known_faces, known_names

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding in face_encodings:

        if len(known_faces) == 0:
            return "Unknown"

        distances = face_recognition.face_distance(known_faces, face_encoding)

        min_distance = min(distances)

        print("Distance:", min_distance)

        # STRICT threshold (important)
        if min_distance < 0.45:
            index = distances.tolist().index(min_distance)
            return known_names[index]

    return "Unknown"
