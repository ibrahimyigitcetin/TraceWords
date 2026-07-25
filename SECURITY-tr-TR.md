# 🛡️ Güvenlik Politikası

TraceWords, dijital adli bilişim ve GDPR/CCPA uyumluluk süreçlerinde kullanılan bir araç olduğundan, kendi güvenlik açıklarımızı da aynı ciddiyetle ele alıyoruz. Bu belge, desteklenen sürümleri ve bir güvenlik açığını nasıl bildirebileceğinizi açıklar.

---

## 📦 Desteklenen Sürümler

TraceWords **v6.0** ile birlikte, salt versiyon numarası artışından çok bir **ürünleşme** aşamasına geçiyor: daha uzun destek pencereleri, daha net bir yama politikası ve bu belgede tarif edilen resmi bir bildirim süreci.

| Sürüm    | Destekleniyor mu? | Notlar |
|----------|:---:|---|
| 6.0.x    | :white_check_mark: | Güncel sürüm — güvenlik yamaları öncelikli olarak buraya uygulanır |
| 5.0.x    | :warning: | Yalnızca **kritik/yüksek önem düzeyli** güvenlik açıkları için, v6.0 yayınından itibaren **90 gün** boyunca desteklenir |
| 4.0.x ve öncesi | :x: | Desteklenmiyor — lütfen v6.0'a yükseltin |

> ⚠️ v6.0 henüz yayınlanmadıysa (yayın öncesi taslak dönem), güncel destek hattı **5.0.x** kabul edilir. Bu tablo, v6.0'ın resmi yayınıyla birlikte güncellenecektir.

**Yükseltme önerisi:** Şifreleme anahtarı yönetimi, ReDoS koruması ve arşiv güvenliği gibi alanlarda sürümler arası düzeltmeler biriktiğinden, mümkün olan en kısa sürede güncel sürüme geçmenizi öneririz.

---

## 📣 Güvenlik Açığı Bildirimi

TraceWords; dosya içeriği tarama, PII tespiti, şifreleme anahtarı yönetimi ve arşiv (ZIP/TAR) işleme gibi hassas veri işleyen bileşenler içerir. Bu nedenle güvenlik açıklarının **sorumlu ifşa** ilkesiyle, herkese açık bir issue/PR üzerinden **değil**, aşağıdaki kanallardan bildirilmesini rica ediyoruz.

### Nereye bildirmeliyim?

1. **Tercih edilen yöntem:** GitHub deposundaki **Security** sekmesinden *"Report a vulnerability"* özelliğini kullanın:
   `https://github.com/ibrahimyigitcetin/TraceWords/security/advisories/new`
2. **Alternatif:** Doğrudan e-posta ile: **ibrahimyigitctn@gmail.com**
   - Konu satırına `[SECURITY] TraceWords - <kısa özet>` yazın.
   - Mümkünse yeniden üretim adımları (PoC), etkilenen sürüm, etki alanı (ör. PII sızıntısı, ReDoS, path traversal, şifreleme anahtarı zafiyeti) ve varsa önerilen düzeltmeyi ekleyin.
   - Kanıt olarak paylaşacağınız örnek verilerde **gerçek/kişisel veri kullanmayın**; sentetik test verisi tercih edin.

**Lütfen açık kaynak bir issue, PR veya tartışma başlığı üzerinden güvenlik açığı paylaşmayın.** Bu, açık henüz yamalanmadan istismar edilme riskini artırır.

### Ne zaman geri dönüş alırım?

| Aşama | Süre |
|---|---|
| İlk teyit (bildirim alındı) | 72 saat içinde |
| Ön değerlendirme / önem derecesi | 7 gün içinde |
| Durum güncellemesi | En az 14 günde bir |
| Düzeltme / yama hedefi (kritik) | 30 gün içinde |
| Düzeltme / yama hedefi (orta/düşük) | 90 gün içinde |

Bu süreler proje tek geliştiricili olduğundan **hedef**tir, kesin garanti değildir; karmaşık durumlarda (ör. üçüncü taraf bağımlılık zafiyeti — `cryptography`, `pypdf`, `python-docx` vb.) süre uzayabilir ve bu durum size bildirilir.

### Kabul / Ret durumunda ne olur?

- **Kabul edilirse:** Açık doğrulanır, bir düzeltme geliştirilir, mümkünse sizden doğrulama istenir, ardından bir güvenlik yaması ve GitHub Security Advisory (CVE talebi dahil, uygunsa) yayınlanır. Bildirimi yapan kişi, aksini istemediği sürece teşekkür bölümünde anılır.
- **Reddedilirse veya "beklenen davranış" olarak değerlendirilirse:** Gerekçesi (ör. kapsam dışı tehdit modeli, zaten bilinen ve dokümante edilmiş sınırlama — örn. `secure_delete()`'in SSD/CoW dosya sistemlerindeki garanti sınırları) tarafınıza açıklanır.
- **Kamuya açıklama:** Yama yayınlandıktan sonra, koordineli olarak (genellikle 7–14 gün içinde) advisory yayınlanır. Sizinle önceden koordine edilmeden erken ifşa yapılmaz.

### Kapsam

**Kapsamda:**
- PII tespiti / maskeleme bypass'ları
- Şifreleme anahtarı yönetimi zafiyetleri (`GDPRCompliantStorage`)
- ReDoS / kaynak tüketimi (regex, arşiv işleme)
- ZIP/TAR bomb koruması bypass'ları, nested archive limit atlatma
- Path traversal (`sanitize_path()` bypass'ları)
- Rich markup / terminal enjeksiyonu (`strip_rich_tags`, `highlight_and_escape`)
- Audit/privacy log bütünlüğü veya sızıntısı
- Güvenli silme (`--wipe-source`) veri kalıntısı senaryoları (belgelenmemiş yeni bulgular)

**Kapsam dışı:**
- `secure_delete()`'in SSD wear-leveling / CoW dosya sistemleri (btrfs, ZFS, APFS) üzerindeki, README ve kod içi docstring'de zaten açıkça belgelenmiş sınırlamaları
- Kullanıcının kendi ortamındaki yanlış yapılandırma (ör. `.tracewords/keyfile` dosyasına dünya-okunabilir izin vermek)
- Yetkisiz dizinlerde/veride araç çalıştırmaktan doğan hukuki sorumluluk

### Güvenli Liman

Bu politikaya iyi niyetle uyarak yapılan güvenlik araştırmaları için: verilerinizi kendi test ortamınızda tutmanız, üretim/gerçek kişisel veri üzerinde test yapmamanız ve açığı kamuya açıklamadan önce bize makul bir düzeltme süresi tanımanız koşuluyla, bu araştırma nedeniyle hukuki işlem başlatmayacağımızı taahhüt ederiz.

---

*TraceWords proje sahibi: İbrahim Yiğit ÇETİN | Son güncelleme: v6.0 hazırlık süreci*
