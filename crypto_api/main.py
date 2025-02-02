from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from typing import List, Optional
from ml.train import train_return_model, train_direction_model
from data_processing.features import merge_and_features
from data_processing.scrape import scrape_router  # Import du scrape_router
from models import MessageResponse, DirectionRequest, DirectionResponse, MVFResponse
from ml.mvf import calculate_mvf
from ml.predict import predict_router
from fastapi import APIRouter
from data_processing.features import merge_and_features




# Création de l'application FastAPI
app = FastAPI(
    title="Crypto Data API",
    description="API pour la collecte et l'analyse de données crypto",
    version="1.0"
)

# Inclusion du router pour le scraping
app.include_router(scrape_router, prefix="/scrape", tags=["Scraping"])

# Configuration des fichiers statiques et des templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.post("/merge_and_features", response_model=MessageResponse, tags=["Feature Engineering"])
def merge_features():
    """
    Fusionne les données et crée des fonctionnalités.
    """
    return merge_and_features()

@app.post("/train-return", response_model=MessageResponse, tags=["Model Training"])
def train_return():
    """
    Entraîne un modèle pour prédire les rendements.
    """
    return train_return_model()

@app.post("/train-direction", response_model=MessageResponse, tags=["Model Training"])
def train_direction():
    """
    Entraîne un modèle pour prédire la direction du marché.
    """
    return train_direction_model()

app.include_router(predict_router, prefix="/predict", tags=["Prediction"])

@app.post("/mvf", response_model=MVFResponse, tags=["Portfolio Optimization"])
def calculate_mvf_endpoint():
    """
    Calcule les métriques de risque et d'allocation optimale.
    """
    return calculate_mvf()

@app.get("/", response_class=HTMLResponse, tags=["UI"])
def home(request: Request):
    """
    Affiche une page d'accueil HTML contenant les descriptions des endpoints.
    """
    return templates.TemplateResponse("home.html", {"request": request})

# Lancement de l'application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
