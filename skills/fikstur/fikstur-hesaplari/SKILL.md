---
name: fikstur-hesaplari
description: "Fikstür hesapları: kenetleme kuvveti, pim-delik boşluğu, elmas pim, konumlama hatası, cıvata torku, pim kesme. 'Kenet yeter mi', 'pim toleransı' gibi sorularda kullan."
---

# Fikstür Hesapları

Hesapları elle değil, [scripts/fikstur_hesap.py](./scripts/fikstur_hesap.py) ile yap. Böylece sonuç tekrarlanabilir olur ve kullanıcı aynı komutu değiştirip yeniden çalıştırabilir. Script yalnızca Python standart kütüphanesini kullanır.

```bash
python3 <skill-klasörü>/scripts/fikstur_hesap.py <komut> --help
```

## Komutlar

| Komut | Ne hesaplar | Asgari girdiler |
|---|---|---|
| `kenet` | Kesme kuvveti ve gereken toplam / kenet başına kuvvet | `--fc` veya `--malzeme --b --h`; `--durum`; `--n` |
| `pim` | Çapsal boşluklar, iki silindirik pim yeterliliği, elmas pim max genişliği, öteleme ve dönme hatası | `--D1 --d1 --D2 --d2` (min max), `--L`, `--tp` |
| `civata` | Önerilen tork veya verilen torktan ön yük, kaymaya karşı kapasite | `--M --sinif`, isteğe bağlı `--tork --n --yuk` |
| `pimkesme` | Pim kesme gerilmesi ve delik yüzey basıncı | `--d --F`, isteğe bağlı `--n --kesit --t` |

### Örnekler

S355 parçada frezeleme, ap = 4 mm, ortalama talaş kalınlığı 0,15 mm, 2 kenet, kuvveti yalnızca sürtünme tutuyor:
```bash
python3 fikstur_hesap.py kenet --malzeme s355 --b 4 --h 0.15 --n 2 --durum surtunme
```

Ø16 H7 delikler, Ø16 g6 pimler, 400 mm ara mesafe, parçada ±0,1:
```bash
python3 fikstur_hesap.py pim --D1 16.000 16.018 --d1 15.983 15.994 --D2 16.000 16.018 --d2 15.983 15.994 --L 400 --tp 0.1 --uzaklik 800
```

## Girdileri toplarken

- **Tolerans değerleri**: ISO 286 sınır ölçülerini (min, max) gir. Kullanıcı "H7" gibi bir tolerans sınıfı verirse sınır ölçüleri ISO 286 tablosundan hesapla ve hangi değerleri kullandığını açıkça yaz.
- **Talaş kalınlığı (h)**: frezede ortalama talaş kalınlığı hm, tornada f * sin(kappa). Kullanıcı yalnızca kesme parametrelerini verirse hesabını göster.
- **Kesme kuvveti zaten biliniyorsa** (CAM yazılımı, takım üreticisi hesaplayıcısı) `--fc` ile doğrudan gir; Kienzle tahmininden daha güvenilirdir.
- **Durum seçimi** (`kenet --durum`):
  - `surtunme`: kesme kuvveti bağlama düzleminde ve onu karşılayan bir dayama yok. En kritik durum.
  - `kaldirma`: kuvvet parçayı dayamalardan uzaklaştırıyor (ör. alttan delme çıkışı, kenetin karşı tarafında işleme).
  - `dayamaya`: kuvvet parçayı sabit bir dayamaya itiyor. En iyi tasarım budur, kullanıcıyı buna yönlendir.

## Sonucu sunarken

1. Kullandığın girdileri ve varsayımları (sürtünme katsayısı, emniyet katsayısı, tablo değerleri) listele.
2. Script çıktısındaki ana sonucu yaz, ardından mühendislik yorumunu ekle: ne seçilmeli, hangi katalog değeriyle karşılaştırılmalı, sonuç sınırdaysa ne yapılmalı.
3. Sonuç sınırdaysa (oran 0,8 ile 1,0 arası) bunu açıkça belirt ve tasarım değişikliği öner: dayama ekleme, kenet sayısını artırma, tırtıllı kenet ucu, pim ekleme.
4. Bunun bir ön boyutlandırma olduğunu hatırlat. Kritik bağlantılar ve iş güvenliğiyle ilgili durumlar (kaldırma noktaları, döner fikstür kilitleri) için standart hesap ve üretici değerleri esas alınmalı.

## Tipik değerler (script varsayılanları)

| Parametre | Varsayılan | Not |
|---|---|---|
| Kenetleme emniyet katsayısı K | 2,0 | Kesintili kesme, titreşimli işlemde 2,5 ile 3 |
| Sürtünme çelik / çelik, işlenmiş, yağlı | 0,12 | Kuru 0,15; tırtıllı kenet ucu 0,25 ile 0,3 |
| Kienzle düzeltmesi | 1,3 | Aşınmış takım ve negatif talaş açısı için |
| Cıvata tork katsayısı K | 0,2 | Yağlı diş 0,15 |
| Cıvata ön yükü | Akmanın %70'i | |
| Pim emniyetli kesme gerilmesi | 150 N/mm2 | Sertleştirilmiş pim, darbeli yük |
| Delik yüzey basıncı | 100 N/mm2 | S235 / S355 gövde, darbeli yük |

Script'e yeni bir hesap eklenmesi gerekirse (ör. hidrolik silindir çapı, yay kuvveti) aynı yapıda yeni bir alt komut olarak ekle, örnek bir çalıştırmayla test et.
