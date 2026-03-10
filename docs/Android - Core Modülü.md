# Android - Core Modülü

Core Modülü, diğer tüm modüllerin kullanımı için temel yapı ve işlevsellikleri sağlayan modüldür. Proje genelinde tekrar kullanılabilir bileşenleri ve altyapıyı barındırır. **Diğer tüm modülleri kullanmadan önce Core Modülü projeye eklenmiş olmalıdır.**

---

Projeye Eklenmesi
-----------------

Maven erişimlerinin sağlandığından emin olduktan sonra aşağıdaki adımları izleyin. (Bkz. Başlarken)

### 1. `libs.versions.toml` dosyasına ekleyin:

wide760[versions]
...
enqualify-plus = "x.x.x.x"
[libraries]
...
enqualify-plus-core = {
group = "com.enqualify.plus",
name = "core",
version.ref = "enqualify-plus"
}

### 2. `build.gradle.kts` dosyasına bağımlılığı ekleyin:

wide760implementation(libs.enqualify.plus.core)

### 3. Gradle Sync

"Sync Now" seçeneğine tıklayarak Gradle dosyalarını senkronize edin.

> ℹ️ Kullanılacak versiyon numarası size özel olarak iletilir. Tüm modüller aynı versiyonu kullanmalıdır.

---

İzinler
-------

SDK, ağ bağlantı tipiyle ilgili detaylı bilgi alabilmek (2G/3G/4.5G) için aşağıdaki iznin **uygulama tarafından manuel olarak alınması** gerekir:

wide760<uses-permission android:name="android.permission.READ\_PHONE\_STATE" />
> ⚠️ Bu izin SDK tarafından otomatik olarak talep edilmez. İzin verilmezse mobil veri tipi yalnızca `"Mobile"` olarak görüntülenir.

---

Veri Modelleri
--------------

### BaseModel

Doğrulama süreçlerinde kullanılan sunucu (backoffice) bağlantı adresini ve SSL sertifika bilgilerini içeren veri modelidir.

Signalling (Görüntülü Görüşme) ve MAPI sertifikaları hem dosya formatında hem de Base64 formatında verilebilir; iki formatın birlikte verilmesine gerek yoktur. Sertifika dosyaları Android projesi içinde `res/raw` klasörüne eklenmelidir ve aynı dosya adı bu modelde parametre olarak verilmelidir. Sertifika verilmezse SDK, SSL Pinning özelliği olmadan çalışır.

wide760data class BaseModel(
var baseURL: String, // Zorunlu alan
var signallingCertificateList: List<String>? = null,
var mapiCertificateList: List<String>? = null,
var signallingCertificateBase64List: List<String>? = null,
var mapiCertificateBase64List: List<String>? = null,
var mobileUser: String, // Zorunlu alan
var countryCode: String? = null, // Default: "TUR"
var locale: String = "TR",
var useEmbeddedLocalSound: Boolean = false
)

#### Özellikler

| Özellik | Tip | Zorunlu | Açıklama |
| --- | --- | --- | --- |
| `baseURL` | `String` | ✅ | API doğrulama işlemleri için kullanılan temel sunucu adresi |
| `mobileUser` | `String` | ✅ | Token işlemi sırasında kullanılan özel keyword |
| `signallingCertificateList` | `List<String?>?` | — | Signalling (GG) sertifikalarının metin formatındaki dizisi |
| `mapiCertificateList` | `List<String?>?` | — | MAPI sertifikalarının metin formatındaki dizisi |
| `signallingCertificateBase64List` | `List<String?>?` | — | Signalling sertifikalarının Base64 formatındaki dizisi |
| `mapiCertificateBase64List` | `List<String?>?` | — | MAPI sertifikalarının Base64 formatındaki dizisi |
| `countryCode` | `String` | — | Okuma işlemi yapılacak kimliğin ülke kodu |
| `locale` | `String` | — | Sesli yönlendirmeler ve metinlerin dili (varsayılan: `"TR"`) |
| `useEmbeddedLocalSound` | `Boolean` | — | Seslerin lokalden mi yoksa servisten mi kullanılacağını belirler (varsayılan: `false`) |

#### Kullanım Örneği

wide760val baseModel = BaseModel(
signallingCertificateList = listOf("AI\_CERT\_1", "AI\_CERT\_2"),
mapiCertificateList = listOf("MAPI\_CERT\_1", "MAPI\_CERT\_2"),
signallingCertificateBase64List = listOf("QUlDRVJU...", "Q0VSVF8y..."),
mapiCertificateBase64List = listOf("TU9SRSB...", "Q0VSVF8z..."),
baseURL = "API\_SERVER\_URL",
mobileUser = "mobile",
countryCode = "TUR",
locale = "TR",
useEmbeddedLocalSound = false
)

