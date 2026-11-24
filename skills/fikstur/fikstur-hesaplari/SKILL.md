---
name: fikstur-hesaplari
description: "Fikstür, kenet ve aparat hesaplarında her zaman kullan: kenetleme kuvveti, kesme kuvveti, kenet sayısı, pim-delik boşluğu, elmas pim, konumlama hatası, cıvata torku, pim kesme."
---

# Fikstür Hesapları

Hesapları elle değil, [scripts/fikstur_hesap.py](./scripts/fikstur_hesap.py) ile yap. Böylece sonuç tekrarlanabilir olur ve kullanıcı aynı komutu değiştirip yeniden çalıştırabilir. Script yalnızca Python standart kütüphanesini kullanır.

```bash
python3 <skill-klasörü>/scripts/fikstur_hesap.py <komut> --help
```

`<skill-klasörü>`: bu SKILL.md dosyasını okuduğun klasör. Komutları her zaman bu tam yolla çalıştır.

## Komutlar

| Komut | Ne hesaplar | Asgari girdiler |
|---|---|---|
| `kenet` | Kesme kuvveti ve gereken toplam / kenet başına kuvvet | `--fc` veya `--malzeme --b --h` (frezede `--ze`); `--durum`; `--n` |
| `pim` | Çapsal boşluklar, iki silindirik pim yeterliliği, elmas pim max genişliği, öteleme ve dönme hatası | `--D1 --d1 --D2 --d2` (min max), `--L`, `--tp` |
| `civata` | Önerilen tork veya verilen torktan ön yük, kaymaya karşı kapasite | `--M --sinif`, isteğe bağlı `--tork --n --yuk --alfa-a` |
| `pimkesme` | Pim kesme gerilmesi ve delik yüzey basıncı | `--d --F`, isteğe bağlı `--n --kesit --t` |

### Örnekler

S355 parçada alın frezeleme: Ø80 freze, 6 diş, ae = 60 mm (ortalı), fz = 0,2 mm, ap = 4 mm, kappa = 90°, 2 kenet, kuvveti yalnızca sürtünme tutuyor. Kavrama açısı phi = 2 * asin(60/80) = 97,2°, z_e = 6 * 97,2 / 360 = 1,62:
```bash
python3 <skill-klasörü>/scripts/fikstur_hesap.py kenet --malzeme s355 --b 4 --h 0.2 --ze 1.62 --n 2 --durum surtunme
```

Ø16 H7 delikler, Ø16 g6 pimler, 400 mm ara mesafe, parçada ±0,1:
```bash
python3 <skill-klasörü>/scripts/fikstur_hesap.py pim --D1 16.000 16.018 --d1 15.983 15.994 --D2 16.000 16.018 --d2 15.983 15.994 --L 400 --tp 0.1 --uzaklik 800
```

## Girdileri toplarken

- **Tolerans değerleri**: ISO 286 sınır ölçülerini (min, max) gir. Kullanıcı "H7" gibi bir tolerans sınıfı verirse sınır ölçüleri ISO 286 tablosundan hesapla ve hangi değerleri kullandığını açıkça yaz.
- **Talaş kalınlığı (h) ve genişliği (b)**:
  - Tornada h = f * sin(kappa), b = ap / sin(kappa), `--ze` verilmez (1).
  - Frezede Kienzle sonucu **tek dişin** kuvvetidir. Kenet hesabında ortalama değil en büyük talaş kalınlığını kullan: h = fz * sin(kappa). b = ap / sin(kappa). Sonucu aynı anda kesen diş sayısıyla çarpmak için `--ze` ver: z_e = z * phi / 360. Kavrama açısı phi: ortalı alın frezede phi = 2 * asin(ae / D), yandan (kenar) frezede phi = acos(1 - 2 * ae / D). z_e < 1 çıkarsa script 1 alır. Hesabını kullanıcıya göster.
