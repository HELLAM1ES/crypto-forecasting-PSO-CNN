
# **Crypto Forecasting with PSO-CNN**
### **Predicting Cryptocurrency Returns and Optimizing Portfolios**

## **📖 Project Overview**
This project is part of the **Quantitative Finance** course within the **Master MOSEF (Modélisation et Méthodes Mathématiques en Économie et Finance)** at **Paris 1 Panthéon-Sorbonne University**. The aim is to develop a scientific approach to forecasting cryptocurrency returns using advanced deep learning methods, coupled with portfolio optimization techniques.

### **Key Objectives**:
1. **Accurate Return Forecasting**:
   - Use a **PSO-CNN model** (Particle Swarm Optimization + Convolutional Neural Networks) to predict future cryptocurrency returns.
   - Analyze time-series data from the cryptocurrency market and on-chain metrics.
2. **Portfolio Optimization**:
   - Apply **Mean-Variance Forecasting (MVF)** to allocate assets dynamically based on predicted returns.
   - Compare portfolio performance against traditional optimization strategies.

This project blends **machine learning**, **financial modeling**, and **cryptocurrency analytics**, providing a robust framework for scientific research in quantitative finance.

---

## **👩‍💻 Authors**
- **Hella Bouhadda**
- **Charlotte Cegarra**
- **Chirine Doxposito**

---

## **📂 Project Structure**
```
📦 crypto-forecasting-PSO-CNN
├── 📂 data/                  # Données collectées et nettoyées
│   ├── raw/                  # Données brutes récupérées
│   │   ├── Arbitrum-ARB_yahoo_data.csv
│   │   ├── Bitcoin-BTC_yahoo_data.csv
│   │   ├── Cardano-ADA_yahoo_data.csv
│   │   ├── Chainlink-LINK_yahoo_data.csv
│   │   ├── Dogecoin-DOGE_yahoo_data.csv
│   │   ├── Ethereum-ETH_yahoo_data.csv
│   │   ├── Filecoin-FIL_yahoo_data.csv
│   │   ├── Litecoin-LTC_yahoo_data.csv
│   │   ├── Polygon-MATIC_yahoo_data.csv
│   │   ├── XRP-XRP_yahoo_data.csv
│   ├── processed/            # Données nettoyées et fusionnées
│   │   ├── merged_data.csv   # Fichier fusionné contenant toutes les données
│   ├── features/             # Données enrichies avec indicateurs techniques
│       ├── .keep
├── 📂 notebooks/              # Notebooks Jupyter pour l'exploration
│   ├── 01_data_collection.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_model_training.ipynb
│   ├── 04_portfolio_optimization.ipynb
├── 📂 models/                 # Modèles entraînés
│   ├── PSO_CNN_model.h5       # Modèle entraîné (placeholder)
│   ├── clustering_model.pkl   # Modèle de clustering (placeholder)
│   ├── .keep
├── 📂 src/                    # Code source pour l'implémentation
│   ├── 📂 api/
│   │   ├── main.py            # API FastAPI pour servir les prédictions
│   ├── 📂 data_processing/
│   │   ├── clean_data.py      # Script de nettoyage et fusion des données
│   │   ├── collect_data.py    # Scripts de collecte de données
│   │   ├── feature_engineering.py # Ajout d’indicateurs techniques
│   ├── 📂 models/
│   │   ├── train_model.py     # Entraînement du modèle PSO-CNN
│   │   ├── clustering.py      # Algorithme de clustering
│   │   ├── predict.py         # Script de prédiction
│   ├── 📂 optimization/
│   │   ├── optimize_portfolio.py # Stratégies d’allocation
│   ├── 📂 web_scraping/
│   │   ├── web.py             # Script pour le scraping des données
├── 📂 results/                # Résultats et visualisations
│   ├── backtesting_results.png
│   ├── model_performance.csv
│   ├── .keep
├── 📂 docs/                   # Documentation du projet
│   ├── methodology.md         # Explication de la méthodologie
│   ├── results.md             # Résumé des résultats
│   ├── references.md          # Revue de littérature
├── README.md                  # Présentation du projet
├── requirements.txt           # Liste des dépendances Python
├── .gitignore                 # Fichiers à exclure du suivi Git

```

---

## **🚀 Features**
- **Return Forecasting**:
  - Train a CNN model optimized with PSO to predict cryptocurrency returns.
  - Analyze market time-series data and blockchain (on-chain) metrics.
- **Portfolio Optimization**:
  - Use Mean-Variance Forecasting (MVF) to compute optimal portfolio allocations.
  - Evaluate portfolio performance using scientific metrics like Sharpe ratio and maximum drawdown.

---

## **🔧 Technologies**
- **Programming Language**: Python
- **Frameworks and Libraries**:
  - TensorFlow/Keras: PSO-CNN modeling
  - Scikit-learn: Clustering and feature engineering
  - FastAPI: Deploying the forecasting model as an API
- **Data Sources**:
  - APIs: Binance, Etherscan, Glassnode
  - Web scraping for macroeconomic events and news

---

## **📚 Installation**
### **1️⃣ Prerequisites**
- Python 3.9 or later
- Pip for dependency management

### **2️⃣ Clone the Repository**
```bash
git clone https://github.com/HELLAM1ES/crypto-forecasting-PSO-CNN.git
cd crypto-forecasting-PSO-CNN
```

### **3️⃣ Install Dependencies**
Install all required Python libraries:
```bash
pip install -r requirements.txt
```

---

## **🛠️ Usage**
### **1️⃣ Collect Data**
Run the script to collect market and on-chain data:
```bash
python src/data_processing/collect_data.py
```

### **2️⃣ Prepare Data**
Run the script to preprocess data and extract features:
```bash
python src/data_processing/feature_engineering.py
```

### **3️⃣ Train the Model**
Train the PSO-CNN model with the following command:
```bash
python src/models/train_model.py
```

### **4️⃣ Optimize the Portfolio**
Run the script to compute the optimal portfolio allocation:
```bash
python src/optimization/optimize_portfolio.py
```

---

## **📝 Contribution Guidelines**
If you want to contribute to this project:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Submit a pull request with a clear description of your changes.

---

## **📄 License**
This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## **📢 Contact**
For any questions or suggestions, feel free to reach out to the authors:
- **Hella Bouhadda**
- **Charlotte Cegarra**
- **Chirine Doxposito**


