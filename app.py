from flask import Flask  # ⚠️ Importuje se třída Flask z knihovny Flask – základ pro spuštění webové aplikace

from app_modules.routes import configure_routes  # ⚠️ Importuje se vlastní funkce pro nastavení rout (adres URL) – musí být správně definovaná, jinak aplikace spadne

app = Flask(__name__)  # ✅ Vytváří se instance aplikace – Flask potřebuje vědět, odkud se spouští (__name__) kvůli správnému načítání cest a souborů

configure_routes(app)  # ✅ Spustí se funkce, která přidá do aplikace jednotlivé cesty (např. /home, /about), aby věděla, co má dělat při různých URL

if __name__ == "__main__":  # ✅ Tímto se kontroluje, jestli se tento soubor spustil přímo (nebyl jen importován jinam)
    app.run(debug=True, port=5500)  # ⚠️ Spustí se vývojový server na portu 5500, s debug režimem (zobrazí chyby v prohlížeči – ne
