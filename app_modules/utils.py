import requests, re
import pandas as pd
import holidays

cz_holidays = holidays.Czechia()

# Nacteni mapovani PSC -> okres
psc_na_okres = {}
df_psc = pd.read_csv("data/obce-psc.csv")
for _, row in df_psc.iterrows():
    okres = row["Okres"]
    for psc in str(row["PSČ"]).split(","):
        psc_na_okres[psc.strip()] = okres


def ziskej_psc_z_pozice(lat, lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&addressdetails=1"
        headers = {"User-Agent": "PalivaApp/1.0"}
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        if "address" in data and "postcode" in data["address"]:
            return data["address"]["postcode"].replace(" ", "")
        return None
    except Exception as e:
        print("[CHYBA ZÍSKÁNÍ PSČ]", e)
        return None


def ziskej_cenu_ropy():
    try:
        res = requests.get("https://data.kurzy.cz/json/komodity/id%5Bropa-brent%5Dden%5B30%5Dmena%5Bczk%5Dcb%5Bvypsat%5D.js")
        match = re.findall(r'"hodnota":([\d.]+)', res.text)
        return float(match[-1]) if match else None
    except:
        return None


def ziskej_kurz_usd():
    try:
        res = requests.get("https://api.cnb.cz/cnbapi/exrates/daily?lang=EN")
        for rate in res.json()["rates"]:
            if rate["currencyCode"] == "USD":
                return float(rate["rate"])
        return None
    except:
        return None


def je_svatek(datum):
    return int(datum in cz_holidays)
