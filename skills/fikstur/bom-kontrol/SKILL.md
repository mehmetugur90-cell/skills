---
name: bom-kontrol
description: "SolidWorks BOM (malzeme listesi) Excel'i kontrol edilmek istendiğinde kullan: boş özel özellikler, tekrar eden Reference No, geçersiz Material veya Process, kalınlık ve ağırlık hataları."
---

# BOM Kontrolü

1. Kullanıcının BOM dosyasını oku (genelde Excel). Excel işlemleri için Skill aracını "xlsx" ile çağır (listede "anthropic-skills:xlsx" olarak görünebilir); bu skill yoksa Python openpyxl kullan.
2. Özel özellik adları ve izin verilen değerler için Skill aracını "solidworks-makro" ile çağır (listede "anthropic-skills:solidworks-makro" olarak görünebilir) ve o skill'in klasöründeki `OZEL-OZELLIKLER.md` dosyasını oku. Bu skill yoksa izin verilen Material ve Process değerlerini kullanıcıdan iste.
3. [BOM-KONTROL.md](./BOM-KONTROL.md) dosyasındaki kontrolleri uygula ve oradaki rapor formatıyla sonucu ver.
4. Orijinal sütunları değiştirme. Bilinmeyen bir değeri düzeltmek yerine kullanıcıya sor.
