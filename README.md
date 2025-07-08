# 🕵️‍♂️ TraceWords — Dijital Anahtar Kelime Adli Taraması Aracı

**TraceWords**, `.txt`, `.json` ve `.csv` dosyalarını tarayarak belirli anahtar kelimelerin izini süren Python tabanlı bir adli bilişim analiz aracıdır. Dijital delil taraması, veri sızıntısı analizi veya duyarlı bilgi tespiti için kullanılabilir.

---

## 📌 Özellikler

- 🔍 `.txt`, `.json`, `.csv` dosyalarında kelime araması yapar  
- ✅ **Tam eşleşme** veya **kapsayıcı eşleşme** seçenekleri  
- 🧠 Küçük/büyük harf farkını göz ardı eder  
- 🧪 Dosya içeriğini Unicode hatalarına karşı dayanıklı şekilde okur  
- 📄 Otomatik olarak adli rapor çıktısı oluşturur  
- 🗂 Genişletilebilir yapıda, kolay modifiye edilebilir  

---

## 🚀 Kurulum

### 💻 Gereksinimler

- Python 3.x  
- `pandas` kütüphanesi

Pandas'ı kurun:

```bash
pip install pandas
```
Repo'yu klonlayın:

```bash
git clone https://github.com/ibrahimyigitcetin/TraceWords.git
cd TraceWords
```

---

## ▶️ Kullanım

Script’i terminal veya komut satırında çalıştır:

```
python tracewords.py
```

Program sizden sırasıyla aşağıdaki bilgileri isteyecektir:

1. Taranacak klasör yolu  
2. Virgülle ayrılmış anahtar kelimeler (örnek: `şifre,hata,kredi`)  
3. Eşleşme tipi:  
   - `e` → tam eşleşme (kelime tam olarak geçiyorsa eşleşir)  
   - `h` → kapsayıcı eşleşme (kelimenin geçtiği her durum eşleşir)  
4. Rapor dosyasının adı (örnek: `rapor.txt`)  

---

### 💡 Örnek Kullanım Şablonu

```
Taranacak klasör yolunu gir: C:\Belgeler\ornek
Aranacak kelimeleri virgülle ayırarak gir (örn: hata,şifre): parola,giriş,şifre
Tam eşleşme (e/h): e
Rapor dosya adını gir (örn: rapor.txt): sifre_raporu.txt
```

Programın çıktısı aşağıdaki gibi olacaktır:

```
Taranan klasör: C:\Belgeler\ornek
Tarama: logs.csv
Tarama: config.json
Tarama: notlar.txt
Taranan dosya sayısı: 3
Tarama süresi: 0.38 saniye
Rapor kaydedildi: C:\Belgeler\ornek\sifre_raporu.txt
```
