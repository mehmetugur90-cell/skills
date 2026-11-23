# BOM Kontrolü

SolidWorks'ten çekilen BOM, satın alma ve imalata gitmeden önce aşağıdaki kurallarla kontrol edilir. Özel özellik adları ve izin verilen değerler `solidworks-makro` skill'indeki `OZEL-OZELLIKLER.md` dosyasındadır.

## Kontroller

| # | Kontrol | Sonuç seviyesi |
|---|---|---|
| 1 | Zorunlu alanlardan boş olan var mı? (Reference No, Description, Material, Process, Thickness, Yüksek Mukavemetli Sac mı?) | Hata |
| 2 | Aynı Reference No farklı parçalarda tekrar ediyor mu? | Hata |
| 3 | Aynı dosya adı farklı Reference No ile mi geçiyor? | Uyarı |
| 4 | Material değeri izin verilen listede mi? Yazım farkı var mı? (ör. "S235" ile "1.0037 (S235JR)") | Hata |
| 5 | Process değeri izin verilen kodlardan biri mi? | Hata |
| 6 | Thickness sayısal mı? Plaka için standart sac kalınlıklarından biri mi? | Uyarı |
| 7 | Thickness ile modeldeki gerçek kalınlık uyuşuyor mu? (BOM'da gerçek kalınlık sütunu varsa) | Hata |
| 8 | Yüksek mukavemetli sac işareti malzemeyle tutarlı mı? (ör. S235JR için EVET olmamalı; S690QL, Hardox için EVET olmalı) | Hata |
| 9 | Ağırlık sıfır veya boş mu? Birim kg mı? (SolidWorks belge birimi gram ise değerler 1000 kat büyük görünür) | Hata |
| 10 | Ağırlık, malzeme yoğunluğu ile hacimden beklenenle uyumlu mu? SolidWorks'te malzeme atanmamışsa kütle yanlış hesaplanır. | Uyarı |
| 11 | Standart elemanlar (pim, burç, kenet, cıvata) ayrı bir grupta mı, adetleri doğru mu? | Uyarı |

## Rapor formatı

```
### BOM Kontrol Özeti
- Toplam satır: N, hata: X, uyarı: Y

### Hatalar
| Satır | Reference No | Dosya | Kontrol | Açıklama |

### Uyarılar
| Satır | Reference No | Dosya | Kontrol | Açıklama |
```

Excel dosyası istendiyse kontrol sonuçlarını BOM'a yeni bir sütun ("Kontrol") olarak ekle, hatalı satırları açık kırmızı, uyarıları açık sarı ile işaretle; orijinal sütunları değiştirme.
