import cv2
import pygame
import time

pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
headshot_sound = pygame.mixer.Sound("headshot.mp3")
channel = pygame.mixer.Channel(0)

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

last_play_time = 0
cooldown = 2.0  # detik

print("Webcam aktif. Tekan ESC untuk keluar.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal membaca webcam")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(60, 60)
    )

    for (x, y, w, h) in faces:
        cx = x + w // 2
        cy = y + h // 6  

        cv2.circle(frame, (cx, cy), 15, (0, 0, 255), 2)
        cv2.line(frame, (cx - 20, cy), (cx + 20, cy), (0, 0, 255), 2)
        cv2.line(frame, (cx, cy - 20), (cx, cy + 20), (0, 0, 255), 2)

    if len(faces) > 0:
        now = time.time()
    if (now - last_play_time > cooldown) and not channel.get_busy():
            channel.play(headshot_sound)
            last_play_time = now

    cv2.imshow("Headshot Effect - Webcam", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
