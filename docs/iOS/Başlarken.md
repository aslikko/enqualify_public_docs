# iOS - Başlarken

Bu sayfa, EnQualify iOS SDK'yı projenize eklemek için gereken tüm adımları kapsar. Modül kurulumuna geçmeden önce bu sayfadaki adımları tamamlamanız gerekir.

---

## **1. Kurulum Yöntemi Seçin**

EnQualify iOS SDK üç farklı yöntemle projeye eklenebilir.

| **Yöntem** | **Ne Zaman Tercih Edilir?** |
| --- | --- |
| CocoaPods | Standart ve önerilen yöntem |
| Swift Package Manager (SPM) | Xcode-native paket yönetimi tercih ediliyorsa |
| Manuel XCFramework | CI/CD pipeline'ı veya özel derleme süreci varsa |

---

## **2. Private Repo Erişimi**

Her üç yöntem de EnQualify'ın private GitHub reposuna erişim gerektirir. Bunun için bir SSH key oluşturmanız ve bu key'i Enqura ekibine iletmeniz gerekmektedir.

**İlk kez kurulum yapıyorsanız:** Aşağıdaki SSH kurulum adımını tamamlamadan CocoaPods veya SPM kurulumuna geçmeyin. Key iletilmeden repo erişimi sağlanamaz.

### SSH Key Oluşturma (CocoaPods için)

wide760# RSA key oluştur
ssh-keygen -t rsa -b 4096 -C "your\_email@example.com"
# GitHub'ı known hosts listesine ekle
ssh-keyscan github.com >> ~/.ssh/known\_hosts
# Public key'i görüntüle ve Enqura ekibine ilet
cat ~/.ssh/id\_rsa.pub

Key iletildikten sonra private repo'yu yerel listenize ekleyin:

wide760pod repo add enquratechnology-enqualifyiospackages \
ssh://git@github.com/EnquraTechnology/EnQualifyiOSPackages.git

### SSH Key Oluşturma (SPM için)

SPM ve Xcode'un private repo'ya erişebilmesi için `ed25519` formatında ayrı bir key oluşturulması önerilir.

wide760# SSH agent'ı başlat
eval "$(ssh-agent -s)"
# Key oluştur
ssh-keygen -t ed25519 -a 100 -f ~/.ssh/id\_github -C "your\_email@example.com"
# Key'i macOS Keychain ve SSH agent'e ekle (Xcode tekrar şifre sormaz)
ssh-add --apple-use-keychain ~/.ssh/id\_github
# Public key'i görüntüle ve Enqura ekibine ilet
cat ~/.ssh/id\_github.pub

`~/.ssh/config` dosyasına aşağıdaki yapılandırmayı ekleyin:

wide760Host github.com
HostName github.com
User git
IdentityFile ~/.ssh/id\_github
UseKeychain yes
AddKeysToAgent yes
IdentitiesOnly yes

GitHub'ı known hosts listesine ekleyin ve bağlantıyı test edin:

wide760ssh-keyscan -H github.com >> ~/.ssh/known\_hosts
ssh -T git@github.com

---

## **3. SDK Kurulumu**

### CocoaPods

`Podfile`'ınıza aşağıdaki source tanımlarını ve modülleri ekleyin. Kullanmayacağınız modülleri eklemenize gerek yoktur.

`ruby`

wide760source 'ssh://git@github.com/EnquraTechnology/EnQualifyiOSPackages.git'
source 'https://github.com/CocoaPods/Specs.git'
platform :ios, '14.0'
use\_frameworks!
target 'YourApp' do
pod 'EnQualify/OCR', '2.1.0.0'
pod 'EnQualify/NFC', '2.1.0.0'
pod 'EnQualify/Face', '2.1.0.0'
pod 'EnQualify/VideoCall', '2.1.0.0'
pod 'EnQualify/Utility', '2.1.0.0'
end

`-s` **eki hakkında:** `pod 'EnQualify/OCR', '2.1.0.0-s'` şeklindeki `-s` sürümleri static linkage içindir. Native iOS projelerinde genellikle gerekmez; aksi belirtilmedikçe `-s` sürümlerini kullanmayın.

`post_install` bloğunu Podfile'a ekleyin. Bu blok tüm modüller için geçerlidir, bir kez tanımlamak yeterlidir:

ruby

wide760post\_install do |installer|
installer.pods\_project.targets.each do |target|
target.build\_configurations.each do |config|
config.build\_settings['BUILD\_LIBRARY\_FOR\_DISTRIBUTION'] = 'YES'
config.build\_settings['EXPANDED\_CODE\_SIGN\_IDENTITY'] = ""
config.build\_settings['CODE\_SIGNING\_REQUIRED'] = "NO"
config.build\_settings['CODE\_SIGNING\_ALLOWED'] = "NO"
config.build\_settings["EXCLUDED\_ARCHS[sdk=iphonesimulator\*]"] = ""
config.build\_settings['VALID\_ARCHS'] = "arm64 x86\_64"
config.build\_settings['IPHONEOS\_DEPLOYMENT\_TARGET'] = '14.0'
config.build\_settings["ONLY\_ACTIVE\_ARCH"] = "YES"
end
end
end

### Swift Package Manager (SPM)

SSH yapılandırması tamamlandıktan sonra Xcode üzerinden şu repo URL'sini ekleyin:

wide760ssh://git@github.com/EnquraTechnology/EnQualifyiOSPackages.git

**Xcode → File → Add Package Dependencies** yolunu izleyin, URL'yi girin ve kullanmak istediğiniz modülleri seçin.

### Manuel XCFramework

