kartony = [
    ("XS", 169, 130, 70), ("S", 213, 153, 109), ("M", 260, 180, 150), ("L", 360, 240, 140),
    ("XL", 450, 320, 210), ("XXL", 600, 400, 340), ("KGS1", 80, 380, 600), ("KGS2", 500, 370, 120),
    ("KGS3", 80, 600, 600), ("KGS4", 190, 380, 600), ("KNC-1", 300, 200, 270), ("KNC-2", 210, 180, 140),
    ("KNC-3", 300, 200, 405), ("KNC-4", 400, 300, 400), ("KNC-5", 295, 165, 310), ("KNC-6", 395, 200, 405),
    ("KNC-7", 300, 180, 200), ("KNC-8", 400, 300, 150), ("KNC-9", 486, 356, 379), ("Rollbox M", 300, 210, 80),
    ("Rollbox L", 330, 230, 100)
]
karton_ceny = {"XS":0.72, "S":0.82, "M":1.26, "L":1.70, "XL":2.50, "XXL":3.50, "KGS1":2.00, "KGS2":2.40,
    "KGS3":2.90, "KGS4":2.50, "KNC-1":1.80, "KNC-2":1.10, "KNC-3":2.80, "KNC-4":3.00, "KNC-5":1.30,
    "KNC-6":2.90, "KNC-7":1.40, "KNC-8":2.00, "KNC-9":3.80, "Rollbox M":1.00, "Rollbox L":1.20
}
koperty = [("A1", 175, 120), ("C3", 225, 170), ("D4", 275, 200), ("F6", 350, 240), ("K10", 490, 370)]
koperta_ceny = {"A1":0.14, "C3":0.18, "D4":0.20, "F6":0.25, "K10":0.29}
foliopaki = [("Mały", 300, 400), ("Średni", 350, 450), ("Duży", 450, 550), ("XXL", 500, 850)]
foliopak_ceny = {"Mały":0.23, "Średni":0.27, "Duży":0.39, "XXL":0.49}

def znajdz_karton(dl, sz, wys):
    for n, d, s, w in kartony:
        if dl <= d and sz <= s and wys <= w:
            return n, karton_ceny.get(n,0)
    return "BRAK", 0

def znajdz_koperta(dl, sz):
    for n, d, s in koperty:
        if dl <= d and sz <= s:
            return n, koperta_ceny.get(n,0)
    return "BRAK", 0

def znajdz_foliopak(dl, sz):
    for n, d, s in foliopaki:
        if dl <= d and sz <= s:
            return n, foliopak_ceny.get(n,0)
    return "BRAK", 0

def kalkulator_pakowania():
    koszt_otwarcia = 2.40
    lista_sku = []
    liczba_sku = int(input("Ile różnych SKU w zamówieniu? "))
    laczna_sztuk = 0
    suma_dl = 0
    max_sz = 0
    max_wys = 0
    for i in range(liczba_sku):
        print(f"\n--- SKU {i+1} ---")
        sztuk = int(input(f"Liczba sztuk tego SKU: "))
        dlugosc = float(input(f"Długość produktu (mm): "))
        szerokosc = float(input(f"Szerokość produktu (mm): "))
        wysokosc = float(input(f"Wysokość produktu (mm): "))
        laczna_sztuk += sztuk
        suma_dl += dlugosc * sztuk
        max_sz = max(max_sz, szerokosc)
        max_wys = max(max_wys, wysokosc)
    koszt_kompletacji = 0.76 + 0.39 * laczna_sztuk
    suma_procesowania = koszt_otwarcia + koszt_kompletacji

    # Pakowanie
    koszt_opakowania = 0
    info_opak = ""
    czy_karton = input("Czy pakować w karton? (t/n): ").strip().lower()
    if czy_karton == 't':
        typ_kartonu, koszt_kartonu = znajdz_karton(suma_dl, max_sz, max_wys)
        if typ_kartonu == "BRAK":
            print("\nProdukt nie mieści się do żadnego kartonu standardowego.")
            dwa_xxl = input("Czy pakować w 2 największe kartony XXL? (t/n): ").strip().lower()
            if dwa_xxl == 't':
                koszt_opakowania = 2 * karton_ceny["XXL"]
                info_opak = "2x Karton XXL"
            else:
                paleta = input("Czy pakować na palecie? (t/n): ").strip().lower()
                if paleta == 't':
                    typ_palety = input("Paleta jednorazowa za 28,33 zł (wpisz 1) czy EURO za 76,67 zł (wpisz 2)?: ").strip()
                    if typ_palety == "1":
                        koszt_opakowania = 28.33
                        info_opak = "Paleta jednorazowa"
                    elif typ_palety == "2":
                        koszt_opakowania = 76.67
                        info_opak = "Paleta EURO"
                    # Dodaj opłatę za wydaną paletę oraz wydanie+foliowanie:
                    koszt_opakowania += 5.00 + 6.46
                    info_opak += " + wydanie palety + wydanie i foliowanie palety"
                else:
                    info_opak = "BRAK możliwości pakowania"
        else:
            koszt_opakowania = koszt_kartonu
            info_opak = f"Karton: {typ_kartonu}"
        print(f"Wybrano: {info_opak}. Koszt: {koszt_opakowania:.2f} zł")
    else:
        czy_foliopak = input("Czy pakować w foliopak? (t/n): ").strip().lower()
        if czy_foliopak == 't':
            typ_foliopaka, koszt_foliopaka = znajdz_foliopak(suma_dl, max_sz)
            koszt_opakowania = koszt_foliopaka
            info_opak = f"Foliopak: {typ_foliopaka}"
            print(f"Wybrano foliopak: {typ_foliopaka} (koszt: {koszt_foliopaka:.2f} zł za całość)")
        else:
            typ_koperty, koszt_koperty = znajdz_koperta(suma_dl, max_sz)
            koszt_opakowania = koszt_koperty
            info_opak = f"Koperta: {typ_koperty}"
            print(f"Wybrano kopertę bąbelkową: {typ_koperty} (koszt: {koszt_koperty:.2f} zł za całość)")

    # Dodatki
    zabezpieczenie = 0
    print("Czy zabezpieczać poduszkami powietrznymi? (t/n)")
    if input().strip().lower() == 't': zabezpieczenie += 0.70
    print("Czy zabezpieczać papierem miętym? (t/n)")
    if input().strip().lower() == 't': zabezpieczenie += 0.70
    print("Czy zabezpieczać matami powietrznymi? (t/n)")
    if input().strip().lower() == 't': zabezpieczenie += 0.70
    print("Czy owijać folią stretch za 1 zł od paczki? (t/n)")
    if input().strip().lower() == 't': zabezpieczenie += 1.0

    suma_calkowita = suma_procesowania + koszt_opakowania + zabezpieczenie

    print(f"\n--- PODSUMOWANIE ---")
    print(f"Suma za procesowanie zamówienia: {suma_procesowania:.2f} zł (otwarcie {koszt_otwarcia:.2f} zł + kompletacja {koszt_kompletacji:.2f} zł)")
    print(f"Suma za opakowanie: {koszt_opakowania:.2f} zł ({info_opak})")
    print(f"Suma za zabezpieczenia: {zabezpieczenie:.2f} zł")
    print(f"Suma całkowita zamówienia: {suma_calkowita:.2f} zł")

kalkulator_pakowania()
