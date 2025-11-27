import cv2
import os

def get_camera():
    """Try all indexes 0–5 until a working camera is found."""
    for i in range(5):
        cam = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cam.isOpened():
            print(f"[INFO] Using camera index {i}")
            return cam
    return None


def AuthenticateFace():
    flag = 0  # default: not recognized

    # Load face recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    trainer_path = os.path.join("backend", "auth", "trainer", "trainer.yml")
    if not os.path.exists(trainer_path):
        print("[Error] Trainer file not found:", trainer_path)
        return 0
    recognizer.read(trainer_path)

    # Haar cascade
    cascadePath = os.path.join("backend", "auth", "haarcascade_frontalface_default.xml")
    if not os.path.exists(cascadePath):
        print("[Error] Haarcascade not found:", cascadePath)
        return 0
    faceCascade = cv2.CascadeClassifier(cascadePath)

    font = cv2.FONT_HERSHEY_SIMPLEX

    # IDs and names (index = label in trainer.yml)
    names = ["", "", "Ankit"]

    # Open first working camera
    cam = get_camera()
    if cam is None:
        print("[Error] No available camera found")
        return 0

    cam.set(3, 640)
    cam.set(4, 480)

    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
        ret, img = cam.read()
        if not ret:
            print("[Error] Failed to capture frame")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            id, accuracy = recognizer.predict(gray[y:y+h, x:x+w])

            if accuracy < 100:
                name = names[id] if id < len(names) else "Unknown"
                accuracy_text = f"{round(100 - accuracy)}%"
                flag = 1
            else:
                name = "Unknown"
                accuracy_text = f"{round(100 - accuracy)}%"
                flag = 0

            cv2.putText(img, str(name), (x+5, y-5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, accuracy_text, (x+5, y+h-5), font, 1, (255, 255, 0), 1)

        cv2.imshow("Face Authentication", img)

        k = cv2.waitKey(10) & 0xFF
        if k == 27:  # ESC
            break
        if flag == 1:  # stop once face recognized
            break

    cam.release()
    cv2.destroyAllWindows()
    return flag
