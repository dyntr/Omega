import csv
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class CrawlerSelenium:
    def __init__(self):
        """
        Inicializuje Selenium WebDriver s možnostmi prohlížeče Chrome.
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def login(self, login_url, username, password):
        """
        Přihlásí se do systému CCS pomocí zadaných přihlašovacích údajů.

        Argumenty:
            login_url (str): URL přihlašovací stránky.
            username (str): Uživatelské jméno pro přihlášení.
            password (str): Heslo pro přihlášení.

        Návratová hodnota:
            bool: True, pokud bylo přihlášení úspěšné, jinak False.
        """
        self.driver.get(login_url)
        user_input = self.driver.find_element(By.NAME, "UserName")
        pass_input = self.driver.find_element(By.NAME, "UserPassword")
        submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        user_input.send_keys(username)
        pass_input.send_keys(password)
        submit_button.click()
        time.sleep(3)
        return "ccs_radar" in self.driver.page_source

    def navigate_to_radar(self):
        """
        Přesměruje na stránku CCS Radar.

        Návratová hodnota:
            bool: True, pokud bylo přesměrování úspěšné, jinak False.
        """
        try:
            radar_link = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@title='CCS Radar']"))
            )
            radar_link.click()
            time.sleep(2)
            return True
        except:
            return False

    def submit_form(self):
        """
        Odešle formulář na stránce CCS Radar a zpracuje data pro každý "okres".

        Návratová hodnota:
            bool: True, pokud byl formulář úspěšně odeslán a data zpracována, jinak False.
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "f_from_y"))
            )
            select_from_y = Select(self.driver.find_element(By.NAME, "f_from_y"))
            select_from_y.select_by_value("2010")
            select_to_y = Select(self.driver.find_element(By.NAME, "f_to_y"))
            select_to_y.select_by_value(time.strftime("%Y"))
            select_kraj = Select(self.driver.find_element(By.NAME, "kraj"))
            select_kraj.select_by_value("*")
            select_okres = Select(self.driver.find_element(By.NAME, "okres"))
            print(len(select_okres.options))
            for _ in range(len(select_okres.options)):
                # Re-fetch the select element and its options
                select_okres = Select(self.driver.find_element(By.NAME, "okres"))
                all_okres_options = select_okres.options
                option = all_okres_options[_]
                
                okres_value = option.get_attribute("value")
                okres_name = option.text.strip()
                print(okres_name)
                if not okres_value or okres_value == "*":
                    print("okres")
                    continue
                print(f"Processing okres: {okres_name} ({okres_value})")
                
                # Re-select the current option
                select_okres.select_by_value(okres_value)
                
                try:
                    update_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="text"]/form/table[1]/tbody/tr[5]/td[2]/input'))
                    )
                    update_button.click()
                    time.sleep(2)
                except Exception as e:
                    print(f"Error clicking update button for okres {okres_name}: {e}")
                    continue

                try:
                    WebDriverWait(self.driver,10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "dynamic"))
                    )
                    print(f"Table loaded for okre: {okres_name}")

                    table_data = self.fetch_data()
                    if table_data:
                        for row in table_data:
                            row.append(okres_name)
                        save_csv(table_data,"okresy.csv")
                        print(f"Data okresu: {okres_name} has been saved to okresy.csv")
                except Exception as e:
                    print(f"Error processing table for okres {okres_name}: {e}")
                finally:
                    print("going next")
                
            return True
        except Exception as e:
            print(f"Error submitting form: {e}")
            return False

    def fetch_data(self):
        """
        Načte data z tabulky na aktuální stránce.

        Návratová hodnota:
            list: Seznam řádků, kde každý řádek je seznam hodnot buněk.
        """
        try:
            table = self.driver.find_element(By.CLASS_NAME, "dynamic")
            rows = table.find_elements(By.TAG_NAME, "tr")
            data = []
            for row in rows:
                cols = [col.text.strip() for col in row.find_elements(By.TAG_NAME, "td")]
                if cols:
                    print(f"Saving:  {cols}")
                    data.append(cols)
            return data
        except:
            return None

    def close(self):
        """
        Uzavře Selenium WebDriver.
        """
        self.driver.quit()

def save_csv(data, filename):
    """
    Uloží poskytnutá data do CSV souboru.

    Argumenty:
        data (list): Data k uložení, kde každý prvek je řádek.
        filename (str): Název CSV souboru.
    """
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)

if __name__ == "__main__":
    """
    Hlavní spuštění skriptu pro CCS crawler.
    """
    crawler = CrawlerSelenium()
    login_url = "https://servis.ccs.cz"
    username = "patrickdyntr"  # Změnit na skutečné údaje
    password = "HA85//wb" 
    if crawler.login(login_url, username, password):
        print("Přihlášení úspěšné.")
        if crawler.navigate_to_radar():
            print("Přesměrování na CCS Radar úspěšné.")
            if crawler.submit_form():
                print("Formulář odeslán.")
            else:
                print("Nepodařilo se odeslat formulář.")
        else:
            print("Nepodařilo se přejít na CCS Radar.")
    else:
        print("Přihlášení selhalo.")
    crawler.close()
