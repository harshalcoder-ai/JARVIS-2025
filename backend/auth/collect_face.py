import cv2
import os

# HARSHAL ONLY
face_id = 1
user_name = "Harshal"

dataset_path = os.path.join("backend", "auth", "dataset")
os.makedirs(dataset_path, exist_ok=True)  # create folder if not exists

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 640)
cam.set(4, 480)

detector = cv2.CascadeClassifier(
    os.path.join("backend", "auth", "haarcascade_frontalface_default.xml")
)

print("📸 Taking samples for Harshal ONLY. Look at camera...")
count = 0

while True:
    ret, img = cam.read()
    if not ret:
        print("[ERROR] Camera read failed")
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        count += 1

        # Save image to dataset folder
        cv2.imwrite(
            os.path.join(dataset_path, f"User.{face_id}.{count}.jpg"),
            gray[y:y+h, x:x+w]
        )

        cv2.imshow("Collect Face - Harshal", img)

    k = cv2.waitKey(100) & 0xff
    if k == 27:  # ESC
        break
    elif count >= 60:  # 50–60 samples enough
        break

print("✅ Face samples taken for Harshal.")
cam.release()
cv2.destroyAllWindows()
