<div align="center">
  <img src="https://img.shields.io/github/languages/count/ibrahimyigitcetin/TraceWords?style=flat-square&color=blueviolet" alt="Language Count">
  <img src="https://img.shields.io/github/languages/top/ibrahimyigitcetin/TraceWords?style=flat-square&color=1e90ff" alt="Top Language">
  <img src="https://img.shields.io/github/last-commit/ibrahimyigitcetin/TraceWords?style=flat-square&color=ff69b4" alt="Last Commit">
  <img src="https://img.shields.io/github/license/ibrahimyigitcetin/TraceWords?style=flat-square&color=yellow" alt="License">
  <img src="https://img.shields.io/badge/Status-Active-green?style=flat-square" alt="Status">
  <img src="https://img.shields.io/badge/Contributions-Welcome-brightgreen?style=flat-square" alt="Contributions">
</div>

# TraceWords

🔍 **GDPR/CCPA Uyumlu Dijital Adli Tarama Aracı v4.0**

TraceWords, veri gizliliği yasalarına uyumlu olarak tasarlanmış, dijital adli bilişim standartlarında anahtar kelime arama ve dijital kanıt toplama aracıdır. Güvenlik uzmanları, sistem yöneticileri ve dijital adli bilişim uzmanları için geliştirilmiştir.

## 🎯 Özellikler

### 🔒 Veri Gizliliği ve Yasal Uyumluluk
- **GDPR Uyumluluğu**: Avrupa Birliği Genel Veri Koruma Tüzüğü
- **CCPA Uyumluluğu**: California Tüketici Gizliliği Yasası
- **PII Otomatik Tespiti**: 12 farklı kişisel veri türü tanıma
- **Veri Maskeleme**: Hassas bilgilerin otomatik maskelenmesi
- **Kullanıcı Onay Sistemi**: Veri işleme için açık rıza
- **Veri Saklama Yönetimi**: Otomatik veri temizleme (90 gün)
- **Audit Loglama**: Tüm işlemlerin denetim kaydı

### 📂 Desteklenen Dosya Formatları
- **Metin dosyaları**: `.txt`, `.log`, `.conf`, `.ini`
- **Kod dosyaları**: `.py`, `.js`, `.php`, `.sql`
- **Markup dosyaları**: `.html`, `.xml`
- **Veri dosyaları**: `.json`, `.csv`

### 🔍 Arama Modları
- **Kısmi Eşleşme**: Kelime parçalarını da bulur
- **Tam Kelime Eşleşmesi**: Sadece tam kelime eşleşmelerini bulur
- **Regex Pattern Arama**: Gelişmiş pattern arama desteği

### 🛡️ Dijital Adli Bilişim Özellikleri
- **MD5 Hash Hesaplama**: Dosya bütünlüğü kontrolü
- **Metadata Toplama**: Dosya oluşturma/değiştirme tarihleri
- **Bağlam Çıkarma**: Bulunan kelimelerin etrafındaki içerik (PII maskelenmiş)
- **Paralel İşleme**: Hızlı analiz için çoklu thread desteği
- **Üçlü Loglama**: Ana, audit ve privacy logları
- **Oturum Takibi**: Her analiz için benzersiz session ID

### 🔐 PII Tespit Edilen Veri Türleri
- E-posta adresleri
- Telefon numaraları (ABD/Uluslararası)
- SSN (Sosyal Güvenlik Numarası)
- Kredi kartı numaraları
- IP adresleri
- MAC adresleri
- T.C. Kimlik numaraları
- IBAN numaraları
- Pasaport numaraları
- Doğum tarihleri
- URL'ler

## 📋 Gereksinimler

```bash
pip install pandas tqdm
```

### Python Modülleri
- `pandas`: CSV dosya işleme
- `tqdm`: İlerleme çubuğu
- `concurrent.futures`: Paralel işleme
- `hashlib`: Hash hesaplama
- `logging`: Loglama
- `uuid`: Oturum ID oluşturma
- `re`: Regex işlemleri

## 🚀 Kurulum

1. Repository'yi klonlayın:
```bash
git clone https://github.com/ibrahimyigitcetin/TraceWords.git
cd TraceWords
```

2. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```

3. TraceWords'ü çalıştırın:
```bash
python tracewords.py
```

## Virtual Environment ile Kurulum (Opsiyonel - Önerilen)

Virtual environment kullanımı zorunlu değildir ancak sistem temizliği için önerilir.

**Windows:**
```bash
# Virtual environment oluştur
python -m venv tracewords_env

# Virtual environment'ı aktifleştir
tracewords_env\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# TraceWords'ü çalıştır
python tracewords.py /path/to/directory -k "password,admin,hack"

# İşlem bittiğinde deaktif et
deactivate
```

**Linux/macOS:**
```bash
# Virtual environment oluştur
python3 -m venv tracewords_env

# Virtual environment'ı aktifleştir
source tracewords_env/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# TraceWords'ü çalıştır
python tracewords.py /path/to/directory -k "password,admin,hack"

