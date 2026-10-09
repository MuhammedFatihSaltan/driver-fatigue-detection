import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

def generate_post_drive_report():
    try:
        # Veritabanına bağlan
        conn = psycopg2.connect(
            dbname="fatigue_logs",
            user="admin",
            password="adminpassword",
            host="localhost",
            port="5433"
        )
        
        # Verileri doğrudan Pandas DataFrame olarak çekiyoruz
        query = "SELECT event_type, timestamp FROM driver_events"
        df = pd.read_sql_query(query, conn)
        conn.close()

        if df.empty:
            print("Veritabanında analiz edilecek kayıt bulunamadı.")
            return

        # Verileri olay türüne göre grupla ve toplam sayılarını al
        event_counts = df['event_type'].value_counts()

        # Çubuk Grafiği (Bar Chart) Oluşturma
        plt.figure(figsize=(10, 6))
        
        # Olay türlerine göre renk belirleme
        colors = []
        for event in event_counts.index:
            if event == "Uyuklama": colors.append('red')
            elif event == "Esneme": colors.append('orange')
            else: colors.append('blue') # Dikkat Dağınıklığı

        bars = plt.bar(event_counts.index, event_counts.values, color=colors)

        # Grafik Tasarım Detayları
        plt.title('Surus Sonu Yorgunluk ve Dikkat Analiz Raporu', fontsize=14, fontweight='bold')
        plt.xlabel('Olay Turu', fontsize=12)
        plt.ylabel('Toplam Olay Sayisi', fontsize=12)
        plt.yticks(range(0, max(event_counts.values) + 3)) # Y eksenini tam sayı yap
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Barların tepe noktasına sayıları yazdır
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, int(yval), 
                     ha='center', va='bottom', fontsize=12, fontweight='bold')

        # Grafiği rapor olarak proje dizinine kaydet
        plt.tight_layout()
        plt.savefig('surus_raporu_grafik.png', dpi=300)
        print("Rapor basariyla olusturuldu ve 'surus_raporu_grafik.png' olarak kaydedildi.")
        
        # Ekranda göster
        plt.show()

    except Exception as e:
        print(f"Rapor olusturma hatasi: {e}")

if __name__ == "__main__":
    generate_post_drive_report()