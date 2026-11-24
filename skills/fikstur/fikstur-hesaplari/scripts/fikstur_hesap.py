#!/usr/bin/env python3
"""Fikstür tasarımı için mühendislik hesapları.

Alt komutlar:
  kenet      Talaşlı işlemede gereken kenetleme kuvveti (Kienzle + sürtünme)
  pim        İki pimli konumlama: boşluk, konum hatası, elmas pim genişliği
  civata     Cıvata ön yükü, sıkma torku ve kaymaya karşı taşıma kapasitesi
  pimkesme   Pim kesme gerilmesi ve delik yüzey basıncı

Girdi birimleri: mm, N, N/mm2 (MPa), Nm. Çıktıda ayrıca kN ve kgf verilir.
Sonuçlar ön boyutlandırma içindir; kritik bağlantılarda standart hesap
(VDI 2230, EN 1993-1-8 vb.) ve üretici katalog değerleri esas alınır.
"""

import argparse
import math
import sys

# Kienzle katsayıları: kc1.1 [N/mm2], mc [-], kaynak notu.
# İlk beş satır ders kitaplarında sık geçen klasik tablo değerleridir
# (S235 ~ St 37, S355 ~ St 50-2, C45 ~ Ck 45 N). Kaynaklar arasında
# saçılma büyüktür. "tahmini" işaretli satırlar için tek bir yerleşik
# kaynak yoktur; mümkünse takım üreticisinin değeri kullanılmalı.
KIENZLE = {
    "s235": (1780, 0.17, "tablo"),
    "s355": (1990, 0.26, "tablo"),
    "c45": (2220, 0.14, "tablo"),
    "42crmo4": (2500, 0.26, "tablo"),
    "gg25": (1160, 0.26, "tablo"),
    "hardox400": (2900, 0.25, "tahmini"),
    "ggg50": (1500, 0.25, "tahmini"),
    "aluminyum": (700, 0.25, "tahmini"),
}

# Metrik kaba diş gerilme kesiti As [mm2] (ISO 898-1)
CIVATA = {
    5: 14.2, 6: 20.1, 8: 36.6, 10: 58.0, 12: 84.3, 14: 115.0, 16: 157.0,
    18: 192.0, 20: 245.0, 22: 303.0, 24: 353.0, 27: 459.0, 30: 561.0,
}

# Akma sınırı Rp0.2 [N/mm2] (ISO 898-1). 8.8 için M16 üstü 660.
SINIF = {"8.8": 640, "10.9": 940, "12.9": 1100}


def pozitif(s):
    v = float(s)
    if v <= 0:
        raise argparse.ArgumentTypeError(f"pozitif olmalı: {s}")
    return v


def negatif_degil(s):
    v = float(s)
    if v < 0:
        raise argparse.ArgumentTypeError(f"negatif olamaz: {s}")
    return v


def pozitif_tam(s):
    v = int(s)
    if v <= 0:
        raise argparse.ArgumentTypeError(f"pozitif tam sayı olmalı: {s}")
    return v


def baslik(metin):
    print()
    print(metin)
    print("-" * len(metin))


def satir(ad, deger, birim=""):
    print(f"  {ad:<56} {deger} {birim}".rstrip())