- **Kesme kuvveti zaten biliniyorsa** (CAM yazılımı, takım üreticisi hesaplayıcısı) `--fc` ile doğrudan gir; Kienzle tahmininden daha güvenilirdir. Frezede bu değer tek dişin değil, aynı anda kesen tüm dişlerin toplamı olmalı.
- **Kienzle tablosu**: s235, s355, c45, 42crmo4 ve gg25 klasik tablo değerleridir; hardox400, ggg50 ve aluminyum tahminidir ve script bunlar için uyarı verir. Kaynaklar arasında saçılma büyüktür; takım üreticisinin değeri varsa `--kc11 --mc` ile birlikte gir.
- **Durum seçimi** (`kenet --durum`):
  - `surtunme`: kesme kuvveti bağlama düzleminde ve onu karşılayan bir dayama yok. En kritik durum.
  - `kaldirma`: kuvvet parçayı desteklerden uzaklaştırıyor (ör. alttan delme çıkışı, kenetin karşı tarafında işleme).
  - `dayamaya`: kuvvet parçayı sabit bir dayamaya itiyor. En iyi tasarım budur, kullanıcıyı buna yönlendir. Ancak frezede kuvvetin yönü takım döndükçe değişir: dayamanın karşılamadığı bileşen (`--fdik`, verilmezse 0,5 * Fc varsayılır) yine sürtünmeyle tutulur. Bu durum yalnızca kuvvet her an dayamaya doğruysa `--fdik 0` ile hesaplanır.

## Sonucu sunarken

1. Kullandığın girdileri ve varsayımları (sürtünme katsayısı, emniyet katsayısı, tablo değerleri, z_e, Fdik) listele.
2. Script çıktısındaki ana sonucu yaz, ardından mühendislik yorumunu ekle: ne seçilmeli, hangi katalog değeriyle karşılaştırılmalı, sonuç sınırdaysa ne yapılmalı.
3. Sonuç sınırdaysa bunu açıkça belirt ve tasarım değişikliği öner (dayama ekleme, kenet sayısını artırma, tırtıllı kenet ucu, pim ekleme). Sınır sayılan durumlar: kapasite / yük oranı 1,0 ile 1,25 arası; cıvatada eksenel gerilme / akma oranı 0,75 üstü (script uyarır).
4. Bunun bir ön boyutlandırma olduğunu hatırlat. Kritik bağlantılar ve iş güvenliğiyle ilgili durumlar (kaldırma noktaları, döner fikstür kilitleri) için standart hesap ve üretici değerleri esas alınmalı.

## Tipik değerler (script varsayılanları)

| Parametre | Varsayılan | Not |
|---|---|---|
| Kenetleme emniyet katsayısı K | 2,0 | Kesintili kesme, titreşimli işlemde 2,5 ile 3 |
| Sürtünme çelik / çelik, işlenmiş, yağlı (mu1, mu2) | 0,12 | Kuru 0,15; tırtıllı kenet ucu 0,25 ile 0,3 |
| Kienzle düzeltmesi | 1,3 | Aşınmış takım ve negatif talaş açısı için |
| Aynı anda kesen diş sayısı z_e | 1 | Tornada 1; frezede hesaplanıp girilmeli |
| Dayamanın karşılamadığı kuvvet Fdik | 0,5 * Fc | Kaba varsayım; yalnızca `dayamaya` durumunda |
| Fikstür pim mesafesi toleransı tf | ±0,01 mm | |
| Cıvata tork katsayısı k | 0,2 | Yağlı diş 0,15 |
| Cıvata ön yükü | Akmanın %70'i | Eşdeğer gerilme yaklaşık %85 ile %89 |
| Sıkma faktörü alfa_A | 1,6 | Tork anahtarı; darbeli tabanca 2,5 |
| Cıvata bağlantı sürtünmesi mu | 0,15 | |
| Kaymaya karşı emniyet | 1,5 | Statik 1,2; titreşimli 1,8 |
| Pim emniyetli kesme gerilmesi | 150 N/mm2 | Sertleştirilmiş pim, darbeli yük |
| Delik yüzey basıncı | 100 N/mm2 | S235 / S355 gövde, darbeli yük |

Script'e yeni bir hesap eklenmesi gerekirse (ör. hidrolik silindir çapı, yay kuvveti) aynı yapıda yeni bir alt komut olarak ekle, örnek bir çalıştırmayla test et.
