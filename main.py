import cv2
import time
from detection.face_detector import FaceDetector
from detection.head_pose import HeadPoseEstimator
from analysis.eye_analysis import calculate_ear
from analysis.blink_analysis import BlinkAnalyzer
from analysis.yawn_analysis import YawnAnalyzer
from alerts.audio_alert import AudioAlert

RIGHT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
LEFT_EYE_INDICES = [362, 385, 387, 263, 373, 380]
MOUTH_INDICES = [78, 308, 13, 14]
HEAD_POSE_INDICES = [1, 152, 33, 263, 61, 291]

def get_coords(landmarks, indices):
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
    head_pose_estimator = HeadPoseEstimator()
    audio_alert = AudioAlert()

    if not cap.isOpened():
        print("Hata: Kamera açılamadı!")
        return

    # FPS hesaplaması için önceki zaman değişkeni
    pTime = 0

    while True:
        ret, frame = cap.read()
        if not ret: break

        frame = cv2.flip(frame, 1)
        frame, landmarks = detector.find_face_mesh(frame, draw=False)
        
        # Tehlike durumu bayrağı (her döngüde sıfırlanır)
        danger_detected = False

        if len(landmarks) != 0:
            right_eye = get_coords(landmarks, RIGHT_EYE_INDICES)
            left_eye = get_coords(landmarks, LEFT_EYE_INDICES)
            mouth = get_coords(landmarks, MOUTH_INDICES)
            head_points = get_coords(landmarks, HEAD_POSE_INDICES)
            
            # 1. Baş Pozisyonu İşlemleri
            if len(head_points) == 6:
                direction, pitch, yaw = head_pose_estimator.estimate_pose(head_points, frame.shape)
                cv2.putText(frame, f"Bas Yonu: {direction}", (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 105, 180), 2)
                
                if direction != "On":
                    danger_detected = True
                    cv2.putText(frame, "DIKKAT: YOLA BAKIN!", (50, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            # 2. Göz İşlemleri
            if len(right_eye) == 6 and len(left_eye) == 6:
                right_ear = calculate_ear(right_eye)
                left_ear = calculate_ear(left_eye)
                avg_ear = (right_ear + left_ear) / 2.0
                
                blink_count, is_fatigued = blink_analyzer.analyze(avg_ear)
                cv2.putText(frame, f"EAR: {avg_ear:.2f}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                cv2.putText(frame, f"Kirpma: {blink_count}", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                
                if is_fatigued:
                    danger_detected = True
                    cv2.putText(frame, "DIKKAT: UYUKLAMA TESPIT EDILDI!", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            # 3. Ağız İşlemleri
            if len(mouth) == 4:
                mar_value = yawn_analyzer.calculate_mar(mouth)
                yawn_count, is_yawning = yawn_analyzer.analyze(mar_value)
                
                cv2.putText(frame, f"MAR: {mar_value:.2f}", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                cv2.putText(frame, f"Esneme: {yawn_count}", (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                
                if is_yawning:
                    danger_detected = True
                    cv2.putText(frame, "ESNEME TESPIT EDILDI", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 3)

        # Eğer herhangi bir tehlike varsa alarm çal
        if danger_detected:
            audio_alert.trigger_alarm()

        # FPS Hesaplama ve Ekrana Yazdırma
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(frame, f"FPS: {int(fps)}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Arayüz başlığını güncelliyoruz
        cv2.imshow('Fatih Saltan - Surucu Yorgunluk Tespit Sistemi', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()