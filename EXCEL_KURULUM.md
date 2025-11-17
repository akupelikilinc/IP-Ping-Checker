# Excel Ping Checker - VBA Makrosu Kurulum Kılavuzu

## 🎯 Hızlı Başlangıç

### 1. Excel Dosyası Oluşturma

Aşağıdaki adımları takip ederek Excel dosyasını ve makroları kurabilirsiniz:

#### **Manuel Kurulum (Tavsiye Edilen)**

1. **Excel'de yeni dosya oluşturun**
   - Excel açın
   - `Boş Çalışma Kitabı` seçin

2. **İlk satıra başlıkları yazın:**
   - `A1`: IP Adresi
   - `B1`: Ping
   - `C1`: Yanıt Süresi
   - `D1`: Cihaz Adı

3. **IP adreslerini ekleyin:**
   - `A2` ve sonraki satırlara IP adresleri yazın
   - Örnek:
     ```
     A2: 8.8.8.8
     A3: 1.1.1.1
     A4: 192.168.1.1
     ```

4. **VBA Makrosunu İçe Aktar**
   - Alt+F11 tuşlarını basarak VBA Editörünü açın
   - Sol tarafta "Microsoft Excel Objects" bölümünü göreceksiniz
   - Sağ tarafta boş bir alana sağ tıklayın → `Modülü İçe Aktar` seçin
   - `PingModule.bas` dosyasını seçin
   - (Veya kolay yolu: aşağıdaki kodu yapıştırabilirsiniz)

5. **Dosyayı Makro Etkin Olarak Kaydedin**
   - Dosya → Farklı Kaydet
   - Dosya adı: `IP_Ping_Sonuclari`
   - Dosya türü: `Excel Makro Etkin Çalışma Kitabı (.xlsm)`

### 2. Makroları Çalıştırma

#### **Otomatik Ping Kontrolü**
1. Menüde `Geliştirici` sekmesini açın (Görünürse)
2. `Makroları Çalıştır` (Macros) tıklayın
3. `OtomatikPingKontrol` seçin
4. `Çalıştır` (Run) tıklayın

**Veya Alt+F8** ile makro iletişim kutusunu açabilirsiniz.

#### **Grafik Oluşturma**
1. Ping kontrolü tamamlandıktan sonra
2. `Geliştirici` → `Makroları Çalıştır`
3. `GrafikOlustur` seçin
4. Yeni bir "Grafikler" sayfası oluşturulacak

#### **Sonuçları Temizleme**
- `SuturlariTemizle` makrosunu çalıştırarak eski sonuçları silebilirsiniz

---

## 📊 Excel Yapısı

Dosya bu şekilde olmalıdır:

```
╔════════════════╦═══════════════╦═════════════════╦════════════════╗
║ IP Adresi (A)  ║ Ping (B)      ║ Yanıt Süresi (C)║ Cihaz Adı (D)  ║
╠════════════════╬═══════════════╬═════════════════╬════════════════╣
║ 8.8.8.8        ║ Yanıt Var     ║ 12ms            ║ dns.google.com ║
║ 1.1.1.1        ║ Yanıt Var     ║ 15ms            ║ -              ║
║ 192.168.1.1    ║ Yanıt Yok     ║ -               ║ -              ║
╚════════════════╩═══════════════╩═════════════════╩════════════════╝
```

---

## 🎨 Formatlamalar

- **Başarılı (Yanıt Var):**
  - Arka Plan: 🟢 Yeşil (RGB: 146, 208, 80)
  - Yazı: **Kalın**, Siyah, Ortada

- **Başarısız (Yanıt Yok):**
  - Arka Plan: 🔴 Kırmızı (RGB: 255, 0, 0)
  - Yazı: **Kalın**, Beyaz, Ortada

- **Geçersiz IP:**
  - Arka Plan: ⚫ Gri
  - Yazı: Kalın, Ortada

---

## 🔧 Makrolarının Açıklaması

