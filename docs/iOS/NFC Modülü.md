# iOS - NFC Modülü

NFC Modülü, T.C. Kimlik Kartı ve pasaport içindeki RFID çipten kimlik verilerini okur. Çip okuma işlemi; MRZ verisi veya doküman numarası ile doğum tarihi ve son geçerlilik tarihi kombinasyonu kullanılarak gerçekleştirilir.

NFC Modülü'nü kullanmadan önce **Core Modülü** projeye eklenmiş ve yapılandırılmış olmalıdır. Detaylar için Core Modülü sayfasına bakınız.

NFC okuma için gerekli Info.plist izinleri, entitlements ve capability ayarları için Başlarken → Proje Konfigürasyonu sayfasına bakınız.

---

## Kurulum

`Podfile`'a aşağıdaki bağımlılığı ekleyin:

wide760pod 'OpenSSL-Universal', '3.3.2000'

XCFramework olarak eklenecekse: `NFCModule.xcframework` ve `CoreModule.xcframework` dosyalarını **Embed and Sign** olarak projeye dahil edin.

`post_install` build ayarları ve kurulum yöntemleri tüm modüller için ortaktır. Detaylar için Başlarken → SDK Kurulumu sayfasına bakınız.

---

## Hızlı Başlangıç

1. **NFC izinleri ve entitlements'ı yapılandır** → Başlarken → NFC Capability ve Entitlements
2. `EnQualifyNFCDelegate`**'i sınıfa ekle** ve delegate fonksiyonlarını implement et
3. `BaseModelNFC` **ve** `SessionModelNFC`**'yi tanımla** → Core Modülü → BaseModel ve Core Modülü → SessionModel
4. `EnQualifyNFC.initialize()`**'ı çağır**
5. `initializeCompleted` **delegate'ini bekle**, ardından NFC akışını başlat

---

## Delegate Implementasyonu

### Sınıfa Ekleme

wide760class ViewController: UIViewController, EnQualifyNFCDelegate {

### Tüm Delegate Fonksiyonları

wide760// NFC İşlem Callback'leri
func nfcReadCompleted() {} // Çip okuma tamamlandı, veri backoffice'e gönderildi
func nfcFailed(error: EnQualifyNfcError) {} // Hata
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

## Initialize

wide760EnQualifyNFC.initialize(
self,
sessionModel: sessionModel, // SessionModelNFC
baseModel: baseModel // BaseModelNFC
)

| Parametre | Tip | Açıklama |
| --- | --- | --- |
| `sender` | `Any?` | Delegate metodlarını karşılayacak `UIViewController` |
| `sessionModel` | `SessionModelNFC` | Oturum bilgileri. Detay: Core Modülü → SessionModel |
| `baseModel` | `BaseModelNFC` | Sertifika ve sunucu bilgileri. Detay: Core Modülü → BaseModel |

`initialize()` çağrıldıktan sonra SDK sırasıyla token oluşturma, oturum açma ve ayarları alma adımlarını otomatik yönetir. Tüm adımlar tamamlandığında `initializeCompleted(moduleName:)` tetiklenir. Initialization lifecycle detayları için Core Modülü → Initialization Lifecycle sayfasına bakınız.

---

## NFC Akışı

`initializeCompleted` geldikten sonra NFC okuma başlatılır:

wide760nfcReadStart() → nfcReadCompleted()
│
▼
Veri backoffice'e gönderildi
CustomerIdentity.shared üzerinden erişilebilir

NFC okuma sırasında sistem kendi arayüzünü gösterir (iOS native NFC sheet). Bu ekran özelleştirilemez.

---

## Fonksiyonlar

### `nfcReadStart` — NFC Çip Okuma

wide760// Yöntem 1 — MRZ verisiyle
EnQualifyNFC.nfcReadStart(in: self, mrzKey: mrzData)
// Yöntem 2 — Doküman numarası, doğum tarihi ve son geçerlilik tarihiyle
EnQualifyNFC.nfcReadStart(
in: self,
documentNumber: "A123456789",
dateOfBirth: "YYMMDD",
expiryDate: "YYMMDD"
)

NFC çipini okur ve verileri backoffice'e gönderir.

**Yöntem 1 parametreleri:**

| Parametre | Tip | Açıklama |
| --- | --- | --- |
| `in` | `UIViewController` | İşlemin yapılacağı view controller |
| `mrzKey` | `String` | OCR akışından elde edilen MRZ verisi |

**Yöntem 2 parametreleri:**

| Parametre | Tip | Açıklama |
| --- | --- | --- |
| `in` | `UIViewController` | İşlemin yapılacağı view controller |
| `documentNumber` | `String` | Kimlik veya pasaport doküman numarası |
| `dateOfBirth` | `String` | Doğum tarihi — `YYMMDD` formatında |
| `expiryDate` | `String` | Son geçerlilik tarihi — `YYMMDD` formatında |

> 💡 OCR modülü kullanılıyorsa Yöntem 1 tercih edilmelidir. MRZ verisi `CustomerIdentity.shared.getMrzKey()` ile alınabilir. Yöntem 2, OCR modülü olmadan bağımsız NFC akışı için uygundur.

**Callback:** `nfcReadCompleted()`

---

### `sessionClose` — Oturumu Kapatma

wide760EnQualifyNFC.sessionClose(finished: false)

Session kapatıldıktan sonra modül tekrar kullanılacaksa `initialize()` yeniden çağrılmalıdır.

---

## Hata Yönetimi

wide760func nfcFailed(error: EnQualifyNfcError) {
switch error {
case .timeout(let message):
// Zaman aşımı — kullanıcı kart okutmadı veya bağlantı kesildi
case .nfcReadFailed(let message):
// Çip okuma başarısız — kart desteklenmiyor veya bozuk çip
case .nfcSave(let message):
// Okunan veriler kaydedilemedi
case .nfcNotSupported(let message):
// Cihaz NFC desteklemiyor
}
}

| Hata | Açıklama |
| --- | --- |
| `.timeout(String)` | Belirlenen sürede NFC bağlantısı kurulamadı |
| `.nfcReadFailed(String)` | Çip okunamadı |
| `.nfcSave(String)` | Veriler backoffice'e gönderilemedi |
| `.nfcNotSupported(String)` | Cihazda NFC donanımı yok veya kapalı |

---

## Okunan Verilere Erişim

NFC akışı tamamlandıktan sonra `CustomerIdentity.shared` üzerinden çipten okunan verilere erişilebilir.

wide760func showNFCResults() {
let doc = CustomerIdentity.shared
let name = doc.getName()
let surname = doc.getSurname()
let birthDate = doc.getDateOfBirth()
let idNumber = doc.getIdentityNumber()
let docNumber = doc.getDocumentNumber()
let gender = doc.getGender()
let nationality = doc.getNationality()
let expiryDate = doc.getExpiryDate()
let mrzKey = doc.getMrzKey() // Sonraki NFC çağrısında kullanılabilir
// Çipten okunan biyometrik fotoğraf
let chipPhoto = doc.getChipPhoto()?.image
}

`CustomerIdentity` singleton yapıdadır ve OCR ile NFC verilerini birlikte tutar. `nfcReadCompleted()` tetiklendikten sonra çip verileri de bu nesne üzerinden erişilebilir hale gelir.

---

Sonraki adım: Face Modülü