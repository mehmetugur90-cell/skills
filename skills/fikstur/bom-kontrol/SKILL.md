---
name: bom-kontrol
description: "SolidWorks'ten çekilen BOM (malzeme listesi, parça listesi) dosyasını satın alma ve imalata gitmeden önce kontrol eder: boş özel özellikler, tekrar eden Reference No, geçersiz Material veya Process değeri, kalınlık ve ağırlık tutarsızlıkları, yüksek mukavemetli sac işareti. Kullanıcı BOM listesi, malzeme listesi veya BOM Excel dosyası paylaşıp kontrol istediğinde kullan."
---

# BOM Kontrolü

1. Kullanıcının BOM dosyasını oku (genelde Excel). Excel işlemleri için Skill aracını "anthropic-skills:xlsx" ile çağır (ortamda varsa); yoksa Python openpyxl kullan.
2. Özel özellik adları ve izin verilen değerler için Skill aracını "solidworks-makro" ile çağır ve oradaki `OZEL-OZELLIKLER.md` dosyasını kullan.
3. [BOM-KONTROL.md](./BOM-KONTROL.md) dosyasındaki kontrolleri uygula ve oradaki rapor formatıyla sonucu ver.
4. Orijinal sütunları değiştirme. Bilinmeyen bir değeri düzeltmek yerine kullanıcıya sor.
