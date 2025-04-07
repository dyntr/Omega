from flask import request, jsonify, render_template
from app_modules.utils import *  # ⚠️ Import všech pomocných funkcí: získání PSČ, ceny ropy, kurzu USD, atd.
from app_modules.predictors import predikuj  # ✅ Import funkce, která provádí predikci pomocí ML modelu
import datetime

# ✅ Hlavní funkce, která zaregistruje všechny routy aplikace
def configure_routes(app):

    @app.route("/")
    def index():
        return render_template("index.html")  # 🏠 Vrací hlavní stránku aplikace

    @app.route("/documentation")
    def documentation():
        return render_template("documentation.html")  # 📚 Stránka s dokumentací

    @app.route("/api/predict", methods=["POST"])
    def predict():
        # ✅ Získání souřadnic z požadavku
        data = request.get_json()
        lat, lon = data.get("lat"), data.get("lon")

        # 🌍 Získání PSČ na základě souřadnic přes Nominatim API
        psc = ziskej_psc_z_pozice(lat, lon)
        okres = psc_na_okres.get(psc)  # Mapa PSČ na název okresu

        # 📅 Dnešní datum a externí ekonomická data
        today = datetime.date.today()
        ropa = ziskej_cenu_ropy()
        usd = ziskej_kurz_usd()

        # ⚠️ Kontrola úplnosti vstupních dat
        if not psc or not okres or ropa is None or usd is None:
            return jsonify({"error": "Chybí data pro predikci"}), 400

        # 🔮 Provede se predikce pro dnešní den
        nafta, natural = predikuj(okres, today, ropa, usd)

        # 📤 Vracíme výsledek ve formátu JSON
        return jsonify({
            "datum": today.isoformat(),
            "psc": psc,
            "okres": okres,
            "ropa": ropa,
            "usd": usd,
            "vikend": int(today.weekday() >= 5),
            "svatek": je_svatek(today),
            "nafta": nafta,
            "natural": natural
        })

    @app.route("/api/predict_future", methods=["POST"])
    def predict_future():
        # ✅ Získání vstupních dat z POST požadavku
        data = request.get_json()
        okres = data.get("okres")
        start_str, end_str = data.get("start"), data.get("end")
        typ_paliva = data.get("typ_paliva", "oboje")  # Defaultní hodnota: oboje paliva

        # 🧪 Převod dat na typ date
        try:
            start_date = datetime.datetime.strptime(start_str, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_str, "%Y-%m-%d").date()
        except:
            return jsonify({"error": "Neplatné datumy"}), 400

        # ⚠️ Ověření platnosti okresu
        if not okres or okres not in df_psc["Okres"].unique():
            return jsonify({"error": f"Neplatný okres: {okres}"}), 400

        # 📥 Načtení externích dat pro predikci
        ropa = ziskej_cenu_ropy()
        usd = ziskej_kurz_usd()

        if ropa is None or usd is None:
            return jsonify({"error": "Chybí data pro predikci"}), 400

        vysledky = []  # 📊 Seznam s denními predikcemi
        current = start_date

        # 🔁 Iterace přes všechny dny v rozsahu
        while current <= end_date:
            nafta, natural = predikuj(okres, current, ropa, usd)
            prediction = {"datum": current.isoformat()}
            if typ_paliva in ["nafta", "oboje"]:
                prediction["nafta"] = nafta
            if typ_paliva in ["natural", "oboje"]:
                prediction["natural"] = natural
            vysledky.append(prediction)
            current += datetime.timedelta(days=1)  # 📅 Posun na další den

        return jsonify({"okres": okres, "predictions": vysledky})  # 📤 Vrací seznam predikcí ve formátu JSON
