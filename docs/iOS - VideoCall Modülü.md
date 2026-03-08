# iOS - VideoCall Modülü

VideoCall Modülü, son kullanıcı ile kimlik doğrulama temsilcisi arasında gerçek zamanlı görüntülü görüşme başlatır. Temsilci eşleşmesi, bekleme kuyruğu, tekrar deneme akışları ve Picture in Picture (PiP) modu bu modül tarafından yönetilir.

VideoCall Modülü'nü kullanmadan önce **Core Modülü** projeye eklenmiş ve yapılandırılmış olmalıdır. Detaylar için Core Modülü sayfasına bakınız.

Görüşme sırasında temsilcinin OCR veya Face adımlarını tekrarlatması isteniyorsa, projeye **OCR Modülü** ve **Face Modülü** de eklenmiş olmalıdır.

---

Kurulum
-------

`Podfile`'a aşağıdaki bağımlılıkları ekleyin:

wide760pod 'OpenSSL-Universal', '3.3.2000'
pod 'GoogleWebRTC'

XCFramework olarak eklenecekse: `VideoCallModule.xcframework` ve `CoreModule.xcframework` dosyalarını **Embed and Sign** olarak projeye dahil edin.

`post_install` build ayarları ve kurulum yöntemleri tüm modüller için ortaktır. Detaylar için Başlarken → SDK Kurulumu sayfasına bakınız.

---

Hızlı Başlangıç
---------------

1. **Info.plist'e kamera ve mikrofon izni ekle** → Başlarken → Info.plist İzinleri
2. **PiP kullanılacaksa capability'leri ekle** → Başlarken → Picture in Picture
3. `EnQualifyVideoCallDelegate`**'i sınıfa ekle** ve delegate fonksiyonlarını implement et
4. `BaseModelVideoCall` **ve** `SessionModelVideoCall`**'ı tanımla** → Core Modülü → BaseModel ve Core Modülü → SessionModel
5. `EnQualifyVideoCall.initialize()`**'ı çağır**
6. `initializeCompleted` **delegate'ini bekle** ve `moduleName == "EnQualifyVideoCall"` doğrulamasını yap, ardından görüşmeyi başlat

---

Delegate Implementasyonu
------------------------

### Sınıfa Ekleme

