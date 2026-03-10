# Android - UI Özelleştirme

EnQualify SDK arayüz bileşenleri, **Backoffice üzerinden tanımlanan parametrelerle** dinamik olarak özelleştirilebilir. Herhangi bir kod değişikliği gerekmez; ayarlar uygulama açılışında veya ilgili akış başlatıldığında API üzerinden otomatik olarak alınır.

---

## Çalışma Mantığı

Backoffice'te tanımlanan UI parametreleri, SDK tarafından `VerifyMobileFlexibleLayoutModel` yapısına parse edilerek arayüz bileşenlerine uygulanır.

wide760Backoffice Parametreleri
↓
API (initialize sırasında otomatik çekilir)
↓
VerifyMobileFlexibleLayoutModel
↓
SDK arayüz bileşenleri dinamik olarak güncellenir
> ℹ️ Geliştirici tarafında ek bir implementasyon gerekmez. Tüm özelleştirmeler Backoffice üzerinden yönetilir.

---

## Özelleştirilebilir Kategoriler

### Font & Renk

| Parametre | Açıklama |
| --- | --- |
| `font` | Uygulama genelinde kullanılacak yazı tipi ve boyutu |
| `fontColor` | Uygulama genelinde metin rengi |

---

### OCR Görselleri

Kimlik doğrulama (OCR) ekranlarında kullanılan çerçeve ve durum görsellerini özelleştirir.

| Parametre | Açıklama |
| --- | --- |
| `ocrFrameDefaultImage` | OCR ekranında varsayılan çerçeve görseli |
| `ocrFrameSuccessImage` | Okuma başarılı olduğunda gösterilen çerçeve görseli |
| `ocrFrameFailImage` | Okuma başarısız olduğunda gösterilen çerçeve görseli |
| `ocrFrameRotateImage` | Kimliği çevirme yönlendirmesinde kullanılan görsel |
| `ocrFrameBackValidImage` | Arka yüz okuma başarılı görseli |
| `ocrFrameBackInvalidImage` | Arka yüz okuma geçersiz görseli |
| `ocrFrameFrontValidImage` | Ön yüz okuma başarılı görseli |
| `ocrFrameFrontInvalidImage` | Ön yüz okuma geçersiz görseli |

---

### Yüz Tanıma Görselleri

Canlılık kontrolü adımlarında kullanılan yönlendirme ve durum görsellerini özelleştirir.

| Parametre | Açıklama |
| --- | --- |
| `faceLeftImage` | Başı sola çevirme yönlendirme görseli |
| `faceRightImage` | Başı sağa çevirme yönlendirme görseli |
| `faceUpImage` | Başı yukarı kaldırma yönlendirme görseli |
| `faceCompletedImage` | Canlılık adımı tamamlandığında gösterilen görsel |
| `faceFailImage` | Canlılık adımı başarısız olduğunda gösterilen görsel |

---

### Yüz Tanıma İlerleme Katmanı

Canlılık işlemi sırasında dairesel ilerleme (progress) halkasının görünümünü özelleştirir.

| Parametre | Açıklama |
| --- | --- |
| `faceProgressLayerColor` | İlerleme halkasının dolgu rengi |
| `faceProgressLayerStroke` | İlerleme halkasının çizgi kalınlığı |

---

## Backoffice'te Yapılandırma

Yukarıdaki tüm parametreler Backoffice yönetim paneli üzerinden tanımlanır. Yapılandırma adımları için Backoffice yöneticinize veya EnQualify destek ekibine başvurunuz.

Parametreler tanımlandıktan sonra bir sonraki SDK initialize işleminde otomatik olarak uygulanır — uygulamada herhangi bir değişiklik yapılması gerekmez.