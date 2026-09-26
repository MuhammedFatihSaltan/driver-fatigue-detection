import cv2
from detection.face_detector import FaceDetector

def main():
    cap = cv2.VideoCapture(0)
    
    # Yüz dedektör sınıfımızı çağırıyoruz
    detector = FaceDetector()

    if not cap.isOpened():
        print("Hata: Kamera açılamadı!")
        return

    print("Sistem başlatıldı. Çıkmak için 'q' tuşuna basın.")

    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Hata: Görüntü alınamıyor.")
            break

        # Görüntüyü dedektöre gönder ve işlenmiş kareyi/noktaları geri al
        frame, landmarks = detector.find_face_mesh(frame, draw=True)

        # Eğer yüz tespit edildiyse, terminale toplam nokta sayısını yazdır (Test amaçlı)
        if len(landmarks) != 0:
            cv2.putText(frame, f"Landmarks: {len(landmarks)}", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Surucu Yorgunluk Tespit Sistemi - Faz 2', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()