---

### SessionModel

Bir çağrı oturumu sırasında kullanıcı ve kimlik bilgilerini içeren veri modelidir. Çağrı türü, kullanıcı detayları, kimlik bilgileri ve oturumla ilgili ek parametreleri içerir.

wide760data class SessionModel(
var callType: String, // Zorunlu alan
var reference: String, // Zorunlu alan
var userName: String? = null,
var surname: String? = null,
var phone: String? = null,
var email: String? = null,
var identityType: String? = null,
var identityNo: String? = null,
var canAutoClose: Boolean = false,
var isContinue: Boolean = false, // Kotlin'de 'continue' rezerve olduğu için isContinue
var category: String? = null,
var taxNumber: String? = null,
var businessReference: String? = null,
var handicapped: Boolean? = false
)

#### Özellikler

| Özellik | Tip | Zorunlu | Açıklama |
| --- | --- | --- | --- |
| `callType` | `String` | ✅ | Çağrı türünü belirten parametre (örn. `"NewCustomer"`) |
| `reference` | `String` | ✅ | Oturum için referans ID'si |
| `userName` | `String?` | — | Kullanıcının adı |
| `surname` | `String?` | — | Kullanıcının soyadı |
| `phone` | `String?` | — | Kullanıcının telefon numarası |
| `email` | `String?` | — | Kullanıcının e-posta adresi |
| `identityType` | `String?` | — | Kimlik türü (örn. `"I"`, `"P"`) |
| `identityNo` | `String?` | — | Kullanıcının kimlik numarası |
| `canAutoClose` | `Boolean` | — | Oturumun otomatik kapanıp kapanmayacağını belirler (varsayılan: `false`) |
| `isContinue` | `Boolean` | — | Oturumun devam eden bir işlem olup olmadığını belirler (varsayılan: `false`) |
| `category` | `String?` | — | Oturumun ait olduğu kategori |
| `taxNumber` | `String?` | — | Kullanıcıya ait vergi numarası |
| `businessReference` | `String?` | — | İşletme ile ilgili referans bilgisi |
| `handicapped` | `Boolean?` | — | Kullanıcının engelli olup olmadığını belirten bayrak (varsayılan: `false`) |

#### Kullanım Örneği

wide760val session = SessionModel(
callType = "NewCustomer",
reference = UUID.randomUUID().toString(),
userName = "Enqura",
surname = "Information",
phone = "+905551234567",
email = "enqualifyplus@enqura.com",
identityType = "TC. Kimlik Kartı",
identityNo = "12345678901",
canAutoClose = true,
isContinue = false,
category = "category",
taxNumber = "9876543210",
businessReference = "COMPANY",
handicapped = false
)

---

### CustomerIDDoc

OCR işlemi sonucunda kimlik belgesi üzerinden okunan verilerin depolandığı veri modelidir. Singleton yapıda çalışır; veriye `CustomerIDDoc.getInstance()` ile erişilir.

> Detaylı bilgi için OCR Modülü sayfasına bakınız.

wide760class CustomerIDDoc {
var identityType: String = ""
var name: String = ""
var surname: String = ""
var identityNumber: String = ""
var issuingState: String = ""
var documentNumber: String = ""
var dateOfBirthDay: String = ""
var expiryDate: String = ""
var nationality: String = ""
var gender: String = ""
var frontImage: Bitmap? = null
var mrzImage: Bitmap? = null
var holoImage: Bitmap? = null
var face: Bitmap? = null
var frontIdentityNumber: String? = null
var frontExpiryDate: String? = null
var frontBirthDate: String? = null
var frontGender: String? = null
var frontDocumentNumber: String? = null
var optionalData1: String? = null
var optionalData2: String? = null
var mrzText: String? = null
val visualItems: MutableMap<String, VisualItem> = mutableMapOf()
var digitDocumentNumber: Char? = null
var digitDateOfBirth: Char? = null
var digitExpiryDate: Char? = null
var sumDigit: Char? = null
}

#### Özellikler