# İşlem bittiğinde deaktif et
deactivate
```

## 💻 Kullanım

### Temel Kullanım
```bash
python tracewords.py /path/to/directory -k "password,admin,hack"
```

### Komut Satırı Parametreleri

| Parametre | Kısaltma | Açıklama | Varsayılan |
|-----------|----------|----------|------------|
| `directory` | - | Analiz edilecek dizin yolu | Zorunlu |
| `--keywords` | `-k` | Virgülle ayrılmış arama terimleri | Zorunlu |
| `--exact` | `-e` | Tam kelime eşleşmesi | False |
| `--regex` | `-r` | Regex pattern arama modu | False |
| `--recursive` | - | Alt dizinleri de analiz et | False |
| `--output` | `-o` | Rapor dosya adı | tracewords_privacy_report.txt |
| `--no-pii-mask` | - | PII maskelemeyi devre dışı bırak | False |
| `--anonymize` | - | Dosya isimlerini anonimleştir | False |
| `--cleanup` | - | Eski verileri temizle (GDPR uyumluluk) | False |

### Örnek Kullanımlar

#### 1. Basit GDPR Uyumlu Arama
```bash
python tracewords.py /var/log -k "error,warning,critical"
```

#### 2. PII Maskeleme ile Tam Kelime Eşleşmesi
```bash
python tracewords.py /home/user/documents -k "password,admin" -e
```

#### 3. Regex Pattern ile Kredi Kartı Tespiti
```bash
python tracewords.py /payment/data -k "\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})\b" -r
```

#### 4. Anonimleştirilmiş Recursive Arama
```bash
python tracewords.py /home/user -k "confidential,secret" --recursive --anonymize
```

#### 5. PII Maskeleme Olmadan Analiz
```bash
python tracewords.py /logs -k "attack,intrusion" --no-pii-mask -o security_report.txt
```

#### 6. GDPR Uyumlu Veri Temizliği
```bash
python tracewords.py --cleanup
```

## 📊 GDPR/CCPA Uyumlu Rapor Formatı

TraceWords, veri gizliliği yasalarına uygun detaylı rapor oluşturur:

```
================================================================================
TRACEWORDS — GDPR/CCPA UYUMLU DİJİTAL ADLİ TARAMA RAPORU
================================================================================
TraceWords v4.0 - GDPR/CCPA Uyumlu Dijital Adli Tarama Aracı
Analiz Tarihi: 2024-01-15 14:30:25
Oturum ID: 550e8400-e29b-41d4-a716-446655440000
Aranan Terimler: password, admin, hack
Bulunan Dijital Kanıt Dosyası: 3
Analiz Edilen Dizin: /var/log

VERİ GİZLİLİĞİ VE UYUMLULUK BİLGİLERİ
--------------------------------------------------
PII Maskeleme Durumu: Aktif
Veri Minimizasyonu: Aktif
Audit Loglama: Aktif
Sonuç Anonimleştirme: Pasif
Veri Saklama Süresi: 90 gün
Silinme Tarihi: 2024-04-15

KİŞİSEL VERİ (PII) TESPİT ÖZETİ
----------------------------------------
  🔒 E-posta Adresi: 5 adet
  🔒 Telefon No: 3 adet
  🔒 IP Adresi: 12 adet

⚠️  Tüm kişisel veriler maskelenmiştir ve orijinal değerler rapordan çıkarılmıştır.

----------------------------------------------------------------------
DİJİTAL KANIT DOSYASI: file_a1b2c3d4.log
----------------------------------------------------------------------
Dosya Boyutu: 2,048 bytes
Son Değiştirilme: 2024-01-15 12:15:30
Oluşturulma Tarihi: 2024-01-14 09:00:00
MD5 Hash (Bütünlük): a1b2c3d4e5f6789012345678901234567
Tespit Edilen PII Türleri: email, ip_address
PII Maskeleme Uygulandı: Evet

BULUNAN DİJİTAL KANITLAR:
  🔍 password: 5 eşleşme
  🔍 admin: 2 eşleşme

KANIT BAĞLAMLARI (PII MASKELENMİŞ):
  [1] Satır 42:
      Eşleşen: Failed password attempt for user admin
  Bağlam:
      Jan 15 12:15:30 server sshd[1234]: Invalid user test from [IP_ADDR_0]
      Jan 15 12:15:30 server sshd[1234]: Failed password attempt for user admin
      Jan 15 12:15:31 server sshd[1234]: Connection closed by [IP_ADDR_0]

================================================================================
GDPR/CCPA UYUMLULUK BİLDİRİMİ
==============================
Bu rapor, Avrupa Birliği Genel Veri Koruma Tüzüğü (GDPR) ve California
Tüketici Gizliliği Yasası (CCPA) gerekliliklerine uygun olarak hazırlanmıştır.

Veri İşleme İlkeleri:
• Kişisel veriler maskelenmiş ve anonimleştirilmiştir
• Veri minimizasyonu ilkesi uygulanmıştır
• Tüm işlemler audit loglarına kaydedilmiştir
• Yasal saklama süreleri uygulanmaktadır
• Veri sahibinin hakları korunmuştur

