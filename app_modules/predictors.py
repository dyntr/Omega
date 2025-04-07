import joblib
import pandas as pd
from app_modules.utils import je_svatek

model_nafta = joblib.load("models/model_nafta_optimized.pkl")
model_natural = joblib.load("models/model_natural_optimized.pkl")

def predikuj(okres, datum, ropa, usd):
    vikend = int(datum.weekday() >= 5)
    svatek = je_svatek(datum)
    df = pd.DataFrame([{
        "okres": okres,
        "svatek": svatek,
        "vikend": vikend,
        "cena_ropy": ropa,
        "usd": usd,
        "den": datum.day,
        "mesic": datum.month,
        "rok": datum.year
    }])
    nafta = round(float(model_nafta.predict(df)[0]), 2)
    natural = round(float(model_natural.predict(df)[0]), 2)
    return nafta, natural