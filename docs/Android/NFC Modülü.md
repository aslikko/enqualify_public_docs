# Android - NFC Modülü

NFC modülü, kimlik kartları veya pasaportlar üzerindeki çip verilerini okumak için kullanılır. Okuma işlemi başarılı olabilmesi için kimlik belgesi üzerinden elde edilen belirli bilgilerin önceden sağlanması gerekir.

> ⚠️ **Ön Koşul:** NFC Modülünü kullanmadan önce Maven erişimi sağlanmış ve Core Modülü projeye eklenmiş olmalıdır. Core Modülü eklenmeden NFC Modülü tek başına çalışmaz.

---

## Gerekli Veriler

Çip verilerinin başarıyla okunabilmesi için aşağıdaki bilgilerin sağlanması zorunludur:

| Veri | Format | Örnek |
| --- | --- | --- |
| Seri Numarası | Alfanümerik | `A11A11111` |
| Kimlik Geçerlilik Tarihi | `YYMMDD` | `280621` |
| Doğum Tarihi | `YYMMDD` | `950621` |

Bu bilgiler sağlanmadan NFC okuma işlemi başarısız olur.

---

## Projeye Eklenmesi

### 1. `libs.versions.toml` dosyasına ekleyin:

wide760[versions]
...
enqualify-plus = "x.x.x.x"
[libraries]
...
enqualify-plus-nfc = {
group = "com.enqualify.plus",
name = "nfc",
version.ref = "enqualify-plus"
}

### 2. `build.gradle.kts` dosyasına bağımlılığı ekleyin:

wide760implementation(libs.enqualify.plus.nfc)

### 3. Gradle Sync

"Sync Now" seçeneğine tıklayarak Gradle dosyalarını senkronize edin.

---

## İmplementasyon

### 1. `onNewIntent` Fonksiyonunun Override Edilmesi

NFC işlemine gelen intent'leri yönetmek için SDK fonksiyonlarının kullanıldığı Activity'de `onNewIntent` override edilmelidir. Bu, EnQualify'dan gelen bir callback değil, `AppCompatActivity` üzerinden gelen bir sistem callback'idir:

wide760override fun onNewIntent(intent: Intent) {
super.onNewIntent(intent)
if (NfcAdapter.ACTION\_TAG\_DISCOVERED == intent.action ||
NfcAdapter.ACTION\_TECH\_DISCOVERED == intent.action) {
setIntent(intent)
} else {
super.onNewIntent(intent)
}
}

### 2. Activity Layout — FrameLayout

NFC işleminin yapılacağı Activity'nin layout'una tam ekran kaplayan bir `FrameLayout` eklenmelidir. SDK, sayfa geçişlerini bu bileşen üzerinden yönetir:

wide760<FrameLayout
android:id="@+id/fragmentContainer"
android:layout\_width="match\_parent"
android:layout\_height="match\_parent" />

### 3. NFCCallbacks Interface'inin Eklenmesi

`NFCCallbacks` interface'i NFC işlemlerini yönetmek için gerekli callback metodlarını içerir ve mutlaka bir **Activity** ile çalışmalıdır.

**Sınıfa eklenmesi:**

wide760class EnQualifyPlusActivity : AppCompatActivity(), NFCCallbacks

**Callback'lerin override edilmesi:**

