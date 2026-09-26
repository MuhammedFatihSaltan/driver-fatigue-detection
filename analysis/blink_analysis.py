class BlinkAnalyzer:
    def __init__(self, ear_threshold=0.22, fatigue_frames=20):
        # Gözün kapalı sayılacağı EAR eşiği (Kendi göz yapına göre 0.20 - 0.25 arası değiştirebilirsin)
        self.EAR_THRESHOLD = ear_threshold
        # Alarmın tetiklenmesi için gözün kapalı kalması gereken kare sayısı
        self.FATIGUE_FRAMES = fatigue_frames
        
        self.closed_frames = 0
        self.blink_count = 0
        self.is_fatigued = False

    def analyze(self, ear_value):
        # Göz kapalıysa
        if ear_value < self.EAR_THRESHOLD:
            self.closed_frames += 1
            # Belirlenen süreden fazla kapalı kaldıysa yorgunluk alarmını tetikle
            if self.closed_frames >= self.FATIGUE_FRAMES:
                self.is_fatigued = True
        # Göz açıksa
        else:
            # Göz açıldığında, eğer daha önce kapalı kaldıysa ve bu süre yorgunluk sınırından azsa kırpma say
            if 1 <= self.closed_frames < self.FATIGUE_FRAMES:
                self.blink_count += 1
            
            # Sayacı ve alarmı sıfırla
            self.closed_frames = 0
            self.is_fatigued = False

        return self.blink_count, self.is_fatigued