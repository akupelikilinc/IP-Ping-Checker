# IP Ping Checker - Docker Image
FROM python:3.11-slim

# Metadata
LABEL maintainer="IP Ping Checker"
LABEL description="Otomatik IP Ping Checker - Excel, Grafik, Zamanlama"
LABEL version="1.0"

# Çalışma dizini oluştur
WORKDIR /app

# Sistem paketlerini güncelle
RUN apt-get update && apt-get install -y \
    iputils-ping \
    dnsutils \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıklarını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY ping_checker.py .
COPY scheduler.py .
COPY app.py .
COPY templates templates

# Çalışma için klasör oluştur
RUN mkdir -p /app/data /app/logs

# Kullanıcı oluştur (security)
RUN useradd -m -u 1000 pinguser && chown -R pinguser:pinguser /app

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV WORKDIR=/app/data
ENV EXCEL_FILENAME=IP_Ping_Sonuclari.xlsx

# Port açıkla (gelecekteki API için)
EXPOSE 5000

# Ping için NET_RAW capability gerekli (Linux'ta)
# Bu capability docker-compose.yml'de ayarlanacak

# Kullanıcıya geç
USER pinguser

# Başlangıç komutunu ayarla - Flask web uygulaması (scheduler dahil)
CMD ["python", "app.py"]
