from flask import request, jsonify, render_template
from app_modules.utils import *
from app_modules.predictors import predikuj
import datetime

def configure_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/predict", methods=["POST"])
    def predict():
        data = request.get_json()
        lat, lon = data.get("lat"), data.get("lon")
        psc = ziskej_psc_z_pozice(lat, lon)
        okres = psc_na_okres.get(psc)

        today = datetime.date.today()
        ropa = ziskej_cenu_ropy()
        usd = ziskej_kurz_usd()

        if not psc or not okres or ropa is None or usd is None:
            return jsonify({"error": "Chybí data pro predikci"}), 400

        nafta, natural = predikuj(okres, today, ropa, usd)

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
        data = request.get_json()
        okres = data.get("okres")
        start_str, end_str = data.get("start"), data.get("end")

        try:
            start_date = datetime.datetime.strptime(start_str, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_str, "%Y-%m-%d").date()
        except:
            return jsonify({"error": "Neplatné datumy"}), 400

        if not okres or okres not in df_psc["Okres"].unique():
            return jsonify({"error": "Neplatný okres"}), 400

        ropa = ziskej_cenu_ropy()
        usd = ziskej_kurz_usd()

        vysledky = []
        current = start_date
        while current <= end_date:
            nafta, natural = predikuj(okres, current, ropa, usd)
            vysledky.append({
                "datum": current.isoformat(),
                "nafta": nafta,
                "natural": natural
            })
            current += datetime.timedelta(days=1)

        return jsonify({"okres": okres, "predictions": vysledky})

