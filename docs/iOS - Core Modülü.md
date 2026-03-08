# iOS - Core Modülü

Core Modülü, EnQualify SDK'nın tüm modüllerinin üzerine inşa edildiği temel altyapıdır. OCR, NFC, Face, VideoCall ve Utility modüllerinin her biri Core Modülü'ne bağımlıdır — bu nedenle herhangi bir modüle geçmeden önce Core'un doğru yapılandırılmış olması gerekir.

Bu sayfada anlatılanlar tüm modüller için geçerlidir. Modül sayfalarında yalnızca o modüle özgü farklılıklar ele alınacaktır.

---

Initialization Lifecycle
------------------------

Her modül `initialize()` çağrıldığında aynı başlatma döngüsünü izler. Bu adımlar SDK tarafından otomatik olarak yönetilir — sizin müdahaleniz gerekmez.

wide760initialize() çağrıldı
│
▼
1. Token oluşturma
✓ → devam ✗ → tokenCreateFailed()
│
▼
2. Oturum açma (Session)
✓ → devam ✗ → sessionAddFailed()
│
▼
3. Backoffice ayarları alınıyor
✓ → devam ✗ → settingGetFailed()
│
▼
initializeCompleted(moduleName:)
→ Artık modüle ait işlemler başlatılabilir

`initializeCompleted` **gelmeden modül fonksiyonlarını çağırmayın.** Örneğin VideoCall'da `startVideoCall()`, bu delegate tetiklenmeden ve `moduleName` değeri `EnQualifyVideoCall` olarak doğrulanmadan çağrılırsa görüşme başlamaz.

Her hata delegate'i bağımsız olarak ele alınmalıdır. SDK, hata durumunda otomatik retry yapmaz.

---

BaseModel
---------

`BaseModel`, her modülün `initialize()` fonksiyonuna geçilen temel yapılandırma modelidir. SSL sertifikaları ve sunucu adresi burada tanımlanır.

Her modülün kendi `BaseModel` türü vardır (`BaseModelOCR`, `BaseModelNFC`, `BaseModelFace`, `BaseModelVideoCall`, `BaseModelUtility`) ancak içerdikleri alanlar aynıdır.

### Model Tanımı

swift

wide760class BaseModel(
var signallingCertificateList: [String]? = nil, // .der dosya adları
var mapiCertificateList: [String]? = nil, // .der dosya adları
var signallingCertificateBase64List: [String]? = nil, // Base64 string
var mapiCertificateBase64List: [String]? = nil, // Base64 string
var baseURL: String, // Zorunlu
var locale: String? = nil,
var mobileUser: String? = nil,
var countryCode: String? = nil,
var useEmbeddedLocalSound: NSNumber? = nil // Yalnızca CoreBaseModel'de
)

### Özellikler

| Özellik | Tip | Zorunlu | Açıklama |
| --- | --- | --- | --- |
| `signallingCertificateList` | `[String]?` | — | Signalling sertifikalarının `.der` dosya adları |
| `mapiCertificateList` | `[String]?` | — | MAPI sertifikalarının `.der` dosya adları |
| `signallingCertificateBase64List` | `[String]?` | — | Signalling sertifikalarının Base64 halleri |
| `mapiCertificateBase64List` | `[String]?` | — | MAPI sertifikalarının Base64 halleri |
| `baseURL` | `String` | ✅ | Doğrulama platformunun sunucu adresi |
| `locale` | `String?` | — | Sesli yönlendirme dili (örn. `"TR"`) |
| `mobileUser` | `String?` | — | Authorization için anonymous user bilgisi |
| `countryCode` | `String?` | — | Ülke/bölge özelinde veri edinimi için (örn. `"TUR"`) |
| `useEmbeddedLocalSound` | `NSNumber?` | — | Yalnızca `CoreBaseModel`'de geçerlidir. Ses dosyası kaynağını belirler. Bkz. [Ses Dosyaları Yönetimi](https://enqura.atlassian.net/wiki/spaces/EDP/pages/25526291/iOS+-+Core+Mod+l#Ses-Dosyalar%C4%B1-Y%C3%B6netimi) |

