import pandas as pd
from fastapi import APIRouter, HTTPException
from models import DirectionRequest, DirectionResponse

# Initialiser le routeur FastAPI
predict_router = APIRouter()

@predict_router.post("/predict-direction", response_model=DirectionResponse)
def predict_direction(request: DirectionRequest):
    """
    Prédit la direction consolidée du marché pour plusieurs cryptos sur une période spécifiée.
    """
    try:
        # Charger le modèle et les données
        model = pd.read_pickle("direction_model.pkl")
        df = pd.read_csv("data/processed/features_data.csv")
        
        # Vérification des colonnes nécessaires
        if 'Crypto' not in df.columns or 'Close' not in df.columns:
            raise HTTPException(status_code=400, detail="Les données ne contiennent pas les colonnes nécessaires.")
        
        predictions = {}
        
        for crypto in request.cryptos:
            # Filtrer pour la crypto spécifiée
            crypto_df = df[df['Crypto'] == crypto]
            if crypto_df.empty:
                predictions[crypto] = "No Data"
                continue
            
            # Utiliser les dernières données correspondant à la période spécifiée
            crypto_df = crypto_df.tail(request.period)
            if crypto_df.empty:
                predictions[crypto] = "Not Enough Data"
                continue
            
            # Préparer les données pour la prédiction
            features = ['Open', 'High', 'Low', 'Close', 'Volume']
            X = crypto_df[features].values
            
            # Faire des prédictions
            predicted_directions = model.predict(X)
            directions = ["Up" if direction == 1 else "Down" for direction in predicted_directions]
            
            # Consolider la direction pour la période
            consolidated_direction = "Up" if directions.count("Up") > directions.count("Down") else "Down"
            predictions[crypto] = consolidated_direction
        
        # Retourner la réponse
        return {"predictions": predictions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
