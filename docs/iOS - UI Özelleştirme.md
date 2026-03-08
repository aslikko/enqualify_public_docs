# iOS - UI Özelleştirme

EnQualify SDK arayüzü Backoffice üzerinden dinamik olarak özelleştirilebilir. Renk, font, ikon ve metin gibi görsel parametreler kod değişikliği gerektirmeden Backoffice panelinden yönetilir; SDK her başlatıldığında güncel ayarları otomatik olarak çeker.

UI özelleştirme parametreleri `settingGetCompleted` adımında SDK tarafından otomatik alınır. Herhangi bir kod entegrasyonu gerekmez.

---

Özelleştirilebilir Alanlar
--------------------------

### Renkler

| Parametre | Açıklama | Örnek |
| --- | --- | --- |
| `primaryColor` | Ana renk — butonlar, vurgular, progress bar | `#1A56DB` |
| `secondaryColor` | İkincil renk — başlıklar, ikonlar | `#0E3F9E` |
| `backgroundColor` | Ekran arka plan rengi | `#FFFFFF` |
| `textColor` | Genel metin rengi | `#111928` |
| `errorColor` | Hata durumu rengi | `#E02424` |
| `successColor` | Başarı durumu rengi | `#057A55` |
| `overlayColor` | Kamera overlay rengi ve opaklığı | `#000000` + `%60` |

### Tipografi

| Parametre | Açıklama |
| --- | --- |
| `fontFamily` | Tüm SDK ekranlarında kullanılacak font ailesi |
| `titleFontSize` | Başlık font boyutu |
| `bodyFontSize` | Gövde metin font boyutu |
| `buttonFontSize` | Buton metin font boyutu |

Özel font kullanılacaksa ilgili font dosyalarının uygulamaya eklenmiş ve `Info.plist`'te tanımlanmış olması gerekir. Aksi halde SDK sistem fontuna geri döner.

### Butonlar ve Şekiller

| Parametre | Açıklama |
| --- | --- |
| `buttonCornerRadius` | Buton köşe yuvarlaklığı (pt) |
| `buttonBorderWidth` | Buton kenarlık kalınlığı (pt) |
| `buttonBorderColor` | Buton kenarlık rengi |
| `cardCornerRadius` | Kart bileşenlerinin köşe yuvarlaklığı |

### İkonlar ve Görseller

| Parametre | Açıklama |
| --- | --- |
| `logoUrl` | Uygulama logosu URL'si — bekleme ve tamamlanma ekranlarında gösterilir |
| `successIconUrl` | Başarı ekranı ikonu |
| `errorIconUrl` | Hata ekranı ikonu |
| `loadingAnimationUrl` | Yükleme animasyonu (Lottie JSON formatında) |

### Metinler ve Çeviri

Tüm SDK ekranlarındaki metinler Backoffice üzerinden özelleştirilebilir. Bu sayede farklı dil desteği kod değişikliği gerektirmeden sağlanabilir.

| Parametre | Açıklama |
| --- | --- |
| `strings` | Ekran bazlı metin tanımları — key-value formatında |
| `locale` | Varsayılan dil kodu (örn. `"TR"`, `"EN"`) |

`locale` değeri `BaseModel`'deki `locale` parametresiyle de ayarlanabilir. Her ikisi tanımlanmışsa `BaseModel`'deki değer önceliklidir.

---

Ekran Bazlı Özelleştirme
------------------------

Her SDK ekranı Backoffice'te bağımsız olarak yapılandırılabilir. Özelleştirilebilir başlıca ekranlar:

| Ekran | Özelleştirilebilir Öğeler |
| --- | --- |
| Karşılama ekranı | Logo, başlık, açıklama metni, buton rengi |
| Kimlik tarama ekranı | Overlay rengi, yönlendirme metinleri, çerçeve rengi |
| Hologram kontrol ekranı | Yönlendirme metinleri, animasyon |
| Canlılık ekranı | Çerçeve rengi, hareket yönlendirme metinleri |
| NFC okuma ekranı | Yönlendirme metinleri, ikon |
| Bekleme ekranı (VideoCall) | Logo, bekleme metni, animasyon |
| Görüşme ekranı | Buton ikonları, PiP boyutu |
| Tamamlanma ekranı | Başarı/hata ikonu, mesaj metni, buton etiketi |

---

Sesli Yönlendirme Özelleştirme
------------------------------

SDK ekranlarındaki sesli yönlendirmeler Backoffice üzerinden değiştirilebilir. Özel ses dosyası kullanmak istiyorsanız iki yöntem mevcuttur:

**Backoffice üzerinden:** Ses dosyaları Backoffice panelinden yüklenir, SDK her başlatmada güncel dosyaları indirir.

**Uygulama bundle'ı üzerinden:** Ses dosyalarını uygulama içine gömmek istiyorsanız, SDK'nın tanıdığı dosya adlarını kullanarak bundle'a eklemeniz yeterlidir. Detaylar için Core Modülü → Ses Dosyaları Yönetimi sayfasına bakınız.

---

Özelleştirme Öncelik Sırası
---------------------------

Aynı parametre birden fazla yerde tanımlanmışsa SDK şu öncelik sırasını izler:

wide7601. BaseModel parametreleri (en yüksek öncelik)
2. Backoffice ayarları
3. SDK varsayılan değerleri (en düşük öncelik)

---