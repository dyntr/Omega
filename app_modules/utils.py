import requests, re
import pandas as pd
import holidays

# Vytvoření seznamu státních svátků v Česku pomocí knihovny holidays
cz_holidays = holidays.Czechia()

# ⚠️ Načtení mapování PSČ na okresy – použito pro lokalizaci uživatele dle PSČ
psc_na_okres = {}
df_psc = pd.read_csv("data/obce-psc.csv")
for _, row in df_psc.iterrows():
    okres = row["Okres"]
    for psc in str(row["PSČ"]).split(","):
        psc_na_okres[psc.strip()] = okres  # Přiřadí každé PSČ správný okres

# 📍 Funkce získá PSČ z GPS souřadnic přes OpenStreetMap Nominatim API
def ziskej_psc_z_pozice(lat, lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&addressdetails=1"
        headers = {"User-Agent": "PalivaApp/1.0"}  # ⚠️ User-Agent je povinný pro korektní dotazování na Nominatim
        r = requests.get(url, headers=headers)
        r.raise_for_status()  # ⚠️ Vyhodí chybu, pokud server vrátí chybný stav
        data = r.json()
        if "address" in data and "postcode" in data["address"]:
            return data["address"]["postcode"].replace(" ", "")  # Odstraní mezery v PSČ
        return None
    except Exception as e:
        print("[CHYBA ZÍSKÁNÍ PSČ]", e)
        return None

# 🛢️ Funkce získá aktuální cenu ropy Brent v CZK ze serveru kurzy.cz
def ziskej_cenu_ropy():
    try:
        res = requests.get("https://data.kurzy.cz/json/komodity/id%5Bropa-brent%5Dden%5B30%5Dmena%5Bczk%5Dcb%5Bvypsat%5D.js")
        match = re.findall(r'"hodnota":([\d.]+)', res.text)  # Hledá hodnoty cen ve formátu "hodnota":xxx
        return float(match[-1]) if match else None  # ⚠️ Vrací poslední hodnotu, tj. nejnovější dostupnou cenu
    except:
        return None

# 💵 Funkce získá denní kurz USD z ČNB API
def ziskej_kurz_usd():
    try:
        res = requests.get("https://api.cnb.cz/cnbapi/exrates/daily?lang=EN")
        for rate in res.json()["rates"]:
            if rate["currencyCode"] == "USD":
                return float(rate["rate"])  # Vrací kurz USD
        return None
    except:
        return None

# 🗓️ Vrací 1 (true), pokud je dané datum svátkem
def je_svatek(datum):
    return int(datum in cz_holidays)

# 🔮 Hlavní predikční funkce – vypočítá cenu nafty a benzínu
def predikuj(okres, datum, ropa, usd):
    """
    Predikuje cenu nafty a benzínu na základě vstupních dat.
    """
    try:
        # 🧾 Připravíme vstupní proměnné pro model
        vstup = {
            "okres": okres,
            "datum": datum.isoformat(),  # Datum převedeno na text (např. "2025-04-07")
            "ropa": ropa,
            "usd": usd,
            "vikend": int(datum.weekday() >= 5),  # 1 pokud je sobota/neděle
            "svatek": je_svatek(datum)  # 1 pokud je svátek
        }

        # 📦 Načteme model z .pkl souboru
        import pickle
        with open("data/model.pkl", "rb") as f:
            model = pickle.load(f)

        # ⚠️ Model očekává jen číselné vstupy (v tomto pořadí)
        vstup_pro_model = [
            vstup["ropa"],
            vstup["usd"],
            vstup["vikend"],
            vstup["svatek"]
        ]

        # 🔮 Provede samotnou predikci pomocí modelu
        predikce = model.predict([vstup_pro_model])

        # 🟩 Předpokládáme, že model vrací dvojici [nafta, natural]
        nafta = predikce[0][0]
        natural = predikce[0][1]

        return nafta, natural
    except Exception as e:
        print("[CHYBA PREDIKCE]", e)
        return None, None  # Pokud se něco pokazí, vracíme None
