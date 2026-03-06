# OCR Modülü

OCR Modülü, arka kamera üzerinden kimlik kartı ve pasaport üzerindeki verileri okur. Görsel obje analizi, hologram tespiti, yüz fotoğrafı okuma, MRZ alanı okuma ve görsel güvenlik öğelerinin doğrulanması bu modül tarafından gerçekleştirilir.

OCR Modülü'nü kullanmadan önce **Core Modülü** projeye eklenmiş ve yapılandırılmış olmalıdır. Detaylar için Core Modülü sayfasına bakınız.

---

Kurulum
-------

`Podfile`'a aşağıdaki bağımlılıkları ekleyin:

ruby

wide760pod 'TensorFlowLiteSwift' # Kimlik tespiti
pod 'TensorFlowLiteSwift/Metal' # Kimlik tespiti
pod 'OpenSSL-Universal', '3.3.2000' # Core Modülü

XCFramework olarak eklenecekse: `OCRModule.xcframework` ve `CoreModule.xcframework` dosyalarını **Embed and Sign** olarak projeye dahil edin.

`post_install` build ayarları ve kurulum yöntemleri tüm modüller için ortaktır. Detaylar için Başlarken → SDK Kurulumu sayfasına bakınız.

---

Hızlı Başlangıç
---------------

OCR Modülü'nü projeye entegre etmek için şu adımları izleyin:

1. **Info.plist'e kamera izni ekle** → Başlarken → Info.plist İzinleri
2. `EnQualifyOCRDelegate`**'i sınıfa ekle** ve delegate fonksiyonlarını implement et
3. `BaseModelOCR` **ve** `SessionModelOCR`**'ı tanımla** → Core Modülü → BaseModel ve Core Modülü → SessionModel
4. `EnQualifyOCR.initialize()`**'ı çağır**
5. `initializeCompleted` **delegate'ini bekle**, ardından OCR akışını başlat

---

Delegate Implementasyonu
------------------------

### Sınıfa Ekleme

swift

