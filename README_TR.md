# 🌐 IP Ping Checker - Kullanım Kılavuzu

## 📋 Özet

Bu araç Excel dosyasındaki IP adreslerine otomatik olarak ping atarak sonuçları renkli hücrelerle görüntülemektedir.

**Özellikler:**
- ✅ Otomatik IP ping kontrolü
- ✅ Yeşil (Yanıt Var) / Kırmızı (Yanıt Yok) hücre renklendirmesi
- ✅ Yanıt süresi gösterimi
- ✅ Cihaz adı otomatik bulma
- ✅ Haftalık/günlük/aralık zamanlama
- ✅ Pasta ve bar grafikleri
- ✅ Detaylı raporlama

---

## 🚀 Hızlı Başlangıç

### 1. Kurulum

1. **Kurulum dosyasını çalıştırın:**
   ```
   kurulum.bat
   ```
   
   Veya terminal/PowerShell'de manuel olarak:
   ```powershell
   pip install -r requirements.txt
   ```

### 2. İlk Çalıştırma

**Bir kez çalıştırmak için:**
```powershell
python ping_checker.py
```

Bu komut:
- Eğer dosya yoksa, örnek IP'lerle "IP_Ping_Sonuclari.xlsx" oluşturur
- IP'lere ping atır
- Sonuçları hücrelerle renklendirir
- Grafikler oluşturur

---

## 📊 Excel Dosyası Yapısı

Dosya otomatik olarak bu yapıda oluşturulur:

| A | B | C | D |
|---|---|---|---|
| **IP Adresi** | **Ping** | **Yanıt Süresi** | **Cihaz Adı** |
| 8.8.8.8 | Yanıt Var | 12ms | dns.google.com |
| 192.168.1.1 | Yanıt Yok | - | - |
| ... | ... | ... | ... |

---

## 🎨 Formatlamalar

- **Başlık:** Mavi arka plan, beyaz yazı, **kalın**
- **Yanıt Var:** 🟢 Yeşil arka plan, siyah yazı, **kalın**
- **Yanıt Yok:** 🔴 Kırmızı arka plan, beyaz yazı, **kalın**
- **Tüm hücreler:** Ortaya hizalanmış

---

## ⏰ Otomatik Zamanlama

`scheduler.py` dosyasını kullanarak otomatik ping kontrolü yapabilirsiniz.

### Seçenek 1: Haftalık Çalışma (Pazartesi 09:00)
```powershell
python scheduler.py
```

Dosyada şu satırı değiştirerek gün/saat ayarlayabilirsiniz:
```python
scheduler.schedule_weekly(day_of_week="monday", hour=9, minute=0)
```

**Örnek:**
```python
# Her Cuma saat 14:30'da çalışsın
scheduler.schedule_weekly(day_of_week="friday", hour=14, minute=30)
```

### Seçenek 2: Günlük Çalışma
Şu satırları değiştirin:
```python
# scheduler.schedule_weekly(day_of_week="monday", hour=9, minute=0)  # Bunu yorum satırı yapın
scheduler.schedule_daily(hour=9, minute=0)  # Bunu etkinleştirin
```

### Seçenek 3: Belirli Aralıklarla Çalışma
```python
# Her 6 saatte bir:
scheduler.schedule_interval(hours=6)

# Her 30 dakikada bir:
scheduler.schedule_interval(minutes=30)
```

---

## 🛠️ Dosya Yapısı Açıklaması

```
IPTEST/
├── ping_checker.py         # Ana program - ping kontrolü yaptığı script
├── scheduler.py            # Otomatik zamanlama scripti
├── requirements.txt        # Gerekli Python paketleri
├── kurulum.bat            # Otomatik kurulum dosyası
├── README_TR.md           # Bu dosya
└── IP_Ping_Sonuclari.xlsx # Oluşturulan Excel dosyası (otomatik)
```

---

## 💻 Komut Örnekleri

### PowerShell'de Çalıştırma

```powershell
# 1. Dizine gitmek (isteğe bağlı)
cd "c:\Users\akupelikilinc\Masaüstü\IPTEST"

# 2. Tek seferlik ping kontrolü
python ping_checker.py

# 3. Otomatik zamanlama (arka planda çalışır, Ctrl+C ile durdurun)
python scheduler.py
```

---

## 🔧 Gelişmiş Kullanım

### Kendi Excel Dosyanızı Kullanmak

`ping_checker.py` dosyasında şu satırı değiştirin:

```python
excel_file = r"c:\Users\akupelikilinc\Masaüstü\IPTEST\IP_Ping_Sonuclari.xlsx"
```

Örneğin:
```python
excel_file = r"C:\Users\Adınız\Documents\Benim_IP_Listesi.xlsx"
```

### IP'leri Manuel Olarak Ekleme

1. Excel dosyasını açın (`IP_Ping_Sonuclari.xlsx`)
2. A sütununa IP adresleri yazın
3. Dosyayı kaydedin
4. `python ping_checker.py` komutunu çalıştırın

Örnek:
```
A2: 8.8.8.8
A3: 1.1.1.1
A4: 192.168.1.1
A5: 10.0.0.1
```

---

## 📈 Grafikler

Ping kontrolü tamamlandıktan sonra:
- **Pasta Grafiği:** Yanıt veren vs vermeyen IP'lerin oranı
- **Bar Grafiği:** Yanıt veren vs vermeyen IP sayıları

Grafikler otomatik olarak "Grafikler" adlı yeni bir sayfaya eklenir.

---

## ❌ Sık Yapılan Hatalar

### "Python bulunamadı" hatası
- **Çözüm:** Python'u yükleyin veya PATH'e ekleyin
- https://www.python.org/downloads/

### "openpyxl modülü bulunamadı" hatası
- **Çözüm:** 
  ```powershell
  pip install openpyxl
  ```

### "schedule modülü bulunamadı" hatası
- **Çözüm:**
  ```powershell
  pip install schedule
  ```

### Ping tüm IP'ler için "Yanıt Yok" gösteriyor
- **Nedeni:** Firewall/güvenlik duvarı ping'i engelliyor olabilir
- **Çözüm:** Windows Defender Güvenlik Duvarı ayarlarını kontrol edin

### Dosya kilidi hatası
- **Nedeni:** Excel dosyası açık olabilir
- **Çözüm:** Excel dosyasını kapatın ve tekrar çalıştırın

---

## 🔐 Güvenlik Notları

- Bu araç sadece ping atarak cihazların ulaşılabilir olup olmadığını kontrol eder
- İnternet bağlantısı gerektirir
- Harici IP'lere ping atılabilir
- Yerel IP'ler (192.168.x.x, 10.0.0.x) için VPN/LAN bağlantısı gerekebilir

---

## 📞 Sorun Giderme

### Program başlatıldığında başlı başına sıkıntı varsa:

```powershell
# Python sürümünü kontrol edin
python --version

# Paketleri yeniden yükleyin
pip install --upgrade -r requirements.txt

# Dosya izinlerini kontrol edin (Yönetici olarak çalıştırın)
```

---

## 🎓 İpuçları

- **Büyük listeler:** 100+ IP için ping işlemi biraz zaman alabilir
- **Zamanlama:** Sunucu/cihazlar için 06:00 ve 18:00 arası kontrol et
- **Raporlama:** Excel dosyasını Outlook'a ekleyerek rapor gönderebilirsiniz
- **Yedekleme:** Eski sonuçları saklamak için Excel dosyasını düzenli yedekleyin

---

**Version:** 1.0  
**Son Güncelleme:** 12 Kasım 2025  
**Dil:** Türkçe
