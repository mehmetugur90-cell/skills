#!/usr/bin/env python3
"""Fikstür tasarımı için mühendislik hesapları.

Alt komutlar:
  kenet      Talaşlı işlemede gereken kenetleme kuvveti (Kienzle + sürtünme)
  pim        İki pimli konumlama: boşluk, konum hatası, elmas pim genişliği
  civata     Cıvata ön yükü, sıkma torku ve kaymaya karşı taşıma kapasitesi
  pimkesme   Pim kesme gerilmesi ve delik yüzey basıncı

Tüm birimler: mm, N, N/mm2 (MPa), Nm. Çıktı Türkçedir.
Sonuçlar ön boyutlandırma içindir; kritik bağlantılarda standart hesap
(VDI 2230, DIN 743 vb.) ve üretici katalog değerleri esas alınır.
"""

import argparse
import math
import sys

# Kienzle katsayıları: kc1.1 [N/mm2], mc [-]. Literatürde sık geçen tipik
# tablo değerleri. Takım aşınması ve negatif talaş açısı kuvveti artırır.
KIENZLE = {
    "s235": (1780, 0.17),
    "s355": (1990, 0.26),
    "c45": (2220, 0.14),
    "42crmo4": (2500, 0.26),
    "hardox400": (2900, 0.25),
    "gg25": (1160, 0.26),
    "ggg50": (1500, 0.25),
    "aluminyum": (700, 0.25),
}

# Metrik kaba diş gerilme kesiti As [mm2] ve hatve P [mm]
CIVATA = {
    5: (14.2, 0.8),
    6: (20.1, 1.0),
    8: (36.6, 1.25),
    10: (58.0, 1.5),
    12: (84.3, 1.75),
    14: (115.0, 2.0),
    16: (157.0, 2.0),
    20: (245.0, 2.5),
    24: (353.0, 3.0),
    30: (561.0, 3.5),
}

# Akma sınırı Rp0.2 [N/mm2] (ISO 898-1)
SINIF = {"8.8": 640, "10.9": 940, "12.9": 1100}


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
        satir("Kesme kuvveti (girilen)", f"{fc:.0f}", "N")
    else:
        if a.b is None or a.h is None:
            sys.exit("Hata: --fc ya da --b ve --h birlikte verilmeli.")
        if a.kc11 is not None and a.mc is not None:
            kc11, mc = a.kc11, a.mc
            kaynak = "girilen"
        else:
            if a.malzeme not in KIENZLE:
                sys.exit(f"Hata: malzeme bilinmiyor. Seçenekler: {', '.join(KIENZLE)}")
            kc11, mc = KIENZLE[a.malzeme]
            kaynak = f"tablo: {a.malzeme}"
        kc = kc11 * a.h ** (-mc)
        fc = a.b * a.h ** (1 - mc) * kc11 * a.duzeltme
        satir(f"kc1.1 / mc ({kaynak})", f"{kc11} / {mc}")
        satir("Talaş genişliği b / kalınlığı h", f"{a.b} / {a.h}", "mm")
        satir("Özgül kesme kuvveti kc", f"{kc:.0f}", "N/mm2")
        satir("Düzeltme katsayısı (aşınma, talaş açısı)", f"{a.duzeltme}")
        satir("Kesme kuvveti Fc = b * h^(1-mc) * kc1.1", f"{fc:.0f}", "N")

    k = a.emniyet
    baslik("Gereken kenetleme kuvveti")
    if a.durum == "surtunme":
        mu = a.mu1 + a.mu2
        ftop = k * fc / mu
        satir("Durum", "kuvvet bağlama düzleminde, yalnızca sürtünme tutuyor")
        satir("Sürtünme mu1 (kenet-parça) + mu2 (parça-dayama)", f"{a.mu1} + {a.mu2}")
        satir("Toplam kenet kuvveti = K * Fc / (mu1 + mu2)", f"{ftop:.0f}", "N")
    elif a.durum == "kaldirma":
        ftop = k * fc
        satir("Durum", "kuvvet parçayı dayamadan uzaklaştırıyor")
        satir("Toplam kenet kuvveti = K * Fc", f"{ftop:.0f}", "N")
    else:  # dayamaya
        ftop = k * fc * a.mu1  # yalnızca titreşim ve kaymaya karşı küçük bir pay
        satir("Durum", "kuvvet parçayı sabit dayamaya itiyor")
        satir("Not", "kuvveti dayama karşılar; kenet konumu korur")
        satir("Önerilen alt sınır = K * Fc * mu1", f"{ftop:.0f}", "N")
        print("  Uyarı: dayamanın kendisi ve bağlantısı Fc için ayrıca kontrol edilmeli.")
    satir("Emniyet katsayısı K", f"{k}")
    satir("Kenet sayısı", f"{a.n}")
    satir("Kenet başına kuvvet", f"{ftop / a.n:.0f}", "N")
    satir("Kenet başına kuvvet", f"{ftop / a.n / 9.81:.0f}", "kgf")
    print("\n  Hızlı kenet seçerken katalogdaki 'tutma kuvveti' (holding capacity)")
    print("  değil, 'sıkma kuvveti' (clamping force) değeri bu sonuçla karşılaştırılmalı.")


