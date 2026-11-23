# Fikstür Tasarım Kontrol Listesi

## A. Genel (her fikstür tipi)

### A1. Konumlama (locating)
- [ ] 3-2-1 prensibi: birincil yüzeyde 3, ikincilde 2, üçüncülde 1 temas noktası var mı?
- [ ] Aşırı belirleme (over-constraint) var mı? Aynı serbestlik derecesini iki eleman tutuyorsa parça zorlanır veya oturmaz.
- [ ] Konumlama yüzeyleri parça resmindeki datumlarla (A, B, C) aynı mı? Farklıysa tolerans zinciri büyür.
- [ ] İki pimli konumlamada ikinci pim elmas pim (diamond pin) mi? İki silindirik pim delik merkez mesafesi toleransını karşılamaz.
- [ ] Konumlama elemanları kenetleme kuvvetinin karşısında mı? Kenet, parçayı dayamaya doğru itmeli; dayamadan uzaklaştırmamalı.
- [ ] Ham (oksit kesimli, plazma kesimli) yüzeye konumlanırken kesim toleransı ve çapak hesaba katıldı mı?
- [ ] Dayama yüzeyleri küçük ve tanımlı mı (pad, pul)? Geniş düz temas yüzeyi, çapak ve kirden dolayı tekrarlanabilirliği bozar.
- [ ] Konumlama elemanları değiştirilebilir mi (aşınma parçası)? Sertleştirilmiş mi?

### A2. Kenetleme (clamping)
- [ ] Kenetleme kuvveti yeterli mi? Hesaplanmadıysa hesapla.
- [ ] Kenetleme noktası parçanın rijit bölgesinde mi, destek noktasının tam üstünde mi? Desteksiz bölgeye kenet parçayı eğer.
- [ ] Kenetleme sırası tanımlı mı? Önce konumlayan, sonra sabitleyen kenetler.
- [ ] Kenet ucu parçada iz bırakır mı (görünür yüzey, işlenmiş yüzey)?
- [ ] Kenet açıkken parça yükleme ve alma yolunu kapatıyor mu?
- [ ] Kenet kolu açık konumda başka bir elemana veya operatöre çarpıyor mu?

### A3. Hata önleme (poka-yoke)
- [ ] Parça ters, simetrik yanlış veya sağ/sol karıştırılarak takılabiliyor mu? Engelleyici pim veya şekil var mı?
- [ ] Benzer parçalar için kullanılan fikstürlerde varyant karışıklığı engelleniyor mu?
- [ ] Parçanın yerinde olduğu kontrol edilebiliyor mu (görsel, sensör)?

### A4. Ergonomi ve iş güvenliği
- [ ] Parça ağırlığı manuel taşımaya uygun mu? Ağırsa vinç veya manipülatör yaklaşma yolu var mı?
- [ ] Fikstürün kendisinde kaldırma noktaları (mapa, kaldırma deliği) ve ağırlık bilgisi var mı?
- [ ] Çalışma yüksekliği uygun mu? Döner (pozisyoner) fikstürlerde kilitleme var mı?
- [ ] Sıkışma (pinch point) ve keskin kenar riski var mı?
- [ ] Ağırlık merkezi döner eksene yakın mı (pozisyoner yükü ve dengesi)?

### A5. İmalat ve bakım
- [ ] Fikstür parçaları atölyede imal edilebilir mi? Gereksiz hassas tolerans var mı?
- [ ] Standart elemanlar (pim, burç, kenet) katalogdan mı seçildi? Özel imalat yerine standart tercih edildi mi?
- [ ] Ayar gerektiren elemanlar ayarlanıp sabitlenebiliyor mu (ayar vidası + kontra somun, şim paketi)?
- [ ] Fikstür kimlik etiketi (fikstür no, parça no, revizyon) için yer var mı?
- [ ] Fikstürün kendi doğrulaması için ölçüm referansları (CMM referans delikleri, referans yüzeyleri) var mı?

## B. Punta fikstürü

