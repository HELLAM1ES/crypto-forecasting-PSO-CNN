
# **Crypto Forecasting API**

## **Description**
Cette API permet de collecter, analyser et prédire les données de crypto-monnaies en utilisant des modèles de machine learning.  
Elle offre plusieurs fonctionnalités, notamment :
- **Scraping** des données financières pour des crypto-monnaies spécifiques.
- **Génération de caractéristiques (features)** à partir des données collectées.
- **Prévision des rendements** (returns) des crypto-monnaies.
- **Prédiction de la direction** du marché (Up/Down).
- **Calcul de la MVF (Maximum Variance Frontier)** pour optimiser les portefeuilles de crypto-monnaies.

---

## **Arborescence du projet**

```
crypto_api/
│
├── main.py                # Point d'entrée principal de l'API
├── models.py              # Contient tous les modèles Pydantic
├── config.py              # Configuration globale (fichiers, constantes)
├── predict.py             # Prédiction des directions de marché
├── train.py               # Code pour entraîner les modèles
├── data_processing/
│   ├── features.py        # Préparation des données et génération des features
│   ├── scrape.py          # Scraping des données
│
├── data/
│   ├── processed/         # Contient `features_data.csv` pour les prédictions
│   ├── raw/               # Données brutes
│
├── templates/             # Contient les fichiers HTML pour la page d'accueil
│   └── index.html
│
└── static/                # Fichiers CSS, JS et images
    ├── css/
    │   └── style.css      # Styles pour la page d'accueil
    └── images/
        └── logo.jpg       # Logo de l'API
```

---

## **Fonctionnalités principales**

### **1. Scraping des données**
- Collecte des données historiques pour des crypto-monnaies spécifiques via Yahoo Finance.

### **2. Génération des caractéristiques (Features)**
- Calcule des indicateurs techniques tels que la volatilité, RSI, SMA, EMA, Bollinger Bands, etc.

### **3. Modèles prédictifs**
- **Prévision des rendements** : Estimation continue des variations de prix.
- **Prédiction de la direction** : Identification des tendances du marché (hausse ou baisse).

### **4. Calcul de MVF**
- Optimisation des portefeuilles en calculant les rendements attendus, la volatilité et le ratio de Sharpe.

---

## **Endpoints disponibles**

### **1. Scraping des données**
- **URL** : `/scrape_data`
- **Méthode** : `POST`
- **Description** : Récupère les données financières pour des crypto-monnaies spécifiques.
- **Exemple de requête** :
  ```json
  {
    "cryptos": ["Bitcoin (BTC)", "Ethereum (ETH)"],
    "start_date": "01/01/2022",
    "end_date": "31/12/2022"
  }
  ```

### **2. Génération des caractéristiques**
- **URL** : `/merge_and_features`
- **Méthode** : `POST`
- **Description** : Calcule les indicateurs techniques et prépare les données pour l'entraînement des modèles.

### **3. Entraînement des modèles**
#### a. Prévision des rendements
- **URL** : `/train-return`
- **Méthode** : `POST`
- **Description** : Entraîne un modèle pour prédire les rendements.
- **Exemple de réponse** :
  ```json
  {
    "message": "Le modèle de prévision des rendements est prêt pour la suite."
  }
  ```

#### b. Prédiction de la direction
- **URL** : `/train-direction`
- **Méthode** : `POST`
- **Description** : Entraîne un modèle pour prédire la direction du marché.
- **Exemple de réponse** :
  ```json
  {
    "message": "Le modèle de prédiction de direction est prêt pour la suite."
  }
  ```

### **4. Prédiction de la direction**
- **URL** : `/predict-direction`
- **Méthode** : `POST`
- **Description** : Prédit la direction consolidée (Up/Down) pour les cryptos sélectionnées.
- **Exemple de requête** :
  ```json
  {
    "cryptos": ["Bitcoin (BTC)", "Ethereum (ETH)"],
    "period": 7
  }
  ```

### **5. Calcul MVF**
- **URL** : `/mvf`
- **Méthode** : `POST`
- **Description** : Calcule le rendement attendu, la volatilité, et le ratio de Sharpe pour optimiser un portefeuille.
- **Exemple de réponse** :
  ```json
  {
    "expected_return": 0.015,
    "volatility": 0.02,
    "sharpe_ratio": 0.75,
    "allocation": {
      "Bitcoin (BTC)": 0.6,
      "Ethereum (ETH)": 0.4
    }
  }
  ```

---

## **Auteurs**
- **Hella BOUHADDA**
- **Chirine DEXPOSITO**
- **Charlotte CEGARRA**

**Encadrants** :
- **Rania KAFFEL**
- **Sarra BENYAHIA**
- **Jose Angel Garcia Sanchez**

---
