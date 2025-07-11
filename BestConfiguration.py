from pathlib import Path
import polars as pl
import geopolars as gpl
from shapely import wkt
from shapely.geometry import Point
import json
import pandas as pd
import os

FINAL_FOLDER_NAME = ""  # Nome della cartella finale
BASE_OUTPUT_DIR = ""  # Directory base di output
CSV_PATH = ""     # Path al file CSV
OUTPUT_DIR = os.path.join(BASE_OUTPUT_DIR, FINAL_FOLDER_NAME)  # Percorso completo della directory di output


def test1():
    file_path = Path("") # Inserisci il percorso del file CSV qui del tensore 
    df_poi = pl.read_csv(file_path, separator=";")

    print(df_poi.head())
    # Stampa i nomi delle colonne e i relativi tipi
    for col_name, col_type in zip(df_poi.columns, df_poi.dtypes):
        print(f"{col_name}: {col_type}")
    print(df_poi.shape)
    print(df_poi.describe())
    print(df_poi.null_count())

# Leggi i risultati dal file CSV
df_results = pd.read_csv(os.path.join(OUTPUT_DIR, "")) # Inserisci il nome del file CSV qui

# Usa il nome corretto della colonna per ordinare i risultati
df_results_sorted = df_results.sort_values(by="final_loss")  # Cambiato da "loss" a "final_loss"

# Estrai la configurazione migliore
best_config = df_results_sorted.iloc[0]
print("Configurazione migliore 1 trovata:")
print(best_config)

best_config = df_results_sorted.iloc[1]
print("Configurazione migliore 2 trovata:")
print(best_config)

best_config = df_results_sorted.iloc[2]
print("Configurazione migliore 3 trovata:")
print(best_config)

best_config = df_results_sorted.iloc[3]
print("Configurazione migliore 4 trovata:")
print(best_config)

best_config = df_results_sorted.iloc[4]
print("Configurazione migliore 5 trovata:")
print(best_config)