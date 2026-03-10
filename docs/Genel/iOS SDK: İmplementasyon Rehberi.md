# iOS SDK: İmplementasyon Rehberi

EnQualify iOS SDK, mobil uygulamanıza uzaktan kimlik doğrulama yetenekleri kazandırır. OCR, NFC, yüz tanıma ve görüntülü görüşme modüllerinden oluşan bu SDK; self-servis, hibrit ve tam temsilci destekli akışları destekler.

---

## Bu Dokümanda Neler Var?

| Bölüm | Ne Bulursunuz? |
| --- | --- |
| Başlarken | Gereksinimler, kurulum yöntemleri, proje konfigürasyonu |
| Core Modülü | BaseModel, SessionModel, SSL sertifikası, ses dosyaları yönetimi |
| OCR Modülü | Kimlik kartı ve pasaport okuma |
| NFC Modülü | Temassız çip okuma (RFID) |
| Face Modülü | Canlılık kontrolü ve yüz karşılaştırma |
| VideoCall Modülü | Müşteri-temsilci görüntülü görüşme |
| Utility Modülü | Randevu, doküman imzalama, adres doğrulama, KYB |
| UI Özelleştirme | Backoffice üzerinden arayüz parametreleri |

---

## SDK'ya Genel Bakış

### Modüler Yapı

EnQualify SDK bağımsız modüllerden oluşur. Her modül ayrı ayrı kurulabilir; ancak tümü **Core Modülü**'ne bağımlıdır.

wide760CoreModule (zorunlu temel)
├── OCRModule → Kimlik kartı / pasaport okuma
├── NFCModule → NFC çip okuma
├── FaceModule → Canlılık ve yüz karşılaştırma
├── VideoCallModule → Görüntülü görüşme
└── UtilityModule → Yardımcı servisler

### Hangi Modüle İhtiyacınız Var?

Uygulamanızın akışına göre modül seçimini yapabilirsiniz:

| Akış Tipi | Gerekli Modüller |
| --- | --- |
| Sadece kimlik okuma (OCR) | Core + OCR |
| OCR + NFC çip doğrulama | Core + OCR + NFC |
| Tam self-servis (OCR + NFC + Yüz) | Core + OCR + NFC + Face |
| Görüntülü görüşmeli tam akış | Core + OCR + NFC + Face + VideoCall |
| Randevu / doküman imzalama | Core + Utility |

> **Not:** VideoCall akışında OCR ve Face tekrarlatma özelliğini kullanmak istiyorsanız, OCR ve Face modülleri de projeye eklenmiş olmalıdır.

---

## Minimum Gereksinimler

| Parametre | Değer |
| --- | --- |
| Xcode | 16.0 ve üzeri |
| Minimum iOS | 14.0 |
| Desteklenen Mimariler | arm64 (fiziksel cihaz), x86\_64 (Intel Mac simülatör) |
| Simülatör Desteği | Derlenir; ancak kamera/NFC gerektiren akışlar çalışmaz |

---

## Kurulum Yöntemleri

SDK üç farklı yöntemle projeye eklenebilir. Detaylı adımlar Başlarken sayfasındadır.

**CocoaPods** — Önerilen yöntem. Private repo erişimi için SSH key gereklidir.

**Swift Package Manager (SPM)** — Xcode üzerinden SSH ile private repo'ya bağlanarak eklenir.

**Doğrudan XCFramework** — `.xcframework` dosyaları manuel olarak projeye eklenir; bağımlılıklar CocoaPods ile kurulur.

---

## Temel Kavramlar

### Initialization Lifecycle

Her modül aynı başlatma döngüsünü izler: `initialize()` çağrıldıktan sonra SDK sırasıyla **token oluşturma → oturum açma → ayarları alma** adımlarını otomatik olarak yönetir. Tüm adımlar tamamlandığında `initializeCompleted(moduleName:)` delegate'i tetiklenir; bu noktadan itibaren modüle ait işlemler başlatılabilir.

Hata durumunda her adım için ayrı delegate mevcuttur: `tokenCreateFailed()`, `sessionAddFailed()`, `settingGetFailed()`. Detaylar için Core Modülü sayfasına bakınız.

### Delegate Yapısı

SDK, sonuçları ve hataları `delegate` pattern'i üzerinden iletir. Her modülün kendi delegate protokolü vardır ve ilgili `UIViewController`'a atanması gerekir. Utility Modülü bu yapıdan farklı olarak `@escaping closure` kullanır.

### SSL Güvenliği

SDK iki katmanlı güvenlik uygular: SSL pinning (ortadaki adam saldırılarına karşı) ve oturum başına yenilenen RSA imzalama. SSL sertifikasının kurulumu Başlarken → SSL Sertifikası Kurulumu bölümünde anlatılmaktadır. Canlı ortamlarda SSL pinning'in devre dışı bırakılması **kesinlikle önerilmez**.

---

## Hızlı Başlangıç Adımları

Projenize ilk kez EnQualify SDK ekliyorsanız şu sırayı takip edin:

1. Başlarken → SSH key oluştur, CocoaPods veya SPM kurulumu yap
2. Başlarken → Proje Konfigürasyonu → Info.plist izinleri, NFC entitlement, SSL sertifikası ekle
3. Core Modülü → `BaseModel` ve `SessionModel` tanımla
4. İlgili modülün sayfasına geç → Initialize et, delegate'leri implement et, akışı başlat

---

*Sorularınız veya entegrasyon sırasında karşılaştığınız sorunlar için destek ekibimizle iletişime geçebilirsiniz.*