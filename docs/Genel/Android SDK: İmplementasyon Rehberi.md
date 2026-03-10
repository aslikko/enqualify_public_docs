# Android SDK: İmplementasyon Rehberi

EnQualify Android SDK, mobil uygulamanıza uzaktan kimlik doğrulama yetenekleri kazandırır. OCR, NFC, yüz tanıma ve görüntülü görüşme modüllerinden oluşan bu SDK; self-servis, hibrit ve tam temsilci destekli akışları destekler.

---

## Bu Dokümanda Neler Var?

| Bölüm | Ne Bulursunuz? |
| --- | --- |
| Başlarken | Gereksinimler, Maven kurulumu, proje konfigürasyonu |
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

EnQualify SDK bağımsız modüllerden oluşur. Her modül ayrı ayrı kurulabilir; ancak tümü Core Modülü'ne bağımlıdır.

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

> ℹ️ VideoCall akışında OCR ve Face tekrarlatma özelliğini kullanmak istiyorsanız, OCR ve Face modülleri de projeye eklenmiş olmalıdır.

---

## Minimum Gereksinimler

| Parametre | Değer |
| --- | --- |
| Minimum Android SDK | API 25 (Android 7.1) |
| Desteklenen Mimariler | `armeabi-v7a`, `arm64-v8a` |
| Build Sistemi | Gradle (Kotlin DSL önerilir) |
| Emülatör Desteği | Derlenir; ancak kamera/NFC gerektiren akışlar çalışmaz |

---

## Kurulum

SDK, Maven üzerinden projeye eklenir. Erişim bilgileri (repo URL, kullanıcı adı, şifre) size özel olarak iletilir. Detaylı kurulum adımları **Başlarken** sayfasındadır.

---

## Temel Kavramlar

### Initialization Lifecycle

Her modül aynı başlatma döngüsünü izler: `initialize()` çağrıldıktan sonra SDK sırasıyla **token oluşturma → oturum açma → ayarları alma** adımlarını otomatik olarak yönetir. Tüm adımlar tamamlandığında `initializeCompleted(module: EnModules)` callback'i tetiklenir; bu noktadan itibaren modüle ait işlemler başlatılabilir.

Hata durumunda her adım için ayrı callback mevcuttur: `tokenCreateFailed()`, `sessionAddFailed()`, `settingsGetFailed()`. Detaylar için Core Modülü sayfasına bakınız.

> ℹ️ Utility Modülü bu akıştan farklıdır: `SessionModel` almaz, yalnızca `BaseModel` ile başlatılır ve `baseModelCompleted()` callback'i ile hazır hale gelir.

### Callback Yapısı

SDK, sonuçları ve hataları **callback (interface) pattern'i** üzerinden iletir. Her modülün kendi `Callbacks` interface'i vardır ve ilgili `Activity`'e implement edilmesi gerekir.

### Fragment & FrameLayout

Tüm modüller kamera ekranlarını ve sayfa geçişlerini bir `FrameLayout` üzerinden yönetir. İlgili Activity'nin layout'unda tam ekran kaplayan bir `FrameLayout` bulunması zorunludur.

### SSL Güvenliği

SDK iki katmanlı güvenlik uygular: **SSL pinning** (ortadaki adam saldırılarına karşı) ve oturum başına yenilenen RSA imzalama. Sertifika yapılandırması `BaseModel.signallingCertificateList` ve `mapiCertificateList` alanları üzerinden yapılır. Canlı ortamlarda SSL pinning'in devre dışı bırakılması kesinlikle önerilmez.

### Singleton Yapı

Tüm modüller singleton olarak çalışır. `initialize()` ile oluşturulan instance, uygulama oturumu boyunca `getInstance()` ile erişilebilir. Mevcut bir session varsa yeni session oluşturulmaz.

---

## Hızlı Başlangıç Adımları

Projenize ilk kez EnQualify SDK ekliyorsanız şu sırayı takip edin:

1. **Başlarken** → Maven erişim bilgilerini al, `libs.versions.toml` ve `settings.gradle.kts` dosyalarını yapılandır
2. **Başlarken** → `AndroidManifest.xml` izinlerini ekle, NFC ve kamera ayarlarını yap
3. **Core Modülü** → `BaseModel` ve `SessionModel` tanımla
4. **İlgili modülün sayfasına geç** → `initialize()` et, callback'leri implement et, akışı başlat

> Sorularınız veya entegrasyon sırasında karşılaştığınız sorunlar için destek ekibimizle iletişime geçebilirsiniz.