wide760class EnQualifyPlusActivity : AppCompatActivity(), NFCCallbacks {
override fun initializeCompleted(modules: EnModules) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
when (modules) {
EnModules.NFC -> {
// NFC işlemleri başlatılabilir
}
}
}
override fun initializeFailed(failureCode: FailureCode, additionalMessage: String) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun nfcCompleted() {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun nfcFailed(nfcFailureCode: NFCFailureCode, additionalMessage: String?) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name} $nfcFailureCode: $additionalMessage")
}
override fun nfcSaveStarted() {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun integrationAddCompleted() {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun integrationAddFailed(errorMessage: String) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
}

### 4. Custom NFCReadFragment Oluşturulması

NFC okuma işlemini gerçekleştiren fragment, `EnNFCBaseFragment` sınıfından türetilmelidir. Bu sınıf NFC işlemlerine yönelik temel fonksiyonları sağlar ve okuma aşamalarını yönetir.

wide760class NfcReadFragment : EnNFCBaseFragment() {
private var \_binding: FragmentNfcReadBinding? = null
private val binding get() = \_binding!!
override fun onCreateView(
inflater: LayoutInflater,
container: ViewGroup?,
savedInstanceState: Bundle?
): View {
\_binding = FragmentNfcReadBinding.inflate(layoutInflater)
setupIndicators()
return binding.root
}
override fun onNfcReadStart() {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
setCurrentIndicator(0, R.string.nfc\_chip\_scan\_start)
}
}
> ℹ️ Tasarıma bağlı olarak fragment üzerinde özelleştirmeler yapılabilir.

### 5. EnQualifyNFC'nin Initialize Edilmesi

NFC işlemlerine başlamadan önce `EnQualifyNFC.initialize()` çağrılmalıdır. Initialize edilmeden başka bir işlem yapılmaya çalışılırsa SDK çalışmaz.

wide760val sessionModel = SessionModel(
callType = "NewCustomer",
reference = UUID.randomUUID().toString()
)
val baseModel = BaseModel(
baseURL = "https://deveqmapi.enqura.com",
signallingCertificateList = listOf("enqura"),
mapiCertificateList = listOf("enqura"),
mobileUser = "mobile",
countryCode = "TUR",
locale = "TR",
useEmbeddedLocalSound = false
)
EnQualifyNFC.initialize(
context = this,
fragmentManager = supportFragmentManager,
containerID = R.id.fragmentContainer,
sessionModel = sessionModel,
baseModel = baseModel
)

#### Initialize Parametreleri

| Parametre | Tip | Açıklama |
| --- | --- | --- |
| `context` | `Context` | Uygulamanın çalışma zamanı bağlamı |
| `sessionModel` | `SessionModel` | NFC işlemi sırasında kullanılacak oturum bilgileri |
| `baseModel` | `BaseModel` | Doğrulama sürecinde temel verileri taşıyan model |
| `fragmentManager` | `FragmentManager` | NFC fragment'lerinin yönetimini sağlar |
| `containerID` | `Int` | NFC fragment'inin ekleneceği container'ın ID'si |

#### Initialize Sonrası Otomatik Akış

`initialize()` çağrıldıktan sonra SDK sırasıyla Token → Session → Settings adımlarını otomatik yürütür. Hata durumlarında ilgili callback'ler tetiklenir:

wide760override fun tokenCreateFailed(errorMessage: String) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name} $errorMessage")
}
override fun sessionAddFailed(errorMessage: String) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun settingsGetFailed(errorMessage: String) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}

Tüm adımlar tamamlandığında `initializeCompleted` tetiklenir ve NFC işlemleri başlatılabilir.

---

## NFC İşlemleri

### Fonksiyonlar

| Fonksiyon | Açıklama |
| --- | --- |
| `addFragment(fragment)` | Mevcut fragment üzerine yeni bir fragment ekler |
| `replaceFragment(fragment)` | Mevcut fragment'i yenisiyle değiştirir |
| `nfcStart(fragment, documentNo, birthDate, expiryDate)` | NFC okuma işlemini başlatır |
| `addIntegration(integrationModel)` | Entegrasyon verisi ekler |
| `closeSession(isFinished: Boolean)` | Session'ı kapatır |
| `clear()` | SDK'yı temizler |

---

### NFC Okuma İşleminin Başlatılması

NFC okuma işlemi için kimlik belgesi verileri gereklidir. Bu veriler genellikle OCR işleminden sonra `CustomerIDDoc` nesnesinden otomatik olarak alınır:

wide760EnQualifyNFC.getInstance().nfcStart(
NfcReadFragment(),
CustomerIDDoc.getInstance().documentNumber,
CustomerIDDoc.getInstance().dateOfBirthDay,
CustomerIDDoc.getInstance().expiryDate
)

#### Fonksiyon Parametreleri

