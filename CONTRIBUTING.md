# 🤝 Katkı Yapma Rehberi

TraceWords projesine katkıda bulunmak istiyorsanız, aşağıdaki rehber size yol gösterecektir.

## 🚀 Katkı Yapma Yolları

Projeye şu yollarla katkıda bulunabilirsiniz:

- **🧠 Kod Katkıları**: Anahtar kelime tarama, PII tespiti veya dijital adli bilişim özelliklerini geliştirebilir, hataları düzeltebilir veya performansı optimize edebilirsiniz.
- **📚 Dokümantasyon**: Mevcut dokümantasyonu iyileştirebilir veya kullanıcıların aracı anlamasına ve kullanmasına yardımcı olacak yeni kılavuzlar ekleyebilirsiniz.
- **🐞 Hata Raporları**: Araç kullanırken karşılaştığınız sorunları veya hataları bildirebilirsiniz.
- **💡 Özellik Önerileri**: GDPR/CCPA uyumluluğunu artıracak, yeni dosya formatlarını destekleyecek veya aracı daha kullanışlı hale getirecek özellikler önerebilirsiniz.

---

## ⚙️ Ortam Kurulumu

Projeye katkıda bulunmak için geliştirme ortamını yerel makinenizde kurmanız gerekir. Aşağıdaki adımları izleyin:

### 1. Depoyu Klonlayın

```bash
git clone https://github.com/ibrahimyigitcetin/TraceWords.git
cd TraceWords
```

### 2. Bağımlılıkları Yükleyin

Proje, Python 3.8 veya daha yüksek bir sürüm gerektirir. Gerekli paketleri şu komutla yükleyin:

```bash
pip install -r requirements.txt
```

### 3. Aracı Çalıştırın

TraceWords'ü şu komutla çalıştırabilirsiniz:

```bash
python tracewords.py
```

### 4. Virtual Environment (Önerilen)

Virtual environment kullanımı sistem temizliği için önerilir:

**Windows:**
```bash
python -m venv tracewords_env
tracewords_env\Scripts\activate
pip install -r requirements.txt
python tracewords.py /path/to/directory -k "password,admin,hack"
deactivate
```

**Linux/macOS:**
```bash
python3 -m venv tracewords_env
source tracewords_env/bin/activate
pip install -r requirements.txt
python tracewords.py /path/to/directory -k "password,admin,hack"
deactivate
```

---

## 🧑‍💻 Kodlama Standartları

Konsistens ve okunabilirlik sağlamak için lütfen aşağıdaki kodlama standartlarına uyun:

- Python kodları için **PEP 8** kurallarına uyun.
- Anlamlı değişken ve fonksiyon isimleri kullanın.
- Tüm fonksiyonlar ve sınıflar için **docstring** yazın.
- Gerektiğinde kodunuza açıklayıcı **yorumlar** ekleyin.
- GDPR/CCPA uyumluluğunu etkileyebilecek değişikliklerde veri gizliliği ilkelerine dikkat edin.

---

## 🔁 Pull Request Süreci

Değişikliklerinizi göndermeye hazır olduğunuzda şu adımları izleyin:

### 1. Yeni Bir Dal Oluşturun

```bash
git checkout -b feature/özellik-adınız
```

### 2. Değişikliklerinizi Kaydedin

```bash
git add .
git commit -m "Açıklayıcı mesajınızı buraya yazın"
```

### 3. GitHub’a Gönderin

```bash
git push origin feature/özellik-adınız
```

### 4. Pull Request Açın

GitHub deposuna gidin ve dalınızdan `main` dalına bir **pull request** açın.  
Değişikliklerinizi ve neden gerekli olduğunu açıkça tarif edin, özellikle GDPR/CCPA uyumluluğuyla ilgiliyse.

### 5. İnceleme Süreci

Pull request’iniz proje yöneticileri tarafından incelenecek.  
Geri bildirimlere göre düzenlemeler yapmaya hazır olun.

---

## 📄 Lisans

Bu proje **MIT Lisansı** altında lisanslanmıştır.  
Projeye katkıda bulunarak, katkılarınızın aynı lisans altında lisanslanacağını kabul etmiş olursunuz.  
Lisans detayları için `LICENSE.md` dosyasını inceleyin.

---

## 📌 Ek Notlar

- **📚 Referanslar**: Proje, GDPR ve CCPA gerekliliklerine uygun olarak geliştirilmiştir. Daha fazla bilgi için `README.md` ve ilgili yasal düzenlemeleri inceleyin.
- **📈 Potansiyel Geliştirme Alanları**: Yeni dosya formatı desteği (ör. `.pdf`, `.docx`), grafik kullanıcı arayüzü, çok dilli dokümantasyon veya yapay zeka tabanlı PII tespiti gibi özellikler projeyi daha geniş bir kitleye hitap edecek hale getirebilir.

---

## 📥 GitHub’a Ekleme Talimatları

Bu dosyayı GitHub’a eklemek için:

```bash
# Projenizin kök dizininde CONTRIBUTING.md adında bir dosya oluşturun
# Yukarıdaki içeriği dosyaya yapıştırın

git add CONTRIBUTING.md
git commit -m "Add CONTRIBUTING.md for contribution guidelines"
git push origin main
```

---

## 🙏 Teşekkürler

TraceWords projesine katkıda bulunmayı düşündüğünüz için teşekkür ederiz!  
Yardımlarınız, aracı daha güvenli ve kullanıcı dostu hale getirmek için çok değerli. Sorularınız veya ek özelleştirme talepleriniz olursa, lütfen bizimle iletişime geçin.
