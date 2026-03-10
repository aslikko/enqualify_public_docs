# Android - Face Modülü

Face modülü, ön kamera üzerinden alınan görüntülerle kişinin gerçek bir birey olup olmadığını analiz eder. Gülümseme, göz kapama, başı sağa/sola çevirme ve yukarı bakma gibi yüz ifadelerini ve hareketlerini algılayabilir. Özellikle canlılık kontrolü gerektiren kimlik doğrulama süreçlerinde kullanılır.

> ⚠️ **Ön Koşul:** Face Modülünü kullanmadan önce Maven erişimi sağlanmış ve Core Modülü projeye eklenmiş olmalıdır.

---

## Projeye Eklenmesi

### 1. `libs.versions.toml` dosyasına ekleyin:

wide760[versions]
...
enqualify-plus = "x.x.x.x"
[libraries]
...
enqualify-plus-face = {
group = "com.enqualify.plus",
name = "face",
version.ref = "enqualify-plus"
}

### 2. `build.gradle.kts` dosyasına bağımlılığı ekleyin:

wide760implementation(libs.enqualify.plus.face)

### 3. Gradle Sync

"Sync Now" seçeneğine tıklayarak Gradle dosyalarını senkronize edin.

---

## İmplementasyon

### 1. İzinler

Kamera izni SDK tarafından manifeste otomatik olarak eklenir ve gerekli noktalarda yine SDK tarafından istenir. Aşağıdaki satır yalnızca bilgi amaçlıdır:

wide760<uses-permission android:name="android.permission.CAMERA" />
> Kamera izni verilmezse Face modülü çalışmaz.

### 2. Activity Layout — FrameLayout

Face işleminin yapılacağı Activity'nin layout'una tam ekran kaplayan bir `FrameLayout` eklenmelidir. SDK, kamera ekranlarını ve sayfa geçişlerini bu bileşen üzerinden yönetir:

wide760<FrameLayout
android:id="@+id/fragmentContainer"
android:layout\_width="match\_parent"
android:layout\_height="match\_parent" />

### 3. FaceCallbacks Interface'inin Eklenmesi

`FaceCallbacks` interface'i Face işlemlerini yönetmek için gerekli callback metodlarını içerir ve mutlaka bir **Activity** ile çalışmalıdır.

**Sınıfa eklenmesi:**

wide760class EnQualifyPlusActivity : AppCompatActivity(), FaceCallbacks

**Callback'lerin override edilmesi:**

wide760class EnQualifyPlusActivity : AppCompatActivity(), FaceCallbacks {
override fun initializeCompleted(modules: EnModules) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
when (modules) {
EnModules.FACE -> {
// Face işlemleri başlatılabilir
}
}
}
override fun initializeFailed(failureCode: FailureCode, additionalMessage: String) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
// Canlılık adımı callback'leri
override fun faceDetected() { Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}") }
override fun smileDetected() { Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}") }
override fun eyeCloseDetected() { Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}") }
override fun eyeCloseIntervalDetected() { Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}") }
override fun faceRightDetected() { Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}") }
override fun faceLeftDetected() { Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}") }
override fun faceUpDetected() { Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}") }
// Karşılaştırma callback'leri
override fun faceCompareStarted() { Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}") }
override fun faceCompareCompleted() { Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}") }
override fun faceCompareFailed(errorMessage: String) { Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}") }
// Tamamlanma / hata callback'leri
override fun faceSaveStarted() { Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}") }
override fun faceCompleted() {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
enQualifyFace.faceCompare() // faceCompleted sonrası faceCompare başlatılır
}
override fun faceDetectFailed(failureCode: FaceFailureCode) { Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}") }
override fun faceFailed(faceFailureCode: FaceFailureCode, additionalMessage: String?) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
// LuminosityFailed iş kesici bir hata değildir; işlem durdurulmamalıdır.
}
override fun integrationAddCompleted() { Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}") }
override fun integrationAddFailed(errorMessage: String) { Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}") }
}

### 4. EnQualifyFace'nin Initialize Edilmesi

