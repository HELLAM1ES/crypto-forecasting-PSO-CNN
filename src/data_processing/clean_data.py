import os
import pandas as pd

def merge_dataframes(data_paths, output_path):
    """
    Fusionne plusieurs DataFrames en un seul et affiche le nombre de lignes pour chaque type de crypto
    avant et après la fusion.

    Args:
        data_paths (list): Liste des chemins des fichiers CSV à fusionner.
        output_path (str): Chemin de sortie pour le fichier fusionné.

    Returns:
        pd.DataFrame: Un DataFrame fusionné.
    """
    dataframes = []
    
    for path in data_paths:
        if os.path.exists(path):
            try:
                # Lecture du fichier
                df = pd.read_csv(path)

                # Extraire le nom de la crypto depuis le chemin du fichier
                crypto_name = path.split("/")[-1].split("_")[0]
                
                # Afficher le nombre de lignes avant la fusion
                print(f"{crypto_name} - Nombre de lignes avant fusion : {len(df)}")
                
                # Ajouter le DataFrame à la liste
                dataframes.append(df)
            except Exception as e:
                print(f"Erreur lors de la lecture de {path}: {e}")
        else:
            print(f"Fichier introuvable : {path}")
    
    if dataframes:
        # Fusionner les DataFrames (concaténation verticale)
        merged_df = pd.concat(dataframes, axis=0, ignore_index=True)
        
        # Sauvegarder le DataFrame fusionné
        merged_df.to_csv(output_path, index=False)
        
        # Compter le nombre de lignes pour chaque crypto après la fusion
        print("\nNombre de lignes par crypto après fusion :")
        crypto_counts = merged_df['Crypto'].value_counts()
        for crypto, count in crypto_counts.items():
            print(f"{crypto} - {count} lignes")
        
        print(f"\nFusion terminée. Fichier enregistré dans {output_path}")
        print(f"Nombre total de lignes dans le fichier fusionné : {len(merged_df)}")
        return merged_df
    else:
        print("Aucun fichier valide à fusionner.")
        return None

if __name__ == "__main__":
    # Liste des chemins des fichiers CSV
    data_paths = [
        "../../data/raw/Bitcoin_(BTC)_yahoo_data.csv",
        "../../data/raw/Ethereum_(ETH)_yahoo_data.csv",
        "../../data/raw/Cardano_(ADA)_yahoo_data.csv",
        "../../data/raw/Dogecoin_(DOGE)_yahoo_data.csv",
        "../../data/raw/Litecoin_(LTC)_yahoo_data.csv",
        "../../data/raw/Cosmos_(ATOM)_yahoo_data.csv",  # Remplacement de Avalanche par Cosmos
        "../../data/raw/Chainlink_(LINK)_yahoo_data.csv",
        "../../data/raw/Polygon_(MATIC)_yahoo_data.csv",
        "../../data/raw/XRP_(XRP)_yahoo_data.csv",
        "../../data/raw/Filecoin_(FIL)_yahoo_data.csv",
    ]
    
    # Chemin de sortie pour le fichier fusionné
    output_path = "../../data/processed/merged_data.csv"
    
    # Fusionner les DataFrames
    merged_df = merge_dataframes(data_paths, output_path)
