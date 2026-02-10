import cv2
import numpy as np
import os
from collections import deque

prediction_buffer = deque(maxlen=10)


# Load trained model
model = cv2.face.LBPHFaceRecognizer_create()
model.read("face_model.yml")

# Load labels
label_map = np.load("labels.npy", allow_pickle=True).item()

# Face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

print("🎥 Camera started. Press ESC to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=6,
        minSize=(100, 100)
    )

    for (x, y, w, h) in faces:
        padding = 20
        face = gray[max(0, y - padding):y + h + padding,
        max(0, x - padding):x + w + padding]

        # 🔥 Resize SAME as training
        face = cv2.resize(face, (200, 200))

        label, confidence = model.predict(face)

        if confidence < 150:
            prediction_buffer.append(label_map[label])
        else:
            prediction_buffer.append("Unknown")

        # Majority vote
        name = max(set(prediction_buffer), key=prediction_buffer.count)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"{name}",
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2
        )

    cv2.imshow("Face Recognition - LBPH", frame)

    if cv2.waitKey(1) == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
