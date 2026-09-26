import cv2

def main():
    # Kamerayı başlat (0 varsayılan web kamerasını temsil eder)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Hata: Kamera açılamadı!")
        return

    print("Sistem başlatıldı. Çıkmak için 'q' tuşuna basın.")

    while True:
        # Kameradan anlık kareleri oku
        ret, frame = cap.read()
        
        if not ret:
            print("Hata: Görüntü alınamıyor.")
            break

        # Görüntüyü ekranda göster
        cv2.imshow('Surucu Yorgunluk Tespit Sistemi - Faz 1', frame)

        # Klavyeden 'q' tuşuna basıldığında döngüyü kır
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Kaynakları temizle ve pencereleri kapat
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()