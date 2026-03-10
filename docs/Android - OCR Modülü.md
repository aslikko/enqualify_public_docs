# Android - OCR Modülü

OCR modülü, arka kamera üzerinden alınan görüntülerle kimlik kartı veya pasaport üzerindeki verileri okur. Görsel obje analizi, hologram tespiti, kimlik ön/arka yüz okuma ve MRZ alanı okuma işlemlerini gerçekleştirir.

> ⚠️ **Ön Koşul:** OCR Modülünü kullanmadan önce Maven erişimi sağlanmış ve Core Modülü projeye eklenmiş olmalıdır.

---

Projeye Eklenmesi
-----------------

### 1. `libs.versions.toml` dosyasına ekleyin:

wide760[versions]
...
enqualify-plus = "x.x.x.x"
[libraries]
...
enqualify-plus-ocr = {
group = "com.enqualify.plus",
name = "ocr",
version.ref = "enqualify-plus"
}

### 2. `build.gradle.kts` dosyasına bağımlılığı ekleyin:

wide760implementation(libs.enqualify.plus.ocr)

### 3. Gradle Sync

"Sync Now" seçeneğine tıklayarak Gradle dosyalarını senkronize edin.

> ℹ️ Versiyon numarası tüm modüllerde aynı olmalıdır.

---

İmplementasyon
--------------

### 1. İzinler

Kamera izni SDK tarafından manifeste otomatik olarak eklenir ve gerekli noktalarda yine SDK tarafından istenir. Aşağıdaki satır yalnızca bilgi amaçlıdır:

wide760<uses-permission android:name="android.permission.CAMERA" />
> Kamera izni verilmezse OCR modülü çalışmaz.

### 2. Activity Layout — FrameLayout

OCR işleminin yapılacağı Activity'nin layout'una tam ekran kaplayan bir `FrameLayout` eklenmelidir. SDK, kamera ekranlarını ve sayfa geçişlerini bu bileşen üzerinden yönetir:

wide760<FrameLayout
android:id="@+id/fragmentContainer"
android:layout\_width="match\_parent"
android:layout\_height="match\_parent" />

### 3. OCRCallbacks Interface'inin Eklenmesi

`OCRCallbacks` interface'i OCR işlemlerini yönetmek için gerekli callback metodlarını içerir ve mutlaka bir **Activity** ile çalışmalıdır.

**Sınıfa eklenmesi:**

wide760class EnQualifyPlusActivity : AppCompatActivity(), OCRCallbacks

**Callback'lerin override edilmesi:**

wide760class EnQualifyPlusActivity : AppCompatActivity(), OCRCallbacks {
override fun IDDocTypeCheckVerified(isFront: Boolean) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun IDDocFrontCompleted() {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun hologramCheckVerified() {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun IDDocBackCompleted() {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun IDDocSaveStarted() {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun IDDocCompleted() {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun IDDocFailed(ocrFailureCode: OCRFailureCode, additionalMessage: String?) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
// LuminosityFailed iş kesici bir hata değildir; okuma durdurulmamalıdır.
}
override fun initializeCompleted(module: EnModules) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
when (module) {
EnModules.OCR -> {
// OCR işlemleri başlatılabilir
}
}
}
override fun initializeFailed(failureCode: FailureCode, additionalMessage: String) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
}

### 4. EnQualifyOCR'ın Initialize Edilmesi

OCR işlemlerine başlamadan önce `EnQualifyOCR.initialize()` çağrılmalıdır. Initialize edilmeden başka bir işlem yapılmaya çalışılırsa SDK çalışmaz.

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
EnQualifyOCR.initialize(
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
| `sessionModel` | `SessionModel` | OCR işlemi sırasında kullanılacak oturum bilgileri |
| `baseModel` | `BaseModel` | Doğrulama sürecinde temel verileri taşıyan model |
| `fragmentManager` | `FragmentManager` | OCR fragment'lerinin yönetimini sağlar |
| `containerID` | `Int` | OCR fragment'inin ekleneceği container'ın ID'si |

#### Initialize Sonrası Otomatik Akış

`initialize()` çağrıldıktan sonra SDK sırasıyla şu adımları otomatik olarak yürütür:

1. **Token Oluşturma** Token oluşturma başarısız olursa `tokenCreateFailed` tetiklenir:

wide760override fun tokenCreateFailed(errorMessage: String) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name} $errorMessage")
}

2. **Oturum Başlatma** Oturum başlatma başarısız olursa `sessionAddFailed` tetiklenir:

wide760override fun sessionAddFailed(errorMessage: String) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}

3. **Ayarların Alınması** Ayarlar alınamazsa `settingsGetFailed` tetiklenir:

wide760override fun settingsGetFailed(errorMessage: String) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}

