# Android - Başlarken

Bu sayfa, EnQualify Android SDK'yı projenize entegre etmek için gereken tüm ön koşulları ve kurulum adımlarını kapsamaktadır.

---

Minimum Gereksinimler
---------------------

### Desteklenen Android Sürümü

| Parametre | Değer |
| --- | --- |
| `minSdkVersion` | **25** |
| Minimum Android sürümü | Android 7.1 (API 25) |

EnQualify SDK, fonksiyonel kapsamı ve bağımlılıkları doğrultusunda minimum desteklediği Android sürümünü API 25 olarak belirlemiştir. `minSdkVersion` değeri 25 ve üzeri olan projelerle uyumlu şekilde çalışmaktadır.

### Desteklenen CPU Mimarileri

EnQualify SDK aşağıdaki CPU mimarileriyle uyumludur:

* `armeabi-v7a`
* `arm64-v8a`

> ⚠️ **Önemli:** Diğer mimarilerin (örn. `x86`, `x86_64`) dahil edilmesi, uygulama boyutunun 4-5 kat artmasına neden olabilir. APK boyutunu optimize etmek için yalnızca yukarıdaki mimarileri hedeflemeniz önerilir.

`abiFilters` ile yalnızca önerilen mimarileri hedefleyebilirsiniz:

wide760android {
defaultConfig {
...
ndk {
abiFilters "armeabi-v7a", "arm64-v8a"
}
}
}

### Emülatör Kısıtlamaları

EnQualify SDK bazı modüllerde fiziksel cihaz donanımı gerektirir. Bu nedenle aşağıdaki modüller Android Emulator üzerinde çalıştırılamaz:

| Modül | Gereksinim |
| --- | --- |
| OCR, Face | Fiziksel cihaz kamerası |
| VideoCall | Kamera ve mikrofon erişimi |
| NFC | Cihazda NFC donanımı |

---

Maven Erişiminin Sağlanması
---------------------------

EnQualify SDK'ları, Enqura tarafında güvenli bir GitHub Packages reposunda barındırılmaktadır. SDK'lara erişmek için size özel üretilen kullanıcı adı ve şifrenin projenize eklenmesi gerekmektedir.

### settings.gradle Yapılandırması

`settings.gradle` dosyasına aşağıdaki repository tanımını ekleyin:

wide760dependencyResolutionManagement {
repositoriesMode.set(RepositoriesMode.PREFER\_SETTINGS)
repositories {
google()
mavenCentral()
maven { url = uri("https://jitpack.io") }
maven {
url = uri("https://maven.pkg.github.com/EnquraTechnology/Android-Packages")
credentials {
username = "YOUR\_USERNAME"
password = "YOUR\_PASSWORD"
}
}
}
}
> 🔐 **Güvenlik Notu:** `username` ve `password` değerlerini doğrudan `settings.gradle.kts` dosyasına yazmak **önerilmez**. Bu bilgilerin `local.properties` veya ortam değişkenleri (ENV) üzerinden okunması daha güvenlidir.

Repo erişim bilgilerini yetkili kişiden almanız gerekmektedir.

### Gradle Sync

Repository yapılandırmasından sonra Android Studio'da **"Sync Project with Gradle Files"** işlemini gerçekleştirin. Bu adım tamamlanmadan modüllere erişmek veya kullanmak mümkün değildir.

---

İzinler
-------

SDK, çoğu gerekli izni otomatik olarak manifest dosyasına ekler. Ancak aşağıdaki izin **uygulama tarafından manuel olarak alınmalıdır**:

wide760<uses-permission android:name="android.permission.READ\_PHONE\_STATE" />

Bu izin, SDK'nın ağ bağlantı tipiyle ilgili detaylı bilgi alabilmesi (2G/3G/4.5G) için kullanılır. İzin verilmezse mobil veri tipi yalnızca `"Mobile"` olarak görüntülenir; gerçek bağlantı türü bilgisi alınamaz.

---

Modül Kurulumu
--------------

Her modül bağımsız olarak projeye eklenir ve aynı versiyon numarasını kullanmalıdır. Versiyon numarası size özel olarak Enqura tarafından iletilir.

### Ortak Kurulum Adımları

Tüm modüller için kurulum adımları aynı kalıbı takip eder:

1. `libs.versions.toml` **dosyasını açın ve versiyonu tanımlayın:**

wide760[versions]
...
enqualify-plus = "x.x.x.x"
[libraries]
...
enqualify-plus-MODULADI = {
group = "com.enqualify.plus",
name = "MODULADI",
version.ref = "enqualify-plus"
}

2. `build.gradle.kts` **dosyasına bağımlılığı ekleyin:**

wide760implementation(libs.enqualify.plus.MODULADI)

3. **Gradle'ı senkronize edin:**

"Sync Now" seçeneğine tıklayarak Gradle dosyalarını senkronize edin.

Her modülün kurulum detayları ilgili modül sayfasında ayrıca belirtilmektedir.

---

Sıradaki Adımlar
----------------

Kurulum tamamlandıktan sonra aşağıdaki sırayla ilerleyebilirsiniz:

1. [**Core Modülü**](https://claude.ai/chat/Core_Mod%C3%BCl%C3%BC_page_linki) — Tüm modüllerin ortak temel yapısı; diğer modülleri kullanmadan önce mutlaka entegre edilmelidir.
2. [**OCR Modülü**](https://claude.ai/chat/OCR_Mod%C3%BCl%C3%BC_page_linki) — Kimlik belgelerinden optik karakter tanıma
3. [**NFC Modülü**](https://claude.ai/chat/NFC_Mod%C3%BCl%C3%BC_page_linki) — Kimlik çiplerinden NFC okuma
4. [**Face Modülü**](https://claude.ai/chat/Face_Mod%C3%BCl%C3%BC_page_linki) — Yüz tanıma ve canlılık kontrolü
5. [**VideoCall Modülü**](https://claude.ai/chat/VideoCall_Mod%C3%BCl%C3%BC_page_linki) — Görüntülü görüşme entegrasyonu