# ---------------------------------------------------------------- pim
def pim(a):
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
    if delta <= 0:
        print("  Merkez mesafesi sapması sıfır, elmas pim hesabı gerekmez.")
    else:
        R = a.D2[0] / 2
        r = a.d2[1] / 2
        bmax = (R * R - r * r - delta * delta) / delta
        if bmax <= 0:
            print("  UYARI: bu boşlukla hiçbir elmas pim genişliği yeterli değil.")
            print("  Boşluğu artır ya da merkez mesafesi toleransını daralt.")
        else:
            satir("Maksimum silindirik yüzey genişliği b", f"{bmax:.2f}", "mm")
            satir("Yaklaşık formül b = D*c/(2*delta)",
                  f"{a.D2[0] * c2min / (2 * delta):.2f}", "mm")
            print("  Not: b, merkez doğrultusuna dik yerleştirilir. Çok küçük b (< 1,5 mm)")
            print("  hızlı aşınır; katalog elmas pimlerinin b değeriyle karşılaştır.")

    baslik("Konumlama hatası (en kötü durum)")
    oteleme = c1max / 2
    donme = math.atan((c1max / 2 + c2max / 2) / a.L)
    satir("Öteleme (1. pim ekseninde, her yönde)", f"+-{oteleme:.3f}", "mm")
    satir("Dönme açısı", f"+-{math.degrees(donme) * 60:.2f}", "dakika (')")
    if a.uzaklik:
        satir(f"Dönmenin {a.uzaklik} mm uzaktaki etkisi",
              f"+-{a.uzaklik * math.tan(donme):.3f}", "mm")


# ---------------------------------------------------------------- civata
def civata(a):
    if a.M not in CIVATA:
        sys.exit(f"Hata: M{a.M} tabloda yok. Seçenekler: {sorted(CIVATA)}")
    if a.sinif not in SINIF:
        sys.exit(f"Hata: sınıf bilinmiyor. Seçenekler: {', '.join(SINIF)}")
    As, P = CIVATA[a.M]
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
        satir("Ön yük hedefi (akmanın %70'i)", "")
        satir("Önerilen sıkma torku T = K * F * d", f"{tork:.0f}", "Nm")
    gerilme = fv / As
    satir("Tork katsayısı K", f"{a.k}")
    satir("Ön yük F", f"{fv / 1000:.1f}", "kN")
    satir("Gerilme / akma oranı", f"{gerilme:.0f} N/mm2  (%{gerilme / rp * 100:.0f})")
    if gerilme > 0.9 * rp:
        print("  UYARI: ön yük akmanın %90'ını aşıyor, torku düşür.")

    baslik("Kaymaya karşı kapasite (sürtünmeli bağlantı)")
    kap = a.n * fv * a.mu * a.yuzey / a.emniyet
    satir("Cıvata sayısı / sürtünme yüzeyi sayısı", f"{a.n} / {a.yuzey}")
    satir("Sürtünme katsayısı mu / emniyet", f"{a.mu} / {a.emniyet}")
    satir("Taşınabilir enine yük", f"{kap / 1000:.1f}", "kN")
    if a.yuk is not None:
        satir("Etkiyen enine yük", f"{a.yuk / 1000:.1f}", "kN")
        satir("Sonuç", "YETERLİ" if kap >= a.yuk else "YETERSİZ: pim ekle veya cıvatayı büyüt")
    print("  Not: konumlama hassasiyeti cıvataya değil pime verilmeli; cıvata deliği boşluklu.")


# ---------------------------------------------------------------- pimkesme
def pimkesme(a):
    alan = math.pi * a.d ** 2 / 4
    tau = a.F / (a.n * a.kesit * alan)
    baslik(f"Pim Ø{a.d} kesme kontrolü")
    satir("Pim sayısı / kesme yüzeyi", f"{a.n} / {a.kesit}")
    satir("Kesme gerilmesi", f"{tau:.0f}", "N/mm2")
    satir("Emniyetli kesme gerilmesi", f"{a.tau_em}", "N/mm2")
    satir("Sonuç", "YETERLİ" if tau <= a.tau_em else "YETERSİZ")
    if a.t:
        p = a.F / (a.n * a.d * a.t)
        baslik("Delik yüzey basıncı")
        satir("Temas boyu t", f"{a.t}", "mm")
        satir("Yüzey basıncı p = F / (n * d * t)", f"{p:.0f}", "N/mm2")
        satir("Emniyetli yüzey basıncı", f"{a.p_em}", "N/mm2")
        satir("Sonuç", "YETERLİ" if p <= a.p_em else "YETERSİZ")


