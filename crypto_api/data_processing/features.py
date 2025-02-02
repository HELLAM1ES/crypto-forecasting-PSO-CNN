import os
import pandas as pd
import numpy as np
from config import RAW_DATA_DIR, PROCESSED_DATA_DIR, FEATURES_FILE
from utils import save_dataframe

def clean_and_convert_data(df):
    """
    Nettoie et convertit les colonnes numériques d'un DataFrame.
    """
    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    for col in numeric_cols:
        df[col] = (
            df[col].replace({',': ''}, regex=True)  # Retirer les virgules
            .astype(float)  # Convertir en float
        )
    return df

def create_features(df):
    """
    Crée des nouvelles fonctionnalités pour l'analyse et la prédiction.
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

def merge_and_features():
    """
    Fusionne les données de `data/raw`, nettoie les données, crée des fonctionnalités
    et sauvegarde le fichier résultant dans `data/processed/features_data.csv`.
    """
    try:
        # Vérification de l'existence du dossier de données brutes
        if not os.path.exists(RAW_DATA_DIR):
            raise FileNotFoundError(f"Le dossier des données brutes '{RAW_DATA_DIR}' est introuvable.")
        
        # Récupération de tous les fichiers CSV dans le dossier `data/raw`
        all_files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith(".csv")]
        if not all_files:
            raise FileNotFoundError(f"Aucun fichier CSV trouvé dans '{RAW_DATA_DIR}'.")
        
        # Lecture et concaténation des fichiers
        df_list = []
        for file in all_files:
            file_path = os.path.join(RAW_DATA_DIR, file)
            print(f"Chargement du fichier : {file_path}")
            df = pd.read_csv(file_path, header=0, names=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Crypto'])
            df_list.append(df)

        combined_df = pd.concat(df_list, ignore_index=True)
        print("Fusion des fichiers terminée.")
        
        # Nettoyage et conversion des données
        combined_df['Date'] = pd.to_datetime(combined_df['Date'], format='%b %d, %Y')
        combined_df = clean_and_convert_data(combined_df)

        # Création des fonctionnalités
        combined_df = create_features(combined_df)

        # Supprimer les lignes avec des valeurs manquantes
        combined_df = combined_df.dropna()

        # Sauvegarde des données traitées
        save_dataframe(combined_df, FEATURES_FILE)

        return {"message": "Données fusionnées et fonctionnalités créées avec succès.", "features_file": FEATURES_FILE}
    except Exception as e:
        raise ValueError(f"Erreur lors de la fusion ou de la création des fonctionnalités : {str(e)}")
