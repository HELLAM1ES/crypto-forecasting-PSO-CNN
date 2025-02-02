import os
import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import numpy as np

def configure_driver():
    """
    Configure et retourne un driver Selenium Chrome.
    """
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-browser-side-navigation")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")  # Activer le mode headless pour exécuter sans interface
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def random_sleep():
    """
    Attendre un temps aléatoire pour simuler un comportement humain.
    """
    time.sleep(random.uniform(2, 5))

def convert_date_to_unix(date_str: str) -> int:
    """
    Convertit une date au format DD/MM/YYYY en timestamp UNIX.
    """
    try:
        dt = datetime.strptime(date_str, "%d/%m/%Y")
        return int(dt.timestamp())
    except ValueError:
        raise ValueError(f"La date {date_str} n'est pas valide. Utilisez le format DD/MM/YYYY.")

def process_crypto_data(driver, name, url):
    """
    Scrape les données historiques d'une crypto depuis Yahoo Finance.
    """
    try:
        print(f"[{name}] Starting data processing from URL: {url}")
        driver.get(url)
        random_sleep()

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Accepter les cookies si nécessaire
        try:
            cookie_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Accept')]"))
            )
            cookie_button.click()
        except Exception:
            pass  # Aucun bouton cookie trouvé

        random_sleep()

        # Extraire les données de la table
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

            # Sauvegarder les données dans le dossier `data/raw`
            output_dir = "data/raw"
            os.makedirs(output_dir, exist_ok=True)

            filename = os.path.join(output_dir, f"{name.replace(' ', '_')}_yahoo_data.csv")
            df.to_csv(filename, index=False, encoding='utf-8')

            print(f"[{name}] Data saved successfully to {filename}")
            return True
        except Exception as e:
            print(f"[{name}] Error extracting data: {str(e)}")
            return False
    except Exception as e:
        print(f"[{name}] General error: {str(e)}")
        return False
    
def clean_and_convert_data(df):
    """
    Nettoie et convertit les colonnes numériques.
    """
    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].replace({',': ''}, regex=True).astype(float)
    return df

def create_features(df):
    """
    Crée des nouvelles features pour l'analyse et la prédiction.
    """
    df['Volatility'] = df['High'] - df['Low']
    df['Return'] = (df['Close'] - df['Open']) / df['Open']
    df['Amplitude'] = (df['High'] - df['Low']) / df['Open']
    df['Price_change'] = df['Close'] - df['Open']
    df['Volatility_ratio'] = df['Volatility'] / df['Close']
    df['High_low_spread'] = df['High'] - df['Low']
    df['SMA_7'] = df['Close'].rolling(window=7).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['EMA_10'] = df['Close'].ewm(span=10).mean()
    df['EMA_50'] = df['Close'].ewm(span=50).mean()
    df['RoC'] = df['Close'].pct_change(periods=10)
    rolling_mean = df['Close'].rolling(window=20).mean()
    rolling_std = df['Close'].rolling(window=20).std()
    df['BB_upper'] = rolling_mean + (2 * rolling_std)
    df['BB_lower'] = rolling_mean - (2 * rolling_std)
    df['ATR'] = (df['High'] - df['Low']).rolling(window=14).mean()
    delta = df['Close'].diff(1)
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    df['RSI'] = 100 - (100 / (1 + gain / loss))
    df['VWAP'] = (df['Volume'] * (df['High'] + df['Low'] + df['Close']) / 3).cumsum() / df['Volume'].cumsum()
    df['OBV'] = (df['Volume'] * np.sign(df['Close'].diff())).fillna(0).cumsum()
    return df

import os
import pandas as pd

def save_dataframe(df: pd.DataFrame, filepath: str) -> None:
    """
    Sauvegarde un DataFrame dans un fichier CSV.

    Args:
        df (pd.DataFrame): Le DataFrame à sauvegarder.
        filepath (str): Le chemin complet du fichier de destination.

    Raises:
        ValueError: Si le DataFrame est vide.
    """
    if df.empty:
        raise ValueError("Le DataFrame est vide et ne peut pas être sauvegardé.")
    
    # Créer le répertoire si nécessaire
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Sauvegarder en CSV
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"Le DataFrame a été sauvegardé avec succès dans : {filepath}")
