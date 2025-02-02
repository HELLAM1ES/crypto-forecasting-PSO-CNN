from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from utils import configure_driver, process_crypto_data, random_sleep, convert_date_to_unix

# Liste des cryptos disponibles par défaut
AVAILABLE_CRYPTOS = [
    "Bitcoin (BTC)", "Ethereum (ETH)", "Cardano (ADA)", "Dogecoin (DOGE)",
    "Litecoin (LTC)", "Cosmos (ATOM)", "Chainlink (LINK)",
    "Polygon (MATIC)", "XRP (XRP)", "Filecoin (FIL)"
]

# Créez un routeur pour le module de scraping
scrape_router = APIRouter()

@scrape_router.post("/data", tags=["Scraping"])
def scrape_data(
    cryptos: Optional[List[str]] = Query(
        default=AVAILABLE_CRYPTOS,
        description="Liste des cryptos à extraire.",
        example=["Bitcoin (BTC)", "Ethereum (ETH)"]
    ),
    start_date: str = Query(
        default="01/01/2022", description="Date de début (format DD/MM/YYYY)."
    ),
    end_date: str = Query(
        default="31/12/2022", description="Date de fin (format DD/MM/YYYY)."
    )
):
    """
    Endpoint pour scraper les données des cryptos spécifiées entre deux dates.
    """
    try:
        # Conversion des dates en timestamps UNIX
        start_timestamp = convert_date_to_unix(start_date)
        end_timestamp = convert_date_to_unix(end_date)

        # Définir les URLs de Yahoo Finance pour le scraping
        yahoo_urls = {
            "Bitcoin (BTC)": f"https://finance.yahoo.com/quote/BTC-USD/history?period1={start_timestamp}&period2={end_timestamp}&interval=1d",
            "Ethereum (ETH)": f"https://finance.yahoo.com/quote/ETH-USD/history?period1={start_timestamp}&period2={end_timestamp}&interval=1d",
            "Cardano (ADA)": f"https://finance.yahoo.com/quote/ADA-USD/history?period1={start_timestamp}&period2={end_timestamp}&interval=1d",
            "Dogecoin (DOGE)": f"https://finance.yahoo.com/quote/DOGE-USD/history?period1={start_timestamp}&period2={end_timestamp}&interval=1d",
            "Litecoin (LTC)": f"https://finance.yahoo.com/quote/LTC-USD/history?period1={start_timestamp}&period2={end_timestamp}&interval=1d",
            "Cosmos (ATOM)": f"https://finance.yahoo.com/quote/ATOM-USD/history?period1={start_timestamp}&period2={end_timestamp}&interval=1d",
            "Chainlink (LINK)": f"https://finance.yahoo.com/quote/LINK-USD/history?period1={start_timestamp}&period2={end_timestamp}&interval=1d",
            "Polygon (MATIC)": f"https://finance.yahoo.com/quote/MATIC-USD/history?period1={start_timestamp}&period2={end_timestamp}&interval=1d",
            "XRP (XRP)": f"https://finance.yahoo.com/quote/XRP-USD/history?period1={start_timestamp}&period2={end_timestamp}&interval=1d",
            "Filecoin (FIL)": f"https://finance.yahoo.com/quote/FIL-USD/history?period1={start_timestamp}&period2={end_timestamp}&interval=1d",
        }

        # Filtrer les URLs valides en fonction des cryptos sélectionnées
        selected_urls = {name: yahoo_urls[name] for name in cryptos if name in yahoo_urls}
        if not selected_urls:
            raise HTTPException(status_code=400, detail="Aucune URL valide pour les cryptos spécifiées.")

        # Initialiser le navigateur pour le scraping
        driver = configure_driver()
        results = {}
        for name, url in selected_urls.items():
            success = process_crypto_data(driver, name, url)
            results[name] = "Success" if success else "Failed"
            random_sleep()
        driver.quit()

        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
