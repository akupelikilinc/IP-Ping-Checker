# 🐳 IP Ping Checker - Docker Rehberi

## 📋 Özet

Docker ile IP Ping Checker'ı container'da çalıştırmak için gereken rehber.

**Avantajlar:**
- ✅ Tüm platformlarda aynı ortam
- ✅ Python kuruluma gerek yok
- ✅ Kolay deployment
- ✅ Scalable
- ✅ Izole çalışma ortamı

---

## 🛠️ Gereksinimler

1. **Docker Desktop** (Windows/Mac) veya **Docker Engine** (Linux)
   - İndir: https://www.docker.com/products/docker-desktop
   - Kurulu olup olmadığını kontrol et: `docker --version`

2. **Docker Compose** (çoğu zaman Docker Desktop'ta gelen)
   - Kontrol: `docker-compose --version`

---

## 🚀 Hızlı Başlangıç

### 1. Docker Image'ı Oluştur

```bash
# Klasöre git
cd c:\Users\akupelikilinc\Masaüstü\IPTEST

# Image'ı build et
docker build -t ip-ping-checker:1.0 .
```

Çıktı:
```
Successfully built abc123def456
Successfully tagged ip-ping-checker:1.0
```

### 2. Container'ı Çalıştır

**Seçenek A: Docker Compose (Tavsiye Edilen)**
```bash
docker-compose up -d
```

**Seçenek B: Docker Komut Satırı**
```bash
docker run -d \
  --name ip-ping-checker \
  -v ./data:/app/data \
  -v ./logs:/app/logs \
  --restart unless-stopped \
  ip-ping-checker:1.0
```

### 3. Çalıştığını Kontrol Et

```bash
# Container'ları listele
docker ps

# Log'ları gör
docker logs ip-ping-checker

# Log'ları canlı izle
docker logs -f ip-ping-checker
```

### 4. Container'ı Durdur

```bash
docker-compose down

# Veya
docker stop ip-ping-checker
docker rm ip-ping-checker
```

---

## 📂 Dosya Yapısı

```
IPTEST/
├── Dockerfile              # Image tanımı
├── docker-compose.yml      # Compose yapılandırması
├── .dockerignore            # Docker'ın ignore edeceği dosyalar
├── ping_checker.py         # Ana script
├── scheduler.py            # Zamanlama
├── requirements.txt        # Bağımlılıklar
├── data/                   # 📁 Excel dosyaları (mount)
├── logs/                   # 📁 Log dosyaları (mount)
└── ...
```

---

## 🔧 Konfigürasyon

### docker-compose.yml Açıklaması

```yaml
services:
  ip-ping-checker:
    build: .                    # Dockerfile'ı build et
    container_name: ip-ping-checker
    
    environment:
      PYTHONUNBUFFERED: 1       # Python buffer devre dışı
      TZ: Europe/Istanbul       # Zaman dilimi
    
    volumes:
      - ./data:/app/data        # Excel dosyaları
      - ./logs:/app/logs        # Log dosyaları
    
    restart: unless-stopped     # Otomatik restart
    
    deploy:
      resources:
        limits:
          cpus: '1'             # Max 1 CPU
          memory: 512M          # Max 512MB RAM
```

---

## 💾 Veri Saklama

### Volumes (Önerilir)

Container durdurulsa bile veri kalıcı olur:

```bash
# ./data klasörü → /app/data (container)
# ./logs klasörü → /app/logs (container)
```

Excel dosyaları ve log'lar bilgisayarında kalır:
```
data/
  ├── IP_Ping_Sonuclari.xlsx
  ├── IP_Ping_Sonuclari_backup.xlsx
  └── ...

logs/
  ├── ping_2025-11-12.log
  └── ...
```

---

## 🖥️ Container'a Erişim

### Container İçinde Komut Çalıştır

```bash
# Bash shell'e gir
docker exec -it ip-ping-checker /bin/bash

# Dosyaları listele
docker exec ip-ping-checker ls -la /app/data

# Python scripti çalıştır
docker exec ip-ping-checker python ping_checker.py
```

### Log Dosyalarını Görüntüle

```bash
# Son 100 satır
docker logs --tail 100 ip-ping-checker

# Son 30 dakikanın log'ları
docker logs --since 30m ip-ping-checker

# Canlı log takibi (Ctrl+C ile çık)
docker logs -f ip-ping-checker
```

---

## 📊 Özel Yapılandırmalar

### Çevre Değişkenleri Değiştir

`docker-compose.yml`'de `environment` bölümünü düzenle:

```yaml
environment:
  PYTHONUNBUFFERED: 1
  TZ: Europe/Istanbul
  PING_TIMEOUT: 2000       # ms cinsinden
  LOG_LEVEL: DEBUG         # DEBUG, INFO, WARNING
```

### CPU/RAM Limiti Değiştir

```yaml
deploy:
  resources:
    limits:
      cpus: '2'            # 2 CPU'ya çıkar
      memory: 1G           # 1GB RAM'a çıkar
```

### Port Açmak (API İçin)

```yaml
ports:
  - "5000:5000"            # Host:Container
```

---

## 🚀 Üretim Ortamı (Production)

### Güvenlikli Yapılandırma

```yaml
services:
  ip-ping-checker:
    build: .
    container_name: ip-ping-checker
    
    # Güvenlik
    read_only: true                    # Dosya sistemi read-only
    cap_drop:
      - ALL
    cap_add:
      - NET_RAW                        # Ping için gerekli
    
    # Network
    networks:
      - ping-network
    
    # Restart
    restart: always
    
    # Health check
    healthcheck:
      test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    
    # Resource limits
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M

networks:
  ping-network:
    driver: bridge
```

---

## 🐳 Docker Hub'a Push (Paylaşım)

### Docker Hub Hesabı Oluştur

1. https://hub.docker.com adresine git
2. Hesap oluştur

### Image'ı Push Et

```bash
# Docker'a giriş yap
docker login

# Image'ı etiketle
docker tag ip-ping-checker:1.0 username/ip-ping-checker:1.0

# Push et
docker push username/ip-ping-checker:1.0
```

Başkaları kullanabilir:
```bash
docker run -d username/ip-ping-checker:1.0
```

---

## 🔍 Sorun Giderme

### "Docker command not found"
```
Windows: Docker Desktop'ı yükle ve yeniden başlat
Mac: Docker Desktop'ı yükle
Linux: sudo apt-get install docker.io docker-compose
```

### "Cannot connect to Docker daemon"
```
Windows/Mac: Docker Desktop'ı başlat
Linux: sudo systemctl start docker
```

### "Permission denied while trying to connect to Docker daemon"
```
Linux: sudo usermod -aG docker $USER
       # Yeniden giriş yap
```

### Container başlamazsa
```bash
# Log'ları detaylı gör
docker logs ip-ping-checker

# Container durumunu kontrol et
docker ps -a

# Container'ı yeniden başlat
docker restart ip-ping-checker

# Container'ı sil ve yeniden oluştur
docker-compose down
docker-compose up -d
```

### Veri yazılamıyorsa
```bash
# Klasör izinlerini kontrol et
ls -la ./data
ls -la ./logs

# Docker kullanıcısı izni ver (Linux)
sudo chown -R 1000:1000 ./data ./logs
```

---

## 📈 İleri Kullanım

### Multiple Containers

```bash
# Production ortamı
docker-compose -f docker-compose.prod.yml up -d

# Development ortamı
docker-compose -f docker-compose.dev.yml up -d
```

### CI/CD Pipeline (GitHub Actions)

```yaml
name: Docker Build and Push

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: docker/setup-buildx-action@v1
      - uses: docker/build-push-action@v2
        with:
          push: true
          tags: username/ip-ping-checker:latest
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ip-ping-checker
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ip-ping-checker
  template:
    metadata:
      labels:
        app: ip-ping-checker
    spec:
      containers:
      - name: ip-ping-checker
        image: ip-ping-checker:1.0
        resources:
          limits:
            memory: "512Mi"
            cpu: "500m"
        volumeMounts:
        - name: data
          mountPath: /app/data
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: ping-data-pvc
```

---

## 📚 Faydalı Docker Komutları

```bash
# Image'ları listele
docker images

# Container'ları listele (tümü)
docker ps -a

# Container'ı kaldır
docker rm container_id

# Image'ı kaldır
docker rmi ip-ping-checker:1.0

# Container İçinden Dosya Kopyala
docker cp ip-ping-checker:/app/data/file.xlsx ./

# Bilgisayardan Container'a Dosya Kopyala
docker cp ./data/file.xlsx ip-ping-checker:/app/data/

# İstatistikleri göster
docker stats

# Network'ü göster
docker network ls

# Volume'ları göster
docker volume ls
```

---

## ✅ Kontrol Listesi

```
☐ Docker kurulu ve çalışıyor
☐ docker-compose.yml dosyası konfigüre edildim
☐ ./data ve ./logs klasörleri oluşturdum
☐ docker build komutu başarılı oldu
☐ docker-compose up -d ile başlattım
☐ docker logs ile çalıştığını kontrol ettim
☐ ./data klasöründe Excel dosyası var mı kontrol ettim
☐ Container'ı durdurdum ve veri kalıcı mı kontrol ettim
```

---

## 🎯 Sonraki Adımlar

1. **Web Dashboard**: Flask/Django ile web arayüzü
2. **API**: RESTful API ile remote erişim
3. **Monitoring**: Prometheus + Grafana
4. **Clustering**: Docker Swarm/Kubernetes
5. **CI/CD**: GitHub Actions ile otomatik deploy

---

## 📞 Yardım

Sorun mu yaşıyorsun?

```bash
# Tüm çalışan container'ları göster
docker ps

# Container log'larını canlı izle
docker logs -f ip-ping-checker

# Container içine gir
docker exec -it ip-ping-checker /bin/bash
```

---

**Versiyon:** 1.0  
**Dil:** Türkçe  
**Tarih:** 12 Kasım 2025

**Başarılar! 🐳**
