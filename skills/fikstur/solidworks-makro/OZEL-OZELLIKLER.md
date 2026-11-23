# Özel Özellikler (Custom Properties)

Kaynak: kullanıcının "Özel Özellikler" görev bölmesi (Parça Bilgisi sekmesi). Adlar birebir bu şekilde yazılmalıdır (büyük / küçük harf ve boşluklar dahil).

| Özellik adı | Tip | Zorunlu | Örnek değer | Not |
|---|---|---|---|---|
| `Reference No` | Metin | Evet | `18112026_3` | Kalıp: GGAAYYYY_sıra (doğrulanacak) |
| `Description` | Metin | Evet | | Parça adı / açıklaması |
| `Material` | Liste | Evet | `1.0037 (S235JR)` | Kalıp: "W.Nr (EN adı)". Tam liste: [DOLDURULACAK] |
| `Process` | Liste | Evet | `C` | Kodların anlamı: [DOLDURULACAK] |
| `Thickness` | Metin (sayı) | Evet | `35` | mm |
| `Yüksek Mukavemetli Sac mı?` | Liste | Evet | `HAYIR` | Değerler: `EVET`, `HAYIR`. VBA'da: `"Y" & ChrW(252) & "ksek Mukavemetli Sac m" & ChrW(305) & "?"` |
| Ağırlık | Bağlantılı (kütle) | Otomatik | `26373.08` | Görev bölmesinde "Weight (kg)" olarak görünüyor, değer gram gibi duruyor. Özellik adı ve birim doğrulanacak |

## Açık sorular
- Process kodlarının tam listesi ve anlamları
- Material listesindeki tüm değerler ve hangilerinin yüksek mukavemetli sayıldığı
- Özelliklerin dosya geneline mi, konfigürasyona özel mi yazıldığı
- Ağırlık özelliğinin gerçek adı ve birimi
