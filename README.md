# 🚗 Sürücü Yorgunluk ve Dikkat Dağınıklığı Tespit Sistemi

Bu proje, sürücülerin direksiyon başındaki yorgunluk, uyuklama ve dikkat dağınıklığı durumlarını gerçek zamanlı olarak tespit edip sesli uyarı veren ve bu verileri analiz için veritabanında saklayan kapsamlı bir bilgisayarlı görü (Computer Vision) sistemidir.

## 🌟 Öne Çıkan Özellikler

* **Gerçek Zamanlı Yüz ve Landmark Tespiti:** Google MediaPipe Face Mesh kullanılarak yüksek doğruluklu yüz haritalama.
* **Uyuklama Tespiti (EAR):** Göz Açıklık Oranı (Eye Aspect Ratio) hesaplanarak mikro uyku ve göz kapanma takibi.
* **Esneme Tespiti (MAR):** Ağız Açıklık Oranı (Mouth Aspect Ratio) ile yorgunluk belirtisi olan esnemelerin algılanması.
* **Dikkat Dağınıklığı Takibi:** OpenCV `solvePnP` algoritması ile baş pozisyonu (Head Pose Estimation) kestirimi yapılarak sürücünün yola bakıp bakmadığının (Sağ, Sol, Yukarı, Aşağı) analizi.
* **Asenkron Uyarı Sistemi:** Tehlike anında programın akışını (FPS) yavaşlatmadan çalışan sesli alarm mekanizması.
* **İzole Veritabanı ve Loglama:** Docker üzerinde koşan PostgreSQL veritabanı ile tespit edilen kritik anların zaman damgalı olarak kayıt altına alınması.
* **Sürüş Sonu Veri Analizi:** Pandas ve Matplotlib kullanılarak sürüş sırasındaki tehlike anlarının istatistiksel ve grafiksel raporlanması.

## 🛠️ Kullanılan Teknolojiler

* **Programlama Dili:** Python 3.11
* **Görüntü İşleme ve Yapay Zeka:** OpenCV, MediaPipe, NumPy
* **Veritabanı ve Altyapı:** PostgreSQL (Alpine), Docker, Docker Compose, psycopg2-binary
* **Veri Analizi ve Görselleştirme:** Pandas, Matplotlib
* **Diğer:** Pygame (asenkron ses yönetimi için)

## 📂 Proje Mimarisi

```text
driver-fatigue-detection/
├── alerts/                # Sesli uyarı modülleri
├── analysis/              # EAR, MAR ve yorgunluk/esneme algoritmaları
├── database/              # PostgreSQL bağlantı ve loglama işlemleri
├── detection/             # Yüz tespiti ve baş pozisyonu algoritmaları
├── reports/               # Sürüş sonu veri analizi ve grafik oluşturma
├── docker-compose.yml     # PostgreSQL veritabanı konteyner yapılandırması
├── main.py                # Ana uygulama döngüsü (Kamera ve arayüz)
├── read_logs.py           # Veritabanındaki son kayıtları terminale dökme
├── requirements.txt       # Gerekli Python kütüphaneleri
└── README.md              # Proje dokümantasyonu

##  🚀 Kurulum ve Çalıştırma

1. Projeyi İndirin ve Sanal Ortam Oluşturun
Projeyi bilgisayarınıza indirdikten sonra terminal üzerinden proje klasörüne girin. Kütüphane çakışmalarını önlemek için izole bir sanal ortam (venv) oluşturup aktifleştirin:

# Sanal ortam oluşturma
python -m venv venv

# Windows için sanal ortamı aktifleştirme komutu:
venv\Scripts\activate

# macOS/Linux için sanal ortamı aktifleştirme komutu:
source venv/bin/activate

2. Gereksinimleri Yükleyin
Sanal ortamınız aktifken (terminal satırının başında (venv) ibaresi varken), projenin çalışması için gerekli olan yapay zeka ve veri analizi kütüphanelerini tek seferde kurun:

pip install -r requirements.txt

3. Veritabanını Ayağa Kaldırın (Docker)
Sistemin yorgunluk ve dikkat dağınıklığı olaylarını kaydedebilmesi için arka planda Docker Desktop'ın açık olduğundan emin olun. Ardından izole PostgreSQL veritabanını başlatın (Yerel veritabanlarıyla çakışmaması için 5433 portunu kullanır):

docker-compose up -d

4. Sistemi Başlatın
Kameranızı bağlayın ve gerçek zamanlı yapay zeka analizini başlatan ana döngüyü çalıştırın:
(Sistem çalışırken uygulamadan güvenli bir şekilde çıkış yapmak için kamera penceresi seçiliyken klavyeden 'q' tuşuna basabilirsiniz.)

python main.py

5. Verileri Okuma ve Raporlama
Sistem tehlikeli durumları veritabanına loglar. Veritabanına düşen son 15 olayı (uyuklama, esneme, yön kayıpları) tarih ve saatleriyle anlık olarak terminalden okumak için:

python read_logs.py

Sürüş sonrasında tüm logları derleyip, pandas ve matplotlib kullanarak detaylı yorgunluk/dikkat grafiği (Sürüş Analiz Raporu) çıkarmak için:

python reports/generate_report.py

(Bu komut ekrana analiz grafiğini getirir ve aynı zamanda projeye surus_raporu_grafik.png adında yüksek çözünürlüklü bir dosya kaydeder.)

  Geliştirici
Muhammed Fatih Saltan

Fırat Üniversitesi Teknoloji Fakültesi - Yazılım Mühendisliği