Sertifikalar için `der` dosya adı ile Base64 string yöntemlerinden birini kullanmanız yeterlidir, ikisini birden doldurmanıza gerek yoktur.

**Sertifika adı eşleşmeli:** `signallingCertificateList` veya `mapiCertificateList`'e verdiğiniz dosya adı, Xcode'a eklediğiniz `.der` dosyasının adıyla birebir eşleşmelidir. Eşleşmezse runtime'da `ResponseValidation` hatası alırsınız.

### Kullanım Örneği

swift

wide760let baseModel = BaseModelOCR(
signallingCertificateList: ["enqura"],
mapiCertificateList: ["enqura"],
baseURL: "https://yourcompany-mapi.enqura.com",
locale: "TR",
mobileUser: "mobile",
countryCode: "TUR"
)
> **SSL Pinning'i devre dışı bırakmak** için sertifika alanlarını boş bırakın. Canlı ortamlarda bu **kesinlikle önerilmez** — ciddi güvenlik açığı oluşturur.

---

SessionModel
------------

`SessionModel`, her modülün `initialize()` fonksiyonuna geçilen oturum bilgisi modelidir. Kullanıcıya ve çağrıya ait bilgileri taşır.

Her modülün kendi `SessionModel` türü vardır (`SessionModelOCR`, `SessionModelNFC`, vb.) ancak içerdikleri alanlar aynıdır.

### Model Tanımı

swift

wide760class SessionModel(
var callType: String, // Zorunlu
var reference: String, // Zorunlu
var userName: String? = nil,
var surname: String? = nil,
var phone: String? = nil,
var email: String? = nil,
var identityType: String? = nil,
var identityNo: String? = nil,
var canAutoClose: Bool = false,
var isContinue: Bool = false,
var category: String? = nil,
var taxNumber: String? = nil,
var businessReference: String? = nil,
var handicapped: Bool? = false
)

### Özellikler

| Özellik | Tip | Zorunlu | Açıklama |
| --- | --- | --- | --- |
| `callType` | `String` | ✅ | Çağrı türü. Backoffice'den alınan değerler kullanılmalıdır (örn. `"NewCustomer"`). Mevcut tipler için Utility Modülü → Çağrı Tiplerinin Alınması sayfasına bakınız. |
| `reference` | `String` | ✅ | Oturuma ait referans ID'si |
| `userName` | `String?` | — | Kullanıcı adı |
| `surname` | `String?` | — | Kullanıcı soyadı |
| `phone` | `String?` | — | Telefon numarası |
| `email` | `String?` | — | E-posta adresi |
| `identityType` | `String?` | — | Kimlik türü: `"I"` (T.C. Kimlik Kartı), `"P"` (Pasaport) |
| `identityNo` | `String?` | — | Kimlik numarası |
| `canAutoClose` | `Bool` | — | Oturumun otomatik kapanıp kapanmayacağı. Varsayılan: `false` |
| `isContinue` | `Bool` | — | Oturumun devam eden bir işlem olup olmadığı. Varsayılan: `false` |
| `category` | `String?` | — | Oturumun ait olduğu kategori |
| `taxNumber` | `String?` | — | Kullanıcıya ait vergi numarası |
| `businessReference` | `String?` | — | İşletme referans bilgisi (KYB akışları için) |
| `handicapped` | `Bool?` | — | Kullanıcının özel gereksinimi olup olmadığı. Varsayılan: `false` |

### Kullanım Örneği

swift

wide760let sessionModel = SessionModelOCR(
callType: "NewCustomer",
reference: "REF123456",
userName: "Ahmet",
surname: "Yılmaz",
phone: "+905551234567",
email: "ahmet@example.com",
identityType: "I",
identityNo: "12345678901",
canAutoClose: true,
isContinue: false
)

---

Ses Dosyaları Yönetimi
----------------------

SDK, akışlar sırasında kullanıcıya sesli yönlendirme yapar. Ses dosyaları üç farklı şekilde yönetilebilir.

