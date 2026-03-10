# Android - Utility Modülü

Utility modülü, doğrudan OCR, NFC, Face veya VideoCall ile ilgili olmayan ancak Dijital Müşteri Edinimi (KYC/KYB) süreçlerinde kullanılabilecek yardımcı fonksiyonları barındırır.

**Modülün sunduğu özellikler:**

* Çağrı Tipi Listeleme
* Randevu Sistemi (Sorgulama / Oluşturma / İptal)
* Döküman Ekleme
* Döküman İmzalama
* Barkod Okuma
* Adres Doğrulama
* Kurumsal Müşteri Edinimi (KYB)

> ⚠️ **Ön Koşul:** Maven erişimi sağlanmış ve Core Modülü projeye eklenmiş olmalıdır.

---

## Projeye Eklenmesi

### 1. `libs.versions.toml` dosyasına ekleyin:

wide760[versions]
...
enqualify-plus = "x.x.x.x"
[libraries]
...
enqualify-plus-utility = {
group = "com.enqualify.plus",
name = "utility",
version.ref = "enqualify-plus"
}

### 2. `build.gradle.kts` dosyasına bağımlılığı ekleyin:

wide760implementation(libs.enqualify.plus.utility)

### 3. Gradle Sync

"Sync Now" seçeneğine tıklayarak Gradle dosyalarını senkronize edin.

---

## İmplementasyon

### 1. Activity Layout — FrameLayout

wide760<FrameLayout
android:id="@+id/fragmentContainer"
android:layout\_width="match\_parent"
android:layout\_height="match\_parent" />

### 2. UtilityCallbacks Interface'inin Eklenmesi

**Sınıfa eklenmesi:**

wide760class EnQualifyPlusActivity : AppCompatActivity(), UtilityCallbacks

**Callback'lerin override edilmesi:**