# ---------------------------------------------------------------- kenet
def kenet(a):
    baslik("Kesme kuvveti")
    if a.fc is not None:
        fc = a.fc
        satir("Kesme kuvveti Fc (girilen)", f"{fc:.0f}", "N")
    else:
        if a.b is None or a.h is None:
            sys.exit("Hata: --fc ya da --b ve --h birlikte verilmeli.")
        if (a.kc11 is None) != (a.mc is None):
            sys.exit("Hata: --kc11 ve --mc birlikte verilmeli.")
        if a.kc11 is not None:
            kc11, mc, kaynak = a.kc11, a.mc, "girilen"
        else:
            kc11, mc, not_ = KIENZLE[a.malzeme]
            kaynak = f"{a.malzeme}, {not_}"
        ze = max(a.ze, 1.0)
        kc = kc11 * a.h ** (-mc)
        fc_dis = a.b * a.h ** (1 - mc) * kc11 * a.duzeltme
        fc = fc_dis * ze
        satir(f"kc1.1 / mc ({kaynak})", f"{kc11} / {mc}")
        satir("Talaş genişliği b / kalınlığı h", f"{a.b} / {a.h}", "mm")
        satir("Özgül kesme kuvveti kc = kc1.1 * h^(-mc)", f"{kc:.0f}", "N/mm2")
        satir("Düzeltme katsayısı (aşınma, talaş açısı)", f"{a.duzeltme}")
        satir("Tek diş kuvveti = b * h^(1-mc) * kc1.1 * düzeltme", f"{fc_dis:.0f}", "N")
        satir("Aynı anda kesen diş sayısı z_e", f"{ze:g}")
        satir("Kesme kuvveti Fc = tek diş kuvveti * z_e", f"{fc:.0f}", "N")
        if a.ze < 1.0:
            print("  Not: z_e < 1 girildi, en az bir diş kesiyor kabul edildi (z_e = 1).")
        if "tahmini" in kaynak:
            print("  UYARI: bu malzemenin Kienzle değeri tahminidir; takım üreticisi değeriyle doğrula.")

    k = a.emniyet
    mu = a.mu1 + a.mu2
    baslik("Gereken kenetleme kuvveti")
    if a.durum == "surtunme":
        ftop = k * fc / mu
        satir("Durum", "kuvvet bağlama düzleminde, yalnızca sürtünme tutuyor")
        satir("Sürtünme mu1 (kenet-parça) + mu2 (parça-destek)", f"{a.mu1} + {a.mu2}")
        satir("Toplam kenet kuvveti = K * Fc / (mu1 + mu2)", f"{ftop:.0f}", "N")
    elif a.durum == "kaldirma":
        ftop = k * fc
        satir("Durum", "kuvvet parçayı desteklerden uzaklaştırıyor")
        satir("Toplam kenet kuvveti = K * Fc", f"{ftop:.0f}", "N")
    else:  # dayamaya
        if a.fdik is not None:
            fdik, fdik_not = a.fdik, "girilen"
        else:
            fdik, fdik_not = 0.5 * fc, "varsayım: 0,5 * Fc"
        ftop = k * fdik / mu
        satir("Durum", "Fc sabit dayamaya doğru, dayama karşılıyor")
        satir(f"Dayamanın karşılamadığı kuvvet Fdik ({fdik_not})", f"{fdik:.0f}", "N")
        satir("Sürtünme mu1 (kenet-parça) + mu2 (parça-destek)", f"{a.mu1} + {a.mu2}")
        satir("Toplam kenet kuvveti = K * Fdik / (mu1 + mu2)", f"{ftop:.0f}", "N")
        print("  Not: frezede kuvvetin yönü takım döndükçe değişir; radyal ve ilerleme")
        print("  bileşenleri dayamaya değil sürtünmeye kalır. Fdik bu bileşenin tahminidir.")
        print("  Uyarı: dayamanın kendisi ve bağlantısı Fc için ayrıca kontrol edilmeli.")
        if fdik == 0:
            print("  Not: Fdik = 0 olsa da kenet parçayı yerinde tutmalı (titreşim, parça ağırlığı,")
            print("  takım çıkışı); kenet seçimini bu sonuca değil işin gereğine göre yap.")
    satir("Emniyet katsayısı K", f"{k}")
    satir("Kenet sayısı", f"{a.n}")
    satir("Kenet başına kuvvet", f"{ftop / a.n:.0f}", "N")
    satir("Kenet başına kuvvet", f"{ftop / a.n / 9.81:.0f}", "kgf")
    print("\n  Hızlı kenet seçerken katalogdaki 'tutma kuvveti' (holding capacity)")
    print("  değil, 'sıkma kuvveti' (clamping force) değeri bu sonuçla karşılaştırılmalı.")


