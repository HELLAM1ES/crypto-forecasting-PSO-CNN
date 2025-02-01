from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import random

def configure_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-browser-side-navigation")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def random_sleep():
    time.sleep(random.uniform(2, 5))

def process_crypto_data(driver, name, url):
    try:
        print(f"[{name}] Starting data processing...")
        driver.get(url)
        random_sleep()

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        try:
            cookie_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Accept')]"))
            )
            cookie_button.click()
        except Exception:
            print(f"[{name}] No cookie banner detected")

        random_sleep()

        try:
            table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            headers = [header.text for header in table.find_elements(By.TAG_NAME, "th")]
            rows_data = []
            rows = table.find_elements(By.TAG_NAME, "tr")[1:]
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                row_data = [cell.text.strip() for cell in cells]
                if row_data:
                    rows_data.append(row_data)

            df = pd.DataFrame(rows_data, columns=headers)
            df['Crypto'] = name
            filename = f"data/raw/{name.replace(' ', '_')}_yahoo_data.csv"
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"[{name}] Data saved to {filename}")
            return True
        except Exception as e:
            print(f"[{name}] Error extracting data: {str(e)}")
            return False
    except Exception as e:
        print(f"[{name}] General error: {str(e)}")
        return False

def main():
    """
    Programme principal pour extraire les données des cryptos spécifiées.
    """
    start_date = 1577836800  # 2020-01-01
    end_date = 1735689600    # 2024-12-31

    # URLs pour les cryptos listées
    yahoo_urls = {
        "Bitcoin (BTC)": f"https://finance.yahoo.com/quote/BTC-USD/history?period1={start_date}&period2={end_date}&interval=1d",
        "Ethereum (ETH)": f"https://finance.yahoo.com/quote/ETH-USD/history?period1={start_date}&period2={end_date}&interval=1d",
        "Cardano (ADA)": f"https://finance.yahoo.com/quote/ADA-USD/history?period1={start_date}&period2={end_date}&interval=1d",
        "Dogecoin (DOGE)": f"https://finance.yahoo.com/quote/DOGE-USD/history?period1={start_date}&period2={end_date}&interval=1d",
        "Litecoin (LTC)": f"https://finance.yahoo.com/quote/LTC-USD/history?period1={start_date}&period2={end_date}&interval=1d",
        "Cosmos (ATOM)": f"https://finance.yahoo.com/quote/ATOM-USD/history?period1={start_date}&period2={end_date}&interval=1d",  # Remplacement par Cosmos
        "Chainlink (LINK)": f"https://finance.yahoo.com/quote/LINK-USD/history?period1={start_date}&period2={end_date}&interval=1d",
        "Polygon (MATIC)": f"https://finance.yahoo.com/quote/MATIC-USD/history?period1={start_date}&period2={end_date}&interval=1d",
        "XRP (XRP)": f"https://finance.yahoo.com/quote/XRP-USD/history?period1={start_date}&period2={end_date}&interval=1d",
        "Filecoin (FIL)": f"https://finance.yahoo.com/quote/FIL-USD/history?period1={start_date}&period2={end_date}&interval=1d",
    }

    driver = configure_driver()
    for name, url in yahoo_urls.items():
        process_crypto_data(driver, name, url)
        random_sleep()
    driver.quit()

if __name__ == "__main__":
    main()
