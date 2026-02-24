import streamlit as st
import face_recognition
import numpy as np
from PIL import Image
import os
import csv
from datetime import datetime

st.title("Smart Attendance System")

DATASET_PATH = "dataset"

known_encodings = []
known_names = []

# Load dataset
for person_name in os.listdir(DATASET_PATH):
    person_folder = os.path.join(DATASET_PATH, person_name)
    
    for image_file in os.listdir(person_folder):
        image_path = os.path.join(person_folder, image_file)
        
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        
        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(person_name)

# Attendance function
def mark_attendance(name):
    file_exists = os.path.isfile("attendance.csv")
    
    with open("attendance.csv", "a", newline="") as file:
        writer = csv.writer(file)
        
        if not file_exists:
            writer.writerow(["Name", "Date", "Time"])
        
        now = datetime.now()
        writer.writerow([name, now.date(), now.strftime("%H:%M:%S")])


# Upload image
uploaded_file = st.file_uploader("Upload your face image", type=["jpg","jpeg","png"])

if uploaded_file is not None:
    
    image = Image.open(uploaded_file)
    image_np = np.array(image)
    
    encodings = face_recognition.face_encodings(image_np)
    
    if encodings:
        
        face_encoding = encodings[0]
        
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        
        if True in matches:
            
            match_index = matches.index(True)
            name = known_names[match_index]
            
            st.success(f"Attendance marked for {name}")
            
            mark_attendance(name)
            
        else:
            st.error("Face not recognized")
            
    else:
        st.error("No face detected")