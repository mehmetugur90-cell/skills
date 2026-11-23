---
name: solidworks-makro
description: "Türkçe SolidWorks 2025 için VBA makro yazar ve düzeltir: özel özellikler, BOM öncesi kontrol, toplu PDF ve DXF, montaj gezme. Makro veya otomasyon istendiğinde kullan."
---

# SolidWorks Makro (VBA)

Kullanıcı SolidWorks 2025'i **Türkçe arayüzle** kullanıyor ve makroları **VBA** ile yazıyor. Daha önce teknik resimden tek tıkla PDF alan bir makrosu var ve kullanıyor.

Bu skill'deki dosyalar:
- [OZEL-OZELLIKLER.md](./OZEL-OZELLIKLER.md): şirketin özel özellik adları ve izin verilen değerler. Özel özelliklere dokunan her makroda bunu oku.
- [MAKRO-FIKIRLERI.md](./MAKRO-FIKIRLERI.md): kullanıcının iş akışına göre önerilen makrolar ve durumları.
- `makrolar/`: hazır makro kaynak kodları (`.bas`), yazıldıkça eklenir.

## Kurallar

### 1. Dil bağımsızlığı
API adları her zaman İngilizcedir, ama modeldeki öğe adları arayüz diline göre değişir.
- Varsayılan düzlemleri adla seçme ("Front Plane" Türkçe arayüzde "Ön Düzlem" olur). Özellik ağacını `FirstFeature` / `GetNextFeature` ile gez ve `GetTypeName2 = "RefPlane"` olan ilk üç özelliği al (sırasıyla Ön, Üst, Sağ).
- Özellik tipini `GetTypeName2` ile kontrol et, özellik adıyla değil.
- Hata ve uyarı metinlerini SolidWorks'ün ürettiği metinle karşılaştırma; dönüş kodlarını (enum) kullan.

### 2. Türkçe karakterler ve kodlama
VBA editörü dosyaları Windows ANSI kod sayfasıyla okur. UTF-8 bir `.bas` dosyası içe aktarıldığında Türkçe karakterler bozulur.
- Ürettiğin `.bas` dosyaları **yalnızca ASCII** karakter içersin.
- Türkçe karakter gereken string'leri `ChrW` ile kur: ı = `ChrW(305)`, İ = `ChrW(304)`, ş = `ChrW(351)`, Ş = `ChrW(350)`, ğ = `ChrW(287)`, Ğ = `ChrW(286)`, ü = `ChrW(252)`, Ü = `ChrW(220)`, ö = `ChrW(246)`, Ö = `ChrW(214)`, ç = `ChrW(231)`, Ç = `ChrW(199)`.
- Kullanıcıya gösterilen mesajlar ASCII Türkçe olabilir ("Acik dokuman yok") ya da `ChrW` ile kurulabilir; özellik adları gibi birebir eşleşmesi gerekenler mutlaka `ChrW` ile kurulmalı.
- Kod içi yorumlar ASCII Türkçe yazılır.

### 3. Kod yapısı
- `Option Explicit` her zaman.
- Giriş noktası `Sub main()`.
- `swconst` referansına bağımlı olmamak için kullanılan enum değerlerini modül başında `Const` olarak tanımla ve yanına enum adını yorum olarak yaz (ör. `Const swDocPART As Long = 1`).
- Değiştirilebilir ayarlar (klasör yolu, özellik adları, dosya adı kalıbı) modülün en üstünde, açıklamalı sabitler olarak dursun. Kullanıcı kodu okumadan ayarlayabilsin.
- Montajları gezerken: bastırılmış (suppressed) bileşenleri atla, BOM'dan hariç tutulanları (`ExcludeFromBOM`) atla, Toolbox parçalarını (`Extension.ToolboxPartType <> 0`) ayrı ele al, aynı dosyayı yol (path) ile tekilleştir, hafif (lightweight) bileşenleri çözümle.
- Özel özellik okurken önce konfigürasyona özel, sonra dosya geneli (`CustomPropertyManager("")`) yöneticisine bak. Kullanıcının "Özel Özellikler" görev bölmesinin hangisine yazdığı şablona bağlıdır.
- Dosya yazan makrolar mevcut dosyanın üzerine yazmadan önce sorsun veya tarih-saat eki kullansın.
- Uzun işlemlerde sonunda özet `MsgBox` göster: kaç dosya işlendi, kaç hata var, çıktı nerede.

### 4. Doğrulama
Bu ortamda SolidWorks yok, makroyu çalıştırarak test edemezsin. Bu yüzden:
- API çağrılarının imzasını ve dönüş tipini dikkatle kontrol et. Emin olmadığın bir API için kullanıcıya SolidWorks API Help'te (Yardım > API Yardımı) hangi sayfaya bakacağını söyle.
- Kullanıcıya test adımlarını ver: önce küçük bir montajda, dosyaların yedeği alınmışken dene.
- Makro dosya değiştiriyorsa (özellik yazma, kaydetme) önce yalnızca rapor üreten bir "deneme modu" sabiti ekle (`Const DENEME_MODU As Boolean = True`).

### 5. Kurulum talimatı (kullanıcıya her yeni makroda ver)
1. SolidWorks'te Araçlar > Makro > Yeni ile boş bir makro oluştur ve kaydet (`.swp`).
2. Açılan VBA editöründe File > Import File ile `.bas` dosyasını içe aktar ya da kodu modüle yapıştır.
3. Tools > References'ta "SldWorks 2025 Type Library" işaretli olmalı (yeni makroda varsayılan olarak işaretlidir).
4. Araç çubuğuna buton eklemek için: Araçlar > Özelleştir > Komutlar > Makro, butonu sürükle ve `.swp` dosyasını seç.
