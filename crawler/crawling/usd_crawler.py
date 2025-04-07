import requests
import csv
from datetime import datetime, timedelta

def fetch_usd_kurz(date):
    """
    Načte kurz USD pro dané datum.

    Argumenty:
        date (str): Datum ve formátu YYYYMMDD.

    Návratová hodnota:
        float nebo None: Kurz USD nebo None, pokud nebyl nalezen.
    """
    url = f"https://data.kurzy.cz/json/meny/b[2]den[{date}].json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        usd_data = data.get("kurzy", {}).get("USD", {})
        return usd_data.get("dev_stred") 
    return None

def save_to_csv(date, usd_kurz):
    """
    Uloží kurz USD do CSV souboru.

    Argumenty:
        date (str): Datum ve formátu YYYYMMDD.
        usd_kurz (float): Kurz USD.
    """
    file_name = "kurzy.csv"
    file_exists = False
    try:
        with open(file_name, "r"):
            file_exists = True
    except FileNotFoundError:
        pass


    formatted_date = datetime.strptime(date, "%Y%m%d").strftime("%Y-%m-%d")

    with open(file_name, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "USD_Kurz"])  
        writer.writerow([formatted_date, usd_kurz])  

def main():
    """
    Načte a uloží kurzy USD pro všechna data od 1. 1. 2010 do dnešního dne.
    """
    start_date = datetime(2010, 1, 1)
    end_date = datetime.now()
    current_date = start_date

    while current_date <= end_date:
        date_str = current_date.strftime("%Y%m%d")
        usd_kurz = fetch_usd_kurz(date_str)
        if usd_kurz is not None:
            save_to_csv(date_str, usd_kurz)  
        current_date += timedelta(days=1)

if __name__ == "__main__":
    """
    Vstupní bod pro skript USD crawleru.
    """
    main()
