# iOS - Utility Modülü

Utility Modülü, kimlik doğrulama akışlarını destekleyen yardımcı servisleri sunar. Randevu yönetimi, doküman imzalama, adres doğrulama ve kurumsal müşteri doğrulama (KYB) işlemleri bu modül üzerinden gerçekleştirilir.

Utility Modülü'nü kullanmadan önce **Core Modülü** projeye eklenmiş ve yapılandırılmış olmalıdır. Detaylar için Core Modülü sayfasına bakınız.

Utility Modülü diğer modüllerden farklı olarak delegate yerine `@escaping closure` pattern'i kullanır. `initialize()` ve delegate implementasyonu gerekmez.

---

## Kurulum

`Podfile`'a aşağıdaki bağımlılığı ekleyin:

wide760pod 'OpenSSL-Universal', '3.3.2000'

XCFramework olarak eklenecekse: `UtilityModule.xcframework` ve `CoreModule.xcframework` dosyalarını **Embed and Sign** olarak projeye dahil edin.

`post_install` build ayarları ve kurulum yöntemleri tüm modüller için ortaktır. Detaylar için Başlarken → SDK Kurulumu sayfasına bakınız.

---

## Genel Kullanım Yapısı

Utility Modülü'ndeki tüm servisler aynı çağrı yapısını izler:

wide760EnQualifyUtility.servisAdi(
baseModel: baseModel, // BaseModelUtility
sessionModel: sessionModel, // SessionModelUtility — bazı servislerde gerekmez
// ... servis parametreleri
) { result in
switch result {
case .success(let response):
// İşlem başarılı
case .failure(let error):
// Hata
}
}

`BaseModelUtility` ve `SessionModelUtility` tanımları için Core Modülü → BaseModel ve Core Modülü → SessionModel sayfalarına bakınız.

---

## Servisler

---

### Çağrı Tiplerinin Alınması

Backoffice'te tanımlı çağrı tiplerini getirir. `SessionModel`'deki `callType` alanında kullanılacak değerler buradan alınmalıdır.

wide760EnQualifyUtility.getCallTypes(
baseModel: baseModel
) { result in
switch result {
case .success(let callTypes):
// callTypes: [CallType]
// callTypes[0].name → çağrı tipi adı (örn. "NewCustomer")
case .failure(let error):
print(error.localizedDescription)
}
}

Bu servis `sessionModel` gerektirmez; yalnızca `baseModel` ile çağrılır.

---

### Randevu Servisleri

#### Randevu Slot'larının Alınması

Belirli bir tarih aralığı için uygun randevu saatlerini getirir.

wide760EnQualifyUtility.getAppointmentSlots(
baseModel: baseModel,
sessionModel: sessionModel,
startDate: "2026-01-01", // YYYY-MM-DD
endDate: "2026-01-07"
) { result in
switch result {
case .success(let slots):
// slots: [AppointmentSlot]
// slots[0].date, slots[0].time
case .failure(let error):
print(error.localizedDescription)
}
}

#### Randevu Oluşturma

wide760EnQualifyUtility.createAppointment(
baseModel: baseModel,
sessionModel: sessionModel,
slotId: "SLOT\_ID", // getAppointmentSlots'tan alınan slot ID'si
note: "Opsiyonel not"
) { result in
switch result {
case .success(let appointment):
// appointment.id → oluşturulan randevu ID'si
// appointment.date, appointment.time
case .failure(let error):
print(error.localizedDescription)
}
}

#### Randevu Güncelleme

wide760EnQualifyUtility.updateAppointment(
baseModel: baseModel,
sessionModel: sessionModel,
appointmentId: "APPOINTMENT\_ID",
slotId: "NEW\_SLOT\_ID",
note: "Güncellenmiş not"
) { result in
switch result {
case .success:
// Güncelleme başarılı
case .failure(let error):
print(error.localizedDescription)
}
}

#### Randevu İptali

wide760EnQualifyUtility.cancelAppointment(
baseModel: baseModel,
sessionModel: sessionModel,
appointmentId: "APPOINTMENT\_ID"
) { result in
switch result {
case .success:
// İptal başarılı
case .failure(let error):
print(error.localizedDescription)
}
}

#### Mevcut Randevunun Alınması

Kullanıcının aktif randevusunu getirir.

wide760EnQualifyUtility.getAppointment(
baseModel: baseModel,
sessionModel: sessionModel
) { result in
switch result {
case .success(let appointment):
// appointment nil ise aktif randevu yok
case .failure(let error):
print(error.localizedDescription)
}
}

---

### Doküman İmzalama

Kullanıcıya imzalatılacak dokümanları listeler ve imza akışını başlatır.

#### İmzalanacak Dokümanların Alınması

wide760EnQualifyUtility.getDocumentsToSign(
baseModel: baseModel,
sessionModel: sessionModel
) { result in
switch result {
case .success(let documents):
// documents: [SignDocument]
// documents[0].id, documents[0].name, documents[0].url
case .failure(let error):
print(error.localizedDescription)
}
}

#### Doküman İmzalama

