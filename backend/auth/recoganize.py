import cv2
import os
import time

# ===================== CONFIG =====================
AUTHORIZED_ID = 1          # ID used during collect_face.py
AUTHORIZED_NAME = "Harshal"
CONFIDENCE_THRESHOLD = 80 # Lower = stricter; adjust 50-100
REQUIRED_FRAMES = 3       # Frames to confirm authentication
# ===================================================

def get_camera(max_index=5):
    """Try multiple camera indexes and return the first available."""
    for i in range(max_index):
        cam = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cam.isOpened():
            print(f"[INFO] Using camera index {i}")
            return cam
    return None

def AuthenticateFace():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # ===== Paths =====
    trainer_path = os.path.join(BASE_DIR, "trainer", "trainer.yml")
    cascade_path = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")

    if not os.path.exists(trainer_path):
        print("[ERROR] Trainer file not found:", trainer_path)
        return 0

    if not os.path.exists(cascade_path):
        print("[ERROR] Haarcascade not found:", cascade_path)
        return 0

    print("[INFO] Trainer path:", trainer_path)
    print("[INFO] Haarcascade path:", cascade_path)

    # ===== Load recognizer and cascade =====
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(trainer_path)
    faceCascade = cv2.CascadeClassifier(cascade_path)
    font = cv2.FONT_HERSHEY_SIMPLEX

    # ===== Open camera =====
    cam = get_camera()
    if cam is None:
        print("[ERROR] No available camera found")
        return 0

    cam.set(3, 640)
    cam.set(4, 480)
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    print(f"🔐 Starting face authentication for {AUTHORIZED_NAME}...")

    # ===== Smooth recognition =====
    success_count = 0

    while True:
        ret, img = cam.read()
        if not ret:
            print("[ERROR] Failed to capture frame")
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

            predicted_id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

            print(f"[DEBUG] Predicted ID: {predicted_id}, Confidence: {confidence:.2f}")

            # Check authorization
            if predicted_id == AUTHORIZED_ID and confidence < CONFIDENCE_THRESHOLD:
                success_count += 1
                cv2.putText(img, AUTHORIZED_NAME, (x+5, y-5), font, 1, (0,255,0), 2)
                cv2.putText(img, "AUTHORIZED", (x+5, y+h+25), font, 1, (0,255,0), 2)

                if success_count >= REQUIRED_FRAMES:
                    print("✅ AUTHORIZED: Harshal")
                    cam.release()
                    cv2.destroyAllWindows()
                    return 1
            else:
                success_count = 0
                cv2.putText(img, "UNAUTHORIZED", (x+5, y-5), font, 1, (0,0,255), 2)
                cv2.putText(img, f"Conf: {int(confidence)}", (x+5, y+h+25), font, 1, (0,0,255), 2)

        cv2.imshow("JARVIS Face Lock", img)

        # ESC to exit
        if cv2.waitKey(10) & 0xFF == 27:
            print("🔒 Authentication canceled by user")
            break

    cam.release()
    cv2.destroyAllWindows()
    print("🔒 Access denied")
    return 0

# ===================== RUN =====================
if __name__ == "__main__":
    result = AuthenticateFace()
    if result == 1:
        print("[INFO] Welcome, Harshal! JARVIS unlocked 🤖")
    else:
        print("[INFO] JARVIS remains locked 🔒")
