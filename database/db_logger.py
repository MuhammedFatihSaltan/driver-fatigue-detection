import psycopg2
from datetime import datetime

class DatabaseLogger:
    def __init__(self):
        # Docker üzerindeki PostgreSQL bağlantı bilgileri
        self.conn_params = {
            "dbname": "fatigue_logs",
            "user": "admin",
            "password": "adminpassword",
            "host": "localhost",
            "port": "5433"  # 5432 yerine 5433 yaptık
        }
        self.conn = None
        self.setup_database()

    def connect(self):
        try:
            if self.conn is None or self.conn.closed:
                self.conn = psycopg2.connect(**self.conn_params)
            return self.conn
        except Exception as e:
            print(f"Veritabanı bağlantı hatası: {e}")
            return None

    def setup_database(self):
        """Uygulama ilk çalıştığında tablo yoksa oluşturur."""
        conn = self.connect()
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS driver_events (
                            id SERIAL PRIMARY KEY,
                            event_type VARCHAR(50) NOT NULL,
                            event_value VARCHAR(50),
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                conn.commit()
            except Exception as e:
                print(f"Tablo oluşturma hatası: {e}")
            finally:
                conn.close()

    def log_event(self, event_type, event_value=""):
        """Tespit edilen olayı (Uyku, Esneme, Dikkat Dağınıklığı) DB'ye yazar."""
        conn = self.connect()
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO driver_events (event_type, event_value, timestamp) VALUES (%s, %s, %s)",
                        (event_type, str(event_value), datetime.now())
                    )
                conn.commit()
            except Exception as e:
                print(f"Log yazma hatası: {e}")
            finally:
                conn.close()