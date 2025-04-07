import requests
import csv

def fetch_and_save_to_csv(api_url, output_csv):
    """
    Načte data z dané API URL a uloží je do CSV souboru.

    Argumenty:
        api_url (str): URL API, ze kterého se mají data načíst.
        output_csv (str): Název výstupního CSV souboru.
    """
    try:
        # Fetch data from the API
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()

        # Extract the relevant data
        rows = data.get("data", [])
        if not rows:
            print("No data found in the API response.")
            return

        # Write data to a CSV file
        with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(["den", "mena", "hodnota"])
            # Write rows
            for row in rows:
                writer.writerow([row["den"], row["mena"], row["hodnota"]])

        print(f"Data successfully saved to {output_csv}.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    """
    Vstupní bod pro skript Ropa crawleru.
    """
    api_url = "https://data.kurzy.cz/json/komodity/id[ropa-brent]den[5572]mena[czk]"
    output_csv = "ropa.csv"
    fetch_and_save_to_csv(api_url, output_csv)