| Özellik | Tip | Açıklama |
| --- | --- | --- |
| `identityType` | `String` | Kimlik türü (`"I"` veya `"P"`) |
| `name` | `String` | Kimlik sahibinin adı |
| `surname` | `String` | Kimlik sahibinin soyadı |
| `identityNumber` | `String` | Kimlik numarası |
| `issuingState` | `String` | Kimliğin verildiği ülke/bölge kodu |
| `documentNumber` | `String` | Kimliğin belge numarası |
| `dateOfBirthDay` | `String` | Kimlik sahibinin doğum tarihi |
| `expiryDate` | `String` | Kimliğin son geçerlilik tarihi |
| `nationality` | `String` | Kimlik sahibinin vatandaşlık ülkesi kodu |
| `gender` | `String` | Cinsiyet (E/M, K/F vb.) |
| `frontImage` | `Bitmap?` | Kimliğin ön yüzü görseli (MRZ önde olan kimliklerde boş gelir) |
| `mrzImage` | `Bitmap?` | MRZ alanının görseli |
| `holoImage` | `Bitmap?` | Hologram alanının görseli |
| `face` | `Bitmap?` | Kimlik üzerindeki fotoğraf (18 yaş altı kimliklerde boş gelebilir) |
| `frontIdentityNumber` | `String?` | Ön yüzden alınan kimlik numarası |
| `frontExpiryDate` | `String?` | Ön yüzden alınan son geçerlilik tarihi |
| `frontBirthDate` | `String?` | Ön yüzden alınan doğum tarihi |
| `frontGender` | `String?` | Ön yüzden alınan cinsiyet bilgisi |
| `frontDocumentNumber` | `String?` | Ön yüzden alınan belge numarası |
| `optionalData1` | `String?` | MRZ alanındaki opsiyonel veri 1 |
| `optionalData2` | `String?` | MRZ alanındaki opsiyonel veri 2 |
| `mrzText` | `String?` | MRZ alanındaki tam metin |
| `visualItems` | `MutableMap<String, VisualItem>` | Görsel analiz sonrası tespit edilen objelerin görselleri |
| `digitDocumentNumber` | `Char?` | Belge numarasının MRZ doğrulama rakamı |
| `digitDateOfBirth` | `Char?` | Doğum tarihinin MRZ doğrulama rakamı |
| `digitExpiryDate` | `Char?` | Son geçerlilik tarihinin MRZ doğrulama rakamı |
| `sumDigit` | `Char?` | MRZ alanının genel doğrulama rakamı |

#### Kullanım Örneği

wide760private lateinit var customerIdDoc: CustomerIDDoc
override fun init() {
customerIdDoc = CustomerIDDoc.getInstance()
initPage()
}

---

### CustomerChip

NFC okuma işlemi sonucunda kimlik çipinden okunan verilerin depolandığı veri modelidir. BAC, CA, HT, AA ve CS gibi NFC güvenlik protokollerinin sonuçlarını da içerir. Singleton yapıda çalışır; veriye `CustomerChip.getInstance()` ile erişilir.

> Detaylı bilgi için NFC Modülü sayfasına bakınız.

wide760class CustomerChip {
var documentCode: DocumentCode = DocumentCode.I
var identityType: String? = null
var identityNo: String? = null
var documentNo: String? = null
var firstName: String? = null
var lastName: String? = null
var gender: String? = null
var birthDate: String? = null
var nationality: String? = null
var expiryDate: String? = null
var faceImage: Bitmap? = null
var nameOfHolder: String? = null
var surnameOfHolder: String? = null
var placeOfBirth: String? = null
var fullDateOfBirth: String? = null
var BAC: NFCFeatureWithResult<Boolean> = NFCFeatureWithResult()
var CA: NFCFeatureWithResult<EACCAResult> = NFCFeatureWithResult()
var HT: NFCFeatureWithResult<MutableMap<Int, HashMatchResult>?> = NFCFeatureWithResult()
var AA: NFCFeatureWithResult<AAResult> = NFCFeatureWithResult()
var CS: NFCFeatureWithResult<Boolean> = NFCFeatureWithResult()
}

#### Temel Özellikler

| Özellik | Tip | Açıklama |
| --- | --- | --- |
| `documentCode` | `DocumentCode` | Belge türünü belirten enum değeri |
| `identityType` | `String?` | Kimlik belgesinin türü |
| `identityNo` | `String?` | Kimlik belgesi numarası |
| `documentNo` | `String?` | Resmi belge numarası |
| `firstName` | `String?` | Belge sahibinin adı |
| `lastName` | `String?` | Belge sahibinin soyadı |
| `gender` | `String?` | Cinsiyet bilgisi |
| `birthDate` | `String?` | Doğum tarihi |
| `nationality` | `String?` | Vatandaşlık ülkesi |
| `expiryDate` | `String?` | Belgenin son geçerlilik tarihi |
| `faceImage` | `Bitmap?` | Çipten alınan biyometrik fotoğraf (Face modülüyle karşılaştırmada kullanılır) |
| `nameOfHolder` | `String?` | Belge sahibinin yerel adı |
| `surnameOfHolder` | `String?` | Belge sahibinin yerel soyadı |
| `placeOfBirth` | `String?` | Doğum yeri |
| `fullDateOfBirth` | `String?` | Tam doğum tarihi (gün, ay, yıl) |

