# Android - VideoCall Modülü

VideoCall modülü, arka veya ön kamera kullanarak müşterinin müşteri temsilcisiyle anlık görüntülü görüşme yapmasını sağlar. Görüşme sırasında temsilci gerekli gördüğünde OCR, NFC veya Face işlemlerini **"İşlem Tekrarlatma"** olarak başlatabilir.

> ⚠️ **Ön Koşul:** VideoCall Modülünü kullanmadan önce Maven erişimi sağlanmış ve Core Modülü projeye eklenmiş olmalıdır. İşlem tekrarlatmaların çalışabilmesi için OCR, NFC ve Face modüllerinin de implemente edilmiş olması gerekir.

---

## Projeye Eklenmesi

### 1. `libs.versions.toml` dosyasına ekleyin:

wide760[versions]
...
enqualify-plus = "x.x.x.x"
[libraries]
...
enqualify-plus-videocall = {
group = "com.enqualify.plus",
name = "videocall",
version.ref = "enqualify-plus"
}

### 2. `build.gradle.kts` dosyasına bağımlılığı ekleyin:

wide760implementation(libs.enqualify.plus.videocall)

### 3. Gradle Sync

"Sync Now" seçeneğine tıklayarak Gradle dosyalarını senkronize edin.

---

## İmplementasyon

### 1. İzinler

Kamera ve mikrofon izinleri SDK tarafından manifeste otomatik olarak eklenir. Aşağıdaki satırlar yalnızca bilgi amaçlıdır:

wide760<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.RECORD\_AUDIO" />
> Kamera veya mikrofon izni verilmezse VideoCall modülü çalışmaz.

### PiP (Picture-in-Picture) Desteği

v2.1.0.0 sürümüyle gelen PiP özelliğinin çalışması için Activity'nin `AndroidManifest.xml` içine aşağıdaki tanımın eklenmesi gerekir:

wide760<activity
android:name="//Your Activity Package Name"
android:resizeableActivity="true"
android:supportsPictureInPicture="true"
android:configChanges="screenSize|smallestScreenSize|screenLayout|orientation|uiMode" />

### 2. Activity Layout — FrameLayout

VideoCall işleminin yapılacağı Activity'nin layout'una tam ekran kaplayan bir `FrameLayout` eklenmelidir:

wide760<FrameLayout
android:id="@+id/fragmentContainer"
android:layout\_width="match\_parent"
android:layout\_height="match\_parent" />

### 3. VideoCallCallbacks Interface'inin Eklenmesi

`VideoCallCallbacks` interface'i mutlaka bir **Activity** ile çalışmalıdır.

**Sınıfa eklenmesi:**

wide760class EnQualifyPlusActivity : AppCompatActivity(), VideoCallCallbacks

**Callback'lerin override edilmesi:**

