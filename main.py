from ultralytics import YOLO
import pygame
import cv2


model = YOLO('best.pt')


pygame.init()
pygame.mixer.init()
alarm_sound = 'alarm.mp3'


def play_alarm():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(alarm_sound)
        pygame.mixer.music.play()


def stop_alarm():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()



cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break


    results = model.predict(source=frame, show=True)


    sleeping_detected = False

    for result in results:
        boxes = result.boxes
        if boxes:
            for box in boxes:
                cls = int(box.cls[0])
                class_name = model.names[cls]
                if class_name == 'uyuyor':
                    sleeping_detected = True
                    break
            if sleeping_detected:
                break


    if sleeping_detected:
        play_alarm()
    else:
        stop_alarm()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()