#### NFC Güvenlik Protokolü Sonuçları

| Özellik | Tip | Açıklama |
| --- | --- | --- |
| `BAC` | `NFCFeatureWithResult<Boolean>` | Basic Access Control — belge okuma güvenlik protokolü sonucu (`true`: başarılı) |
| `CA` | `NFCFeatureWithResult<EACCAResult>` | Chip Authentication — chip kimlik doğrulama sonucu |
| `HT` | `NFCFeatureWithResult<MutableMap<Int, HashMatchResult>?>` | Hash Table — hash değeri doğrulama sonuçları |
| `AA` | `NFCFeatureWithResult<AAResult>` | Active Authentication — asimetrik şifreleme ile kimlik doğrulama sonucu |
| `CS` | `NFCFeatureWithResult<Boolean>` | Chip Signature — chip imzası geçerlilik sonucu (`true`: geçerli) |

#### Kullanım Örneği

wide760private lateinit var customerChip: CustomerChip
override fun init() {
customerChip = CustomerChip.getInstance()
initPage()
}

---

### CustomerFace

Yüz tanıma ve canlılık kontrolü işlemi sonucunda elde edilen verilerin depolandığı veri modelidir. Singleton yapıda çalışır; veriye `CustomerFace.getInstance()` ile erişilir.

> Detaylı bilgi için Face Modülü sayfasına bakınız.

#### Temel Özellikler

| Özellik | Tip | Açıklama |
| --- | --- | --- |
| `faceDetectedImage` | `Bitmap?` | Kamerada algılanan yüzün görüntüsü |
| `smilingDetectedImage` | `Bitmap?` | Gülümseme algılandığında elde edilen görüntü |
| `possibilityOfSmiling` | `Float?` | Gülümseme olasılığı (0–1 arası) |
| `faceLeftDetectedImage` | `Bitmap?` | Baş sola döndüğünde elde edilen görüntü |
| `faceRightDetectedImage` | `Bitmap?` | Baş sağa döndüğünde elde edilen görüntü |
| `faceUpDetectedImage` | `Bitmap?` | Baş yukarıya kaldırıldığında elde edilen görüntü |
| `eyeCloseDetectedImage` | `Bitmap?` | Gözler kapalı olduğunda elde edilen görüntü |
| `antiSpoofing` | `Double?` | Sahtecilik tespiti skoru |
| `antiSpoofingValidityLevel` | `Int?` | Anti-spoofing geçerlilik seviyesi |
| `idDocConfidence` | `Int?` | Kimlik fotoğrafı ile yüz karşılaştırma güven derecesi |
| `idDocDistance` | `Double?` | Kimlik belgesi ile yüz arasındaki mesafe |
| `chipConfidence` | `Int?` | NFC çipi biyometriği ile yüz karşılaştırma güven derecesi |
| `chipDistance` | `Double?` | NFC çipi ile yüz arasındaki mesafe |

---

### IntegrationModel

`addIntegration` fonksiyonu aracılığıyla entegrasyon aşamasında SDK üzerinden veri göndermek için kullanılan veri modelidir.

wide760data class IntegrationModel(
val phone: String? = null,
val email: String? = null,
val formUrl: String? = null,
val idRegistration: IDRegistration? = null,
val addressRegistration: AddressRegistration? = null,
val data: String
)

---

Proguard Kuralları
------------------

Release paketlerinde (`minifyEnabled = true`, `debuggable = false`) Core SDK'nın doğru çalışabilmesi için `proguard-rules.pro` dosyasına aşağıdaki kuralları ekleyin:

wide760-keep interface com.enqualify.plus.core.CoreCallbacks { \*; }
-keep public class com.enqualify.plus.core.\*\* { \*; }
-keepclassmembers class \* { public static <methods>; }
-keep interface com.enqualify.plus.core.\*\* { \*; }
-keep class com.enqualify.plus.core.\*\* { abstract \*; }
-keep @androidx.annotation.Keep class \* { \*; }
-keepclassmembers,allowobfuscation class \* { @androidx.annotation.Keep \*; }

---

Sıradaki Adımlar
----------------

Core Modülü kurulumunu tamamladıktan sonra ihtiyacınıza göre aşağıdaki modüllere geçebilirsiniz:

* OCR Modülü — Kimlik belgelerinden optik karakter tanıma
* NFC Modülü — Kimlik çiplerinden NFC okuma
* Face Modülü — Yüz tanıma ve canlılık kontrolü
* VideoCall Modülü — Görüntülü görüşme entegrasyonu