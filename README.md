<div align="center">
  <img src="https://img.shields.io/github/languages/count/ibrahimyigitcetin/TraceWords?style=flat-square&color=blueviolet" alt="Language Count">
  <img src="https://img.shields.io/github/languages/top/ibrahimyigitcetin/TraceWords?style=flat-square&color=1e90ff" alt="Top Language">
  <img src="https://img.shields.io/github/last-commit/ibrahimyigitcetin/TraceWords?style=flat-square&color=ff69b4" alt="Last Commit">
  <img src="https://img.shields.io/github/license/ibrahimyigitcetin/TraceWords?style=flat-square&color=yellow" alt="License">
  <img src="https://img.shields.io/badge/Status-Active-green?style=flat-square" alt="Status">
  <img src="https://img.shields.io/badge/Contributions-Welcome-brightgreen?style=flat-square" alt="Contributions">
</div>

# 🕵️‍♂️ TraceWords — Dijital Anahtar Kelime Adli Taraması Aracı

**TraceWords**, `.txt`, `.json` ve `.csv` dosyalarını tarayarak belirli anahtar kelimelerin izini süren Python tabanlı bir adli bilişim analiz aracıdır. Dijital delil taraması, veri sızıntısı analizi veya duyarlı bilgi tespiti için kullanılabilir.

---

## 📌 Özellikler

- 🔍 `.txt`, `.json`, `.csv` dosyalarında anahtar kelime araması  
- ✅ **Tam eşleşme** veya **kapsayıcı eşleşme** seçenekleri  
- 🧠 Küçük/büyük harf farkını göz ardı eder  
- 🧪 Unicode hatalarına karşı dayanıklı dosya okuma  
- 📄 Otomatik adli rapor çıktısı oluşturur  
- ⚡ **Paralel işlem** ile hızlı tarama (ThreadPoolExecutor)  
- 📊 İlerleme çubuğu (tqdm) ile kullanıcı dostu arayüz  
- 🛡️ Hata yönetimi ve günlük kaydı (`forensic.log`)  
- 🗂 Genişletilebilir ve modüler yapı  

---

## 🚀 Kurulum

### 💻 Gereksinimler

- Python 3.6 veya üstü  
- Gerekli kütüphaneler: `pandas`, `tqdm`

Kütüphaneleri kurun:

```bash
pip install pandas tqdm
```

Depoyu klonlayın:

```bash
git clone https://github.com/ibrahimyigitcetin/TraceWords.git
cd TraceWords
```

---

## ▶️ Kullanım

**TraceWords**, hem interaktif modda hem de komut satırı argümanlarıyla çalıştırılabilir.

### 1. Interaktif Mod

Script’i çalıştırın:

```bash
python tracewords.py
```

Program sizden sırasıyla şunları isteyecektir:
1. Taranacak klasör yolu  
2. Virgülle ayrılmış anahtar kelimeler (örnek: `şifre,hata,kredi`)  
3. Eşleşme tipi:  
   - `e` → Tam eşleşme (kelime tam olarak geçiyorsa eşleşir)  
   - `h` → Kapsayıcı eşleşme (kelimenin geçtiği her durum eşleşir)  
4. Rapor dosyası zaten varsa, üzerine yazma onayı (`e/h`)  

### 2. Komut Satırı Argümanları

Komut satırı ile doğrudan tarama yapabilirsiniz:

```bash
python tracewords.py <klasör_yolu> -k <anahtar_kelimeler> [-e] [-o <rapor_dosyası>]
```

- `<klasör_yolu>`: Taranacak klasör yolu (örn: `C:\Belgeler\ornek`)  
- `-k`: Virgülle ayrılmış anahtar kelimeler (örn: `şifre,hata`)  
- `-e`: Tam eşleşme (isteğe bağlı)  
- `-o`: Rapor dosya adı (varsayılan: `forensic_report.txt`)  

---

### 💡 Örnek Kullanımlar

#### İnteraktif Mod Örneği

```bash
$ python tracewords.py
Taranacak klasör yolunu gir: C:\Belgeler\ornek
Aranacak kelimeleri virgülle ayırarak gir (örn: hata,şifre): parola,giriş,şifre
Tam eşleşme (e/h): e
sifre_raporu.txt zaten mevcut. Üzerine yazılsın mı? (e/h): e
```

**Çıktı:**
```
Taranan klasör: C:\Belgeler\ornek
Dosyalar taranıyor: 100%|██████████| 3/3 [00:00<00:00, 7.89dosya/s]
Taranan dosya sayısı: 3
Tarama süresi: 0.38 saniye
Rapor kaydedildi: C:\Belgeler\ornek\sifre_raporu.txt
```

#### Komut Satırı Örneği

```bash
python tracewords.py C:\Belgeler\ornek -k parola,giriş,şifre -e -o sifre_raporu.txt
```

**Çıktı:**
```
Taranan klasör: C:\Belgeler\ornek
Dosyalar taranıyor: 100%|██████████| 3/3 [00:00<00:00, 7.89dosya/s]
Taranan dosya sayısı: 3
Tarama süresi: 0.38 saniye
Rapor kaydedildi: C:\Belgeler\ornek\sifre_raporu.txt
```

---

## 📝 Rapor Formatı

Rapor, tarama sonuçlarını ve dosya bilgilerini içerir. Örnek:

```
Dijital Anahtar Kelime Adli Taraması Aracı Raporu
Tarih: 2025-07-09 17:19:45

Dosya: logs.csv (Son değiştirilme: Wed Jul 09 10:15:30 2025)
  - parola: 5 eşleşme
  - şifre: 2 eşleşme

Dosya: notlar.txt (Son değiştirilme: Wed Jul 09 09:45:12 2025)
  - giriş: 3 eşleşme
```

Eğer eşleşme bulunmazsa:
```
Hiçbir eşleşme bulunamadı.
```

---

## 🛠️ Geliştirme ve Katkı

- **Günlük Kayıtları**: Tarama işlemleri ve hatalar `forensic.log` dosyasına kaydedilir.  
- **Dosya Türleri**: Yeni dosya türleri eklemek için `read_file_content` fonksiyonunu genişletin.  
- **Katkı**: Pull request’ler ve sorun bildirimleri için GitHub reposunu ziyaret edin.

---

## ⚠️ Sınırlamalar

- Maksimum dosya boyutu: 100 MB (daha büyük dosyalar atlanır)  
- Desteklenen dosya türleri: `.txt`, `.json`, `.csv`  
- Unicode veya format hataları için dayanıklı okuma, ancak bozuk dosyalar atlanabilir  

---

## 📜 Lisans

MIT Lisansı ile lisanslanmıştır. Ayrıntılar için `LICENSE` dosyasına bakın.
