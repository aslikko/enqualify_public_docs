# 🚀 Hızlı Başlangıç

Bu sayfa, EnQualify SDK'yı ilk kez deneyen developerlar için hazırlanmıştır. Demo ortamına bağlanacak, örnek uygulamayı çalıştıracak ve ilk akışı ayağa kaldıracaksınız.

---

## Adım 1 — Demo Uygulamayı İndir

iOS ve Android için ayrı demo uygulamalar mevcuttur. İkisini de indirebilir ya da çalıştığınız platforma göre birini seçebilirsiniz.

| Platform | İndirme |
| --- | --- |
| iOS | 🔴 Project Managerınızdan tedarik edebilirsiniz. |
| Android | 🔴 Project Managerınızdan tedarik edebilirsiniz. |

İndirdiğiniz zip'i açın. Klasör yapısı şöyle görünecektir:

**iOS:**

wide760EnQualifyDemo-iOS/
├── EnQualifyDemo.xcodeproj
├── Podfile
├── EnQualifyDemo/
│ ├── AppDelegate.swift
│ ├── ViewController.swift
│ └── ...

**Android:**

wide760EnQualifyDemo-Android/
├── app/
│ ├── src/
│ └── build.gradle
├── build.gradle
└── ...

---

## Adım 2 — Demo Ortamı Bilgileri

Aşağıdaki bilgiler EnQualify demo ortamına bağlanmak için hazır olarak sunulmaktadır. Herhangi bir kayıt veya hesap açma gerekmez.

| Alan | Değer |
| --- | --- |
| Ortam | Sandbox |
| API Key | Demo uygulamanın içinde otomatik tanımlıdır. Ama kendi uygulamanızı demo ortama baktırmak isterseniz bunun için Project Managerınızdan tedarik etmeniz gerekir. |
| Sunucu URL | <https://enqualifymapip.enqura.com> |
| SSL Sertifikası | Demo uygulamanın içinde otomatik tanımlıdır. Kendi uygulamanızı demo ortama baktırmak isterseniz, Project Managerınızdan tedarik etmeniz gerekir. |

> 💡 Demo ortamı OCR, NFC, Face ve VideoCall akışlarının tamamını destekler. Gerçek kimlik kartı ve cihaz kamerası gereklidir.

> ⚠️ Demo ortamı yalnızca test amaçlıdır. Gerçek kullanıcı verileriyle test yapılmaması önerilir.

---

## Adım 3 — SSL Sertifikasını Projeye Ekle

Demo ortamına bağlanabilmek için SSL sertifikasının projeye eklenmesi gerekir.

**iOS:**

1. İndirilen `.der` dosyasını Xcode projesine sürükleyin
2. "Copy items if needed" seçeneğini işaretleyin
3. Target'ınızın seçili olduğundan emin olun

**Android:**

1. İndirilen `.der` dosyasını `app/src/main/assets/` klasörüne kopyalayın

Sertifika kurulumu hakkında detaylı bilgi için ilgili sayfaya bakınız:

* [iOS → Başlarken → SSL Sertifikası Kurulumu](https://claude.ai/chat/480be464-6ba9-44fc-9c5c-fa20430b9003#)
* [Android → Başlarken → SSL Sertifikası Kurulumu](https://claude.ai/chat/480be464-6ba9-44fc-9c5c-fa20430b9003#)

---

## Adım 4 — Demo Bilgilerini Yapılandır

Demo uygulamasını açın ve aşağıdaki dosyada demo bilgilerini girin:

**iOS** — `ViewController.swift`:

wide760let baseModel = BaseModelOCR(
url: "DEMO\_URL",
apiKey: "DEMO\_API\_KEY",
sslCertificateName: "demo\_certificate", // .der uzantısı olmadan
sslCertificateExtension: "der"
)
let sessionModel = SessionModelOCR(
callType: "NewCustomer",
reference: "demo-test-001",
mobileUser: MobileUser(
name: "Demo",
surname: "User",
mobilePhone: "5551234567",
email: "demo@test.com"
)
)

**Android** — `MainActivity.kt`:

wide760val baseModel = BaseModelOCR(
url = "DEMO\_URL",
apiKey = "DEMO\_API\_KEY",
sslCertificateName = "demo\_certificate",
sslCertificateExtension = "der"
)
val sessionModel = SessionModelOCR(
callType = "NewCustomer",
reference = "demo-test-001",
mobileUser = MobileUser(
name = "Demo",
surname = "User",
mobilePhone = "5551234567",
email = "demo@test.com"
)
)

---

## Adım 5 — Uygulamayı Çalıştır

**iOS:**

1. Terminal'de `pod install` çalıştırın
2. `.xcworkspace` dosyasını açın (`.xcodeproj` değil)
3. Fiziksel cihaz seçin — NFC ve kamera simülatörde çalışmaz
4. `Cmd + R` ile çalıştırın

**Android:**

1. Android Studio'da projeyi açın
2. `Sync Project with Gradle Files` yapın
3. Fiziksel cihaz seçin
4. Run butonuna basın

---

## Adım 6 — İlk Akışı Dene

Uygulama açıldığında aşağıdaki akışları deneyebilirsiniz:

| Akış | Ne Test Eder? | Gereksinim |
| --- | --- | --- |
| **OCR** | Kimlik kartı tarama, hologram kontrolü | Kimlik kartı + kamera |
| **NFC** | Çip okuma | NFC destekli cihaz + kimlik kartı |
| **Face** | Canlılık kontrolü, yüz karşılaştırma | Ön kamera |
| **VideoCall** | Temsilciyle görüşme | Kamera + mikrofon + internet |

> 💡 İlk denemede **OCR → NFC → Face** sırasını izlemenizi öneririz. Bu akış gerçek entegrasyonun en yaygın kullanım senaryosunu yansıtır.

---

## Sonraki Adımlar

Demo çalıştı, sıra entegrasyona geldi:

* **iOS entegrasyonuna başla** → [iOS SDK: İmplementasyon Rehberi](https://claude.ai/chat/480be464-6ba9-44fc-9c5c-fa20430b9003#)
* **Android entegrasyonuna başla** → [Android SDK: İmplementasyon Rehberi](https://claude.ai/chat/480be464-6ba9-44fc-9c5c-fa20430b9003#)
* **Ortam farkları hakkında bilgi al** → [Teknik Mimari & Servis Altyapısı](https://claude.ai/chat/480be464-6ba9-44fc-9c5c-fa20430b9003#)

---

## Takıldın mı?

Sık karşılaşılan ilk kurulum sorunları:

| Sorun | Çözüm |
| --- | --- |
| iOS'ta `pod install` başarısız | SSH key ayarlanmamış olabilir → [Başlarken → SSH Key Kurulumu](https://claude.ai/chat/480be464-6ba9-44fc-9c5c-fa20430b9003#) |
| SSL hatası | Sertifika adı veya uzantısı hatalı girilmiş olabilir |
| NFC çalışmıyor | Cihazda NFC kapalı olabilir veya kart desteklenmiyor olabilir |
| VideoCall bağlanamıyor | Demo ortamında aktif temsilci olmayabilir, tekrar deneyin |

Sorun devam ediyorsa → 🔴 Project Managerınız ile iletişime geçebilirsiniz.