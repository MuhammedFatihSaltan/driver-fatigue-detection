import cv2
from detection.face_detector import FaceDetector
from analysis.eye_analysis import calculate_ear

# MediaPipe'ın sağ ve sol göz için kullandığı nokta indeksleri
RIGHT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
LEFT_EYE_INDICES = [362, 385, 387, 263, 373, 380]

def get_eye_coords(landmarks, indices):
    """Belirli indekslere sahip landmarkların (x,y) koordinatlarını listeler."""
    coords = []
    for idx in indices:
        for lm in landmarks:
            if lm[0] == idx:
                coords.append((lm[1], lm[2]))
                break
    return coords

def main():
    cap = cv2.VideoCapture(0)
    detector = FaceDetector()

    if not cap.isOpened():
        print("Hata: Kamera açılamadı!")
        return

    print("Sistem başlatıldı. Çıkmak için 'q' tuşuna basın.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Sadece yüz noktalarını (mesh) çizmeden al (draw=False yaparak kalabalığı azaltıyoruz)
        frame, landmarks = detector.find_face_mesh(frame, draw=False)

        if len(landmarks) != 0:
            # Sağ ve sol göz koordinatlarını ayıkla
            right_eye = get_eye_coords(landmarks, RIGHT_EYE_INDICES)
            left_eye = get_eye_coords(landmarks, LEFT_EYE_INDICES)
            
            # Göz noktaları tam olarak tespit edildiyse
            if len(right_eye) == 6 and len(left_eye) == 6:
                right_ear = calculate_ear(right_eye)
                left_ear = calculate_ear(left_eye)
                
                # Her iki gözün ortalamasını al
                avg_ear = (right_ear + left_ear) / 2.0
                
                # EAR değerini ekrana yazdır (Virgülden sonra 2 hane)
                cv2.putText(frame, f"EAR: {avg_ear:.2f}", (30, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Surucu Yorgunluk Tespit Sistemi - Faz 3', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()