Face işlemlerine başlamadan önce `EnQualifyFace.initialize()` çağrılmalıdır. Initialize edilmeden başka bir işlem yapılmaya çalışılırsa SDK çalışmaz.

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
EnQualifyFace.initialize(
context = this,
fragmentManager = supportFragmentManager,
containerID = R.id.fragmentContainer,
sessionModel = sessionModel,
baseModel = baseModel,
stepCount = 3
)

#### Initialize Parametreleri

| Parametre | Tip | Açıklama |
| --- | --- | --- |
| `context` | `Context` | Uygulamanın çalışma zamanı bağlamı |
| `stepCount` | `Int` | Canlılık akışında yapılacak adım sayısı |
| `sessionModel` | `SessionModel` | Face işlemi sırasında kullanılacak oturum bilgileri |
| `baseModel` | `BaseModel` | Doğrulama sürecinde temel verileri taşıyan model |
| `fragmentManager` | `FragmentManager` | Face fragment'lerinin yönetimini sağlar |
| `containerID` | `Int` | Face fragment'inin ekleneceği container'ın ID'si |

#### Initialize Sonrası Otomatik Akış

`initialize()` çağrıldıktan sonra SDK sırasıyla Token → Session → Settings adımlarını otomatik yürütür. Hata durumlarında ilgili callback'ler tetiklenir. Tüm adımlar başarıyla tamamlandığında `initializeCompleted` tetiklenir ve Face işlemleri başlatılabilir.

---

## Face İşlemleri

### Fonksiyonlar

| Fonksiyon | Varsayılan Başarı Koşulu | Açıklama |
| --- | --- | --- |
| `faceDetect()` | X ve Y ekseninde -15° ≤ açı ≤ 15° | Kamerada yüz tespiti — diğer adımlar için zorunlu başlangıç |
| `smileDetect()` | Gülümseme değeri > 0.9 | Gülümseme tespiti |
| `eyeCloseDetect()` | Göz kapalılık değeri < 0.3 | Göz kapama tespiti |
| `faceRightDetect()` | Sağa dönüş açısı ≥ 15° | Başı sağa çevirme tespiti |
| `faceLeftDetect()` | Sola dönüş açısı ≥ 15° | Başı sola çevirme tespiti |
| `faceUpDetect()` | Yukarı kaldırma açısı ≥ 10° | Başı yukarı kaldırma tespiti |
| `faceComplete()` | — | Tüm canlılık adımlarının bittiğini SDK'ya bildirir; kamera analizi durur, veriler backoffice'e gönderilir |
| `faceCompare()` | — | Canlılık görselini OCR/NFC'den alınan biyometrik fotoğrafla karşılaştırır |
| `addFragment(fragment)` | — | Mevcut fragment üzerine yeni fragment ekler |
| `replaceFragment(fragment)` | — | Mevcut fragment'i yenisiyle değiştirir |
| `addIntegration(integrationModel)` | — | Entegrasyon verisi ekler |
| `closeSession(isFinished: Boolean)` | — | Session'ı kapatır |
| `clear()` | — | SDK'yı temizler |

---

### Tipik Canlılık Akışı

Aşağıda önerilen tipik bir canlılık akışı örneği verilmiştir. `stepCount` değerine ve iş akışınıza göre adımlar özelleştirilebilir:

wide760// 1. Yüz tespiti
enQualifyFace.faceDetect()
override fun faceDetected() {
// 2. Gülümseme
enQualifyFace.smileDetect()
}
override fun smileDetected() {
// 3. Göz kapama
enQualifyFace.eyeCloseDetect()
}
override fun eyeCloseDetected() {
// Tüm adımlar tamamlandı — akışı bitir
enQualifyFace.faceComplete()
}
override fun faceCompleted() {
// Veriler backoffice'e iletildi — karşılaştırmayı başlat
enQualifyFace.faceCompare()
}
override fun faceCompareCompleted() {
// Canlılık ve karşılaştırma başarılı — sonuç sayfasına geç
enQualifyFace.replaceFragment(FaceResultFragment())
}

---

### Yüz Karşılaştırma (faceCompare)

`faceCompare()`, canlılık adımında alınan görsel ile OCR ve NFC işlemlerinden elde edilen biyometrik fotoğrafı karşılaştırarak yüz tanıma işlemi gerçekleştirir.

wide760enQualifyFace.faceCompare()