wide760class EnQualifyPlusActivity : AppCompatActivity(), UtilityCallbacks {
override fun tokenCreateCompleted(isNewCreatedToken: Boolean) {
Log.i(TAG, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun tokenCreateFailed(errorMessage: String) {
Log.i(TAG, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun settingGetFailed(errorMessage: String) {
Log.i(TAG, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun sessionAddFailed(errorMessage: String) {
Log.i(TAG, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun sessionCloseCompleted(status: CallSessionTypeStatus) {
Log.i(TAG, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun sessionCloseFailed(errorMessage: String) {
Log.i(TAG, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun integrationAddCompleted() {
Log.i(TAG, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun integrationAddFailed(errorMessage: String) {
Log.i(TAG, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun initializeFailed(failureCode: FailureCode, additionalMessage: String) {
Log.i(TAG, "${object {}.javaClass.enclosingMethod?.name}")
}
override fun baseModelCompleted() {
Log.i(TAG, "${object {}.javaClass.enclosingMethod?.name}")
// SDK hazır — Utility fonksiyonları kullanılabilir
}
}

### 3. EnQualifyUtility'nin Initialize Edilmesi

Utility modülü diğer modüllerden farklı olarak `SessionModel` almaz ve `settings` kullanmaz. Yalnızca `BaseModel` ile başlatılır:

wide760val baseModel = BaseModel(
baseURL = "https://deveqmapi.enqura.com",
signallingCertificateList = listOf("enqura"),
mapiCertificateList = listOf("enqura"),
mobileUser = "mobile",
countryCode = "TUR"
)
EnQualifyUtility.setBaseModel(
context = this,
fragmentManager = supportFragmentManager,
containerId = R.id.fragmentContainer,
baseModel = baseModel
)

#### Initialize Parametreleri

| Parametre | Tip | Açıklama |
| --- | --- | --- |
| `context` | `Context` | Uygulamanın çalışma zamanı bağlamı |
| `baseModel` | `BaseModel` | Sunucu bağlantı ve sertifika bilgilerini taşıyan model |
| `fragmentManager` | `FragmentManager` | Fragment yönetimini sağlar |
| `containerId` | `Int` | Fragment'in ekleneceği container'ın ID'si |

Initialize tamamlandığında `baseModelCompleted` tetiklenir ve tüm Utility fonksiyonları kullanılabilir hale gelir.

---

## Genel Yanıt Modeli — DataModel

Tüm Utility fonksiyonları sonuçlarını `DataModel<T>` üzerinden döndürür:

wide760data class DataModel<T>(
val isSuccess: Boolean,
val data: T? = null,
val errorMessage: String? = null
)

`data` alanı, fonksiyona göre `String`, `Boolean` veya özel bir sınıf olabilir.

---

## Çağrı Tipi Listeleme

Mevcut ortamdaki aktif çağrı tiplerini listeler. Dönen `code` değeri `SessionModel.callType` alanına set edilebilir.

wide760EnQualifyUtility.getInstance().CallTypeGet(
handler = "", // Bireysel KYC için boş bırakılabilir; farklı akışlar için belirtilmeli
callTypeListener = { dataModel: DataModel<ArrayList<CallType>> ->
// Çağrı tiplerine ait sonuç burada kullanılabilir
}
)

**CallType modeli:**

wide760data class CallType(
var code: String? = null, // SessionModel.callType değerine karşılık gelir
var name: String? = null // Son kullanıcıya gösterilebilecek görünen ad
)

---

## Randevu Sistemi

Parçalı başvuru (randevulu görüntülü görüşme) akışında kullanılır. Parçalı başvuru yapılacaksa `SessionModel.isContinue = true` olarak set edilmelidir.

### Uygun Randevu Slotlarını Sorgulama

wide760EnQualifyUtility.getInstance().AppointmentAvailableGet(
callType = "NewCustomer",
startDate = "2025-09-22T08:42:26.306Z",
endDate = "2025-09-22T08:42:26.306Z",
appointmentAvailableListListener = { dataModel: DataModel<ArrayList<AppointmentAvailableListResponseData>> ->
// Uygun randevu slotları burada kullanılabilir
}
)

**AppointmentAvailableListResponseData modeli:**

wide760data class AppointmentAvailableListResponseData(
var date: String? = null,
var startTime: String? = null,
var endTime: String? = null,
var count: Int? = null
)

### Randevu Oluşturma

wide760val appointmentSave = AppointmentSaveData(
callType = "NewCustomer",
date = "2025-09-22T08:42:26.306Z",
startTime = "2025-09-22T08:42:26.306Z"
)
EnQualifyUtility.getInstance().AppointmentSave(
appointmentSaveData = appointmentSave,
appointmentSaveListener = { dataModel: DataModel<Boolean> ->
// Randevu oluşturma sonucu burada kullanılabilir
}
)

**AppointmentSaveData modeli:**

wide760data class AppointmentSaveData(
var callType: String? = null,
var date: String? = null,
var startTime: String? = null,
var identityType: String? = null,
var identityNo: String? = null,
var name: String? = null,
var surname: String? = null,
var phone: String? = null,
var email: String? = null
)

### Randevu İptal Etme

wide760EnQualifyUtility.getInstance().AppointmentCancel(
callType = "NewCustomer",
identityType = "TC Kimlik Kartı",
identityNo = "12345678910",
appointmentCancelListener = { dataModel: DataModel<Boolean> ->
// Randevu iptal sonucu burada kullanılabilir
}
)

### Mevcut Randevuları Sorgulama

wide760EnQualifyUtility.getInstance().AppointmentGet(
identityType = "TC Kimlik Kartı",
identityNo = "12345678910",
appointmentListListener = { dataModel: DataModel<ArrayList<AppointmentListResponseData>> ->
// Mevcut randevular burada kullanılabilir
}
)

**AppointmentListResponseData modeli:**

wide760data class AppointmentListResponseData(
var uId: String? = null,
var callType: String? = null,
var callTypeValue: String? = null,
var identityType: String? = null,
var identityNo: String? = null,
var name: String? = null,
var surname: String? = null,
var phone: String? = null,
var email: String? = null,
var startDate: String? = null,
var endDate: String? = null,
var isPriorityCustomer: Boolean? = null
)

---

## Döküman Ekleme

### 1. Döküman Kategori Tipi Listeleme

Döküman yüklemeden önce yüklenebilecek kategorileri listeleyin:

wide760EnQualifyUtility.getInstance().DocumentCategoryGetV2(
subjectType = "Mobile", // Bireysel: "Mobile" | Kurumsal: "KYB"
callType = "NewCustomer",
documentCategoryGetV2Listener = { dataModel: DataModel<DocumentCategoryGetV2ResponseData> ->
// Döküman kategorileri burada kullanılabilir
}
)

**DocumentCategoryGetV2ResponseData modeli:**

wide760data class DocumentCategoryGetV2ResponseData(
var category: String? = null,
var name: String? = null,
var nameEn: String? = null,
var sequence: Int? = null
)

### 2. Döküman Ekleme

Kategori bilgisi alındıktan sonra döküman yüklemek için kullanılır. Her döküman için üç bilgi gereklidir:

| Alan | Açıklama |
| --- | --- |
| `extension` | Dosya uzantısı (`.pdf`, `.doc`, `.word` vb.) |
| `content` | Dosyanın Base64 formatına dönüştürülmüş içeriği |
| `contentHash` | `content` değerinin hash'i |

wide760val document = DocumentAddDocument(
extension = ".pdf",
content = "FileBase64Content",
contentHash = "FileBase64ContentHash"
)
EnQualifyUtility.getInstance().DocumentAdd(
category = "SürücüBelgesi", // DocumentCategoryGetV2 sonucundan gelen değer olmalıdır
documents = arrayListOf(document),
documentAddListener = { dataModel: DataModel<Boolean> ->
// Döküman ekleme sonucu burada kullanılabilir
}
)

---

## Döküman İmzalama

### 1. İmza Ayarlama

wide760EnQualifyUtility.getInstance().SigningSet(
data = "Base64Content", // İmzalanacak dökümanın Base64 içeriği
reference = "123456789", // SessionModel.reference değeri
documentReference = "123456789", // İmzalanacak dökümanın referans numarası
signingSetListener = { dataModel: DataModel<Boolean> ->
// İmza ayarlama sonucu burada kullanılabilir
}
)

### 2. İmza Sonlandırma

wide760EnQualifyUtility.getInstance().SigningFinish(
reference = "123456789", // SigningSet'te kullanılan reference ile aynı olmalıdır
signingFinishListener = { dataModel: DataModel<Boolean> ->
// İmzalama sonlandırma sonucu burada kullanılabilir
}
)

---

## Barkod Okuma

E-Devlet üzerinden alınan bir belgenin barkodunu okumak için kullanılır:

wide760EnQualifyUtility.getInstance().BarcodeRead(
content = "Content", // Barkod okunacak dökümanın Base64 içeriği
identityNo = "123456789", // İşlem yapan kullanıcının TC Kimlik Numarası
isWithAddress = true, // Dökümanla adres doğrulama yapılıp yapılmayacağı
barcodeReadListener = { dataModel: DataModel<VerifyBarcodeReadResponseData> ->
// Barkod okuma sonucu burada kullanılabilir
}
)

**VerifyBarcodeReadResponseData modeli:**

wide760data class VerifyBarcodeReadResponseData(
var barcode: String? = null,
var address: String? = null,
var isSameIdentity: Boolean? = null,
var expireDate: String? = null
)

---

## Adres Doğrulama

E-Devlet üzerinden ikametgah belgesiyle kullanıcının adresini doğrulamak için kullanılır:

wide760EnQualifyUtility.getInstance().AddressVerify(
identityNo = "123456789", // İşlem yapan kullanıcının TC Kimlik Numarası
barcode = "Barcode", // BarcodeRead adımından elde edilen barkod sonucu
addressVerifyListener = { dataModel: DataModel<Boolean> ->
// Adres doğrulama sonucu burada kullanılabilir
}
)

---

## Kurumsal Müşteri Edinimi (KYB)

### 1. Müşteri Ekleme

wide760EnQualifyUtility.getInstance().CallBusinessAddV2(
taxNumber = "123456",
name = "FullCompanyName",
shortName = "CompanyShortName",
data = "ExtraData",
type = "CompanyType",
reference = "123456789",
callBusinessAddV2Listener = { dataModel: DataModel<CallBusinessAddV2ResponseData> ->
// callBusinessUId burada alınmalı — sonraki tüm KYB işlemlerinde kullanılır
}
)
> ℹ️ `callBusinessAddV2Listener`'dan dönen `callBusinessUId`, sonraki tüm KYB servislerinde zorunlu parametre olarak kullanılır.

### 2. Müşteri Kontrol Etme

wide760EnQualifyUtility.getInstance().CallBusinessCheckV2(
taxNumber = "123456",
callBusinessCheckV2Listener = { dataModel: DataModel<CallBusinessCheckV2ResponseData> ->
// Müşteri kayıt durumu burada kullanılabilir
}
)

**CallBusinessCheckV2ResponseData modeli:**

wide760data class CallBusinessCheckV2ResponseData(
var checkRecord: Boolean? = null,
var callBusinessUId: String? = null,
var type: String? = null
)

### 3. Müşteri Güncelleme

wide760EnQualifyUtility.getInstance().CallBusinessUpdate(
callBusinessUId = "123456", // Müşteri Ekleme adımından gelen ID
type = "CompanyType",
reference = "123456789",
isInProgress = true, // Diğer KYB adımlarına başlanıp başlanmadığını belirtir
callBusinessUpdateListener = { dataModel: DataModel<Boolean> -> }
)

### 4. Yetkili Kişi Ekleme

wide760EnQualifyUtility.getInstance().CallBusinessStaffAdd(
callBusinessUId = "123456",
name = "StaffName",
surname = "StaffSurname",
identityNo = "123456",
birthDate = "01/01/1990",
phone = "905055055050",
callBusinessStaffAddListener = { dataModel: DataModel<Boolean> -> }
)

### 5. Yetkili Kişi Silme

wide760EnQualifyUtility.getInstance().CallBusinessStaffRemove(
callBusinessUId = "123456",
identityNo = "123456",
callBusinessStaffRemoveListener = { dataModel: DataModel<Boolean> -> }
)

### 6. Yetkili Kişi Kontrolü

wide760EnQualifyUtility.getInstance().CallBusinessStaffCheckV2(
identityNo = "123456",
callBusinessUId = "123456",
callBusinessStaffCheckV2Listener = { dataModel: DataModel<CallBusinessStaffCheckV2ResponseData> -> }
)

### 7. Kurumsal Döküman Kategorisi Listeleme

wide760EnQualifyUtility.getInstance().DocumentKYBCategoryListV2(
documentKYBCategoryListV2Listener = { dataModel: DataModel<ArrayList<DocumentKYBCategoryListV2ResponseData>> ->
// Kurumsal döküman kategorileri burada kullanılabilir
}
)

**DocumentKYBCategoryListV2ResponseData modeli:**

wide760data class DocumentKYBCategoryListV2ResponseData(
var category: String? = null,
var name: String? = null,
var nameEn: String? = null,
var sequence: Int? = null
)

### 8. Kurumsal Döküman Ekleme

wide760val document = CallBusinessDocumentAddRequestDocument(
extension = ".pdf",
content = "FileBase64Content",
contentHash = "FileBase64ContentHash"
)
EnQualifyUtility.getInstance().CallBusinessDocumentAdd(
category = "Category", // Döküman Kategorisi Listeleme adımından gelen değer olmalıdır
documents = arrayListOf(document),
documentAddListener = { dataModel: DataModel<Boolean> ->
// Döküman ekleme sonucu burada kullanılabilir
}
)

---

## Callback Referansı

| Callback | Açıklama |
| --- | --- |
| `tokenCreateCompleted(isNewCreatedToken: Boolean)` | Token oluşturulduğunda tetiklenir |
| `tokenCreateFailed(errorMessage: String)` | Token oluşturma hatası |
| `settingGetFailed(errorMessage: String)` | Ayarlar alınamadığında tetiklenir |
| `sessionAddFailed(errorMessage: String)` | Session oluşturma hatası |
| `sessionCloseCompleted(status: CallSessionTypeStatus)` | Session kapatıldığında tetiklenir |
| `sessionCloseFailed(errorMessage: String)` | Session kapatma hatası |
| `integrationAddCompleted()` | Entegrasyon verisi başarıyla eklendi |
| `integrationAddFailed(errorMessage: String)` | Entegrasyon verisi eklenemedi |
| `initializeFailed(failureCode: FailureCode, additionalMessage: String)` | Initialize hatası |
| `baseModelCompleted()` | Initialize tamamlandı, Utility fonksiyonları hazır |