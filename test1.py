from ultralytics import YOLO
import pygame
import cv2


model = YOLO('best.pt') #ağırlık dosyası, model içe aktarıldı

pygame.init() #pygame başlatıldı, çalınacak alarm sesi atandı
pygame.mixer.init()
alarm_sound = 'alarm.mp3'

def play_alarm(volume): # alarm çalmıyorsa ses dosyasını yüklerve sonsuz döngüde çalar. alarmın ses seviyesi ayarlanır
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(alarm_sound)
        pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(volume)

def stop_alarm(): # alarm çalıyorsa alarmı durdurur
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()


cap = cv2.VideoCapture(0) #video akışını başlatır

while cap.isOpened(): # kameradan kare okutur, frame okunan kareyi içerir
    ret, frame = cap.read()
    if not ret: #kare okunmazsa döngü kırılır
        break

    results = model.predict(source=frame, show=True) #mevcut kare üzerinden tahmin yapar ve sonucu gösterir

    sleeping_detected = False #uyuyan durumu tespit edilir
    drowsy_detected = False

    for result in results: #tahmin sonuçlarını döngüye sokar ve tespit edilen nesnelerin kutularını alır
        boxes = result.boxes
        if boxes:
            for box in boxes:
                cls = int(box.cls[0]) #tespit edilen nesnenin sınıfını alır
                class_name = model.names[cls] #sınıf etiketini alır
                if class_name == 'uyuyor':
                    sleeping_detected = True
                    break
                elif class_name == 'uykulu':
                    drowsy_detected = True
            if sleeping_detected:
                break

    if sleeping_detected: #uyuyan durumu tespit edilirse alarm maksimum ses seviyesinde çalınır
        play_alarm(1.0)
    elif drowsy_detected:
        play_alarm(0.5)
    else:
        stop_alarm()


    if cv2.waitKey(1) & 0xFF == ord('q'): #q tuşuna basınca döngü sonlanır
        break


cap.release()
cv2.destroyAllWindows()
pygame.quit()