Karşılaştırma başladığında `faceCompareStarted` tetiklenir. Bu aşamada kullanıcıya progress göstergesi sunulması önerilir:

wide760override fun faceCompareStarted() {
// Progress göster
}
override fun faceCompareCompleted() {
// Karşılaştırma başarılı; sonuç sayfasına yönlendir
}
override fun faceCompareFailed(errorMessage: String) {
// Karşılaştırma başarısız; hata yönetimi
}

---

### Entegrasyon Verisi Ekleme

wide760val integrationModel = IntegrationModel(
idRegistration = IDRegistration(),
addressRegistration = AddressRegistration(),
data = ""
)
enQualifyFace.addIntegration(integrationModel)
wide760override fun integrationAddCompleted() { Log.i(TAG, "integrationAddCompleted") }
override fun integrationAddFailed(errorMessage: String) { Log.i(TAG, "integrationAddFailed: $errorMessage") }

---

### Session Kapatma ve Temizleme

wide760enQualifyFace.closeSession(isFinished = true)
override fun sessionCloseCompleted() {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun sessionCloseFailed(errorMessage: String) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name} $errorMessage")
}
// SDK'yı temizle
enQualifyFace.clear()
> ℹ️ Session kapatıldıktan sonra SDK'yı tekrar kullanmak için `initialize()` yeniden çağrılmalıdır.

---

## Hata Kodları

### FaceFailureCode

wide760enum class FaceFailureCode(val errorMessage: String) {
SmilingError("No smile detected during the capture session."),
FaceDetectionError("No face detected during the capture session."),
FaceUpError("No Face Up during the capture session."),
FaceLeftError("No Face Left detected during the capture session."),
FaceRightError("No Face Right during the capture session."),
EyeCloseError("No Eye close during the capture session."),
EyeOpenError("No Eye Open detected during the capture session."),
FaceTimeout("FaceTimeout"),
EyeCloseIntervalError("No Eye close during the capture session."),
NoFaceFrameCountError("NoFaceFrameCountError"),
LuminosityFailed("LuminosityFailed"), // İş kesici değildir
Failed(""),
FaceSaveFailed("")
}

`faceFailed` callback'i aracılığıyla iletilir:

wide760override fun faceFailed(faceFailureCode: FaceFailureCode, additionalMessage: String?) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
> ⚠️ **Önemli:** `LuminosityFailed` bir uyarı niteliğindedir ve iş kesici değildir. Bu hata geldiğinde işlem durdurulmamalıdır.

---

## Sonuç Verisine Erişim

Face işlemi tamamlandıktan sonra elde edilen verilere `CustomerFace` nesnesi üzerinden erişilir:

wide760CustomerFace.getInstance()

`CustomerFace` modeli ve tüm alanlarının açıklaması için Core Modülü — CustomerFace sayfasına bakınız.

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

### Face — Canlılık Adımları

| Callback | Açıklama |
| --- | --- |
| `initializeCompleted(module: EnModules)` | Initialize tamamlandı, Face hazır |
| `faceDetected()` | Yüz algılandı |
| `smileDetected()` | Gülümseme algılandı |
| `eyeCloseDetected()` | Göz kapama algılandı |
| `eyeCloseIntervalDetected()` | Gözlerin belirli süre kapalı tutulduğu algılandı |
| `faceRightDetected()` | Başı sağa çevirme algılandı |
| `faceLeftDetected()` | Başı sola çevirme algılandı |
| `faceUpDetected()` | Başı yukarı kaldırma algılandı |
| `faceSaveStarted()` | Veriler backoffice'e gönderilmeye başlandı |
| `faceCompleted()` | Veriler backoffice'e başarıyla iletildi |
| `faceDetectFailed(failureCode: FaceFailureCode)` | Yüz algılama başarısız |
| `faceFailed(faceFailureCode, additionalMessage)` | Face işlem hatası |

### Face — Karşılaştırma

| Callback | Açıklama |
| --- | --- |
| `faceCompareStarted()` | Karşılaştırma başladı |
| `faceCompareCompleted()` | Karşılaştırma başarıyla tamamlandı |
| `faceCompareFailed(errorMessage: String)` | Karşılaştırma hatası |