# iOS - Face Modülü

Face Modülü, kullanıcının canlılık kontrolünü (liveness detection) ve kimlik kartındaki fotoğrafla yüz karşılaştırmasını gerçekleştirir. Ayrıca isteğe bağlı olarak akış sırasında video kaydı alınabilir.

Face Modülü'nü kullanmadan önce **Core Modülü** projeye eklenmiş ve yapılandırılmış olmalıdır. Detaylar için Core Modülü sayfasına bakınız.

---

## Kurulum

`Podfile`'a aşağıdaki bağımlılıkları ekleyin:

wide760pod 'GoogleMLKit/FaceDetection'
pod 'OpenSSL-Universal', '3.3.2000'

XCFramework olarak eklenecekse: `FaceModule.xcframework` ve `CoreModule.xcframework` dosyalarını **Embed and Sign** olarak projeye dahil edin.

`post_install` build ayarları ve kurulum yöntemleri tüm modüller için ortaktır. Detaylar için Başlarken → SDK Kurulumu sayfasına bakınız.

---

## Hızlı Başlangıç

1. **Info.plist'e kamera izni ekle** → Başlarken → Info.plist İzinleri
2. `EnQualifyFaceDelegate`**'i sınıfa ekle** ve delegate fonksiyonlarını implement et
3. `BaseModelFace` **ve** `SessionModelFace`**'i tanımla** → Core Modülü → BaseModel ve Core Modülü → SessionModel
4. `EnQualifyFace.initialize()`**'ı çağır**
5. `initializeCompleted` **delegate'ini bekle**, ardından canlılık akışını başlat

---

## Delegate Implementasyonu

### Sınıfa Ekleme

