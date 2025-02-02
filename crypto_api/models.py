from pydantic import BaseModel, Field
from typing import List, Dict
from pydantic import BaseModel

from pydantic import BaseModel, Field
from typing import List, Dict
import pandas as pd

# Charger les cryptos disponibles depuis le fichier features_data.csv
FEATURES_FILE = "data/processed/features_data.csv"
try:
    df = pd.read_csv(FEATURES_FILE)
    AVAILABLE_CRYPTOS = df['Crypto'].unique().tolist()  # Récupérer les cryptos uniques
except Exception as e:
    print(f"Erreur lors du chargement des cryptos : {str(e)}")
    AVAILABLE_CRYPTOS = []  # Utiliser une liste vide si une erreur survient

# Modèle pour les métriques des modèles
class MetricsResponse(BaseModel):
    rmse: float = None
    r2: float = None
    accuracy: float = None
    precision: float = None
    recall: float = None

# Modèle pour la réponse du calcul MVF
class MVFResponse(BaseModel):
    expected_return: float
    volatility: float
    sharpe_ratio: float
    allocation: Dict[str, float]

# Modèle pour les requêtes de prédiction de direction
class DirectionRequest(BaseModel):
    cryptos: List[str] = Field(
        default=AVAILABLE_CRYPTOS,
        description="Liste des cryptos sélectionnées pour la prédiction. Toutes les cryptos disponibles sont incluses par défaut.",
        example=["Bitcoin (BTC)", "Ethereum (ETH)", "Cardano (ADA)"]
    )
    period: int = Field(
        default=7,
        description="Nombre de jours à prendre en compte pour la prédiction.",
        example=7
    )

# Modèle pour les réponses des prédictions de direction
class DirectionResponse(BaseModel):
    predictions: Dict[str, str]  # Dictionnaire contenant les prédictions consolidées par crypto

# Modèle pour les messages génériques
class MessageResponse(BaseModel):
    message: str





















































