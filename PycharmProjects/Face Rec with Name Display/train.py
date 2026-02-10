print("🚀 train.py started")

import cv2
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(BASE_DIR, "dataset")

print("📂 Dataset path:", dataset_path)

if not os.path.exists(dataset_path):
    print("❌ Dataset folder NOT found")
    exit()

persons = os.listdir(dataset_path)
print("📂 Found persons:", persons)

faces = []
labels = []
label_map = {}

label_id = 0

for person_name in persons:
    person_path = os.path.join(dataset_path, person_name)

    if not os.path.isdir(person_path):
        continue

    print(f"👤 Processing person: {person_name}")
    label_map[label_id] = person_name

    for image_name in os.listdir(person_path):
        img_path = os.path.join(person_path, image_name)
        print(f"   🖼 Loading image: {img_path}")

        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.equalizeHist(img)

        if img is None:
            print("   ⚠ Image could not be read, skipping")
            continue

        # 🔥 Normalize size (THIS FIXES YOUR ERROR)
        img = cv2.resize(img, (200, 200))

        faces.append(img)
        labels.append(label_id)

    label_id += 1

if len(faces) == 0:
    print("❌ No images were loaded. Training aborted.")
    exit()

faces = np.array(faces, dtype="uint8")
labels = np.array(labels)

model = cv2.face.LBPHFaceRecognizer_create()
model.train(faces, labels)

model.save("face_model.yml")
np.save("labels.npy", label_map)

print("✅ Training completed successfully")
