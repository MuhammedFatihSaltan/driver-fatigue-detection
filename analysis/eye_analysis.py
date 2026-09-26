import math

def calculate_distance(point1, point2):
    """İki nokta (x,y) arasındaki Öklid mesafesini hesaplar."""
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def calculate_ear(eye_landmarks):
    """
    Göz açıklık oranını (EAR) hesaplar.
    eye_landmarks: Gözü çevreleyen 6 noktanın (x,y) koordinat listesi
    """
    # Gözün dikey mesafelerini hesapla
    v1 = calculate_distance(eye_landmarks[1], eye_landmarks[5])
    v2 = calculate_distance(eye_landmarks[2], eye_landmarks[4])
    
    # Gözün yatay mesafesini hesapla
    h = calculate_distance(eye_landmarks[0], eye_landmarks[3])
    
    # EAR formülü
    ear = (v1 + v2) / (2.0 * h)
    return ear