wide760class ViewController: UIViewController, EnQualifyVideoCallDelegate {

### Tüm Delegate Fonksiyonları

wide760// Görüşme Akışı
func videoCallStarted() {} // Görüşme başladı, temsilci bağlandı
func videoCallFinished(status: String) {} // Görüşme tamamlandı
func videoCallFailed(error: EnQualifyVideoCallError) {} // Hata
// Bekleme ve Kuyruk
func waitingForAgent() {} // Uygun temsilci bekleniyor
func waitingForAgentTimeout() {} // Bekleme süresi doldu, temsilci bulunamadı
// Temsilci Tekrar Deneme Akışları
func retryOCR() {} // Temsilci OCR adımını yeniden başlattı
func retryFace() {} // Temsilci Face adımını yeniden başlattı
func retryNFC() {} // Temsilci NFC adımını yeniden başlattı
// Picture in Picture
func pipStarted() {} // PiP modu başladı
func pipStopped() {} // PiP modu sona erdi
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

wide760EnQualifyVideoCall.initialize(
self,
sessionModel: sessionModel, // SessionModelVideoCall
baseModel: baseModel // BaseModelVideoCall
)

| Parametre | Tip | Açıklama |
| --- | --- | --- |
| `sender` | `Any?` | Delegate metodlarını karşılayacak `UIViewController` |
| `sessionModel` | `SessionModelVideoCall` | Oturum bilgileri. Detay: Core Modülü → SessionModel |
| `baseModel` | `BaseModelVideoCall` | Sertifika ve sunucu bilgileri. Detay: Core Modülü → BaseModel |

`initialize()` çağrıldıktan sonra SDK sırasıyla token oluşturma, oturum açma ve ayarları alma adımlarını otomatik yönetir. Tüm adımlar tamamlandığında `initializeCompleted(moduleName:)` tetiklenir.

`initializeCompleted` geldikten sonra `moduleName == "EnQualifyVideoCall"` kontrolü yapılmalıdır. Bu doğrulama yapılmadan `startVideoCall()` çağrılırsa görüşme başlamaz.

wide760func initializeCompleted(moduleName: String) {
if moduleName == "EnQualifyVideoCall" {
EnQualifyVideoCall.startVideoCall(in: self)
}
}

---

VideoCall Akışı
---------------

wide760initialize()
│
▼
initializeCompleted(moduleName: "EnQualifyVideoCall")
│
▼
startVideoCall()
│
▼
waitingForAgent() ← uygun temsilci bekleniyor
│
├─ Temsilci bulundu → videoCallStarted()
│ │
│ [Görüşme devam ediyor]
│ │
│ ┌────────────┴────────────┐
│ │ │
│ retryOCR() / retryFace() videoCallFinished()
│ retryNFC() │
│ │ sessionClose()
│ [İlgili modül akışı]
│ [Tamamlanınca geri dön]
│
└─ Temsilci bulunamadı → waitingForAgentTimeout()
│
sessionClose()

---

Fonksiyonlar
------------

### `startVideoCall` — Görüşmeyi Başlatma

wide760EnQualifyVideoCall.startVideoCall(in: self)

Temsilci kuyruğuna girer ve uygun temsilci beklenir. Temsilci bulunduğunda görüşme otomatik olarak başlar.

| Parametre | Açıklama |
| --- | --- |
| `in` | İşlemin yapılacağı `UIViewController` |

**Callback'ler:** `waitingForAgent()` → `videoCallStarted()` veya `waitingForAgentTimeout()`

---

### Temsilci Tarafından Tetiklenen Retry Akışları

Görüşme sırasında temsilci, backoffice üzerinden kullanıcıdan OCR, Face veya NFC adımlarını tekrar yapmasını isteyebilir. Bu durumda ilgili delegate tetiklenir ve uygulamanın ilgili modülü yeniden başlatması beklenir.

wide760func retryOCR() {
// OCR modülünü yeniden initialize et ve akışı başlat
EnQualifyOCR.initialize(self, sessionModel: sessionModel, baseModel: baseModel)
}
func retryFace() {
// Face modülünü yeniden initialize et ve akışı başlat
EnQualifyFace.initialize(self, sessionModel: sessionModel, baseModel: baseModel)
}
func retryNFC() {
// NFC modülünü yeniden initialize et ve akışı başlat
EnQualifyNFC.initialize(self, sessionModel: sessionModel, baseModel: baseModel)
}

Retry akışları için OCR, Face ve NFC modüllerinin projeye eklenmiş olması gerekir. Eklenmeden bu delegate'ler tetiklenirse akış kırılır.

İlgili modül akışı tamamlandıktan sonra (`idDocCompleted`, `livenessCompleted`, `nfcReadCompleted`) görüşme otomatik olarak kaldığı yerden devam eder, `startVideoCall()` tekrar çağrılmasına gerek yoktur.

---

### `sessionClose` — Oturumu Kapatma

wide760EnQualifyVideoCall.sessionClose(finished: false)

Görüşme tamamlandığında (`videoCallFinished`) veya zaman aşımı durumunda (`waitingForAgentTimeout`) çağrılmalıdır.

Session kapatıldıktan sonra modül tekrar kullanılacaksa `initialize()` yeniden çağrılmalıdır.

---

Picture in Picture (PiP)
------------------------

PiP modu, görüşme sırasında kullanıcı uygulamayı arka plana aldığında ya da başka bir ekrana geçtiğinde görüşme penceresini küçük bir kayan panel olarak sürdürür.

### Gereksinimler

PiP özelliğinin çalışması için capability ayarlarının yapılmış olması gerekir. Detaylar için Başlarken → Picture in Picture sayfasına bakınız.

Bu ayarlar yapılmadan PiP moduna geçildiğinde görüntü yerine gri ekran görünür.

### Delegate Kullanımı

wide760func pipStarted() {
// Görüşme PiP moduna geçti
// Gerekiyorsa UI güncellemesi yapılabilir
}
func pipStopped() {
// PiP modu sona erdi, görüşme tam ekrana döndü
}

---

Hata Yönetimi
-------------

wide760func videoCallFailed(error: EnQualifyVideoCallError) {
switch error {
case .timeout(let message):
// Bağlantı zaman aşımına uğradı
case .connectionFailed(let message):
// Görüşme bağlantısı kurulamadı veya koptu
case .cameraSetup(let message):
// Kamera başlatılamadı
case .microphoneSetup(let message):
// Mikrofon başlatılamadı
}
}

| Hata | Açıklama |
| --- | --- |
| `.timeout(String)` | Bağlantı veya kuyruk zaman aşımı |
| `.connectionFailed(String)` | WebRTC bağlantısı kurulamadı veya koptu |
| `.cameraSetup(String)` | Kamera başlatılamadı |
| `.microphoneSetup(String)` | Mikrofon başlatılamadı |

---

`videoCallFinished` — Kapanış Durumu
------------------------------------

Görüşme tamamlandığında `videoCallFinished(status: String)` tetiklenir. `status` parametresi görüşmenin nasıl sonuçlandığını taşır.

| `status` Değeri | Açıklama |
| --- | --- |
| `"Approved"` | Temsilci kimlik doğrulamayı onayladı |
| `"Rejected"` | Temsilci kimlik doğrulamayı reddetti |
| `"Cancelled"` | Görüşme iptal edildi |
| `"Timeout"` | Görüşme zaman aşımına uğradı |

`status` değerleri backoffice konfigürasyonuna göre farklılık gösterebilir. Mevcut değerlerin tam listesi için Enqura ekibiyle iletişime geçin.

---

Sonraki adım: Utility Modülü