| Parametre | Tip | Açıklama |
| --- | --- | --- |
| `fragment` | `EnNFCBaseFragment` | `EnNFCBaseFragment`'tan türetilmiş NFC okuma fragment'i |
| `documentNo` | `String` | Belge/seri numarası |
| `birthDate` | `String` | Doğum tarihi — `YYMMDD` formatında (örn. 21.06.1995 → `950621`) |
| `expiryDate` | `String` | Geçerlilik tarihi — `YYMMDD` formatında (örn. 21.06.2028 → `280621`) |

> ℹ️ NFC işlemi OCR'dan önce yapılmak istenirse veriler manuel olarak yukarıdaki formatlarda girilmelidir.

---

### Okuma Akışı

1. **Okuma Tamamlandığında**

NFC okuma tamamlandığında SDK, okunan verileri backoffice'e otomatik göndermeye başlar ve `nfcSaveStarted` tetiklenir:

wide760override fun nfcSaveStarted() {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}

2. **Veri Gönderimi Tamamlandığında**

Veriler backoffice'e başarıyla iletildiğinde `nfcCompleted` tetiklenir:

wide760override fun nfcCompleted() {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
fragmentManager.replaceFragment(NfcResultFragment(), false)
}

---

### Hata Yönetimi

**Ciddi Hatalar:** NFC işleminin devam etmesini engelleyen hatalar `nfcFailed` ile iletilir:

wide760override fun nfcFailed(nfcFailureCode: NFCFailureCode, additionalMessage: String?) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name} $nfcFailureCode: $additionalMessage")
}

**Anlık Hatalar:** Temassızlık gibi geçici hatalar, `EnNFCBaseFragment`'tan türetilmiş fragment içindeki `onNfcError` callback'i ile iletilir:

wide760override fun onNfcError(error: String) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name} : $error")
if (isAdded) setCurrentIndicator(-1, R.string.empty)
}

---

### Entegrasyon Verisi Ekleme

wide760val integrationModel = IntegrationModel(
idRegistration = IDRegistration(),
addressRegistration = AddressRegistration(),
data = ""
)
enQualifyNFC.addIntegration(integrationModel)
wide760override fun integrationAddCompleted() {
Log.i(TAG, "integrationAddCompleted")
}
override fun integrationAddFailed(errorMessage: String) {
Log.i(TAG, "integrationAddFailed: $errorMessage")
}

---

### Session Kapatma ve Temizleme

wide760// Session'ı kapat
enQualifyNFC.closeSession(isFinished = true)
override fun sessionCloseCompleted() {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun sessionCloseFailed(errorMessage: String) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name} $errorMessage")
}
// SDK'yı temizle
enQualifyNFC.clear()
> ℹ️ Session kapatıldıktan sonra SDK'yı tekrar kullanmak için `initialize()` yeniden çağrılmalıdır.

---

## EnNFCBaseFragment

`EnNFCBaseFragment`, NFC okuma işlemini gerçekleştiren özel fragment'in türetileceği temel sınıftır. Okuma aşamalarını yönetmek, ilerleme göstergelerini güncellemek ve hata mesajlarını işlemek için gerekli fonksiyonları içerir.

### Callback Fonksiyonları

| Fonksiyon | Açıklama |
| --- | --- |
| `onNfcReadStart()` | NFC okuma başladığında çağrılır |
| `onNfcTagDetected()` | NFC etiketi okunduğunda tetiklenir |
| `onNfcRead(data: Any?)` | NFC verisi okunduğunda tetiklenir |
| `onNfcReadFinish()` | NFC okuma tamamlandığında tetiklenir |
| `onFirsLevelCompleted()` | Okuma sürecinin 1. aşaması tamamlandığında çağrılır |
| `onSecondLevelCompleted()` | Okuma sürecinin 2. aşaması tamamlandığında çağrılır |
| `onThirdLevelCompleted()` | Okuma sürecinin 3. aşaması tamamlandığında çağrılır |
| `onFourthLevelCompleted()` | Okuma sürecinin 4. aşaması tamamlandığında çağrılır |
| `onNfcError(error: String)` | Okuma sırasında geçici hata oluştuğunda çağrılır |

---

## Hata Kodları

### NFCFailureCode

