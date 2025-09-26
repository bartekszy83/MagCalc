import streamlit as st

kartony = [
    ("XS", 169, 130, 70), ("S", 213, 153, 109), ("M", 260, 180, 150), ("L", 360, 240, 140),
    ("XL", 450, 320, 210), ("XXL", 600, 400, 340), ("KGS1", 80, 380, 600), ("KGS2", 500, 370, 120),
    ("KGS3", 80, 600, 600), ("KGS4", 190, 380, 600), ("KNC-1", 300, 200, 270), ("KNC-2", 210, 180, 140),
    ("KNC-3", 300, 200, 405), ("KNC-4", 400, 300, 400), ("KNC-5", 295, 165, 310), ("KNC-6", 395, 200, 405),
    ("KNC-7", 300, 180, 200), ("KNC-8", 400, 300, 150), ("KNC-9", 486, 356, 379), ("Rollbox M", 300, 210, 80),
    ("Rollbox L", 330, 230, 100)
]
karton_ceny = {
    "XS": 0.72, "S": 0.82, "M": 1.26, "L": 1.70, "XL": 2.50, "XXL": 3.50, "KGS1": 2.00, "KGS2": 2.40,
    "KGS3": 2.90, "KGS4": 2.50, "KNC-1": 1.80, "KNC-2": 1.10, "KNC-3": 2.80, "KNC-4": 3.00,
    "KNC-5": 1.30, "KNC-6": 2.90, "KNC-7": 1.40, "KNC-8": 2.00, "KNC-9": 3.80, "Rollbox M": 1.00, "Rollbox L": 1.20
}
koperty = [
    ("A1", 175, 120), ("C3", 225, 170), ("D4", 275, 200), ("F6", 350, 240), ("K10", 490, 370)
]
koperta_ceny = {
    "A1": 0.14, "C3": 0.18, "D4": 0.20, "F6": 0.25, "K10": 0.29
}
foliopaki = [
    ("Mały", 300, 400), ("Średni", 350, 450), ("Duży", 450, 550), ("XXL", 500, 850)
]
foliopak_ceny = {
    "Mały": 0.23, "Średni": 0.27, "Duży": 0.39, "XXL": 0.49
}

def znajdz_karton(dl, sz, wys):
    for n, d, s, w in kartony:
        if dl <= d and sz <= s and wys <= w:
            return n, karton_ceny.get(n, 0)
    return "BRAK", 0

def znajdz_koperta(dl, sz):
    for n, d, s in koperty:
        if dl <= d and sz <= s:
            return n, koperta_ceny.get(n, 0)
    return "BRAK", 0

def znajdz_foliopak(dl, sz):
    for n, d, s in foliopaki:
        if dl <= d and sz <= s:
            return n, foliopak_ceny.get(n, 0)
    return "BRAK", 0

def main():
    st.title("MagCalc - Kalkulator Pakowania i Kosztów")

    koszt_otwarcia = 2.40

    liczba_sku = st.number_input("Ile różnych SKU w zamówieniu?", min_value=1, step=1)
    laczna_sztuk = 0
    suma_dl = 0
    max_sz = 0
    max_wys = 0

    for i in range(int(liczba_sku)):
        st.subheader(f"SKU {i + 1}")
        sztuk = st.number_input(f"Liczba sztuk SKU {i + 1}:", min_value=1, step=1, key=f"sztuki{i}")
        dlugosc = st.number_input(f"Długość produktu SKU {i + 1} (mm):", min_value=1.0, step=1.0, key=f"dlugosc{i}")
        szerokosc = st.number_input(f"Szerokość produktu SKU {i + 1} (mm):", min_value=1.0, step=1.0, key=f"szerokosc{i}")
        wysokosc = st.number_input(f"Wysokość produktu SKU {i + 1} (mm):", min_value=1.0, step=1.0, key=f"wysokosc{i}")

        laczna_sztuk += sztuk
        suma_dl += dlugosc * sztuk
        max_sz = max(max_sz, szerokosc)
        max_wys = max(max_wys, wysokosc)

    koszt_kompletacji = 0.76 + 0.39 * laczna_sztuk
    suma_procesowania = koszt_otwarcia + koszt_kompletacji

    czy_karton = st.radio("Czy pakować w karton?", ("Tak", "Nie"))

    koszt_opakowania = 0
    info_opak = ""

    if czy_karton == "Tak":
        typ_kartonu, koszt_kartonu = znajdz_karton(suma_dl, max_sz, max_wys)
        if typ_kartonu == "BRAK":
            st.warning("Produkt nie mieści się do żadnego kartonu standardowego.")
            dwa_xxl = st.radio("Czy pakować w 2 największe kartony XXL?", ("Tak", "Nie"))
            if dwa_xxl == "Tak":
                koszt_opakowania = 2 * karton_ceny["XXL"]
                info_opak = "2x Karton XXL"
            else:
                paleta = st.radio("Czy pakować na palecie?", ("Tak", "Nie"))
                if paleta == "Tak":
                    typ_palety = st.radio(
                        "Paleta jednorazowa za 28,33 zł czy EURO za 76,67 zł?",
                        ("Jednorazowa", "EURO"),
                    )
                    if typ_palety == "Jednorazowa":
                        koszt_opakowania = 28.33
                        info_opak = "Paleta jednorazowa"
                    else:
                        koszt_opakowania = 76.67
                        info_opak = "Paleta EURO"
                    koszt_opakowania += 5.00 + 6.46
                    info_opak += " + wydanie palety + foliowanie"
                else:
                    info_opak = "BRAK możliwości pakowania"
                    koszt_opakowania = 0
        else:
            koszt_opakowania = koszt_kartonu
            info_opak = f"Karton: {typ_kartonu}"
    else:
        czy_foliopak = st.radio("Czy pakować w foliopak?", ("Tak", "Nie"))
        if czy_foliopak == "Tak":
            typ_foliopaka, koszt_foliopaka = znajdz_foliopak(suma_dl, max_sz)
            koszt_opakowania = koszt_foliopaka
            info_opak = f"Foliopak: {typ_foliopaka}"
        else:
            typ_koperty, koszt_koperty = znajdz_koperta(suma_dl, max_sz)
            koszt_opakowania = koszt_koperty
            info_opak = f"Koperta: {typ_koperty}"

    zabezpieczenie = 0
    if st.checkbox("Zabezpieczać poduszkami powietrznymi (0,70 zł)"):
        zabezpieczenie += 0.70
    if st.checkbox("Zabezpieczać papierem miętym (0,70 zł)"):
        zabezpieczenie += 0.70
    if st.checkbox("Zabezpieczać matami powietrznymi (0,70 zł)"):
        zabezpieczenie += 0.70
    if st.checkbox("Owijać folią stretch (1 zł)"):
        zabezpieczenie += 1.00

    suma_calkowita = suma_procesowania + koszt_opakowania + zabezpieczenie

    st.subheader("Podsumowanie")
    st.write(f"Suma za procesowanie zamówienia: {suma_procesowania:.2f} zł ({koszt_otwarcia:.2f} otwarcie + {koszt_kompletacji:.2f} kompletacja)")
    st.write(f"Suma za opakowanie: {koszt_opakowania:.2f} zł ({info_opak})")
    st.write(f"Suma za zabezpieczenia: {zabezpieczenie:.2f} zł")
    st.write(f"Suma całkowita: {suma_calkowita:.2f} zł")

if __name__ == "__main__":
    main()
