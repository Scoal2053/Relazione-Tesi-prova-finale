import pandas as pd
from collections import Counter

# Percorso del file gigante
file_path = "" # Sostituisci con il percorso del tuo file 

# Lista di possibili formati da verificare
possible_formats = [
    "%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S",
    "%d/%m/%Y %H:%M:%S.%f", "%d/%m/%Y %H:%M:%S",
    "%Y/%m/%d %H:%M:%S.%f", "%Y/%m/%d %H:%M:%S",
    "%d.%m.%Y %H:%M:%S", "%d %b %Y %H:%M:%S",
    "%d %B %Y %H:%M:%S", "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%d %H:%M:%S %Z", "%m-%d-%Y %I:%M:%S %p",
    "%s"  # Unix timestamp in secondi
]

# Funzione per riconoscere il formato di una data
def detect_date_format(date_str):
    date_str = str(date_str).strip()
    if date_str.lower() in ["nan", "none", "nat"]:  # Ignora NaN/NaT
        return "INVALID"
    
    for fmt in possible_formats:
        try:
            _ = pd.to_datetime(date_str, format=fmt)
            return fmt
        except ValueError:
            continue
    
    return "UNKNOWN"

# Leggi il file gigante in chunk per evitare problemi di memoria
chunk_size = 100000  # Dimensione del chunk
formats_start = Counter()
formats_end = Counter()

for chunk in pd.read_csv(file_path, chunksize=chunk_size):
    if 'local_ts_start' in chunk.columns and 'local_ts_end' in chunk.columns:
        formats_start.update(chunk['local_ts_start'].dropna().astype(str).apply(detect_date_format))
        formats_end.update(chunk['local_ts_end'].dropna().astype(str).apply(detect_date_format))
    else:
        print(f"Le colonne 'local_ts_start' e 'local_ts_end' non esistono nel chunk")

# Stampa i risultati
print("Formati rilevati per 'local_ts_start':")
for fmt, count in formats_start.items():
    print(f"  {fmt}: {count} occorrenze")

print("\nFormati rilevati per 'local_ts_end':")
for fmt, count in formats_end.items():
    print(f"  {fmt}: {count} occorrenze")