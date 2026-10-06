import cv2
from detection.face_detector import FaceDetector
from analysis.eye_analysis import calculate_ear
from analysis.blink_analysis import BlinkAnalyzer
from analysis.yawn_analysis import YawnAnalyzer

RIGHT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
LEFT_EYE_INDICES = [362, 385, 387, 263, 373, 380]
# Sırasıyla: Sol köşe, Sağ köşe, Üst iç dudak, Alt iç dudak
MOUTH_INDICES = [78, 308, 13, 14]

def get_coords(landmarks, indices):
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
    
    blink_analyzer = BlinkAnalyzer(ear_threshold=0.22, fatigue_frames=20)
    yawn_analyzer = YawnAnalyzer(mar_threshold=0.5, yawn_frames=15)

    if not cap.isOpened():
        print("Hata: Kamera açılamadı!")
        return

    while True:
        ret, frame = cap.read()
        if not ret: break

        frame, landmarks = detector.find_face_mesh(frame, draw=False)

        if len(landmarks) != 0:
            right_eye = get_coords(landmarks, RIGHT_EYE_INDICES)
            left_eye = get_coords(landmarks, LEFT_EYE_INDICES)
            mouth = get_coords(landmarks, MOUTH_INDICES)
            
            # Göz işlemleri
            if len(right_eye) == 6 and len(left_eye) == 6:
                right_ear = calculate_ear(right_eye)
                left_ear = calculate_ear(left_eye)
                avg_ear = (right_ear + left_ear) / 2.0
                
                blink_count, is_fatigued = blink_analyzer.analyze(avg_ear)
                
                cv2.putText(frame, f"EAR: {avg_ear:.2f}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                cv2.putText(frame, f"Kirpma: {blink_count}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                
                if is_fatigued:
                    cv2.putText(frame, "DIKKAT: UYUKLAMA TESPIT EDILDI!", (50, 250), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            # Ağız (Esneme) işlemleri
            if len(mouth) == 4:
                mar_value = yawn_analyzer.calculate_mar(mouth)
                yawn_count, is_yawning = yawn_analyzer.analyze(mar_value)
                
                cv2.putText(frame, f"MAR: {mar_value:.2f}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                cv2.putText(frame, f"Esneme: {yawn_count}", (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                
                if is_yawning:
                    cv2.putText(frame, "ESNEME TESPIT EDILDI", (50, 300), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 3)

        cv2.imshow('Surucu Yorgunluk Tespit Sistemi - Faz 5', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()