def main():
    ana = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    alt = ana.add_subparsers(dest="komut", required=True)

    k = alt.add_parser("kenet", help="Talaşlı işleme kenetleme kuvveti")
    k.add_argument("--fc", type=float, help="Kesme kuvveti biliniyorsa [N]")
    k.add_argument("--malzeme", default="s355", help=f"Kienzle tablosu: {', '.join(KIENZLE)}")
    k.add_argument("--kc11", type=float, help="kc1.1 [N/mm2] (tablo yerine)")
    k.add_argument("--mc", type=float, help="mc [-] (tablo yerine)")
    k.add_argument("--b", type=float, help="Talaş genişliği [mm] (tornada ap/sin(kappa))")
    k.add_argument("--h", type=float, help="Talaş kalınlığı [mm] (frezede ortalama hm)")
    k.add_argument("--duzeltme", type=float, default=1.3,
                   help="Aşınma ve talaş açısı düzeltmesi (varsayılan 1.3)")
    k.add_argument("--durum", choices=["surtunme", "kaldirma", "dayamaya"], default="surtunme")
    k.add_argument("--mu1", type=float, default=0.12, help="Kenet-parça sürtünmesi")
    k.add_argument("--mu2", type=float, default=0.12, help="Parça-dayama sürtünmesi")
    k.add_argument("--emniyet", type=float, default=2.0, help="Emniyet katsayısı K")
    k.add_argument("--n", type=int, default=1, help="Kenet sayısı")
    k.set_defaults(fonk=kenet)

    p = alt.add_parser("pim", help="İki pimli konumlama")
    p.add_argument("--D1", type=float, nargs=2, required=True, metavar=("MIN", "MAX"),
                   help="1. delik çapı min max")
    p.add_argument("--d1", type=float, nargs=2, required=True, metavar=("MIN", "MAX"),
                   help="1. pim (silindirik) çapı min max")
    p.add_argument("--D2", type=float, nargs=2, required=True, metavar=("MIN", "MAX"))
    p.add_argument("--d2", type=float, nargs=2, required=True, metavar=("MIN", "MAX"))
    p.add_argument("--L", type=float, required=True, help="Delikler arası mesafe [mm]")
    p.add_argument("--tp", type=float, required=True, help="Parça merkez mesafesi toleransı +- [mm]")
    p.add_argument("--tf", type=float, default=0.01, help="Fikstür pim mesafesi toleransı +- [mm]")
    p.add_argument("--uzaklik", type=float, help="Dönme etkisinin bakılacağı mesafe [mm]")
    p.set_defaults(fonk=pim)

    c = alt.add_parser("civata", help="Cıvata ön yükü ve kayma kapasitesi")
    c.add_argument("--M", type=int, required=True, help="Nominal çap, ör. 12")
    c.add_argument("--sinif", default="8.8")
    c.add_argument("--tork", type=float, help="Uygulanan tork [Nm] (yoksa önerilir)")
    c.add_argument("--k", type=float, default=0.2, help="Tork katsayısı (kuru ~0.2, yağlı ~0.15)")
    c.add_argument("--n", type=int, default=1, help="Cıvata sayısı")
    c.add_argument("--mu", type=float, default=0.15, help="Bağlantı yüzeyi sürtünmesi")
    c.add_argument("--yuzey", type=int, default=1, help="Sürtünme yüzeyi sayısı")
    c.add_argument("--emniyet", type=float, default=1.5)
    c.add_argument("--yuk", type=float, help="Etkiyen enine yük [N]")
    c.set_defaults(fonk=civata)

    s = alt.add_parser("pimkesme", help="Pim kesme ve yüzey basıncı")
    s.add_argument("--d", type=float, required=True, help="Pim çapı [mm]")
    s.add_argument("--F", type=float, required=True, help="Toplam enine kuvvet [N]")
    s.add_argument("--n", type=int, default=1, help="Pim sayısı")
    s.add_argument("--kesit", type=int, default=1, choices=[1, 2], help="Tek / çift kesme")
    s.add_argument("--tau-em", type=float, default=150,
                   help="Emniyetli kesme [N/mm2] (sertleştirilmiş pim, darbeli yük için ~150)")
    s.add_argument("--t", type=float, help="Delikteki temas boyu [mm]")
    s.add_argument("--p-em", type=float, default=100,
                   help="Emniyetli yüzey basıncı [N/mm2] (S235 / S355 gövde, darbeli ~100)")
    s.set_defaults(fonk=pimkesme)

    a = ana.parse_args()
    a.fonk(a)


if __name__ == "__main__":
    main()
