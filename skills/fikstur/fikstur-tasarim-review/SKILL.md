---
name: fikstur-tasarim-review
description: "Punta fikstürü, kaynak fikstürü, talaşlı işleme fikstürü, şablon ve aparat tasarımlarını sistematik olarak gözden geçirir (fixture design review). Kullanıcı bir fikstür konseptini, 3D model ekran görüntüsünü veya tasarım fikrini paylaşıp kontrol, görüş, eleştiri, risk analizi istediğinde; konumlama (3-2-1, locating), kenetleme (clamping), pim, burç, dayama, torç erişimi, çarpılma, talaş tahliyesi, poka-yoke, ergonomi konuları geçtiğinde kullan."
---

# Fikstür Tasarım Gözden Geçirme

Amaç: tasarımcının gözden kaçırabileceği riskleri, atölyeye çıkmadan önce yakalamak. Bulgular somut, uygulanabilir ve öncelik sıralı olmalı. Genel tavsiye listesi değil, **bu tasarıma** özel bulgular üret.

## 1. Bağlamı topla

Gözden geçirmeye başlamadan önce şunlar belli olmalı. Eksik olan ve sonucu değiştirecek bilgiyi kullanıcıya sor, tahmin etme:

| Bilgi | Neden önemli |
|---|---|
| Fikstür tipi: punta / kaynak / talaşlı işleme / şablon / kontrol aparatı | Kontrol listesinin hangi bölümleri uygulanacak |
| Parça: malzeme, kalınlık, ağırlık, boyut | Kenetleme kuvveti, taşıma, çarpılma |
| Parça resmindeki datumlar ve kritik toleranslar (GD&T) | Konumlama elemanları bu datumlara oturmalı |
| Operasyon: manuel / robotlu kaynak, tezgah tipi (yatay / dikey işleme merkezi, borwerk) | Erişim ve çarpışma kontrolü |
| Üretim adedi (yıllık / parti) | Hızlı kenet mi, cıvatalı bağlama mı; maliyet seviyesi |
| Önceki operasyon ve sonraki operasyon | Punta fikstüründen kaynak fikstürüne, kaynaktan işlemeye referans sürekliliği |

Kullanıcı ekran görüntüsü paylaştıysa önce görüntüde ne gördüğünü kısa bir paragrafla tarif et; yanlış anladıysan kullanıcı düzeltebilsin.

## 2. Kontrol listesini uygula

[KONTROL-LISTESI.md](./KONTROL-LISTESI.md) dosyasını oku. Genel bölüm her zaman, diğer bölümler fikstür tipine göre uygulanır. Maddeleri tek tek "uygun" diye işaretleyip rapora dökme: yalnızca **sorun, risk veya belirsizlik** bulunan maddeleri raporla. Göremediğin bir şeyi (ör. görüntüde görünmeyen arka taraf) "uygun" sayma, "doğrulanamadı" olarak not et.

Hesap gerektiren bir şüphe varsa (kenetleme kuvveti yeterli mi, pim boşluğu toleransı karşılıyor mu, cıvata kayma yapar mı) Skill aracını "fikstur-hesaplari" ile çağır ve sayıyla cevap ver.

## 3. Rapor formatı

```
### Özet
<2-3 cümle: tasarımın genel durumu ve en kritik 1-2 konu>

### Bulgular
| # | Bölüm | Bulgu | Risk | Öneri |
|---|-------|-------|------|-------|
| 1 | Konumlama | ... | Yüksek | ... |

### Doğrulanamayanlar
- <görüntüden / bilgiden anlaşılamayan konular ve kullanıcıdan istenen bilgi>
```

Risk seviyeleri:
- **Yüksek**: Parça hatalı (ölçü dışı) çıkar, iş güvenliği riski var veya fikstür kullanılamaz.
- **Orta**: Kalite dalgalanır, çevrim süresi uzar, operatör zorlanır.
- **Düşük**: İyileştirme fırsatı, maliyet veya bakım kolaylığı.

Bulguları risk seviyesine göre sırala. Öneriler uygulanabilir olsun: "konumlamayı iyileştir" değil, "B datum yüzeyine 2 adet sabit dayama ekle, ölçüden 5 mm içeride" gibi.

## Terimler

Türkçe terim kullan, ilk geçtiği yerde İngilizcesini parantez içinde ver: konumlama pimi (locating pin), elmas pim (diamond pin), dayama (stop / rest pad), hızlı kenet (toggle clamp), ön gerdirme (pre-set), çarpılma (distortion), sıfır noktası bağlama (zero-point clamping).
