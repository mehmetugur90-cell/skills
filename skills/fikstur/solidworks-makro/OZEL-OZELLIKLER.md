# Özel Özellikler (Custom Properties)

Kaynak: kullanıcının "Özel Özellikler" görev bölmesi (Parça Bilgisi sekmesi). Adlar birebir bu şekilde yazılmalıdır (büyük / küçük harf ve boşluklar dahil).

| Özellik adı | Tip | Zorunlu | Örnek değer | Not |
|---|---|---|---|---|
| `Reference No` | Metin | Evet | `18112026_3` | Kalıp: GGAAYYYY_sıra (doğrulanacak) |
| `Description` | Metin | Evet | | Parça adı / açıklaması |
| `Material` | Liste | Evet | `1.0037 (S235JR)` | Kalıp: "W.Nr (EN adı)". Tam liste: [DOLDURULACAK]. Not: güncel EN 10025-2'de S235JR = 1.0038; 1.0037 eski St 37-2 numarasıdır. Şirket listesindeki değer olduğu için olduğu gibi kullanılır, kullanıcıya bir kez hatırlatılır. |
| `Process` | Liste | Evet | `C` | Kodların anlamı: [DOLDURULACAK] |
| `Thickness` | Metin (sayı) | Evet (imal edilen parçalarda) | `35` | mm. Şirketin kullandığı sac kalınlıkları: [DOLDURULACAK] |
| `Yüksek Mukavemetli Sac mı?` | Liste | Evet | `HAYIR` | Değerler: `EVET`, `HAYIR`. VBA'da: `"Y" & ChrW(252) & "ksek Mukavemetli Sac m" & ChrW(305) & "?"` |
| Ağırlık | Bağlantılı (kütle) | Otomatik | `26373.08` | Görev bölmesinde "Weight (kg)" olarak görünüyor ama değer gram cinsinden: 35 mm plaka parça için 26373,08 g = 26,4 kg (belgenin kütle birimi gram). Özelliğin gerçek adı doğrulanacak |

## Açık sorular
- Process kodlarının tam listesi ve anlamları
- Material listesindeki tüm değerler ve hangilerinin yüksek mukavemetli sayıldığı (Yüksek Mukavemetli Sac mı? = EVET olması gerekenler)
- Şirketin kullandığı standart sac kalınlıkları
- Özelliklerin dosya geneline mi, konfigürasyona özel mi yazıldığı
- Ağırlık özelliğinin gerçek adı ve birimi