wide760class EnQualifyPlusActivity : AppCompatActivity(), VideoCallCallbacks {
override fun initializeCompleted(moduleName: EnModules) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
when (moduleName) {
EnModules.VideoCall -> {
// VideoCall işlemleri başlatılabilir
}
}
}
override fun initializeFailed(failureCode: FailureCode, additionalMessage: String) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun callStarted() {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun agentRequest(agentRequestType: AgentRequestType) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
// Agent tekrarlatma isteklerini burada yönetin
}
override fun hangupConfirmation() {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun callResultCompleted(result: String, description: String, reference: String) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun callResultFailed(errorMessage: String) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun cameraFailed() {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun sessionAddFailed(errorMessage: String) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun sessionCloseCompleted(status: CallSessionTypeStatus) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun integrationAddCompleted() {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun integrationAddFailed(errorMessage: String) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
}

### 4. EnQualifyVideoCall'un Initialize Edilmesi

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
EnQualifyVideoCall.initialize(
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
| `sessionModel` | `SessionModel` | VideoCall işlemi sırasında kullanılacak oturum bilgileri |
| `baseModel` | `BaseModel` | Doğrulama sürecinde temel verileri taşıyan model |
| `fragmentManager` | `FragmentManager` | VideoCall fragment'lerinin yönetimini sağlar |
| `containerID` | `Int` | VideoCall fragment'inin ekleneceği container'ın ID'si |

Initialize tamamlandığında `initializeCompleted` tetiklenir ve görüşme başlatılabilir.

---

## VideoCall İşlemleri

### Fonksiyonlar

| Fonksiyon | Açıklama |
| --- | --- |
| `startVideoCall()` | Görüntülü görüşmeyi başlatır; Socket ve WebRTC bağlantılarını kurar |
| `faceRetry()` | Agent tarafından istenen Face işlemini tekrarlatır |
| `ocrRetry()` | Agent tarafından istenen OCR işlemini tekrarlatır |
| `backToVideoCall()` | OCR veya Face tekrarlatmasından sonra görüşmeye geri döner |
| `backToVideoCallAfterNfc()` | NFC tekrarlatmasından sonra görüşmeye geri döner |
| `endVideoCall()` | Görüntülü görüşmeyi sonlandırır |
| `setupCallLayout(...)` | Görüşme ekranındaki Rotate ve Close butonlarını yapılandırır |
| `updateSession(...)` | Engelli kullanıcı için session günceller |
| `addFragment(fragment)` | Mevcut fragment üzerine yeni fragment ekler |
| `replaceFragment(fragment)` | Mevcut fragment'i yenisiyle değiştirir |
| `addIntegration(integrationModel)` | Entegrasyon verisi ekler |
| `closeSession(isFinished: Boolean)` | Session'ı kapatır |
| `clear()` | SDK'yı temizler |

---

### Görüşme Başlatma

wide760enQualifyVideoCall.startVideoCall()

Çağrı bir agent tarafından karşılandığında `callStarted` tetiklenir:

wide760override fun callStarted() {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}

---

### Agent İsteklerini Karşılama (İşlem Tekrarlatma)

Görüşme sırasında temsilci bir işlem tekrarlatma isteği gönderdiğinde `agentRequest` callback'i tetiklenir. İlgili SDK'nın önceden initialize edilmiş olması gerekir:

wide760lateinit var enQualifyOCR: EnQualifyOCR
lateinit var enQualifyNFC: EnQualifyNFC
lateinit var enQualifyFace: EnQualifyFace
fun setupOCRSdk() { enQualifyOCR = EnQualifyOCR.getInstance() }
fun setupNFCSdk() { enQualifyNFC = EnQualifyNFC.getInstance() }
fun setupFaceSdk() { enQualifyFace = EnQualifyFace.getInstance() }
override fun agentRequest(agentRequestType: AgentRequestType) {
when (agentRequestType) {
AgentRequestType.OCR -> enQualifyVideoCall.ocrRetry()
AgentRequestType.FACE -> enQualifyVideoCall.faceRetry()
AgentRequestType.NFC -> { /\* NFC başlat, bitince backToVideoCallAfterNfc() \*/ }
}
}

**Tekrarlatma sonrası görüşmeye dönüş:**

wide760// OCR veya Face tekrarlatmasından sonra
enQualifyVideoCall.backToVideoCall()
// NFC tekrarlatmasından sonra
enQualifyVideoCall.backToVideoCallAfterNfc()

---

### Görüşmeyi Sonlandırma

wide760enQualifyVideoCall.endVideoCall()
wide760override fun callResultCompleted(result: String, description: String, reference: String) {
// Görüşme başarıyla sonlandı
}
override fun callResultFailed(errorMessage: String) {
// Sonlandırma sırasında hata oluştu
}

---

### Arayüz Özelleştirme

Görüşme ekranındaki **Rotate** ve **Close** butonları özelleştirilebilir. Bu fonksiyon kullanılmazsa her iki buton da varsayılan SDK ikonlarıyla gösterilir:

wide760enQualifyVideoCall.setupCallLayout(
showRotateButton = true,
showCancelButton = true,
rotateIconRes = R.drawable.ic\_call\_rotate,
closeIconRes = R.drawable.ic\_call\_cancel
)

---

### Engelli Kullanıcı için Session Güncelleme

İşaret dili ile görüşme imkânı sağlamak için görüşme başlamadan önce çağrılmalıdır:

wide760enQualifyVideoCall.updateSession(
handicapped = true,
visuallyHandicapped = false
)

---

### Session Kapatma ve Temizleme

wide760enQualifyVideoCall.closeSession(isFinished = true)
override fun sessionCloseCompleted(status: CallSessionTypeStatus) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun sessionCloseFailed(errorMessage: String) {
Log.i(tag, "${object {}.javaClass.enclosingMethod?.name} $errorMessage")
}
enQualifyVideoCall.clear()

---

## Proguard Kuralları

wide760-keep class org.webrtc.\*\* { \*; }

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

### VideoCall

| Callback | Açıklama |
| --- | --- |
| `initializeCompleted(module: EnModules)` | Initialize tamamlandı, VideoCall hazır |
| `callStarted()` | Görüşme agent tarafından karşılandı |
| `agentRequest(agentRequestType: AgentRequestType)` | Agent işlem tekrarlatma isteği gönderdi |
| `hangupConfirmation()` | Kullanıcı kapatma tuşuna bastı |
| `callResultCompleted(result, description, reference)` | Görüşme başarıyla sonlandı |
| `callResultFailed(errorMessage: String)` | Görüşme sonlandırma hatası |
| `cameraFailed()` | Kamera başlatma hatası |
| `videoCallFailed(videoCallFailure, additionalMessage)` | Görüşmeye bağlanma hatası |
| `socketInitializeFailed()` | Socket bağlantısı kurulamadı |
| `sessionRoomFailed(errorMessage: String)` | Room session oluşturma hatası |