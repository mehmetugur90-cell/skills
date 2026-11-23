# Makro Fikirleri

Kullanıcının iş akışı: parça bazında özel özellikleri doldurma, BOM çekme, teknik resimden PDF alma (mevcut makrosu var).

| # | Makro | Ne yapar | Nerede kullanılır | Durum |
|---|---|---|---|---|
| 1 | Özellik kontrol | Montajdaki tüm parçalarda boş zorunlu özellikleri ve malzeme atanmamış parçaları raporlar (CSV) | BOM çekmeden önce | Önerildi |
| 2 | Kalınlık ve ağırlık doldurma | Thickness'ı modelden (sac kalınlığı veya en ince sınır ölçüsü), ağırlığı kg olarak yazar | Montajda toplu | Önerildi |
| 3 | Malzeme eşitleme | Material değerine göre SolidWorks malzemesini atar, yüksek mukavemet alanını otomatik doldurur | Özellikler doldurulduktan sonra | Önerildi |
| 4 | Toplu DXF | Kesime gidecek parçaların DXF'ini `ReferenceNo_Malzeme_Kalinlik.dxf` adıyla çıkarır | Lazer / plazma kesime gönderirken | Önerildi |
| 5 | Montajdan toplu PDF | Montajdaki parçaların teknik resimlerini bulup PDF'e çevirir, resmi olmayanları listeler | Proje tesliminde | Önerildi |
| 6 | Reference No numaralama | Boş Reference No alanlarına tarih_sıra kalıbıyla numara verir | Yeni montajda | Önerildi |
| 7 | Teknik resim kontrolü | Antet alanları, görünümler ve kopuk ölçüler için PDF öncesi kontrol | Mevcut PDF makrosunun başında | Önerildi |

Öneri: 1, 2 ve 3 tek bir "BOM hazırlık" makrosunda birleştirilebilir.