- [ ] Punta noktalarına torç ve operatör eli rahat erişebiliyor mu?
- [ ] Punta sonrası parça fikstürden çıkarılabilir mi? Kapalı kutu yapılarda parça fikstüre kilitlenmesin.
- [ ] Punta fikstürünün konumlama referansları kaynak fikstürü ve talaşlı işleme referanslarıyla uyumlu mu?
- [ ] Parçalar arası kaynak ağzı aralığı (kök aralığı) fikstürle sağlanıyor mu? Aralık plakası veya ayar pimi gerekir mi?
- [ ] Sac ve plaka kesim toleransları birikince montaj mümkün kalıyor mu?

## C. Kaynak fikstürü

- [ ] Torç erişimi: tüm dikişlere doğru torç açısıyla ulaşılabiliyor mu? Robotlu kaynakta robot erişim simülasyonu yapıldı mı?
- [ ] Kaynak pozisyonu: dikişlerin çoğu oluk (PA) veya yatay (PB) pozisyonda kaynatılabiliyor mu? Pozisyoner gerekir mi?
- [ ] Çarpılma: kaynak sonrası çekme yönü ve miktarı değerlendirildi mi? Ön gerdirme (pre-set) veya ters açı verildi mi?
- [ ] Kaynak sonrası parça fikstürden çıkabiliyor mu? Çekme parçayı pimlere kilitleyebilir: konik pim, geri çekilebilir pim, sökülebilir dayama düşünüldü mü?
- [ ] Sıçrantı (spatter): pim, burç, mil ve kenet mekanizmaları sıçrantıdan korunuyor mu? Dikiş altında bakır veya sıçrantı tutmayan altlık var mı?
- [ ] Topraklama (şase) bağlantısı fikstür üzerinden mi? Akım yatak, mil, pnömatik eleman üzerinden geçiyor mu (ark izi, yatak hasarı)?
- [ ] Isı: kaynak bölgesine yakın konumlama elemanları ısıdan genleşip parçayı sıkıştırır mı? Plastik ve kauçuk elemanlar ısıya dayanıklı mı?
- [ ] Ön tav gereken malzemelerde (yüksek mukavemetli, kalın kesit) ön tav ekipmanı için erişim var mı?
- [ ] Kaynak dumanı emişi için alan var mı?

## D. Talaşlı işleme fikstürü

- [ ] Kesme kuvvetleri konumlama elemanlarına doğru mu yönleniyor? Kuvvetin yalnızca sürtünmeyle tutulması gereken durumlar belirlendi mi?
- [ ] Rijitlik: parçanın işlenen bölgesi altında destek var mı? Uzun konsollu bölgelerde ayarlı destek (yaylı / hidrolik destek) var mı?
- [ ] Ayarlı destekler parçayı kaldırmadan, kenetlemeden sonra mı kilitleniyor?
- [ ] Takım çarpışması: takım, takım tutucu ve iş mili kafası fikstüre veya kenetlere çarpıyor mu? En uzun takımla kontrol edildi mi?
- [ ] Tek bağlamada işlenebilecek yüzeyler maksimize edildi mi (bağlama sayısı = hata kaynağı)?
- [ ] Talaş tahliyesi: talaş ve kesme sıvısı birikecek cep var mı? Konumlama yüzeyleri talaştan kolay temizlenebiliyor mu?
- [ ] Fikstürün tezgah tablasına bağlanması: T kanal, sıfır noktası sistemi, referans pimleri tanımlı mı? Fikstür sıfırı tezgaha nasıl aktarılıyor?
- [ ] Kaynaklı parçada işleme payı: kaynak çarpılması işleme payını tüketebilir mi? Önceki operasyondaki referanslarla uyum var mı?
- [ ] Hidrolik veya pnömatik bağlamada basınç kaybında güvenlik (çek valf, basınç anahtarı) var mı?

## E. Şablon, mastar ve aparat

- [ ] Şablonun referans aldığı yüzey parça resmindeki datum mu?
- [ ] Delme şablonunda burç tipi (sabit / değiştirilebilir) ve burç ile parça arası mesafe uygun mu? (talaş çıkışı için genelde 0,5 d ile 1 d arası)
- [ ] Mastar toleransı ölçülen toleransın yaklaşık onda biri mi? Aşınma payı bırakıldı mı?
- [ ] Geçer ve geçmez tarafları açıkça işaretli mi (renk, kazıma)?
- [ ] Şablonun ağırlığı ve tutma yeri operatöre uygun mu?
- [ ] Şablon üzerinde parça no, revizyon ve şablon kimliği kazıma veya etiketle var mı?