Veri Sahibi Hakları:
• Erişim hakkı (GDPR Madde 15, CCPA §1798.110)
• Düzeltme hakkı (GDPR Madde 16)
• Silme hakkı (GDPR Madde 17, CCPA §1798.105)
• Taşınabilirlik hakkı (GDPR Madde 20)
• İtiraz etme hakkı (GDPR Madde 21, CCPA §1798.120)
```

## 🔧 Yapılandırma

### GDPR/CCPA Uyumluluk Ayarları
```python
PRIVACY_SETTINGS = {
    "enable_pii_masking": True,           # PII maskeleme
    "enable_data_minimization": True,     # Veri minimizasyonu
    "enable_audit_logging": True,         # Audit loglama
    "retention_period_days": 90,          # Veri saklama süresi
    "anonymize_results": False,           # Sonuç anonimleştirme
    "require_consent": True,              # Kullanıcı onayı
    "enable_right_to_be_forgotten": True  # Unutulma hakkı
}
```

### Sabitler
```python
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB maksimum dosya boyutu
LOG_FILE = "tracewords.log"         # Ana log dosyası
AUDIT_LOG_FILE = "tracewords_audit.log"     # Audit log dosyası
PRIVACY_LOG_FILE = "tracewords_privacy.log" # Privacy log dosyası
```

### Üçlü Loglama Sistemi
TraceWords üç farklı log dosyası oluşturur:
1. **tracewords.log**: Ana sistem logları
2. **tracewords_audit.log**: Denetim kayıtları
3. **tracewords_privacy.log**: Veri gizliliği olayları

## 🛠️ Gelişmiş Özellikler

### GDPR/CCPA Uyumluluk
- Kullanıcı onay sistemi
- PII otomatik tespiti ve maskeleme
- Veri saklama süreleri yönetimi
- Audit trail oluşturma
- Veri minimizasyonu
- Anonimleştirme seçenekleri

### Paralel İşleme
- 4 thread ile eşzamanlı dosya işleme
- Büyük dizinler için optimize edilmiş performans
- İlerleme çubuğu ile gerçek zamanlı durum

### Dijital Kanıt Bütünlüğü
- MD5 hash hesaplama
- Dosya metadata toplama
- Zaman damgası koruma
- PII maskelenmiş bağlam çıkarma

### Hata Yönetimi
- Graceful error handling
- Detaylı hata loglama
- Dosya erişim kontrolü
- Encoding sorunları çözümü

## 🚨 Güvenlik ve Yasal Notlar

### Veri Gizliliği
1. **GDPR Uyumluluk**: AB vatandaşlarının verilerini işlerken GDPR gerekliliklerine uyun
2. **CCPA Uyumluluk**: California sakinlerinin verilerini işlerken CCPA gerekliliklerine uyun
3. **PII Koruma**: Kişisel tanımlayıcı bilgileri her zaman maskeleyin
4. **Veri Minimizasyonu**: Sadece gerekli verileri işleyin

### Güvenlik
1. **Yetkilendirme**: Sadece yetkiniz olan dosyaları analiz edin
2. **Gizlilik**: Hassas bilgileri içeren raporları güvenli yerlerde saklayın
3. **Yasal Uyumluluk**: Yerel yasalara uygun olarak kullanın
4. **Veri Bütünlüğü**: Hash değerlerini doğrulayın

### Veri Sahibi Hakları
- **Erişim Hakkı**: Veri sahipleri işlenen verilerine erişim talep edebilir
- **Düzeltme Hakkı**: Yanlış verilerin düzeltilmesini talep edebilir
- **Silme Hakkı**: Verilerinin silinmesini talep edebilir
- **Taşınabilirlik Hakkı**: Verilerini başka bir sisteme aktarabilir
- **İtiraz Hakkı**: Veri işlemeye itiraz edebilir

## 📝 Sürüm Notları

### v4.0 (GDPR/CCPA Uyumlu)
- GDPR ve CCPA uyumluluk özellikleri
- PII otomatik tespiti ve maskeleme (12 tür)
- Kullanıcı onay sistemi
- Üçlü loglama sistemi (ana, audit, privacy)
- Veri saklama süreleri yönetimi
- Otomatik veri temizleme
- Anonimleştirme seçenekleri
- Oturum takibi (Session ID)
- Yasal uyumluluk raporlaması

### v3.0
- Dijital adli bilişim standartları desteği
- MD5 hash hesaplama özelliği
- Gelişmiş bağlam çıkarma
- Paralel işleme optimizasyonu
- Detaylı rapor formatı

### v2.x
- Regex pattern desteği
- Recursive arama
- CSV/JSON dosya desteği

### v1.x
- Temel anahtar kelime arama
- Basit rapor oluşturma

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

Detaylar için [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) dosyasını inceleyiniz.

## 📄 Lisans

Bu proje MIT lisansı altında dağıtılmaktadır. Detaylar için [LICENSE.md](LICENSE.md) dosyasını inceleyiniz.

---

**TraceWords v4.0** - GDPR/CCPA uyumlu dijital adli bilişim standartlarında anahtar kelime analizi aracı

🔒 **Veri Gizliliği Yasalarına Uyumlu • PII Maskeleme • Audit Loglama • Yasal Uyumluluk**
