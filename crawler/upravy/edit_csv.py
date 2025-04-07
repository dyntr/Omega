import csv
from datetime import datetime

input_file = './okresy_updated.csv'
output_file = 'spojene_data.csv'  
svatek_file = './vikendy_a_svatky.csv' 
ropa_file = './ropa.csv' 
kurzy_file = './kurzy.csv' 

# Načtení dat o svátcích a víkendech do slovníku
svatek_vikend_data = {}
with open(svatek_file, mode='r', newline='', encoding='utf-8') as svatek_csv:
    svatek_reader = csv.DictReader(svatek_csv)
    for row in svatek_reader:
        svatek_vikend_data[row['datum']] = {
            'svatek': 'yes' if row['je_svatecni_den'] == 'True' else 'no',
            'vikend': 'yes' if row['je_vikend'] == 'True' else 'no'
        }

# Načtení dat o ropě do slovníku s propagací dat
ropa_data = {}
last_price = None
with open(ropa_file, mode='r', newline='', encoding='utf-8') as ropa_csv:
    ropa_reader = csv.DictReader(ropa_csv)
    for row in ropa_reader:
        date = row['den']
        price = row['hodnota']
        ropa_data[date] = price
        last_price = price
    # Propagate the last known price for missing dates
    for date in sorted(ropa_data.keys()):
        if ropa_data[date] is None:
            ropa_data[date] = last_price
        else:
            last_price = ropa_data[date]

# Načtení dat o kurzu USD do slovníku
usd_data = {}
with open(kurzy_file, mode='r', newline='', encoding='utf-8') as kurzy_csv:
    kurzy_reader = csv.DictReader(kurzy_csv)
    for row in kurzy_reader:
        usd_data[row['datum']] = row['hodnota']

with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
     open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = [field for field in reader.fieldnames if field not in ('zmena_95', 'zmena_naf')] + ['svatek', 'vikend', 'cena_ropy', 'usd']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in reader:
        # Odstranění nežádoucích sloupců
        row.pop('zmena_95', None)
        row.pop('zmena_naf', None)
        
        # Convert date format from DD.MM.YYYY to YYYY-MM-DD
        date_converted = datetime.strptime(row['datum'], '%d.%m.%Y').strftime('%Y-%m-%d')
        svatek_vikend = svatek_vikend_data.get(date_converted, {'svatek': 'no', 'vikend': 'no'})
        row['svatek'] = svatek_vikend['svatek']
        row['vikend'] = svatek_vikend['vikend']
        
        # Přidání ceny ropy
        row['cena_ropy'] = ropa_data.get(date_converted, last_price)  # Use the last known price if date not found
        
        # Přidání kurzu USD
        row['usd'] = usd_data.get(date_converted, 'N/A')  # Default to 'N/A' if no rate is found
        writer.writerow(row)