1. Enqura ekibinden temin ettiğiniz `.xcframework` dosyalarını proje dizininize kopyalayın.
2. **Xcode → Project Settings → General → Frameworks, Libraries, and Embedded Content** bölümüne gidin.
3. Her `.xcframework` dosyasını **Embed and Sign** olarak ekleyin.
4. Bağımlılıkları `post_install` bloğu dahil CocoaPods üzerinden kurun (framework dosyalarının `podspec`'inde belirtilen sürümleri kullanın).

---

## **4. Simülatör Desteği**

EnQualify SDK kamera ve NFC donanımı gerektirdiğinden simülatörde çalışmaz; ancak başarıyla **derlenebilir**. Simülatörde derleme hatası alıyorsanız aşağıdaki adımı uygulayın.

**Xcode → Project Target → Build Settings → OTHER\_LDFLAGS** bölümüne gidin. **Any iOS Simulator SDK** seçeneği altında `$(inherited)` bayrağını kaldırın ve şu kütüphanelere ait bayrakları silin:

wide760MLKitCommon · MLKitVision · MLKitFaceDetection · MLImage
TensorFlowLiteC · WebRTC

Manuel düzenleme tercih ederseniz `.xcodeproj` paketini açıp `.pbxproj` dosyasında `OTHER_LDFLAGS[sdk=iphonesimulator*]` anahtarını bulun ve ilgili değerleri temizleyin.

---

## **5. Proje Konfigürasyonu**

### Info.plist İzinleri

SDK'nın kamera, mikrofon ve NFC özelliklerine erişebilmesi için `Info.plist` dosyasına aşağıdaki anahtarları ekleyin. Kullanmadığınız modüllere ait izinleri eklemenize gerek yoktur.

`xml`

wide760<!-- OCR ve Face modülleri için -->
<key>NSCameraUsageDescription</key>
<string>Kimlik doğrulama için kameranıza erişim gerekmektedir.</string>
<!-- VideoCall modülü için -->
<key>NSMicrophoneUsageDescription</key>
<string>Görüntülü görüşme sırasında mikrofonunuza erişim gerekmektedir.</string>
<!-- NFC modülü için -->
<key>NFCReaderUsageDescription</key>
<string>Kimlik kartınızdaki çipi okumak için NFC erişimi gerekmektedir.</string>
<!-- NFC modülü için — ISO 7816 standardı -->
<key>com.apple.developer.nfc.readersession.iso7816.select-identifiers</key>
<array>
<string>A0000002471001</string>
</array>

### NFC Capability ve Entitlements

NFC okuma özelliği için projenize **Near Field Communication Tag Reading** capability'sini ekleyin:

**Xcode → Target → Signing & Capabilities → + Capability → Near Field Communication Tag Reading**

Bu işlem otomatik olarak `.entitlements` dosyası oluşturur ve içine aşağıdaki girdiyi ekler. Dosya oluşturulmazsa manuel olarak oluşturun:

xml

wide760<key>com.apple.developer.nfc.readersession.formats</key>
<array>
<string>Tag</string>
<string>ISO7816</string>
<string>FeliCa</string>
</array>

**Entitlements dosyası eksik veya hatalıysa** NFC işlevi beklendiği gibi çalışmaz, uygulamanız NFC erişimini talep edemez.

### Picture in Picture (PiP) — VideoCall için

VideoCall modülünde PiP desteği kullanılacaksa şu adımları izleyin:

**Xcode → Target → Signing & Capabilities → + Capability** yolundan şunları ekleyin:

1. **Multitasking Camera Access**
2. **Background Modes** → **Audio, AirPlay and Picture in Picture** seçeneğini işaretleyin

Bu ayar yapılmadan PiP moduna geçildiğinde görüntü yerine gri ekran görünür.

---

## **6. SSL Sertifikası Kurulumu**

EnQualify SDK, backend ile iletişimde SSL pinning kullanır. Sertifikanın projeye eklenmesi zorunludur.

### Sertifikayı İndirme ve Dönüştürme

1. Enqura tarafından sağlanan doğrulama platformu URL'sini **Firefox** ile açın.
2. Adres çubuğundaki kilit simgesine tıklayın → **Daha Fazla Bilgi → Sertifikayı Görüntüle**.
3. Açılan sayfadan **PEM (chain)** dosyasını indirin.
4. İndirilen dosyanın bulunduğu klasörde terminali açın ve `.pem` dosyasını `.der` formatına dönüştürün:

`bash`

wide760openssl x509 -outform der -in \_.enqualify.io.pem -out enqura.der
> Alternatif olarak Enqura'nın sağladığı **DerGeneratorApp** macOS uygulamasını kullanabilirsiniz. Uygulama hem URL üzerinden otomatik indirme hem de mevcut `.pem` dosyasını dönüştürme seçeneklerini sunar.

### Sertifikayı Projeye Ekleme

1. Oluşturulan `.der` dosyasını Xcode'da proje gezginine sürükleyin.
2. Açılan iletişim kutusunda hedef target'ın seçili olduğundan emin olun.
3. **Build Phases → Copy Bundle Resources** altında sertifikanın göründüğünü doğrulayın.

Sertifika adının `BaseModel` içinde verdiğiniz adla eşleşmesi gerekir; aksi halde runtime'da hata alırsınız. Detaylar için Core Modülü → BaseModel bölümüne bakınız.

> **Birden fazla sertifika** gerekiyorsa `setBaseModel()` içindeki `signallingCertificateList` ve `mapiCertificateList` alanlarına birden fazla değer geçebilirsiniz. `.der` dosyası yerine Base64 string olarak da sertifika tanımlanabilir.

---

Kurulum ve konfigürasyon tamamlandıktan sonra Core Modülü sayfasına geçerek `BaseModel` ve `SessionModel` tanımlarını yapabilirsiniz.