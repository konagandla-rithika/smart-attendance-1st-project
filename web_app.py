import streamlit as st
import cv2
from app.face_recog import recognize_face

st.title("Smart Attendance System")

if st.button("Start Camera"):
    cap = cv2.VideoCapture(0)
    frame_window = st.image([])

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        names = recognize_face(frame)

        for name in names:
            st.write(f"{name} marked present")

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_window.image(frame)

    cap.release()