wide760enum class NFCFailureCode(errorMessage: String) {
NFCReadFailed(""),
NFCStoreFailed(""),
NFCTimeout("Nfc timeout"),
NFCDisable("NFC is disabled on the device."),
PermissionDenied("NFC permission denied"),
MissingNFCKey("Invalid or Null MRZ keys."),
BacFailed("BAC failed"),
EfComNotRead("EF\_COM Access File not read"),
SodNotRead("Failed to retrieve EF.SOD file. Possible chip or file corruption"),
SodHashError("Failed to extract hash values from EF.SOD. Missing or unsupported algorithm."),
UnsupportedAlgorithm("Failed to extract hash values from EF.SOD. Missing or unsupported algorithm."),
Dg1NotRead("DG1 File not read"),
Dg11NotRead("DG11 File not read"),
Dg2NotRead("DG2 File not read"),
NotSupport("Device does not support NFC"),
Failed(""),
ChipAuthenticationFailed("Chip Authentication failed"),
ActiveAuthenticationFailed("Active Authentication failed"),
Dg14FileEmpty("DG14 File is empty"),
SodFileEmpty("SOD File is empty"),
StoredHashError(""),
CertificateValidationFailed("Certificate Validation failed"),
FidNotRead(""),
Dg14NotRead(""),
CertificateValidation(""),
HashMatchError("")
}

---

## Proguard Kuralları

Release paketlerinde NFC SDK'nın doğru çalışabilmesi için `proguard-rules.pro` dosyasına aşağıdaki kuralları ekleyin:

wide760-keep class net.sf.scuba.smartcards.\*\* { \*; }
-keep class org.bouncycastle.\*\* { \*; }
-dontwarn javax.naming.\*\*
-dontwarn org.bouncycastle.cert.dane.fetcher.JndiDANEFetcherFactory
-dontwarn com.enqualify.plus.ocr.OCRCallbacks$DefaultImpls
-dontwarn org.bouncycastle.jsse.BCSSLParameters
-dontwarn org.bouncycastle.jsse.BCSSLSocket
-dontwarn org.bouncycastle.jsse.provider.BouncyCastleJsseProvider
-dontwarn org.conscrypt.Conscrypt$Version
-dontwarn org.conscrypt.Conscrypt
-dontwarn org.conscrypt.ConscryptHostnameVerifier
-dontwarn org.openjsse.javax.net.ssl.SSLParameters
-dontwarn org.openjsse.javax.net.ssl.SSLSocket
-dontwarn org.openjsse.net.ssl.OpenJSSE

---

## Sonuç Verisine Erişim

NFC okuma işlemi tamamlandıktan sonra okunan verilere `CustomerChip` nesnesi üzerinden erişilir:

wide760CustomerChip.getInstance()

`CustomerChip` modeli ve tüm alanlarının açıklaması için Core Modülü — CustomerChip sayfasına bakınız.

---

## Callback Referansı

### Token / Session / Settings

| Callback | Açıklama |
| --- | --- |
| `tokenCreateCompleted(isNewCreatedToken: Boolean)` | Token oluşturulduğunda tetiklenir |
| `tokenCreateFailed(errorMessage: String)` | Token oluşturma hatası |
| `sessionAddFailed(errorMessage: String)` | Session oluşturma hatası |
| `settingsGetFailed(errorMessage: String)` | Ayarlar alınamadığında tetiklenir |
| `sessionCloseCompleted(status: CallSessionTypeStatus)` | Session kapatıldığında tetiklenir |
| `sessionCloseFailed(errorMessage: String)` | Session kapatma hatası |
| `integrationAddCompleted()` | Entegrasyon verisi başarıyla eklendi |
| `integrationAddFailed(errorMessage: String)` | Entegrasyon verisi eklenemedi |
| `initializeFailed(failureCode: FailureCode, additionalMessage: String)` | Core initialize hatası |

### NFC

| Callback | Açıklama |
| --- | --- |
| `initializeCompleted(module: EnModules)` | Initialize tamamlandı, NFC hazır |
| `nfcSaveStarted()` | Veriler backoffice'e gönderilmeye başlandı |
| `nfcCompleted()` | Veriler backoffice'e başarıyla iletildi |
| `nfcFailed(nfcFailureCode, additionalMessage)` | NFC işlem hatası (ciddi) |