<div align="center">
  <img src="https://img.shields.io/github/languages/count/ibrahimyigitcetin/TraceWords?style=flat-square&color=blueviolet" alt="Language Count">
  <img src="https://img.shields.io/github/languages/top/ibrahimyigitcetin/TraceWords?style=flat-square&color=1e90ff" alt="Top Language">
  <img src="https://img.shields.io/github/last-commit/ibrahimyigitcetin/TraceWords?style=flat-square&color=ff69b4" alt="Last Commit">
  <img src="https://img.shields.io/github/license/ibrahimyigitcetin/TraceWords?style=flat-square&color=yellow" alt="License">
  <img src="https://img.shields.io/badge/Status-Active-green?style=flat-square" alt="Status">
  <img src="https://img.shields.io/badge/Contributions-Welcome-brightgreen?style=flat-square" alt="Contributions">
</div>

# 🕵️‍♂️ TraceWords — Dijital Anahtar Kelime Adli Taraması Aracı

🔍 **Dijital Anahtar Kelime Adli Taraması Aracı v3.0**

TraceWords, dijital adli bilişim standartlarına uygun olarak tasarlanmış, dosyalar içerisinde anahtar kelime arama ve dijital kanıt toplama aracıdır. Güvenlik uzmanları, sistem yöneticileri ve dijital adli bilişim uzmanları için geliştirilmiştir.

## 🎯 Özellikler

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
- **Bağlam Çıkarma**: Bulunan kelimelerin etrafındaki içerik
- **Paralel İşleme**: Hızlı analiz için çoklu thread desteği
- **Detaylı Loglama**: Tüm işlemlerin kayıt altına alınması

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
| `--output` | `-o` | Rapor dosya adı | tracewords_report.txt |

### Örnek Kullanımlar

#### 1. Basit Arama
```bash
python tracewords.py /var/log -k "error,warning,critical"
```

#### 2. Tam Kelime Eşleşmesi
```bash
python tracewords.py /home/user/documents -k "password,admin" -e
```

#### 3. Regex Pattern Arama
```bash
python tracewords.py /var/www -k "\b\d{3}-\d{2}-\d{4}\b,email.*@.*\.com" -r
```

#### 4. Recursive Arama
```bash
python tracewords.py /home/user -k "confidential,secret" --recursive
```

#### 5. Özel Rapor Dosyası
```bash
python tracewords.py /logs -k "attack,intrusion" -o security_report.txt
```

## 📊 Rapor Formatı

TraceWords, her analiz sonrasında detaylı bir rapor oluşturur:

```
=======================================================================
TRACEWORDS — DİJİTAL ANAHTAR KELİME ADLİ TARAMASI RAPORU
=======================================================================
TraceWords v3.0 - Dijital Anahtar Kelime Adli Taraması Aracı
Analiz Tarihi: 2024-01-15 14:30:25
Aranan Terimler: password, admin, hack
Bulunan Dijital Kanıt Dosyası: 3
Analiz Edilen Dizin: /var/log

------------------------------------------------------------
DİJİTAL KANIT DOSYASI: auth.log
------------------------------------------------------------
Dosya Boyutu: 2,048 bytes
Son Değiştirilme: 2024-01-15 12:15:30
Oluşturulma Tarihi: 2024-01-14 09:00:00
MD5 Hash (Bütünlük): a1b2c3d4e5f6789012345678901234567

BULUNAN DİJİTAL KANITLAR:
  🔍 password: 5 eşleşme
  🔍 admin: 2 eşleşme

KANIT BAĞLAMLARI:
  [1] Satır 42:
      Eşleşen: Failed password attempt for user admin
  Bağlam:
      Jan 15 12:15:30 server sshd[1234]: Invalid user test
      Jan 15 12:15:30 server sshd[1234]: Failed password attempt for user admin
      Jan 15 12:15:31 server sshd[1234]: Connection closed by 192.168.1.100
```

## 🔧 Yapılandırma

### Sabitler
```python
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB maksimum dosya boyutu
LOG_FILE = "tracewords_log.txt"    # Log dosyası adı
SUPPORTED_FORMATS = (              # Desteklenen dosya formatları
    ".txt", ".json", ".csv", ".log", ".xml", 
    ".html", ".py", ".js", ".php", ".sql", 
    ".conf", ".ini"
)
```

### Loglama
TraceWords tüm işlemleri `tracewords_log.txt` dosyasına kaydeder:
- Analiz başlangıç/bitiş zamanları
- İşlenen dosya bilgileri
- Hata mesajları
- Sistem uyarıları

## 🛠️ Gelişmiş Özellikler

### Paralel İşleme
- 4 thread ile eşzamanlı dosya işleme
- Büyük dizinler için optimize edilmiş performans
- İlerleme çubuğu ile gerçek zamanlı durum

### Dijital Kanıt Bütünlüğü
- MD5 hash hesaplama
- Dosya metadata toplama
- Zaman damgası koruma
- Bağlam çıkarma

### Hata Yönetimi
- Graceful error handling
- Detaylı hata loglama
- Dosya erişim kontrolü
- Encoding sorunları çözümü

## 🚨 Güvenlik Notları

1. **Yetkilendirme**: Sadece yetkiniz olan dosyaları analiz edin
2. **Gizlilik**: Hassas bilgileri içeren raporları güvenli yerlerde saklayın
3. **Yasal Uyumluluk**: Yerel yasalara uygun olarak kullanın
4. **Veri Bütünlüğü**: Hash değerlerini doğrulayın

## 📝 Sürüm Notları

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

## 📄 Lisans

Bu proje MIT lisansı altında dağıtılmaktadır. Detaylar için [LICENSE](LICENSE) dosyasını inceleyiniz.

---

**TraceWords** - Dijital adli bilişim standartlarında anahtar kelime analizi aracı
