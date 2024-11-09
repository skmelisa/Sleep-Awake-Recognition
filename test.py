from ultralytics import YOLO
import pygame
import cv2

# Modeli yükle
model = YOLO('best.pt')

# Pygame'i başlat ve ses dosyasını yükle
pygame.init()
pygame.mixer.init()
alarm_sound = 'alarm.mp3'


def play_alarm(volume):
    if not pygame.mixer.music.get_busy():  # Eğer müzik çalmıyorsa
        pygame.mixer.music.load(alarm_sound)
        pygame.mixer.music.play(-1)  # Döngü ile sürekli çalsın
    pygame.mixer.music.set_volume(volume)  # Ses seviyesini ayarla


def stop_alarm():
    if pygame.mixer.music.get_busy():  # Eğer müzik çalıyorsa
        pygame.mixer.music.stop()


# Kameradan görüntü al
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Modeli çalıştır ve sonuçları al
    results = model.predict(source=frame, show=True)

    # "uyuyor" ve "uykulu" sınıflarını kontrol etmek için bayraklar oluşturun
    sleeping_detected = False
    drowsy_detected = False

    # Sonuçları kontrol et
    for result in results:
        boxes = result.boxes  # Alınan kutuları al
        if boxes:q
            for box in boxes:
                cls = int(box.cls[0])  # Sınıf indeksini al
                class_name = model.names[cls]  # Sınıf adını al
                if class_name == 'uyuyor':
                    sleeping_detected = True
                    break
                elif class_name == 'uykulu':
                    drowsy_detected = True
            if sleeping_detected:
                break

    # Eğer "uyuyor" tespit edildiyse yüksek sesle alarmı çal, "uykulu" tespit edildiyse kısık sesle alarmı çal, aksi halde alarmı durdur
    if sleeping_detected:
        play_alarm(1.0)  # Yüksek ses
    elif drowsy_detected:
        play_alarm(0.5)  # Kısık ses
    else:
        stop_alarm()


    # 'q' tuşuna basıldığında döngüyü sonlandır
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırak
cap.release()
cv2.destroyAllWindows()
pygame.quit()