# ---------------------------------------------------------------- pim
def pim(a):
    for ad in ("D1", "d1", "D2", "d2"):
        lo, hi = getattr(a, ad)
        if lo > hi:
            sys.exit(f"Hata: --{ad} için önce MIN sonra MAX gir.")
    c1max = a.D1[1] - a.d1[0]
    c1min = a.D1[0] - a.d1[1]
    c2max = a.D2[1] - a.d2[0]
    c2min = a.D2[0] - a.d2[1]
    delta = a.tp + a.tf  # merkez mesafesinde karşılanması gereken toplam sapma

    baslik("Boşluklar (çapsal)")
    satir("1. delik / pim (silindirik)  min / max", f"{c1min:.3f} / {c1max:.3f}", "mm")
    satir("2. delik / pim               min / max", f"{c2min:.3f} / {c2max:.3f}", "mm")
    if c1min < 0 or c2min < 0:
        print("  UYARI: min boşluk negatif, en kötü durumda parça pime girmez.")

    baslik("Merkez mesafesi uyumu")
    satir("Merkez mesafesi L", f"{a.L}", "mm")
    satir("Parça toleransı + fikstür toleransı (+-)", f"{a.tp} + {a.tf} = {delta:.3f}", "mm")
    iki_silindirik_ok = (c1min + c2min) / 2 >= delta
    satir("İki silindirik pim yeterli mi? (c1min+c2min)/2 >= delta",
          "EVET" if iki_silindirik_ok else "HAYIR")

    baslik("Elmas pim (2. pim)")
    a_kalan = delta - max(c1min, 0.0) / 2  # 1. pimin min boşluğu sapmanın bir kısmını karşılar
    if a_kalan <= 0:
        print("  1. pimin boşluğu sapmayı tek başına karşılıyor; elmas pim genişliği kısıtsız.")
    elif c2min <= 0:
        print("  UYARI: 2. delik / pim min boşluğu sıfır veya negatif; elmas pim girmez.")
    else:
        R = a.D2[0] / 2
        r = a.d2[1] / 2
        bmax = (R * R - r * r - a_kalan * a_kalan) / a_kalan
        satir("Elmas pimin karşılaması gereken sapma a = delta - c1min/2", f"{a_kalan:.3f}", "mm")
        if bmax <= 0:
            print("  UYARI: bu boşlukla hiçbir elmas pim genişliği yeterli değil.")
            print("  2. pim boşluğunu artır ya da merkez mesafesi toleransını daralt.")
        else:
            satir("Maksimum silindirik temas genişliği b", f"{bmax:.2f}", "mm")
            print("  b, merkezleri birleştiren doğru boyunca ölçülür. Silindirik temas yüzeyleri")
            print("  bu doğruya dik yönde, traşlanmış yüzler bu doğru yönünde yerleştirilir.")
            if bmax < 1.5:
                print("  Not: b < 1,5 mm hızlı aşınır. 2. pimin boşluğunu artırmak b'yi büyütür")
                print("  ama dönme hatasını da artırır; katalog elmas pimlerinin b değeriyle karşılaştır.")

    baslik("Konumlama hatası (en kötü durum)")
    oteleme = c1max / 2
    donme = math.atan((c1max / 2 + c2max / 2) / a.L)
    satir("Öteleme (1. pim ekseninde, her yönde)", f"+-{oteleme:.3f}", "mm")
    satir("Dönme açısı", f"+-{math.degrees(donme) * 60:.2f}", "dakika (')")
    if a.uzaklik is not None:
        X = a.uzaklik
        sapma = c1max / 2 * abs(1 - X / a.L) + c2max / 2 * abs(X) / a.L
        satir(f"1. pimden {X:g} mm uzaktaki noktanın dik sapması", f"+-{sapma:.3f}", "mm")
        print("  (nokta merkezleri birleştiren doğru üzerinde; doğru boyunca ayrıca")
        print(f"  +-{oteleme:.3f} mm öteleme olabilir)")


