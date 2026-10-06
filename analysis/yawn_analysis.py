import math

def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

class YawnAnalyzer:
    def __init__(self, mar_threshold=0.5, yawn_frames=15):
        # Esneme sayılması için gereken ağız açıklık sınırı
        self.MAR_THRESHOLD = mar_threshold
        # Ağzın ne kadar süre açık kalması gerektiği (Kare sayısı)
        self.YAWN_FRAMES = yawn_frames
        
        self.open_frames = 0
        self.yawn_count = 0
        self.is_yawning = False

    def calculate_mar(self, mouth_landmarks):
        """
        Ağız açıklık oranını (MAR) hesaplar.
        mouth_landmarks: [sol_kose, sag_kose, ust_dudak, alt_dudak]
        """
        # Ağzın yatay genişliği
        h = calculate_distance(mouth_landmarks[0], mouth_landmarks[1])
        # Ağzın dikey açıklığı
        v = calculate_distance(mouth_landmarks[2], mouth_landmarks[3])
        
        if h == 0:
            return 0
            
        mar = v / h
        return mar

    def analyze(self, mar_value):
        if mar_value > self.MAR_THRESHOLD:
            self.open_frames += 1
            self.is_yawning = True
        else:
            # Ağız kapandığında, eğer daha önce yeterince uzun süre açık kaldıysa 1 esneme say
            if self.is_yawning and self.open_frames >= self.YAWN_FRAMES:
                self.yawn_count += 1
            
            self.is_yawning = False
            self.open_frames = 0
            
        return self.yawn_count, self.is_yawning