SPSE Jecna Test Report
========================================

GENERAL INFORMATION
----------------------------------------
Tester: Václav Vondráček
Test Date: 7. dubna 2025
Platform: macOS Ventura 13.3
Device: MacBook Pro (M1, 2021)

Preparation and Precondition
----------------------------------------
- Aplikace byla nainstalována podle dokumentace.
- Byly ověřeny všechny závislosti uvedené v `requirements.txt`.
- Testovací prostředí bylo připraveno s následujícími daty:
  - Data o cenách ropy: `crawler/crawling/data/ropa.csv`
  - Data o víkendech a svátcích: `crawler/crawling/data/vikendy_a_svatky.csv`
  - Mapování PSČ na okresy: `data/obce-psc.csv`

Notes:
- Testování probíhalo na lokálním serveru Flask na adrese `http://127.0.0.1:5500`.

ENVIRONMENTAL
----------------------------------------
Database engine: CSV soubory (bez relační databáze)
Software and runtime environment:
- Python 3.12
- Flask 2.2.3
- macOS Ventura 13.3
- Webový prohlížeč: Safari 16.3

TEST CASES
========================================

Test Case 1: Predikce aktuálních cen
----------------------------------------
**Popis:** Ověření, že aplikace správně predikuje aktuální ceny na základě polohy uživatele.
**Kroky:**
1. Otevřít hlavní stránku aplikace.
2. Kliknout na tlačítko "Získat predikci".
3. Ověřit, že se zobrazí predikované ceny nafty a benzínu.
**Výsledek:** Úspěšné
**Poznámky:** Predikce byla správná, data odpovídala očekávaným hodnotám.

Test Case 2: Predikce budoucích cen
----------------------------------------
**Popis:** Ověření, že aplikace správně predikuje ceny na základě zadaných parametrů.
**Kroky:**
1. Vybrat okres "Praha 2".
2. Nastavit časové období od "2025-04-07" do "2025-04-14".
3. Vybrat typ paliva "Oboje".
4. Kliknout na tlačítko "Predikovat".
5. Ověřit, že se zobrazí predikované ceny a graf.
**Výsledek:** Úspěšné
**Poznámky:** Graf byl vykreslen správně, data odpovídala očekávaným hodnotám.

Test Case 3: API `/api/predict`
----------------------------------------
**Popis:** Ověření, že API endpoint `/api/predict` vrací správná data.
**Kroky:**
1. Odeslat POST požadavek na `/api/predict` s parametry `lat=50.0755` a `lon=14.4378`.
2. Ověřit, že odpověď obsahuje správné hodnoty.
**Výsledek:** Úspěšné
**Poznámky:** API odpovědělo správně, data odpovídala očekávaným hodnotám.

Test Case 4: API `/api/predict_future`
----------------------------------------
**Popis:** Ověření, že API endpoint `/api/predict_future` vrací správná data.
**Kroky:**
1. Odeslat POST požadavek na `/api/predict_future` s parametry:
   - `okres="Praha 2"`
   - `start="2025-04-07"`
   - `end="2025-04-14"`
   - `typ_paliva="oboje"`
2. Ověřit, že odpověď obsahuje predikce pro zadané období.
**Výsledek:** Úspěšné
**Poznámky:** API odpovědělo správně, data odpovídala očekávaným hodnotám.

Test Case 5: Chyby při neplatných datech
----------------------------------------
**Popis:** Ověření, že aplikace správně zpracovává neplatné vstupy.
**Kroky:**
1. Odeslat POST požadavek na `/api/predict` bez parametrů.
2. Ověřit, že odpověď obsahuje chybu.
**Výsledek:** Úspěšné
**Poznámky:** Aplikace správně vrátila chybu "Chybí data pro predikci".

BUGS
========================================
**Bug ID:** BUG-001
**Popis:** Při zadání neplatného okresu v API `/api/predict_future` aplikace vrací chybu 500 místo 400.
**Očekávaný výsledek:** Aplikace by měla vrátit chybu 400 s popisem "Neplatný okres".
**Reprodukční kroky:**
1. Odeslat POST požadavek na `/api/predict_future` s neplatným okresem.
2. Ověřit odpověď.

**Bug ID:** BUG-002
**Popis:** Graf na stránce predikce budoucích cen se nezobrazí, pokud není vybrán žádný typ paliva.
**Očekávaný výsledek:** Aplikace by měla zobrazit chybovou hlášku "Vyberte typ paliva".
**Reprodukční kroky:**
1. Nevybrat žádný typ paliva.
2. Kliknout na tlačítko "Predikovat".

INCIDENTS
========================================

Incident ID: INC-001
----------------------------------------
**Summary:** API `/api/predict` vrací prázdnou odpověď při nedostupnosti dat o ropě.
**Expected result:** Aplikace by měla vrátit chybu "Chybí data o ceně ropy".
**Test result:** Selhání
**Repro steps:**
1. Zablokovat přístup k API `kurzy.cz`.
2. Odeslat požadavek na `/api/predict`.
**Note:** Problém byl způsoben nedostupností externího API.

Incident ID: INC-002
----------------------------------------
**Summary:** Crawler neukládá data o víkendech a svátcích při chybě zápisu do souboru.
**Expected result:** Crawler by měl logovat chybu a pokračovat v práci.
**Test result:** Selhání
**Repro steps:**
1. Nastavit neexistující cestu pro výstupní soubor.
2. Spustit crawler.
**Note:** Problém byl způsoben nesprávnou konfigurací cesty.

NOTES
========================================
- Testování proběhlo úspěšně s výjimkou výše uvedených bugů a incidentů.
- Doporučuje se opravit chyby a znovu otestovat aplikaci.