4. **Tamamlanma** Tüm adımlar başarıyla tamamlandığında `initializeCompleted` tetiklenir ve OCR işlemleri başlatılabilir.

---

OCR İşlemleri
-------------

### Fonksiyonlar

| Fonksiyon | Açıklama |
| --- | --- |
| `addFragment(fragment)` | Mevcut fragment üzerine yeni bir fragment ekler |
| `replaceFragment(fragment)` | Mevcut fragment'i yenisiyle değiştirir |
| `iDDocTypeCheckStart(isFront: Boolean = true)` | Kimlik tipi tanıma işlemini başlatır |
| `hologramCheckStart()` | Hologram tespit işlemini başlatır |
| `iDDocFrontStart(withVisualAnalysis: Boolean = false)` | Kimlik ön yüzü taramasını başlatır |
| `iDDocBackStart(withVisualAnalysis: Boolean = false)` | Kimlik arka yüzü taramasını başlatır |
| `iDDocComplete()` | Tüm kimlik okuma adımlarının tamamlandığını SDK'ya bildirir |
| `addIntegration(integrationModel)` | Entegrasyon verisi ekler |
| `closeSession(isFinished: Boolean)` | Session'ı kapatır |
| `clear()` | SDK'yı temizler |

---

### Kimlik Tipi Tanıma

wide760enQualifyOCR.iDDocTypeCheckStart(isFront = true)

İşlem tamamlandığında `IDDocTypeCheckVerified` tetiklenir. `isFront` parametresi, sürecin `iDDocFrontStart` mı yoksa `iDDocBackStart` mı ile devam edeceğini belirler:

wide760override fun IDDocTypeCheckVerified(isFront: Boolean) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}

---

### Kimlik Ön Yüzü Tarama

wide760enQualifyOCR.iDDocFrontStart(withVisualAnalysis = true)

İşlem tamamlandığında `IDDocFrontCompleted` tetiklenir:

wide760override fun IDDocFrontCompleted() {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}

---

### Hologram Tespiti

wide760enQualifyOCR.hologramCheckStart()

İşlem tamamlandığında `hologramCheckVerified` tetiklenir:

wide760override fun hologramCheckVerified() {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}

---

### Kimlik Arka Yüzü Tarama

wide760enQualifyOCR.iDDocBackStart(withVisualAnalysis = true)

İşlem tamamlandığında `IDDocBackCompleted` tetiklenir:

wide760override fun IDDocBackCompleted() {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}

---

### Kimlik Okuma Akışını Bitirme

Tüm adımlar tamamlandığında `iDDocComplete()` çağrılır. Bu fonksiyon kamera analizini durdurur, işlem sürecini sonlandırır ve okunan verilerin backoffice'e gönderilmesini başlatır:

wide760enQualifyOCR.iDDocComplete()

Veriler backoffice'e başarıyla iletildiğinde `IDDocCompleted` tetiklenir:

wide760override fun IDDocCompleted() {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}

---

### Entegrasyon Verisi Ekleme

wide760val integrationModel = IntegrationModel(
idRegistration = IDRegistration(),
addressRegistration = AddressRegistration(),
data = ""
)
enQualifyOCR.addIntegration(integrationModel)

Sonuçlar aşağıdaki callback'lerle dinlenir:

