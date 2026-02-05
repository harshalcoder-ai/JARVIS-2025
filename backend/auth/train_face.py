import cv2
import numpy as np
from PIL import Image
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dataset_path = os.path.join(BASE_DIR, 'dataset')
trainer_path = os.path.join(BASE_DIR, 'trainer', 'trainer.yml')

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def getImagesAndLabels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    face_samples = []
    ids = []

    for image_path in image_paths:
        gray_img = Image.open(image_path).convert('L')
        img_np = np.array(gray_img, 'uint8')

        id = int(os.path.split(image_path)[-1].split(".")[1])

        faces = detector.detectMultiScale(img_np)

        for (x, y, w, h) in faces:
            face_samples.append(img_np[y:y+h, x:x+w])
            ids.append(id)

    return face_samples, ids

print("\n [INFO] Training faces. This may take a few seconds...")

faces, ids = getImagesAndLabels(dataset_path)

recognizer.train(faces, np.array(ids))

os.makedirs("trainer", exist_ok=True)
recognizer.write(trainer_path)

print(f"\n [INFO] Training completed. Model saved to {trainer_path}")