wide760class ViewController: UIViewController, EnQualifyOCRDelegate {

### Tüm Delegate Fonksiyonları

swift

wide760// OCR İşlem Callback'leri
func idDocTypeCheckVerified(isFront: Bool) {} // Kimlik tipi tespit edildi
func idDocFrontCompleted() {} // Ön yüz okuma tamamlandı
func idDocBackCompleted() {} // Arka yüz okuma tamamlandı
func idDocCompleted() {} // Tüm okuma tamamlandı, veri backoffice'e gönderildi
func hologramCheckVerified() {} // Hologram doğrulandı
func idDocFailed(error: EnQualifyOcrError) {} // Hata
// Signing
func signingSetCompleted() {}
func signingCompleted() {}
func signingSetFailed(error: String) {}
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

---

Initialize
----------

swift

wide760EnQualifyOCR.initialize(
self,
sessionModel: sessionModel, // SessionModelOCR
baseModel: baseModel // BaseModelOCR
)

| Parametre | Tip | Açıklama |
| --- | --- | --- |
| `sender` | `Any?` | Delegate metodlarını karşılayacak `UIViewController` |
| `sessionModel` | `SessionModelOCR` | Oturum bilgileri. Detay: Core Modülü → SessionModel |
| `baseModel` | `BaseModelOCR` | Sertifika ve sunucu bilgileri. Detay: Core Modülü → BaseModel |

`initialize()` çağrıldıktan sonra SDK sırasıyla token oluşturma, oturum açma ve ayarları alma adımlarını otomatik yönetir. Tüm adımlar tamamlandığında `initializeCompleted(moduleName:)` tetiklenir. Initialization lifecycle detayları için Core Modülü → Initialization Lifecycle sayfasına bakınız.

---

OCR Akışı
---------

`initializeCompleted` geldikten sonra kimlik okuma adımları sırasıyla çağrılır. Tipik bir akış aşağıdaki gibidir:

wide760idDocTypeCheckStart() → idDocTypeCheckVerified()
│
▼
idDocFrontStart() → idDocFrontCompleted()
│
▼
hologramCheckStart() → hologramCheckVerified() ← opsiyonel
│
▼
idDocBackStart() → idDocBackCompleted()
│
▼
idDocComplete() → idDocCompleted() ← veri backoffice'e gönderildi

💡 Kullanıcıya her adım öncesinde bilgilendirme ekranı gösterilmesi önerilir.

---

Fonksiyonlar
------------

### `idDocTypeCheckStart` — Kimlik Tipi Tanıma

swift

wide760EnQualifyOCR.idDocTypeCheckStart(in: self, isFront: true)

Kimlik tipini (T.C. Kimlik Kartı / Pasaport) tespit eder.

| Parametre | Açıklama |
| --- | --- |
| `in` | İşlemin yapılacağı `UIViewController` |
| `isFront` | `true` → ön yüz taraması, `false` → arka yüz taraması |

**Callback:** `idDocTypeCheckVerified(isFront: Bool)`

---

### `idDocFrontStart` — Kimlik Ön Yüz Tarama

swift

wide760EnQualifyOCR.idDocFrontStart(in: self, withVisualAnalysis: true)

Kimliğin ön yüzündeki verileri okur.

| Parametre | Açıklama |
| --- | --- |
| `in` | İşlemin yapılacağı `UIViewController` |
| `withVisualAnalysis` | `true` → görsel güvenlik öğeleri analizi de yapılır |

**Callback:** `idDocFrontCompleted()`

---

### `hologramCheckStart` — Hologram Tespiti

swift

wide760EnQualifyOCR.hologramCheckStart(in: self)

Kimlik ön yüzündeki hologramı tespit eder.

**Callback:** `hologramCheckVerified()`

---

### `idDocBackStart` — Kimlik Arka Yüz Tarama

swift

wide760EnQualifyOCR.idDocBackStart(in: self, withVisualAnalysis: true)

Kimliğin arka yüzündeki MRZ alanı dahil tüm verileri okur.

| Parametre | Açıklama |
| --- | --- |
| `in` | İşlemin yapılacağı `UIViewController` |
| `withVisualAnalysis` | `true` → görsel güvenlik öğeleri analizi de yapılır |

**Callback:** `idDocBackCompleted()`

---

### `idDocComplete` — Okuma Akışını Bitirme

swift

wide760EnQualifyOCR.idDocComplete(withDelay: 0.0)

Tüm kimlik okuma adımları tamamlandığında çağrılır. Kamera analizi durdurulur, okunan veriler backoffice'e gönderilir.

| Parametre | Açıklama |
| --- | --- |
| `withDelay` | Kamera oturumunun kapatılması için bekleme süresi (saniye) |

**Callback:** Veriler backoffice'e ulaştığında `idDocCompleted()` tetiklenir.

---

### `sessionClose` — Oturumu Kapatma

swift

wide760EnQualifyOCR.sessionClose(finished: false)

Session kapatıldıktan sonra modül tekrar kullanılacaksa `initialize()` yeniden çağrılmalıdır.

---

### `replaceSound` — Ses Değiştirme

Belirli bir adımda çalınacak sesi dinamik olarak değiştirir veya sessize alır.

swift

wide760EnQualifyOCR.replaceSound(
currentVoice: ["fail\_ocr\_voice"],
newVoice: "go\_to\_videocall"
)

| Parametre | Tip | Açıklama |
| --- | --- | --- |
| `currentVoice` | `[String]` | Değiştirilecek ses dosyasının adı. Dizi olarak alır çünkü aynı adımda birden fazla ses tetiklenebilir. |
| `newVoice` | `String` | Yerine çalınacak ses. Boş string `""` verilirse o adım sessiz geçer. |

**Kullanım senaryosu:** Örneğin üçüncü başarısız OCR denemesinde `"fail_ocr_voice"` yerine `"go_to_videocall"` sesini çalmak için:

swift

wide760replaceSound(currentVoice: ["fail\_ocr\_voice"], newVoice: "go\_to\_videocall")

---

Hata Yönetimi
-------------

swift

wide760func idDocFailed(error: EnQualifyOcrError) {
switch error {
case .timeout(let state, let message):
// Zaman aşımı — state: hangi adımda olduğu
case .idDocFailed(let state, let message):
// Kimlik tanıma başarısız
case .idDocSave(let message):
// Veri kaydetme hatası
case .cameraSetup(let message):
// Kamera başlatma hatası
}
}

| Hata | Açıklama |
| --- | --- |
| `.timeout(OCRState, String)` | Belirlenen sürede işlem tamamlanamadı |
| `.idDocFailed(OCRState, String)` | Kimlik doğrulama başarısız |
| `.idDocSave(String)` | Okunan veriler kaydedilemedi |
| `.cameraSetup(String)` | Kamera başlatılamadı |

---

Okunan Verilere Erişim
----------------------

OCR akışı tamamlandıktan sonra `CustomerIdentity.shared` üzerinden okunan verilere erişilebilir.

swift

wide760func showOCRResults() {
let doc = CustomerIdentity.shared
let name = doc.getName()
let surname = doc.getSurname()
let birthDate = doc.getFrontDateOfBirthDay()
let idNumber = doc.getIdentityNumber()
let docNumber = doc.getDocumentNumber()
let gender = doc.getGender()
let nationality = doc.getNationality()
let expiryDate = doc.getExpiryDate()
// Görsel veriler
let holoImage = doc.getHoloFrontImage()?.image
let frontImage = doc.getFrontImage()?.image
let backImage = doc.getBackImage()?.image
}

`CustomerIdentity` singleton yapıdadır. Veriler `idDocCompleted()` delegate'i tetiklendikten sonra erişilebilir hale gelir.

---

Sonraki adım: NFC Modülü