# ---------------------------------------------------------------- civata
def civata(a):
    if a.M not in CIVATA:
        sys.exit(f"Hata: M{a.M} tabloda yok. Seçenekler: {sorted(CIVATA)}")
    As = CIVATA[a.M]
    rp = SINIF[a.sinif]
    if a.sinif == "8.8" and a.M > 16:
        rp = 660

    baslik(f"M{a.M} {a.sinif} cıvata")
    satir("Gerilme kesiti As / akma Rp0.2", f"{As} mm2 / {rp}", "N/mm2")
    if a.tork is not None:
        fv = a.tork * 1000 / (a.k * a.M)
        satir("Girilen tork", f"{a.tork}", "Nm")
    else:
        fv = 0.7 * rp * As
        tork = a.k * fv * a.M / 1000
        satir("Ön yük hedefi", "akmanın %70'i")
        satir("Önerilen sıkma torku T = k * F * d", f"{tork:.0f}", "Nm")
    gerilme = fv / As
    satir("Tork katsayısı k", f"{a.k}")
    satir("Ön yük F", f"{fv / 1000:.1f}", "kN")
    satir("Eksenel gerilme / akma oranı", f"{gerilme:.0f} N/mm2  (%{gerilme / rp * 100:.0f})")
    if gerilme > 0.75 * rp:
        print("  UYARI: eksenel gerilme akmanın %75'ini aşıyor; sıkma burulmasıyla eşdeğer")
        print("  gerilme akmaya yaklaşır (VDI 2230 sınırı %90). Torku düşür.")

    baslik("Kaymaya karşı kapasite (sürtünmeli bağlantı)")
    fmin = fv / a.alfa_a
    kap = a.n * fmin * a.mu * a.yuzey / a.emniyet
    satir("Sıkma faktörü alfa_A (ön yük saçılması)", f"{a.alfa_a}")
    satir("En düşük ön yük F / alfa_A", f"{fmin / 1000:.1f}", "kN")
    satir("Cıvata sayısı / sürtünme yüzeyi sayısı", f"{a.n} / {a.yuzey}")
    satir("Sürtünme katsayısı mu / kayma emniyeti", f"{a.mu} / {a.emniyet}")
    satir("Taşınabilir enine yük", f"{kap / 1000:.1f}", "kN")
    if a.yuk is not None:
        satir("Etkiyen enine yük", f"{a.yuk / 1000:.1f}", "kN")
        satir("Sonuç", "YETERLİ" if kap >= a.yuk else "YETERSİZ: pim ekle veya cıvatayı büyüt")
    print("  Not: oturma kaybı (embedding) hesaba katılmadı. Konumlama hassasiyeti")
    print("  cıvataya değil pime verilmeli; cıvata deliği boşluklu.")


# ---------------------------------------------------------------- pimkesme
def pimkesme(a):
    alan = math.pi * a.d ** 2 / 4
    tau = a.F / (a.n * a.kesit * alan)
    baslik(f"Pim Ø{a.d:g} kesme kontrolü")
    satir("Pim sayısı / kesme yüzeyi", f"{a.n} / {a.kesit}")
    satir("Kesme gerilmesi = F / (n * kesit * pi * d^2 / 4)", f"{tau:.0f}", "N/mm2")
    satir("Emniyetli kesme gerilmesi", f"{a.tau_em:g}", "N/mm2")
    satir("Sonuç", "YETERLİ" if tau <= a.tau_em else "YETERSİZ")
    if a.t:
        p = a.F / (a.n * a.d * a.t)
        baslik("Delik yüzey basıncı")
        satir("Temas boyu t", f"{a.t:g}", "mm")
        satir("Yüzey basıncı p = F / (n * d * t)", f"{p:.0f}", "N/mm2")
        satir("Emniyetli yüzey basıncı", f"{a.p_em:g}", "N/mm2")
        satir("Sonuç", "YETERLİ" if p <= a.p_em else "YETERSİZ")


