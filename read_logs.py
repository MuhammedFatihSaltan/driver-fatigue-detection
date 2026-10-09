import psycopg2

def read_latest_logs():
    try:
        conn = psycopg2.connect(
            dbname="fatigue_logs",
            user="admin",
            password="adminpassword",
            host="localhost",
            port="5433"
        )
        cur = conn.cursor()
        
        # Veritabanından son 15 olayı en yeniden eskiye doğru çekiyoruz
        cur.execute("SELECT * FROM driver_events ORDER BY timestamp DESC LIMIT 15;")
        rows = cur.fetchall()
        
        print("\n--- SON 15 YORGUNLUK VE DIKKAT KAYDI ---")
        if not rows:
            print("Henüz veritabanına kaydedilmiş bir olay bulunmuyor.")
        else:
            for row in rows:
                print(f"ID: {row[0]:<4} | Olay: {row[1]:<20} | Deger: {row[2]:<15} | Zaman: {row[3]}")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Veritabani okuma hatasi: {e}")

if __name__ == "__main__":
    read_latest_logs()