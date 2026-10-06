import threading
import winsound
import time

class AudioAlert:
    def __init__(self):
        self.is_playing = False

    def _play_sound(self):
        self.is_playing = True
        # 2500 Hz frekansında 500 ms (yarım saniye) boyunca bip sesi çıkarır
        winsound.Beep(2500, 500)
        time.sleep(0.1) # Sesler arası kısa bekleme
        self.is_playing = False

    def trigger_alarm(self):
        # Eğer zaten bir ses çalmıyorsa yeni bir ses thread'i başlat
        if not self.is_playing:
            threading.Thread(target=self._play_sound, daemon=True).start()