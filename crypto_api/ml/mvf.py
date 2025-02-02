import pickle
import numpy as np
import pandas as pd
from config import FEATURES_FILE
from models import MVFResponse

RETURN_MODEL_PATH = "return_model.pkl"

def calculate_mvf():
    try:
        # Charger le modèle et les données
        model = pickle.load(open("return_model.pkl", "rb"))
        df = pd.read_csv("data/processed/features_data.csv")

        # Vérification des colonnes nécessaires
        if 'Close' not in df.columns or 'Crypto' not in df.columns:
            raise ValueError("Les données ne contiennent pas les colonnes nécessaires.")

        # Calcul des rendements par crypto
        df['Return'] = df.groupby('Crypto')['Close'].pct_change()
        df = df.dropna()

        # Caractéristiques utilisées pour la prédiction
        features = ['Open', 'High', 'Low', 'Close', 'Volume', 'Volatility', 'Amplitude', 
                    'Price_change', 'Volatility_ratio', 'High_low_spread', 'SMA_7', 'SMA_50',
                    'EMA_10', 'EMA_50', 'RoC', 'BB_upper', 'BB_lower', 'ATR', 'RSI', 'VWAP', 'OBV']

        cryptos = df['Crypto'].unique()
        expected_returns = {}
        volatilities = {}
        sharpe_ratios = {}

        risk_free_rate = 0.02 / 252  # Taux sans risque annualisé divisé par 252 jours de marché

        # Calcul des métriques pour chaque crypto
        for crypto in cryptos:
            crypto_df = df[df['Crypto'] == crypto]
            X = crypto_df[features].values  # Assurez-vous d'utiliser les mêmes caractéristiques
            predicted_returns = model.predict(X)

            mean_return = predicted_returns.mean()
            volatility = predicted_returns.std()
            sharpe_ratio = (mean_return - risk_free_rate) / volatility if volatility != 0 else 0

            expected_returns[crypto] = mean_return
            volatilities[crypto] = volatility
            sharpe_ratios[crypto] = sharpe_ratio

        # Allocation basée sur le Sharpe Ratio
        total_sharpe = sum(sharpe_ratios.values())
        allocation = {crypto: sharpe_ratios[crypto] / total_sharpe for crypto in cryptos} if total_sharpe != 0 else {crypto: 1/len(cryptos) for crypto in cryptos}

        return {
            "message": "Calcul du MVF terminé avec succès.",
            "expected_return": np.mean(list(expected_returns.values())),
            "volatility": np.mean(list(volatilities.values())),
            "sharpe_ratio": np.mean(list(sharpe_ratios.values())),
            "allocation": allocation
        }
    except Exception as e:
        raise ValueError(f"Erreur dans le calcul du MVF : {str(e)}")







