wide760class ViewController: UIViewController, EnQualifyFaceDelegate {

### Tüm Delegate Fonksiyonları

wide760// Face İşlem Callback'leri
func livenessCompleted() {} // Canlılık kontrolü tamamlandı
func livenessCompletedWithVideoRecord(url: URL) {} // Canlılık tamamlandı + video kaydı hazır
func faceCompareFailed(error: EnQualifyFaceError) {} // Hata
// Token / Session / Settings (tüm modüllerde ortaktır)
func initializeCompleted(moduleName: String) {}
func initializeFailed(with key: CustomNSError) {}
func tokenCreateCompleted() {}
func tokenCreateFailed() {}
func sessionAddFailed() {}
func settingGetFailed() {}
func sessionCloseCompleted(status: String) {}
func sessionCloseFailed() {}
func integrationAddCompleted() {}
func integrationAddFailed() {}

Token / Session / Settings delegate'lerinin açıklamaları için Core Modülü → Ortak Delegate'ler sayfasına bakınız.

`livenessCompleted` ve `livenessCompletedWithVideoRecord` aynı anda implement edilmemelidir. Video kaydı kullanılıyorsa yalnızca `livenessCompletedWithVideoRecord`'u, kullanılmıyorsa yalnızca `livenessCompleted`'ı implement edin.

---

## Initialize

wide760EnQualifyFace.initialize(
self,
sessionModel: sessionModel, // SessionModelFace
baseModel: baseModel // BaseModelFace
)

| Parametre | Tip | Açıklama |
| --- | --- | --- |
| `sender` | `Any?` | Delegate metodlarını karşılayacak `UIViewController` |
| `sessionModel` | `SessionModelFace` | Oturum bilgileri. Detay: Core Modülü → SessionModel |
| `baseModel` | `BaseModelFace` | Sertifika ve sunucu bilgileri. Detay: Core Modülü → BaseModel |

`initialize()` çağrıldıktan sonra SDK sırasıyla token oluşturma, oturum açma ve ayarları alma adımlarını otomatik yönetir. Tüm adımlar tamamlandığında `initializeCompleted(moduleName:)` tetiklenir. Initialization lifecycle detayları için Core Modülü → Initialization Lifecycle sayfasına bakınız.

---

## Face Akışı

`initializeCompleted` geldikten sonra canlılık akışı başlatılır:

wide760livenessStart()
│
▼
[Kullanıcı hareketleri: baş döndürme, göz kırpma, gülümseme]
│
├─ Video kaydı kapalı → livenessCompleted()
│
└─ Video kaydı açık → livenessCompletedWithVideoRecord(url: URL)
│
▼
Veri + video backoffice'e gönderildi

---

## Fonksiyonlar

### `livenessStart` — Canlılık Kontrolü

wide760// Video kaydı olmadan
EnQualifyFace.livenessStart(in: self)
// Video kaydıyla
EnQualifyFace.livenessStart(in: self, withVideoRecord: true)

Ön kamera üzerinden kullanıcının canlılık kontrolünü başlatır. Backoffice'te tanımlanmış hareketler (baş döndürme, göz kırpma, gülümseme vb.) sırasıyla kullanıcıdan istenir.

| Parametre | Tip | Açıklama |
| --- | --- | --- |
| `in` | `UIViewController` | İşlemin yapılacağı view controller |
| `withVideoRecord` | `Bool` | `true` → akış boyunca video kaydedilir |

**Callback:**

* Video kaydı kapalıysa: `livenessCompleted()`
* Video kaydı açıksa: `livenessCompletedWithVideoRecord(url: URL)` — `url` parametresi kaydedilen videonun cihaz üzerindeki geçici konumunu içerir

---

### `sessionClose` — Oturumu Kapatma

wide760EnQualifyFace.sessionClose(finished: false)

Session kapatıldıktan sonra modül tekrar kullanılacaksa `initialize()` yeniden çağrılmalıdır.

---

### `replaceSound` — Ses Değiştirme

wide760EnQualifyFace.replaceSound(
currentVoice: ["fail\_face\_voice"],
newVoice: "go\_to\_videocall"
)

Belirli bir adımda çalınacak sesi dinamik olarak değiştirir veya sessize alır. Boş string `""` verilirse o adım sessiz geçer. Parametre açıklamaları için OCR Modülü → replaceSound bölümüne bakınız.

---

## Video Kaydı

Video kaydı özelliği etkinleştirildiğinde canlılık akışı boyunca ön kamera görüntüsü kaydedilir.

wide760func livenessCompletedWithVideoRecord(url: URL) {
// url: videonun cihaz üzerindeki geçici dosya yolu
// Bu noktada video backoffice'e de otomatik gönderilmiştir
// Gerekiyorsa url üzerinden yerel kopyaya da erişilebilir
}

`url` parametresindeki dosya geçici bir konumdadır. Kalıcı olarak saklanması gerekiyorsa bu delegate içinde kopyalanmalıdır.

Video kaydı backoffice ayarlarından da zorunlu hale getirilebilir. Bu durumda `withVideoRecord: false` ile başlatılsa bile kayıt alınır.

---

## Hata Yönetimi

wide760func faceCompareFailed(error: EnQualifyFaceError) {
switch error {
case .timeout(let message):
// Zaman aşımı — kullanıcı hareketi tamamlayamadı
case .livenessFailed(let message):
// Canlılık kontrolü başarısız
case .faceCompareFailed(let message):
// Yüz karşılaştırma başarısız
case .cameraSetup(let message):
// Kamera başlatılamadı
case .videoRecord(let message):
// Video kaydı alınamadı
}
}

| Hata | Açıklama |
| --- | --- |
| `.timeout(String)` | Belirlenen sürede hareket tamamlanamadı |
| `.livenessFailed(String)` | Canlılık testi geçilemedi |
| `.faceCompareFailed(String)` | Yüz, kimlik kartındaki fotoğrafla eşleşmedi |
| `.cameraSetup(String)` | Kamera başlatılamadı |
| `.videoRecord(String)` | Video kaydı alınamadı veya gönderilemedi |

---

Sonraki adım: VideoCall Modülü