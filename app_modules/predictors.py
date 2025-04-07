import joblib
import pandas as pd
from app_modules.utils import je_svatek  # ✅ Import funkce, která zjistí, zda je daný den státní svátek v ČR

# ⚠️ Načtení dvou oddělených modelů: jeden pro naftu, druhý pro benzín (natural)
model_nafta = joblib.load("models/model_nafta_optimized.pkl")
model_natural = joblib.load("models/model_natural_optimized.pkl")

# 🔮 Funkce, která přijímá vstupní data a vrací predikované ceny nafty a benzínu
def predikuj(okres, datum, ropa, usd):
    vikend = int(datum.weekday() >= 5)  # ✅ 1 = sobota/neděle, 0 = pracovní den
    svatek = je_svatek(datum)           # ✅ 1 = svátek, 0 = běžný den

    # 📄 Vytvoření vstupního dataframe pro modely – jeden řádek s požadovanými sloupci
    df = pd.DataFrame([{
        "okres": okres,            # název okresu (kategorická proměnná)
        "svatek": svatek,          # binární příznak (0/1)
        "vikend": vikend,          # binární příznak (0/1)
        "cena_ropy": ropa,         # cena ropy v CZK
        "usd": usd,                # kurz USD vůči CZK
        "den": datum.day,          # den v měsíci (1–31)
        "mesic": datum.month,      # měsíc (1–12)
        "rok": datum.year          # rok (např. 2025)
    }])

    # 🧠 Použití modelů k predikci – výstup je pole s jednou hodnotou → konverze na float a zaokrouhlení
    nafta = round(float(model_nafta.predict(df)[0]), 2)
    natural = round(float(model_natural.predict(df)[0]), 2)

    return nafta, natural  # ✅ Vrací tuple s predikcí ceny nafty a benzínu (např. 36.25, 37.80)
