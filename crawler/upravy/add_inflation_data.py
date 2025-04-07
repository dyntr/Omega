import pandas as pd

# Dictionary s daty o inflaci (rok -> míra inflace)
inflation_rates = {
    2000: 3.9,  2001: 4.7,  2002: 1.8,  2003: 0.1,  2004: 2.8,  2005: 1.9,
    2006: 2.5,  2007: 2.8,  2008: 6.3,  2009: 1.0,  2010: 1.5,  2011: 1.9,
    2012: 3.3,  2013: 1.4,  2014: 0.4,  2015: 0.3,  2016: 0.7,  2017: 2.5,
    2018: 2.1,  2019: 2.8,  2020: 3.2,  2021: 3.8,  2022: 15.1, 2023: 10.7,
    2024: 2.4
}

# Získání cesty k souboru od uživatele
file_path = './spojene_data_cleaned.csv'  # Nahraďte požadovanou cestou k vstupnímu souboru
# Načtení CSV souboru
df = pd.read_csv(file_path)

# Převod 'datum' na datetime a extrakce roku
df['datum'] = pd.to_datetime(df['datum'], format='%d.%m.%Y')
df['year'] = df['datum'].dt.year

# Mapování roční inflace na jednotlivé řádky
df['yearly_inflation'] = df['year'].map(inflation_rates)

# Uložení aktualizovaného CSV souboru
output_path = file_path.replace('.csv', '_with_inflation.csv')
df.to_csv(output_path, index=False)

print(f"Updated CSV saved as: {output_path}")