### `useEmbeddedLocalSound` Parametresi

`CoreBaseModel` içindeki bu parametre SDK'nın ses kaynağını belirler.

| Değer | Davranış |
| --- | --- |
| `1` (true) | SDK yalnızca uygulamaya gömülü ses dosyalarını kullanır. Ağ isteği atmaz. |
| `0` (false) | SDK başlatıldığında Backoffice'e bağlanır, güncel olmayan ses dosyalarını indirir ve günceller. |

### Özel Ses Dosyası Kullanımı (Local Override)

SDK'nın varsayılan seslerini kendi ses dosyalarınızla değiştirmek istiyorsanız, aşağıdaki listedeki dosya adlarıyla birebir aynı isimde ses dosyalarınızı uygulama bundle'ına ekleyin. SDK bu dosyaları otomatik olarak algılar ve varsayılan sesler yerine kullanır.

wide760snd\_start\_face snd\_start\_face\_left snd\_start\_face\_right
snd\_start\_face\_up snd\_face\_fail snd\_end\_liveness
snd\_liveness\_timeout snd\_liveness\_completed snd\_start\_eye\_close
snd\_end\_eye\_close snd\_start\_smile snd\_end\_smile
snd\_start\_id\_front snd\_end\_id\_front snd\_start\_id\_back
snd\_end\_id\_read snd\_id\_read\_timeout snd\_id\_type\_check\_timeout
snd\_start\_type\_check\_front snd\_start\_type\_check\_back
snd\_cross\_check\_fail snd\_start\_holo snd\_end\_chip
snd\_start\_chip\_front snd\_detect\_chip snd\_chip\_timeout
snd\_chip\_fail snd\_waiting\_agent snd\_ready\_to\_start\_id
snd\_ready\_to\_start\_chip

---

UI Özelleştirme
---------------

SDK arayüzü Backoffice üzerinden dinamik olarak özelleştirilebilir. Detaylar için UI Özelleştirme sayfasına bakınız.

---

Ortak Delegate'ler
------------------

Tüm modüllerde aşağıdaki delegate'ler ortaktır. Modüle özgü delegate'ler ilgili modül sayfasında ele alınmıştır.

### Token / Session / Settings

| Delegate | Ne Zaman Tetiklenir? |
| --- | --- |
| `tokenCreateCompleted()` | Token başarıyla oluşturulduğunda. Mevcut token varsa yeniden oluşturulmaz. |
| `tokenCreateFailed()` | Token oluşturulurken hata alındığında |
| `sessionAddFailed()` | Yeni oturum açılırken hata alındığında |
| `settingGetFailed()` | Backoffice ayarları çekilirken hata alındığında |
| `sessionCloseCompleted(status: String)` | Oturum başarıyla kapatıldığında. `status` parametresi oturumun kapanış durumunu taşır. |
| `sessionCloseFailed()` | Oturum kapatılırken hata alındığında |
| `integrationAddCompleted()` | IntegrationAdd servisi başarıyla tamamlandığında |
| `integrationAddFailed()` | IntegrationAdd servisinde hata alındığında |
| `initializeCompleted(moduleName: String)` | Tüm başlatma adımları tamamlandığında. `moduleName` ile hangi modülün hazır olduğu doğrulanabilir. |
| `initializeFailed(with key: CustomNSError)` | Başlatma sırasında (genellikle kamera izni verilmediğinde) hata alındığında |

### Session Kapatma

Her modülde `sessionClose()` aynı şekilde çalışır:

swift

wide760EnQualifyOCR.sessionClose(finished: false)
// finished: true → akış tamamlandı
// finished: false → akış iptal edildi veya yarıda bırakıldı

⚠️ Session kapatıldıktan sonra aynı modül tekrar kullanılacaksa `initialize()` yeniden çağrılmalıdır.

---

Modül sayfalarına geçmek için: OCR Modülü · NFC Modülü · Face Modülü · VideoCall Modülü · Utility Modülü