wide760EnQualifyUtility.signDocument(
baseModel: baseModel,
sessionModel: sessionModel,
documentId: "DOCUMENT\_ID",
in: self // İmza ekranının sunulacağı UIViewController
) { result in
switch result {
case .success:
// İmzalama tamamlandı
case .failure(let error):
print(error.localizedDescription)
}
}

İmza akışı SDK tarafından yönetilen bir ekran üzerinden gerçekleşir. `in` parametresine geçilen view controller üzerine imza ekranı modal olarak sunulur.

---

### Adres Doğrulama

Kullanıcının adres bilgisini doğrular. Adres verisi OCR'dan veya manuel giriş yoluyla sağlanabilir.

wide760EnQualifyUtility.verifyAddress(
baseModel: baseModel,
sessionModel: sessionModel,
address: AddressModel(
street: "Atatürk Caddesi",
buildingNo: "42",
apartmentNo: "5",
district: "Çankaya",
city: "Ankara",
postalCode: "06550",
country: "TUR"
)
) { result in
switch result {
case .success(let verificationResult):
// verificationResult.isVerified → Bool
// verificationResult.matchScore → güven skoru
case .failure(let error):
print(error.localizedDescription)
}
}

`AddressModel` **alanları:**

| Alan | Tip | Zorunlu | Açıklama |
| --- | --- | --- | --- |
| `street` | `String` | ✅ | Sokak / cadde adı |
| `buildingNo` | `String` | ✅ | Bina numarası |
| `apartmentNo` | `String?` | — | Daire numarası |
| `district` | `String` | ✅ | İlçe |
| `city` | `String` | ✅ | Şehir |
| `postalCode` | `String?` | — | Posta kodu |
| `country` | `String` | ✅ | Ülke kodu (örn. `"TUR"`) |

---

### KYB — Kurumsal Kimlik Doğrulama

Kurumsal müşteri doğrulama akışları için kullanılır. Şirket bilgisi sorgulanır ve yetkili kişi doğrulaması yapılır.

#### Şirket Sorgulama

wide760EnQualifyUtility.queryBusiness(
baseModel: baseModel,
sessionModel: sessionModel,
taxNumber: "1234567890"
) { result in
switch result {
case .success(let business):
// business.name → şirket adı
// business.taxNumber
// business.authorizedPersons → [AuthorizedPerson]
case .failure(let error):
print(error.localizedDescription)
}
}

#### Yetkili Kişi Doğrulaması Başlatma

wide760EnQualifyUtility.startBusinessVerification(
baseModel: baseModel,
sessionModel: sessionModel,
businessId: "BUSINESS\_ID", // queryBusiness'tan alınan ID
authorizedPersonId: "PERSON\_ID" // Doğrulanacak yetkili kişi ID'si
) { result in
switch result {
case .success(let verificationSession):
// verificationSession.sessionId → doğrulama oturumu başlatıldı
// Bu session ile OCR / Face / VideoCall akışları başlatılabilir
case .failure(let error):
print(error.localizedDescription)
}
}

KYB doğrulama oturumu başlatıldıktan sonra standart OCR, NFC ve Face akışları bu oturum üzerinden yürütülür. `SessionModel`'deki `businessReference` alanına `verificationSession.sessionId` değerini geçin.

---

### Diğer Yardımcı Servisler

#### OTP Doğrulama

SMS ile gönderilen OTP kodunu doğrular.

wide760EnQualifyUtility.verifyOTP(
baseModel: baseModel,
sessionModel: sessionModel,
otpCode: "123456"
) { result in
switch result {
case .success:
// OTP doğrulandı
case .failure(let error):
print(error.localizedDescription)
}
}

#### OTP Yeniden Gönderme

wide760EnQualifyUtility.resendOTP(
baseModel: baseModel,
sessionModel: sessionModel
) { result in
switch result {
case .success:
// OTP yeniden gönderildi
case .failure(let error):
print(error.localizedDescription)
}
}

#### Oturum Durumu Sorgulama

Mevcut oturumun backoffice tarafındaki durumunu sorgular.

wide760EnQualifyUtility.getSessionStatus(
baseModel: baseModel,
sessionModel: sessionModel
) { result in
switch result {
case .success(let status):
// status.state → oturum durumu (örn. "Pending", "Completed")
// status.message → açıklama
case .failure(let error):
print(error.localizedDescription)
}
}

---

## Hata Yönetimi

Tüm Utility servisleri aynı hata yapısını kullanır:

wide760case .failure(let error):
switch error {
case .networkError(let message):
// Ağ bağlantısı hatası
case .serverError(let code, let message):
// Sunucu taraflı hata — code: HTTP status kodu
case .validationError(let message):
// Parametre doğrulama hatası — eksik veya hatalı alan
case .unauthorized:
// Token geçersiz veya süresi dolmuş
}

| Hata | Açıklama |
| --- | --- |
| `.networkError(String)` | Sunucuya ulaşılamadı |
| `.serverError(Int, String)` | Sunucu hata döndürdü |
| `.validationError(String)` | Zorunlu parametre eksik veya hatalı |
| `.unauthorized` | Yetkilendirme hatası — token yenilenmesi gerekebilir |

---

Sonraki adım: UI Özelleştirme