def main():
    ana = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    alt = ana.add_subparsers(dest="komut", required=True)

    k = alt.add_parser("kenet", help="Talaşlı işleme kenetleme kuvveti")
    k.add_argument("--fc", type=pozitif, help="Kesme kuvveti biliniyorsa [N] (frezede tüm kesen dişlerin toplamı)")
    k.add_argument("--malzeme", type=str.lower, choices=list(KIENZLE), default="s355",
                   help="Kienzle tablosu malzemesi")
    k.add_argument("--kc11", type=pozitif, help="kc1.1 [N/mm2] (tablo yerine, --mc ile birlikte)")
    k.add_argument("--mc", type=pozitif, help="mc [-] (tablo yerine, --kc11 ile birlikte)")
    k.add_argument("--b", type=pozitif, help="Talaş genişliği [mm] (ap / sin(kappa))")
    k.add_argument("--h", type=pozitif,
                   help="Talaş kalınlığı [mm] (tornada f*sin(kappa); frezede kenet için fz*sin(kappa))")
    k.add_argument("--ze", type=pozitif, default=1.0,
                   help="Frezede aynı anda kesen diş sayısı z*phi/360 (tornada 1)")
    k.add_argument("--duzeltme", type=pozitif, default=1.3,
                   help="Aşınma ve talaş açısı düzeltmesi (varsayılan 1.3)")
    k.add_argument("--durum", choices=["surtunme", "kaldirma", "dayamaya"], default="surtunme")
    k.add_argument("--fdik", type=negatif_degil,
                   help="dayamaya: dayamanın karşılamadığı kuvvet [N] (varsayılan 0,5*Fc)")
    k.add_argument("--mu1", type=pozitif, default=0.12, help="Kenet-parça sürtünmesi")
    k.add_argument("--mu2", type=pozitif, default=0.12, help="Parça-destek yüzeyi sürtünmesi")
    k.add_argument("--emniyet", type=pozitif, default=2.0, help="Emniyet katsayısı K")
    k.add_argument("--n", type=pozitif_tam, default=1, help="Kenet sayısı")
    k.set_defaults(fonk=kenet)

    p = alt.add_parser("pim", help="İki pimli konumlama")
    p.add_argument("--D1", type=pozitif, nargs=2, required=True, metavar=("MIN", "MAX"),
                   help="1. delik çapı min max")
    p.add_argument("--d1", type=pozitif, nargs=2, required=True, metavar=("MIN", "MAX"),
                   help="1. pim (silindirik) çapı min max")
    p.add_argument("--D2", type=pozitif, nargs=2, required=True, metavar=("MIN", "MAX"),
                   help="2. delik çapı min max")
    p.add_argument("--d2", type=pozitif, nargs=2, required=True, metavar=("MIN", "MAX"),
                   help="2. pim (elmas) çapı min max")
    p.add_argument("--L", type=pozitif, required=True, help="Delikler arası mesafe [mm]")
    p.add_argument("--tp", type=negatif_degil, required=True,
                   help="Parça merkez mesafesi toleransı +- [mm]")
    p.add_argument("--tf", type=negatif_degil, default=0.01,
                   help="Fikstür pim mesafesi toleransı +- [mm] (varsayılan 0,01)")
    p.add_argument("--uzaklik", type=float,
                   help="1. pimden merkez doğrultusu boyunca mesafe [mm]; o noktanın sapması hesaplanır")
    p.set_defaults(fonk=pim)

    c = alt.add_parser("civata", help="Cıvata ön yükü ve kayma kapasitesi")
    c.add_argument("--M", type=int, required=True, help=f"Nominal çap: {sorted(CIVATA)}")
    c.add_argument("--sinif", choices=list(SINIF), default="8.8", help="Mukavemet sınıfı")
    c.add_argument("--tork", type=pozitif, help="Uygulanan tork [Nm] (yoksa önerilir)")
    c.add_argument("--k", type=pozitif, default=0.2, help="Tork katsayısı k (kuru ~0.2, yağlı ~0.15)")
    c.add_argument("--n", type=pozitif_tam, default=1, help="Cıvata sayısı")
    c.add_argument("--mu", type=pozitif, default=0.15, help="Bağlantı yüzeyi sürtünmesi")
    c.add_argument("--yuzey", type=pozitif_tam, default=1, help="Sürtünme yüzeyi sayısı")
    c.add_argument("--alfa-a", type=pozitif, default=1.6,
                   help="Sıkma faktörü alfa_A (tork anahtarı ~1,6; darbeli tabanca ~2,5)")
    c.add_argument("--emniyet", type=pozitif, default=1.5,
                   help="Kaymaya karşı emniyet (statik ~1,2; titreşimli ~1,8)")
    c.add_argument("--yuk", type=pozitif, help="Etkiyen enine yük [N]")
    c.set_defaults(fonk=civata)

    s = alt.add_parser("pimkesme", help="Pim kesme ve yüzey basıncı")
    s.add_argument("--d", type=pozitif, required=True, help="Pim çapı [mm]")
    s.add_argument("--F", type=pozitif, required=True, help="Toplam enine kuvvet [N]")
    s.add_argument("--n", type=pozitif_tam, default=1, help="Pim sayısı")
    s.add_argument("--kesit", type=int, default=1, choices=[1, 2], help="Tek / çift kesme")
    s.add_argument("--tau-em", type=pozitif, default=150,
                   help="Emniyetli kesme [N/mm2] (sertleştirilmiş pim, darbeli yük için ~150)")
    s.add_argument("--t", type=pozitif, help="Delikteki temas boyu [mm]")
    s.add_argument("--p-em", type=pozitif, default=100,
                   help="Emniyetli yüzey basıncı [N/mm2] (S235 / S355 gövde, darbeli ~100)")
    s.set_defaults(fonk=pimkesme)

    a = ana.parse_args()
    a.fonk(a)


if __name__ == "__main__":
    main()
