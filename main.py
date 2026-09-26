import cv2
from detection.face_detector import FaceDetector
from analysis.eye_analysis import calculate_ear
from analysis.blink_analysis import BlinkAnalyzer

RIGHT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
LEFT_EYE_INDICES = [362, 385, 387, 263, 373, 380]

def get_eye_coords(landmarks, indices):
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
    
    # Kırpma analizörümüzü başlatıyoruz
    # Eğer gözlüğün varsa veya kameran uzaktaysa ear_threshold değerini 0.20 yapabilirsin
    blink_analyzer = BlinkAnalyzer(ear_threshold=0.22, fatigue_frames=20)

    if not cap.isOpened():
        print("Hata: Kamera açılamadı!")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame, landmarks = detector.find_face_mesh(frame, draw=False)

        if len(landmarks) != 0:
            right_eye = get_eye_coords(landmarks, RIGHT_EYE_INDICES)
            left_eye = get_eye_coords(landmarks, LEFT_EYE_INDICES)
            
            if len(right_eye) == 6 and len(left_eye) == 6:
                right_ear = calculate_ear(right_eye)
                left_ear = calculate_ear(left_eye)
                avg_ear = (right_ear + left_ear) / 2.0
                
                # EAR değerini analizöre gönder ve güncel durumu al
                blink_count, is_fatigued = blink_analyzer.analyze(avg_ear)
                
                # Ekrana temel bilgileri yazdır
                cv2.putText(frame, f"EAR: {avg_ear:.2f}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                cv2.putText(frame, f"Kirpma: {blink_count}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                
                # Uyku durumu tespit edildiyse kırmızı uyarı bas
                if is_fatigued:
                    cv2.putText(frame, "DIKKAT: UYUKLAMA TESPIT EDILDI!", (50, 250), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        cv2.imshow('Surucu Yorgunluk Tespit Sistemi - Faz 4', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()