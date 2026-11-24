# BOM Kontrolü

SolidWorks'ten çekilen BOM, satın alma ve imalata gitmeden önce aşağıdaki kurallarla kontrol edilir. Özel özellik adları ve izin verilen değerler `solidworks-makro` skill'indeki `OZEL-OZELLIKLER.md` dosyasındadır. O dosyada `[DOLDURULACAK]` olarak işaretli bir liste (ör. Process kodları) henüz belli değilse ilgili kontrolü Hata değil Uyarı olarak raporla ve kullanıcıdan listeyi iste.

Standart ve satın alma elemanları (Toolbox parçaları, pim, burç, kenet, cıvata, somun) imal edilen parça değildir. Bunlar için Thickness ve Yüksek Mukavemetli Sac mı? alanlarının boş olması hata sayılmaz.

## Kontroller

| # | Kontrol | Sonuç seviyesi |
|---|---|---|
| 1 | İmal edilen parçalarda zorunlu alanlardan boş olan var mı? (Reference No, Description, Material, Process, Thickness, Yüksek Mukavemetli Sac mı?) | Hata |
| 2 | Aynı Reference No farklı parçalarda tekrar ediyor mu? | Hata |
| 3 | Aynı dosya adı farklı Reference No ile mi geçiyor? | Uyarı |
| 4 | Material değeri izin verilen listede mi? Yazım farkı var mı? (ör. "S235" ile "1.0037 (S235JR)") | Hata |
| 5 | Process değeri izin verilen kodlardan biri mi? | Hata |
| 6 | Thickness sayısal mı? Şirketin kullandığı sac kalınlıklarından biri mi? Liste `OZEL-OZELLIKLER.md` dosyasında yoksa bu kontrolü atla ve kullanıcıya listeyi sor. | Uyarı |
| 7 | Thickness ile modeldeki gerçek kalınlık uyuşuyor mu? (BOM'da gerçek kalınlık sütunu varsa) | Hata |
| 8 | Yüksek mukavemetli sac işareti malzemeyle tutarlı mı? S235JR veya S355 için EVET ise Hata. Diğer malzemeler, `OZEL-OZELLIKLER.md` dosyasındaki yüksek mukavemetli malzeme listesi doğrulanana kadar Uyarı olarak raporlanır. | Hata / Uyarı |
| 9 | Ağırlık sıfır veya boş mu? Birim kg mı? SolidWorks belgesinin kütle birimi gram ise değerler 1000 kat büyük görünür (ör. 26373,08 değeri 26,4 kg'dır). | Hata |
| 10 | Ağırlık, malzeme yoğunluğu ile hacimden beklenenle uyumlu mu? SolidWorks'te malzeme atanmamışsa yoğunluk 1000 kg/m³ alınır; çelik parça yaklaşık 7,85 kat hafif görünür. | Uyarı |
| 11 | Standart elemanlar (pim, burç, kenet, cıvata) ayrı bir grupta mı, adetleri doğru mu? | Uyarı |

Material listesinde "1.0037 (S235JR)" değeri şirket listesinden geldiği için olduğu gibi kabul edilir. Ancak güncel EN 10025-2'de S235JR'nin malzeme numarası 1.0038'dir (1.0037 eski St 37-2 numarasıdır); raporda bunu bir kez not olarak belirt.

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
