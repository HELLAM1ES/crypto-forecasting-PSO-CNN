import os
import pandas as pd

# Chemins des fichiers et dossiers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
FEATURES_FILE = os.path.join(PROCESSED_DATA_DIR, "features_data.csv")

# Vérification et création des dossiers si nécessaire
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# Charger les cryptos disponibles
try:
    df = pd.read_csv(FEATURES_FILE)
    if 'Crypto' not in df.columns:
        raise ValueError("Les données ne contiennent pas de colonne 'Crypto'.")
    AVAILABLE_CRYPTOS = df['Crypto'].unique().tolist()
except FileNotFoundError:
    AVAILABLE_CRYPTOS = []  # Si le fichier n'existe pas encore

# Paramètres pour l'entraînement des modèles
TRAIN_TEST_SPLIT = 0.2
RANDOM_STATE = 42