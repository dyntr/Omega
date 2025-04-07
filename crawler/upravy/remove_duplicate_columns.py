import csv

input_file = 'spojene_data.csv'  # Cesta k souboru s duplicitními sloupci
output_file = 'spojene_data_cleaned.csv'  # Cesta k vyčištěnému výstupnímu souboru

with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
     open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    # Odstranění duplicitních sloupců vytvořením unikátního seznamu názvů sloupců
    fieldnames = []
    seen = set()
    for field in reader.fieldnames:
        if field not in seen:
            fieldnames.append(field)
            seen.add(field)
    
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader:
        # Zapsání pouze unikátních sloupců
        writer.writerow({field: row[field] for field in fieldnames})