### 1. `OtomatikPingKontrol()`
- A sütunundaki tüm IP adresleri kontrol eder
- Her IP'ye ping atıp sonucu B sütununa yazar
- Yanıt süresini C sütununa, cihaz adını D sütununa yazar
- Otomatik olarak hücreleri renklendirir

### 2. `GrafikOlustur()`
- Ping sonuçlarından pasta grafiği oluşturur
- Yeni "Grafikler" sayfasına eklenir
- Yanıt veren vs vermeyen IP'leri karşılaştırır

### 3. `SuturlariTemizle()`
- Önceki ping sonuçlarını temizler
- Yeniden baştan kontrole başlamak için kullanılır

### 4. `PingHost()`
- Windows ping komutunu çalıştırır
- Sonuç ve yanıt süresini döndürür

### 5. `ExtractResponseTime()`
- Ping çıktısından yanıt süresini çıkarır

### 6. `IsValidIP()`
- IP adresinin geçerliliğini kontrol eder
- 0-255 aralığında 4 sayıyı kontrol eder

### 7. `GetDeviceName()`
- IP adresinin cihaz adını bulmaya çalışır
- nslookup komutu kullanır

---

## ⚙️ VBA Kodu Manuel Ekleme (İsteğe Bağlı)

Dosyayı `.xlsm` olarak kaydettin sonra:

1. Alt+F11 tuşlarını bas → VBA Editörü açılır
2. Proje penceresinde dosya adına sağ tıkla
3. `Modülü İçe Aktar` → `PingModule.bas` seçin

Veya:
1. VBA Editöründe Insert → Module
2. `PingModule.bas` dosyasının içeriğini yapıştır

---

## ❌ Sık Sorunlar ve Çözümleri

### "Makro bulunamadı" hatası
- Dosyayı `.xlsm` (Makro Etkin) olarak kaydettiğinizden emin olun

### "ActiveX Denetimi bulunamadı" hatası
- Excel'i yönetici olarak açın
- Office'i tamir edin: Kontrol Paneli → Program Ekle/Kaldır → Office → Hızlı Onarım

### Ping tüm IP'ler için "Yanıt Yok" gösteriyor
- Güvenlik Duvarı ping'i engelliyor olabilir
- Windows Defender ayarlarını kontrol edin
- Komut isteminde `ping 8.8.8.8` test edin

### "WScript.Shell" hatası
- Güvenlik ayarı makroları engelliyor olabilir
- Dosyayı Güvenilir Konumlara ekleyin (Dosya → Seçenekler → Güvenlik Merkezi)

---

## 📋 Kurulum Adımlarının Özeti

```
1. ✓ Excel dosyası oluş
2. ✓ Başlıkları yaz (A1:D1)
3. ✓ IP'leri ekle (A2 ve sonrası)
4. ✓ PingModule.bas'ı içe aktar
5. ✓ .xlsm olarak kaydet
6. ✓ OtomatikPingKontrol makrosını çalıştır
7. ✓ Sonuçları kontrol et
```

---

## 💡 İpuçları

- **Kısa kontrol:** 10-20 IP için ~30 saniye
- **Büyük listeler:** 100+ IP için birkaç dakika sürebilir
- **Harici IP'ler:** İnternet bağlantısı gerekir
- **Yerel IP'ler:** LAN bağlantısı gerekir
- **Dosya yedeklemesi:** Ping kontrol öncesi dosya kopyasını tutun

---

## 🚀 Otomatik Zamanlama (Windows Görev Planlayıcısı)

Excel makrolarını düzenli aralıklarla otomatik çalıştırmak için:

1. Görev Planlayıcısını aç (Başlat → "görev planlayıcısı")
2. Temel Görev Oluştur
3. Tetikleyici: Haftalık (her Pazartesi 09:00)
4. İşlem: Program başlat
   - Program: `C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE`
   - Bağımsız değişkenler: `/X "C:\Yol\IP_Ping_Sonuclari.xlsm" /m OtomatikPingKontrol`

---

**Versiyon:** 1.0  
**Son Güncelleme:** 12 Kasım 2025  
**Dil:** Türkçe
