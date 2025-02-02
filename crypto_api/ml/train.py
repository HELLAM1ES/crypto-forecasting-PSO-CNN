import pandas as pd
import numpy as np
import pickle
import math
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, precision_score, recall_score
from config import FEATURES_FILE, TRAIN_TEST_SPLIT, RANDOM_STATE

# Entraînement du modèle de prévision des rendements
def train_return_model():
    df = pd.read_csv(FEATURES_FILE)
    if 'Close' not in df.columns:
        raise ValueError("Les données ne contiennent pas de colonne 'Close'.")
    
    df['Return'] = df['Close'].pct_change()
    df = df.dropna()
    
    features = ['Open', 'High', 'Low', 'Close', 'Volume', 'Volatility', 'Amplitude', 
                'Price_change', 'Volatility_ratio', 'High_low_spread', 'SMA_7', 'SMA_50',
                'EMA_10', 'EMA_50', 'RoC', 'BB_upper', 'BB_lower', 'ATR', 'RSI', 'VWAP', 'OBV']
    
    X = df[features].values
    y = df['Return'].values
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TRAIN_TEST_SPLIT, random_state=RANDOM_STATE)
    
    model = RandomForestRegressor(n_estimators=100, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    
    pickle.dump(model, open("return_model.pkl", "wb"))
    
    return {"message": "Le modèle de prévision des rendements est prêt pour la suite."}

def train_direction_model():
    df = pd.read_csv(FEATURES_FILE)
    if 'Close' not in df.columns:
        raise ValueError("Les données ne contiennent pas de colonne 'Close'.")
    
    df['Return'] = df['Close'].pct_change()
    df['Direction'] = (df['Return'] > 0).astype(int)
    df = df.dropna()
    
    features = ['Open', 'High', 'Low', 'Close', 'Volume']
    X = df[features].values
    y = df['Direction'].values
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TRAIN_TEST_SPLIT, random_state=RANDOM_STATE)
    
    model = RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    
    pickle.dump(model, open("direction_model.pkl", "wb"))
    
    return {"message": "Le modèle de prédiction de direction du marché est prêt pour la suite."}