wide760override fun integrationAddCompleted() {
Log.i(TAG, "integrationAddCompleted")
}
override fun integrationAddFailed(errorMessage: String) {
Log.i(TAG, "integrationAddFailed: $errorMessage")
}

---

### Session Kapatma ve Temizleme

wide760// Session'ı kapat
enQualifyOCR.closeSession(isFinished = true)
// Session kapatma callback'leri
override fun sessionCloseCompleted() {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun sessionCloseFailed(errorMessage: String) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name} $errorMessage")
}
// SDK'yı temizle (session kapatıldıktan sonra çağrılmalıdır)
enQualifyOCR.clear()
> ℹ️ Session kapatıldıktan sonra SDK'yı tekrar kullanmak için `initialize()` yeniden çağrılmalıdır.

---

Hata Yönetimi
-------------

### FailureCode (Core / Initialize Hataları)

wide760enum class FailureCode(val errorMessage: String) {
CameraError("Unable to access the camera. Please check device settings and retry."),
CameraStartError(""),
CameraNotSupported("Failed to initialize the camera. Device may not support required resolution or FPS."),
SdkInitializationError("Required sdk initialization did not completed."),
CameraPermissionDenied("Camera permission denied"),
CertificateFailed("Certificate failed"),
AIModelNotFound("AI model not found"),
NfcCertificateNotFound("Nfc Certificate not found")
}

`initializeFailed` callback'i aracılığıyla iletilir:

wide760override fun initializeFailed(failureCode: FailureCode, additionalMessage: String) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}

### OCRFailureCode (OCR İşlem Hataları)

wide760enum class OCRFailureCode(errorMessage: String) {
IDDocSaveFailed("save failed"),
LuminosityFailed("Luminosity failed"), // İş kesici değildir — okuma durdurulmamalıdır
TypeCheckFailed(""),
HologramCheckError(""),
VisualAnalysingFrontError(""),
VisualAnalysingBackError(""),
ReadIdDocFrontError(""),
ReadIdDocBackError(""),
ReadPassportError(""),
IDDocError(""),
CameraError("Unable to access the camera. Please check device settings and retry."),
CameraStartError(""),
CameraNotSupported("Failed to initialize the camera. Device may not support required resolution or FPS."),
SdkInitializationError("Required sdk initialization did not completed."),
CameraPermissionDenied("Camera permission denied"),
Failed(""),
IDDocTimeout("Timeout")
}

`IDDocFailed` callback'i aracılığıyla iletilir:

wide760override fun IDDocFailed(ocrFailureCode: OCRFailureCode, additionalMessage: String?) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
> ⚠️ **Önemli:** `LuminosityFailed` bir uyarı niteliğindedir ve iş kesici değildir. Bu hata geldiğinde okuma işlemi durdurulmamalıdır.

---

Sonuç Verisine Erişim
---------------------

OCR okuma işlemi tamamlandıktan sonra okunan verilere `CustomerIDDoc` nesnesi üzerinden erişilir:

wide760CustomerIDDoc.getInstance()

`CustomerIDDoc` modeli ve tüm alanlarının açıklaması için Core Modülü — CustomerIDDoc sayfasına bakınız.

---

Callback Referansı
------------------

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

### OCR

| Callback | Açıklama |
| --- | --- |
| `initializeCompleted(module: EnModules)` | Initialize tamamlandı, OCR hazır |
| `IDDocTypeCheckVerified(isFront: Boolean)` | Kimlik tipi başarıyla tespit edildi |
| `hologramCheckVerified()` | Hologram başarıyla tespit edildi |
| `IDDocFrontCompleted()` | Ön yüz okuma tamamlandı |
| `IDDocBackCompleted()` | Arka yüz okuma tamamlandı |
| `IDDocSaveStarted()` | Veriler backoffice'e gönderilmeye başlandı |
| `IDDocCompleted()` | Veriler backoffice'e başarıyla iletildi |
| `IDDocFailed(ocrFailureCode, additionalMessage)` | OCR işlem hatası |