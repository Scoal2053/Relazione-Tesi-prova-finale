# Relazione-Tesi-prova-finale
Questa repository contiene il codice del lavoro svolto durante lo stage triennale effettuato presso l'Università degli studi Milano-Bicocca

Di seguito sono riportate le desrizioni dei codici utilizzati

In tutti i file sono stati rimossi i path delle cartelle in quanto cambiano da compure a computer, sono da reinserire prima di riutilizzare i codici

# AnalisiDatiComuneMilano.py

## Descrizione

Script Python per la creazione di una mappa interattiva che visualizza la distribuzione geografica delle stazioni, fermate autobus e fermate metro del Comune di Milano.

## Requisiti

- Python 3.x
- Pandas
- GeoPandas  
- Folium
- Shapely


## Formato Dati

I file CSV devono contenere le seguenti colonne:

**Stazioni**: `Stazione`, `LONG_X_4326`, `LAT_Y_4326`
**Fermate Autobus**: `LONG_X_4326`, `LAT_Y_4326`  
**Fermate Metro**: `LONG_X_4326`, `LAT_Y_4326`

Formato file: CSV con separatore `;` e virgolette come delimitatori.

## Utilizzo

1. Aggiorna i percorsi dei file CSV nella funzione `load_data()`:
```python
stazioni = pd.read_csv("percorso/stazioni.csv", sep=";", quotechar='"')
fermate = pd.read_csv("percorso/fermate.csv", sep=";", quotechar='"')
metro_fermate = pd.read_csv("percorso/metro_fermate.csv", sep=";", quotechar='"')
```

2. Esegui lo script:
```bash
python AnalisiDatiComuneMilano.py
```

3. La mappa viene salvata come `mappa_trasporti.html`

## Output

La mappa generata include:
- Stazioni principali: marker blu con popup informativi
- Fermate autobus: cerchi rossi
- Fermate metro: cerchi verdi

# BestConfiguration.py

## Descrizione

Script Python per l'analisi e visualizzazione dei risultati di grid search per modelli autoencoder. Il codice carica i dati di input, legge i risultati di un esperimento di grid search e identifica le migliori configurazioni basate sulla loss finale.

## Requisiti

- Python 3.x
- Polars
- GeoPandas (geopolars)
- Shapely
- Pandas
- JSON
- Pathlib


## Configurazione

Modifica le seguenti variabili nel codice:

```python
FINAL_FOLDER_NAME = "1"  # Nome cartella risultati
BASE_OUTPUT_DIR = "/percorso/base/output"  # Directory base risultati
CSV_PATH = "/percorso/dataset/tensore_5_1.csv"  # Path dataset input
```

## Utilizzo

1. Assicurati che i file CSV siano presenti nei percorsi specificati

2. Esegui lo script:
```bash
python BestConfiguration.py
```

## Funzionalità

### Analisi Dataset (`test1()`)
- Carica il dataset di input utilizzando Polars
- Visualizza le prime righe del dataset
- Mostra informazioni su colonne e tipi di dati
- Calcola statistiche descrittive
- Conta i valori nulli

### Analisi Risultati Grid Search
- Legge i risultati dal file `risultati_grid_search2.csv`
- Ordina le configurazioni per loss finale (crescente)
- Estrae e visualizza le top 5 configurazioni migliori

## Output

Lo script produce:

1. **Informazioni dataset**:
   - Prime righe del dataset
   - Schema delle colonne con tipi
   - Dimensioni del dataset
   - Statistiche descrittive
   - Conteggio valori nulli

2. **Top 5 configurazioni**:
   - Configurazione migliore (loss più bassa)
   - Quattro configurazioni successive per confronto

## Formato File CSV

### Dataset Input (tensore_5_1.csv)
- Separatore: `;`
- Formato: CSV standard con intestazioni

### Risultati Grid Search (risultati_grid_search2.csv)
- Deve contenere la colonna `final_loss`
- Ogni riga rappresenta una configurazione testata
- Altre colonne possono includere parametri del modello

## Note Tecniche

- Utilizza Polars per performance migliori su dataset grandi
- GeoPandas per supporto dati geospaziali se necessario
- Shapely per manipolazione geometrie
- Ordinamento basato su loss finale per identificare migliori performance

# grafici.py

## Descrizione

Script Python per la creazione di grafici e mappe per l'analisi di cluster ottenuti da algoritmi di clustering su dati di mobilità. Il codice genera visualizzazioni temporali (ore e giorni della settimana) e mappe geografiche per diversi cluster identificati tramite K-means con varie configurazioni.

## Requisiti

- Python 3.x
- Pandas
- Seaborn
- Matplotlib
- Plotly
- GeoPandas
- Contextily


## Configurazione

Modifica il percorso del file di input:
```python
final_path = "/percorso/al/tuo/file/tensore_5_1_with_clusters_2-1.csv"
```

## Formato Dati

Il file CSV deve contenere le seguenti colonne:
- `start_hour`: Ora di partenza (0-23)
- `weekday_num_start`: Giorno della settimana numerico (0-6, 0=Lunedì)
- `latitude_start`: Latitudine punto di partenza
- `longitude_start`: Longitudine punto di partenza
- `kmeans_labels_X`: Etichette cluster per diverse configurazioni K-means (X = numero cluster)

## Utilizzo

Esegui lo script:
```bash
python grafici.py
```

## Funzionalità Principali

### 1. Analisi Temporale Oraria (`plot_temporal_patterns`)
- Genera istogrammi della distribuzione delle ore di partenza
- Confronta più cluster sovrapposti
- Salva grafici come file JPG ad alta risoluzione

### 2. Analisi Giorni della Settimana (`plot_weekday_patterns`)
- Visualizza la distribuzione per giorni della settimana
- Mappa numerica: 0=Lunedì, 6=Domenica
- Barre affiancate per confronto cluster

### 3. Mappe Geografiche (`plot_cluster_map`)
- Crea mappe con punti colorati per cluster
- Utilizza basemap CartoDB Positron
- Sistema di coordinate Web Mercator (EPSG:3857)

### 4. Mappe Ottimizzate (`plot_cluster_map_k500_optimized`)
- Gestisce outlier geografici usando percentili
- Punti ingranditi per migliore visibilità
- Rimozione automatica valori estremi

### 5. Mappe Specializzate (`plot_cluster_map_k2000_large`)
- Funzione dedicata per cluster specifici
- Punti molto grandi con bordi definiti
- Colori vivaci per massima visibilità

## Configurazioni Cluster Supportate

Lo script analizza diverse configurazioni K-means:
- K=12: Cluster 2, 9
- K=50: Cluster 38, 39
- K=100: Cluster 20
- K=500: Cluster 50, 56, 237
- K=1000: Cluster 328, 810
- K=2000: Cluster 231, 511

## Output

### File Generati
- `temporal_pattern_combined_[cluster]_[k].jpg`: Grafici temporali orari
- `weekday_pattern_combined_[cluster]_[k].jpg`: Grafici giorni settimana
- `map_combined_clusters_[cluster]_[k].jpg`: Mappe geografiche standard
- `map_large_points_clusters_[cluster]_[k].jpg`: Mappe con punti ingranditi
- `map_optimized_clusters_[cluster]_[k].jpg`: Mappe ottimizzate

### Caratteristiche Grafici
- Risoluzione: 300 DPI
- Formato: JPG
- Palette colori: HSV e Set1 per distinguibilità
- Legende automatiche con etichette cluster

## Gestione Errori

- Controllo esistenza colonne richieste
- Verifica cluster non vuoti
- Fallback per download basemap
- Filtraggio outlier geografici automatico

## Personalizzazione

### Modifica Colori
```python
colors = ["#FF0000", "#0011FF", "#48FF00"]  # Personalizza colori cluster
```

### Dimensioni Grafici
```python
plt.figure(figsize=(12, 6))  # Modifica dimensioni figure
```

### Parametri Mappa
```python
markersize=16  # Dimensione punti
alpha=0.7      # Trasparenza
```

## Note Tecniche

- Proiezione geografica: WGS84 (EPSG:4326) → Web Mercator (EPSG:3857)
- Gestione memoria ottimizzata per dataset grandi
- Rimozione automatica outlier geografici (1° e 99° percentile)
- Basemap provider: CartoDB Positron per migliore leggibilità

# MappaInterattiva.py

## Descrizione

Script Python per la creazione di mappe interattive con controlli di animazione per visualizzare cluster di dati di mobilità. Genera mappe HTML con funzionalità di play/pause, controllo velocità e selezione cluster per analizzare punti di partenza e arrivo dei viaggi.

## Requisiti

- Python 3.x
- Pandas
- Folium
- Branca


## Configurazione

Modifica i percorsi nel codice:
```python
# Percorso file dati
final_path = "/percorso/al/tuo/file/tensore_5_1_with_clusters_2-1.csv"

# Percorso output mappe
output_path = "/percorso/output/mappa_cluster_start.html"
```

## Formato Dati

Il file CSV deve contenere le seguenti colonne:
- `id`: Identificativo univoco del record
- `latitude_start`: Latitudine punto di partenza
- `longitude_start`: Longitudine punto di partenza
- `latitude_end`: Latitudine punto di arrivo
- `longitude_end`: Longitudine punto di arrivo
- `kmeans_labels_10000`: Etichette cluster (configurabile)

## Utilizzo

1. Esegui lo script:
```bash
python MappaInterattiva.py
```

2. Scegli il tipo di mappa:
   - `1`: Mappa punti di partenza
   - `2`: Mappa punti di arrivo
   - `3`: Entrambe le mappe

3. Apri il file HTML generato in un browser

## Funzionalità Principali

### Generazione Mappe
- **start()**: Crea mappa interattiva per punti di partenza
- **end()**: Crea mappa interattiva per punti di arrivo
- Clustering automatico dei marker per performance ottimali
- Sistema di layer per ogni cluster

### Controlli Interattivi
La mappa include una console di controllo con:

#### Controlli Animazione
- **Play**: Avvia animazione sequenziale dei cluster
- **Pause**: Mette in pausa/riprende l'animazione
- **Stop**: Ferma e resetta l'animazione

#### Controlli Layer
- **Seleziona tutti**: Mostra tutti i cluster contemporaneamente
- **Deseleziona tutti**: Nasconde tutti i cluster

#### Controllo Velocità
- **Velocità 1x**: 2000ms tra cluster (lento)
- **Velocità 2x**: 1000ms tra cluster (normale)
- **Velocità 5x**: 400ms tra cluster (veloce)
- **Velocità 10x**: 200ms tra cluster (molto veloce)

### Caratteristiche Tecniche
- **MarkerCluster**: Raggruppamento automatico marker sovrapposti
- **LayerControl**: Pannello controllo layer espandibile
- **Popup**: Informazioni ID e cluster per ogni punto
- **Scala**: Controllo scala integrato

## Personalizzazione

### Colori Cluster
Modifica la palette colori:
```python
colori = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 
          'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue']
```

### Configurazione Cluster
Cambia la colonna cluster da analizzare:
```python
cluster_column = 'kmeans_labels_XXXX'  # Sostituisci XXXX con il numero desiderato
```

### Parametri Mappa
```python
zoom_start=12        # Livello zoom iniziale
control_scale=True   # Mostra controllo scala
```

### Velocità Animazione
Modifica i livelli di velocità:
```python
speedLevels = [2000, 1000, 400, 200]  # Millisecondi tra transizioni
```

## Output

### File Generati
- `mappa_cluster_start.html`: Mappa punti di partenza
- `mappa_cluster_end.html`: Mappa punti di arrivo

### Caratteristiche HTML
- Completamente interattivo in browser
- JavaScript integrato per controlli
- Responsive design
- Compatibile con tutti i browser moderni

## Interazione Utente

### Avvio Animazione
1. Cliccare "Play"
2. Inserire numero cluster di partenza quando richiesto
3. L'animazione mostrerà i cluster in sequenza

### Controllo Manuale
- Utilizzare il pannello layer per selezionare cluster specifici
- Combinare più cluster per confronti
- Zoom e pan per esplorare aree specifiche

## Gestione Performance

### Ottimizzazioni Implementate
- MarkerCluster per grandi dataset
- Layer separati per controllo memoria
- Caricamento lazy dei marker
- Animazione con controllo velocità

### Limitazioni
- Performance dipende dal numero di punti per cluster
- Browser limitato da memoria disponibile
- Animazione può rallentare con molti cluster attivi

## Risoluzione Problemi

### Mappa Non Si Carica
- Verificare percorsi file corretti
- Controllare formato CSV
- Assicurarsi che le colonne coordinate esistano

### Animazione Lenta
- Ridurre numero cluster visualizzati
- Aumentare velocità animazione
- Verificare risorse browser

### Marker Non Visibili
- Controllare valori coordinate validi
- Verificare zoom appropriato
- Assicurarsi che i cluster contengano dati

## Note Tecniche

- Sistema coordinate: WGS84 (EPSG:4326)
- Mappa base: OpenStreetMap via Folium
- Clustering: Algoritmo Leaflet MarkerCluster
- Controlli: JavaScript vanilla integrato
- Compatibilità: Tutti i browser moderni con JavaScript abilitato

# StudioDatiNIL.py

## Descrizione

Script Python per la visualizzazione di dati geografici NIL (Nuclei di Identità Locale) di Milano. Carica file GeoJSON e crea mappe interattive per l'analisi territoriale dei quartieri e zone amministrative della città.

## Requisiti

- Python 3.x
- GeoPandas
- Folium


## Configurazione

Modifica il percorso del file GeoJSON:
```python
file_path = r"c:\percorso\al\tuo\file\ds964_nil_wm.geojson"
```

## Formato Dati

Il file deve essere in formato GeoJSON standard contenente:
- Geometrie poligonali dei NIL
- Attributi descrittivi delle zone
- Sistema di coordinate compatibile (WGS84 raccomandato)

## Utilizzo

Esegui lo script:
```bash
python StudioDatiNil.py
```

Lo script genererà automaticamente una mappa interattiva visualizzabile nel browser.

## Funzionalità Principali

### Caricamento Dati (`load_geojson`)
- Legge file GeoJSON utilizzando GeoPandas
- Gestione errori per file non validi o percorsi inesistenti
- Verifica integrità dati geografici

### Creazione Mappa (`create_map`)
- Calcola automaticamente il centro della mappa dai centroidi delle geometrie
- Imposta zoom appropriato per visualizzazione ottimale
- Crea mappa base con Folium

### Visualizzazione
- Overlay GeoJSON sulla mappa base
- Geometrie poligonali per delimitazione NIL
- Mappa interattiva con controlli zoom e pan

## Caratteristiche Tecniche

### Sistema Coordinate
- Supporto per coordinate geografiche standard
- Calcolo automatico centroidi per centratura mappa
- Compatibilità con proiezioni comuni

### Mappa Interattiva
- Zoom iniziale: livello 12 (visualizzazione urbana)
- Tiles di base: OpenStreetMap
- Controlli interattivi standard Leaflet

### Gestione Errori
- Controllo esistenza file
- Verifica formato GeoJSON valido
- Messaggi informativi per debug

## Personalizzazione

### Parametri Mappa
```python
zoom_start=12    # Modifica livello zoom iniziale
```

### Stile Geometrie
Aggiungi stili personalizzati al GeoJSON:
```python
folium.GeoJson(
    gdf,
    style_function=lambda feature: {
        'fillColor': 'blue',
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.7
    }
).add_to(m)
```

### Popup Informativi
Aggiungi informazioni sui NIL:
```python
folium.GeoJson(
    gdf,
    popup=folium.Popup('Informazioni NIL', parse_html=True)
).add_to(m)
```

## Estensioni Possibili

### Analisi Dati
- Calcolo aree NIL
- Statistiche demografiche per zona
- Analisi distribuzione servizi

### Visualizzazioni Avanzate
- Colorazione per categorie NIL
- Heatmap popolazione/densità
- Layer multipli per confronti

### Interattività
- Click per informazioni dettagliate
- Filtri per tipologia NIL
- Search box per ricerca zone

## Output

Lo script produce una mappa interattiva che mostra:
- Confini dei NIL di Milano
- Geometrie poligonali precise
- Interfaccia web navigabile
- Controlli zoom e spostamento

## Dati NIL Milano

I NIL (Nuclei di Identità Locale) rappresentano:
- Suddivisione amministrativa di Milano
- 88 zone con identità territoriale specifica
- Base per analisi urbanistiche e sociali
- Riferimento per politiche territoriali

## Note Tecniche

- GeoPandas per manipolazione dati geospaziali
- Folium per mappe web interattive
- Supporto formato GeoJSON standard
- Compatibilità browser moderni
- Performance ottimizzata per dataset urbani

## Risoluzione Problemi

### File Non Trovato
- Verificare percorso corretto del file GeoJSON
- Controllare permessi di lettura
- Assicurarsi che il file esista

### Errore Formato
- Validare struttura GeoJSON
- Verificare sistema coordinate
- Controllare integrità geometrie

### Mappa Non Visualizzata
- Verificare installazione Folium
- Controllare connessione internet per tiles
- Assicurarsi browser JavaScript abilitato

# StudioDatiPoi

## Descrizione

Notebook Jupyter per l'analisi e visualizzazione dei Points of Interest (POI) della città di Milano utilizzando i dati di Overture Maps. Il progetto include caricamento dati da cloud, analisi geografiche, clustering e visualizzazioni interattive per lo studio della distribuzione spaziale dei punti di interesse urbani.

## Requisiti

### Librerie Python
- Pandas
- NumPy
- Seaborn
- Matplotlib
- GeoPandas
- Folium
- Shapely
- DuckDB
- GeoPy
- JupySQL
- DuckDB-engine

### Piattaforme Supportate
- Google Colab (consigliato)
- Jupyter Notebook

### Servizi Cloud
- Accesso a Amazon S3 (per dati Overture Maps)
- Google Drive (per storage su Colab)

## Installazione

### Google Colab (Automatica)
Il notebook installa automaticamente le dipendenze:
```python
platform = 'colab'
device = 'cpu'
```

### Jupyter Notebook Locale
```bash
pip install -r requirements.txt
```

Librerie richieste:
```bash
pip install geopandas folium shapely duckdb jupysql duckdb-engine geopy
```

## Configurazione

### 1. Selezione Piattaforma
Modifica i parametri nel notebook:
```python
platform = 'colab'  # o 'jupyter_notebook'
device = 'cpu'      # o 'cuda'
```

### 2. Configurazione Google Drive (Colab)
Il notebook si connette automaticamente a Google Drive per storage persistente.

### 3. Database DuckDB
Configurazione automatica per accesso ai dati Overture Maps via S3.

## Struttura Notebook

### 0. Configurazione Ambiente
- Installazione librerie
- Import dipendenze
- Configurazione piattaforma

### 1. Dataset
- Configurazione Google Drive
- Setup DuckDB e estensioni spatial
- Connessione a Overture Maps S3

### 2. Caricamento Dati POI
- Query dati Milano da Overture Maps
- Filtraggio per località italiana
- Export in formati CSV e GeoJSON

### 3. Analisi Geografica
- Verifica coordinate Milano
- Analisi distribuzione spaziale
- Calcoli geometrici con Shapely

### 4. Preprocessing Dati
- Pulizia dataset
- Standardizzazione categorie POI
- Preparazione per analisi

### 5. Analisi Esplorativa
- Statistiche descrittive
- Distribuzione categorie POI
- Analisi patterns spaziali

### 6. Clustering POI
- Algoritmi di raggruppamento geografico
- Identificazione zone ad alta densità
- Analisi cluster per tipologia

### 7. Visualizzazioni
- Mappe interattive con Folium
- Grafici distribuzione categorie
- Heatmap densità POI

## Dati Overture Maps

### Fonte
Overture Maps Foundation - Release 2025-02-19.0
- URL: s3://overturemaps-us-west-2/release/2025-02-19.0/theme=places/

### Struttura Dati POI
- `id`: Identificativo univoco
- `geometry`: Coordinate geografiche (Point)
- `names`: Nomi localizzati del POI
- `categories`: Categorie e tipologie
- `confidence`: Livello di confidenza dati
- `addresses`: Indirizzi completi

### Filtri Applicati
- Paese: Italia ('IT')
- Località: Milano
- Coordinate valide nel bounding box milanese

## Funzionalità Principali

### Query Dati
- Accesso diretto ai dati Overture Maps
- Filtraggio geografico Milano
- Export multipli formati (CSV, GeoJSON)

### Analisi Spaziale
- Verifica validità coordinate
- Calcolo distanze e densità
- Identificazione hotspot POI

### Categorizzazione
- Analisi tipologie POI
- Raggruppamento per settori
- Statistiche per categoria

### Visualizzazione
- Mappe interattive Folium
- Layer multipli per categoria
- Popup informativi dettagliati

## Output

### File Generati
- `sample_milano_places.csv`: Dataset POI in formato tabellare
- `sample_milano_places_map.geojson`: Dati geografici per mapping
- Grafici statistici salvati come immagini
- Mappe HTML interattive

### Visualizzazioni
- Distribuzione geografica POI
- Heatmap densità per zona
- Grafici categorie più frequenti
- Cluster analysis risultati

## Utilizzo

1. **Avvia il notebook** in Google Colab o Jupyter
2. **Esegui configurazione** ambiente (sezione 0)
3. **Configura database** DuckDB (sezione 1)
4. **Carica dati** Milano da Overture Maps
5. **Esegui analisi** sezioni sequenzialmente
6. **Visualizza risultati** mappe e grafici generati

## Personalizzazione

### Cambiare Città
Modifica il filtro geografico:
```sql
WHERE addresses[1].locality ILIKE 'NomeCittà'
```

### Categorie POI
Filtra per tipologie specifiche:
```sql
WHERE array_contains(categories, 'restaurant')
```

### Parametri Visualizzazione
```python
# Colori mappa
colors = ['red', 'blue', 'green']

# Dimensioni markers
marker_size = 5

# Zoom iniziale
zoom_start = 12
```

## Limitazioni

### Performance
- Query grandi dataset possono richiedere tempo
- Memoria limitata per visualizzazioni estese
- Dipendente da connessione internet stabile

### Dati
- Disponibilità dati varia per località
- Qualità dipende da contributi community
- Aggiornamenti periodici dataset

## Troubleshooting

### Errori Connessione S3
- Verificare configurazione AWS region
- Controllare estensioni DuckDB caricate
- Riavviare kernel se necessario

### Problemi Google Drive
- Autorizzare accesso Drive in Colab
- Verificare spazio storage disponibile
- Controllare percorsi file

### Errori Visualizzazione
- Verificare coordinate valide
- Controllare formato dati geometrici
- Aggiornare librerie GeoPandas/Folium

## Note Tecniche

- Sistema coordinate: WGS84 (EPSG:4326)
- Formato geometrie: Well-Known Text (WKT)
- Database: DuckDB con estensioni spatial
- Storage cloud: Amazon S3 + Google Drive
- Compatibilità: Python 3.7+

# SuddivisioneMesi

## Descrizione

Script Python per la suddivisione di dataset con periodi temporali estesi in file separati organizzati per mese. Processa dati di provider con date di inizio e fine, spezzando i periodi che attraversano più mesi e creando file CSV distinti per ogni mese.

## Requisiti

- Python 3.x
- Pandas

## Configurazione

Modifica i percorsi nel codice:
```python
# File di input
file_path = r'/percorso/al/file/202209-202311_provider_periods.csv'

# Cartella di output
output_folder = '/percorso/output/split_by_month'
```

## Formato Dati Input

Il file CSV deve contenere almeno le seguenti colonne:
- `start_date`: Data di inizio periodo (formato data)
- `end_date`: Data di fine periodo (formato data)
- Altre colonne: Vengono preservate nel file di output

Esempio formato date supportati:
- 'YYYY-MM-DD'
- 'YYYY-MM-DD HH:MM:SS'
- Formati standard riconosciuti da pandas

## Utilizzo

Esegui lo script:
```bash
python SuddivizioneMesi.py
```

Lo script processerà automaticamente tutti i record e creerà i file mensili.

## Funzionalità Principali

### Processamento Periodi
- **Caricamento dati**: Legge file CSV con periodi temporali
- **Conversione date**: Trasforma colonne date in formato datetime
- **Split periodi**: Divide periodi multi-mese in segmenti mensili

### Algoritmo Split
1. **Identificazione mesi**: Calcola tutti i mesi attraversati dal periodo
2. **Segmentazione**: Crea un record per ogni mese del periodo
3. **Preservazione dati**: Mantiene tutte le altre colonne del record originale
4. **Aggiustamento date**: Adatta start_date e end_date per ogni segmento

### Organizzazione Output
- **File per mese**: Un CSV per ogni mese presente nei dati
- **Nomenclatura**: Format 'YYYY-MM.csv' (es: '2022-09.csv')
- **Struttura**: Stessa struttura del file originale

## Esempio Funzionamento

### Input
```csv
id,start_date,end_date,provider,value
1,2022-09-15,2022-11-10,ProviderA,100
```

### Output
**2022-09.csv:**
```csv
id,provider,value,start_date,end_date
1,ProviderA,100,2022-09-15,2022-09-30
```

**2022-10.csv:**
```csv
id,provider,value,start_date,end_date
1,ProviderA,100,2022-10-01,2022-10-31
```

**2022-11.csv:**
```csv
id,provider,value,start_date,end_date
1,ProviderA,100,2022-11-01,2022-11-10
```

## Caratteristiche Tecniche

### Gestione Date
- Conversione automatica formati datetime
- Calcolo preciso confini mensili
- Preservazione informazioni temporali originali

### Algoritmo Split
```python
# Logica principale
while current <= end:
    month_start = current.replace(day=1)
    next_month_start = (month_start + pd.DateOffset(months=1))
    period_end = min(end, next_month_start - pd.Timedelta(days=1))
```

### Preservazione Dati
- Tutte le colonne originali vengono mantenute
- Solo date di inizio/fine vengono aggiornate
- Integrità referenziale preservata

## Casi d'Uso

### Analisi Temporali
- Suddivisione dati per reporting mensile
- Aggregazioni temporali specifiche
- Analisi trend su base mensile

### Data Processing
- Preparazione dati per sistemi di billing
- Segmentazione periodi per analisi performance
- Normalizzazione dataset temporali

### Ottimizzazione Storage
- File più piccoli per processing parallelo
- Caricamento selettivo per periodo
- Backup incrementali per mese

## Personalizzazione

### Modifica Periodo Split
```python
# Per settimane invece di mesi
period = split_df['start_date'].dt.to_period('W')

# Per giorni
period = split_df['start_date'].dt.to_period('D')
```

### Formato Nome File
```python
# Formato personalizzato
year_month_str = year_month.strftime('%Y_%m_data')
output_file = f'provider_{year_month_str}.csv'
```

### Filtri Aggiuntivi
```python
# Solo determinati provider
df_filtered = df[df['provider'].isin(['ProviderA', 'ProviderB'])]

# Solo periodi specifici
df_filtered = df[df['start_date'] >= '2022-01-01']
```

## Output

### File Generati
- Cartella `split_by_month/` creata automaticamente
- Un file CSV per ogni mese presente nei dati
- Nomenclatura: `YYYY-MM.csv`

### Informazioni Console
- Conferma completamento processamento
- Percorso cartella output
- Numero file generati

## Gestione Errori

### Validazione Input
- Controllo esistenza file input
- Verifica formato colonne date
- Gestione record con date invalide

### Robustezza
- Creazione automatica cartelle output
- Sovrascrittura sicura file esistenti
- Preservazione formato originale

## Limitazioni

### Performance
- Memory usage proporzionale a numero split
- Performance degrada con periodi molto lunghi
- Raccomandato per dataset <100k records

### Formato Date
- Richiede colonne `start_date` e `end_date`
- Formati date devono essere riconoscibili da pandas
- Timezone non gestito esplicitamente

## Note Tecniche

- Utilizza pandas DateOffset per calcoli mensili
- Gestione automatica anni bisestili
- Preservazione precision datetime originale
- Output CSV compatibile con Excel
- Encoding UTF-8 di default


# TensoreAutoencoder(Torch)

## Descrizione

Notebook Jupyter completo per l'analisi di dati di mobilità urbana utilizzando tecniche di deep learning. Il progetto implementa autoencoder con PyTorch per l'analisi dimensionale e clustering di dataset di viaggi, integrando preprocessing geospaziale, feature engineering temporali e visualizzazioni avanzate.

## Requisiti

### Librerie Python Core
- PyTorch (con supporto CUDA)
- Polars
- GeoPandas (geopolars)
- NumPy
- Pandas
- Scikit-learn

### Librerie Specializzate
- UMAP-learn
- Matplotlib
- Seaborn
- Folium
- Shapely
- Holidays

### Ambiente Esecuzione
- Google Colab (consigliato)
- Jupyter Notebook
- GPU CUDA compatibile (opzionale ma consigliato)

## Installazione

### Google Colab (Automatica)
Il notebook installa automaticamente tutte le dipendenze:
```python
!pip install --upgrade "pip<24.1"
!pip install polars==1.29.0 geopolars
!pip install torch scikit-learn matplotlib numpy
!pip install torch-xla
!pip install umap-learn holidays folium
```

### Ambiente Locale
```bash
pip install torch torchvision torchaudio
pip install polars geopolars shapely scikit-learn
pip install matplotlib seaborn folium umap-learn holidays
```

## Struttura Notebook

### 1. Inizializzazione
- Installazione librerie specializzate
- Import dipendenze
- Connessione Google Drive
- Configurazione ambiente PyTorch

### 2. Caricamento Dataset
- Estrazione file ZIP viaggi
- Caricamento dati con Polars
- Validazione formato e integrità

### 3. Preprocessing Geospaziale
- Parsing coordinate WKT (Well-Known Text)
- Estrazione latitudine/longitudine
- Validazione bounds geografici
- Conversione sistemi coordinate

### 4. Feature Engineering Temporale
- Estrazione componenti datetime
- Calcolo giorno settimana
- Identificazione festività italiane
- Calcolo durate effettive

### 5. Preprocessing Categorico
- One-hot encoding tipi veicolo
- Standardizzazione features numeriche
- Gestione valori mancanti
- Normalizzazione distribuzioni

### 6. Tensore Construction
- Creazione tensori PyTorch
- Reshape per autoencoder
- Split train/validation/test
- DataLoader configuration

### 7. Architettura Autoencoder
- Design encoder/decoder layers
- Implementazione loss functions
- Configurazione ottimizzatori
- Learning rate scheduling

### 8. Training Deep Learning
- Loop di training con validazione
- Monitoring loss curves
- Early stopping implementation
- Model checkpointing

### 9. Dimensionality Reduction
- Estrazione features latenti
- Applicazione UMAP/t-SNE
- Visualizzazione spazio ridotto
- Interpretazione componenti

### 10. Clustering Analysis
- K-means su features latenti
- Ottimizzazione numero cluster
- Valutazione metriche clustering
- Analisi interpretabilità cluster

### 11. Visualizzazioni
- Mappe interattive Folium
- Scatter plots dimensioni ridotte
- Heatmap correlazioni features
- Grafici distribuzione cluster

## Configurazione

### Percorsi File
```python
# File ZIP dati viaggi
file_path = Path("/content/drive/MyDrive/data/trips.zip")

# Directory output
output_dir = "/content/drive/MyDrive/AI_STAGE/results/"
```

### Parametri Autoencoder
```python
# Architettura rete
input_dim = 64  # Dimensione features input
hidden_dims = [32, 16, 8]  # Layers encoder
latent_dim = 4  # Dimensione spazio latente

# Training
batch_size = 128
learning_rate = 0.001
epochs = 100
```

### Parametri Clustering
```python
# Range numero cluster da testare
k_range = range(2, 50)

# Algoritmi dimensionality reduction
umap_params = {'n_neighbors': 15, 'min_dist': 0.1}
tsne_params = {'perplexity': 30, 'n_iter': 1000}
```

## Dati Input

### Formato Dataset
- File ZIP contenente CSV viaggi
- Coordinate in formato WKT
- Timestamp in formato datetime
- Campi categorici per tipo veicolo

### Colonne Richieste
- `geom_wkt_raw_start_point`: Coordinate partenza
- `geom_wkt_raw_end_point`: Coordinate arrivo  
- `local_ts_start`: Timestamp inizio
- `local_ts_end`: Timestamp fine
- `type_vehicle`: Tipologia veicolo (C/B/M/S)

## Funzionalità Principali

### Preprocessing Avanzato
- Parsing automatico coordinate geospaziali
- Feature engineering temporali complesse
- Gestione festività nazionali italiane
- Normalizzazione multi-dimensionale

### Deep Learning Pipeline
- Autoencoder personalizzato PyTorch
- Training con early stopping
- Hyperparameter optimization
- Model evaluation metrics

### Clustering Intelligente
- Determinazione automatica K ottimale
- Multiple evaluation metrics
- Silhouette/Davies-Bouldin/Calinski-Harabasz
- Interpretazione cluster geografica

### Visualizzazioni Interattive
- Mappe Folium con cluster colorati
- Scatter plots dimensioni ridotte
- Animazioni temporali pattern
- Dashboard analisi risultati

## Output

### File Generati
- `tensore_processed.csv`: Dataset preprocessato
- `autoencoder_model.pth`: Modello PyTorch salvato
- `latent_features.npy`: Features spazio latente
- `cluster_results.csv`: Assegnazioni cluster
- `evaluation_metrics.json`: Metriche performance

### Visualizzazioni
- Mappe HTML interattive per cluster
- Grafici loss/convergenza training
- Plots distribuzione features latenti
- Heatmap correlazioni spazio ridotto

## Casi d'Uso

### Mobilità Urbana
- Identificazione pattern di spostamento
- Segmentazione utenti per tipologia
- Analisi temporale comportamenti
- Ottimizzazione servizi trasporto

### Analisi Comportamentale
- Clustering viaggi per similitudine
- Identificazione anomalie pattern
- Previsione destinazioni probabili
- Personalizzazione raccomandazioni

### Urban Planning
- Identificazione hotspot mobilità
- Analisi distribuzione geospaziale
- Ottimizzazione infrastrutture
- Valutazione impatto interventi

## Personalizzazione

### Architettura Autoencoder
```python
class CustomAutoencoder(nn.Module):
    def __init__(self, input_dim, hidden_dims, latent_dim):
        super().__init__()
        # Personalizza layers encoder/decoder
        self.encoder = nn.Sequential(...)
        self.decoder = nn.Sequential(...)
```

### Feature Engineering
```python
# Aggiungi nuove features temporali
df = df.with_columns([
    pl.col("timestamp").dt.hour().alias("hour"),
    pl.col("timestamp").dt.season().alias("season")
])
```

### Clustering Algorithms
```python
# Prova algoritmi alternativi
from sklearn.cluster import DBSCAN, AgglomerativeClustering
```

## Performance

### Ottimizzazioni Implementate
- Utilizzo Polars per processamento veloce
- Batch processing per memoria efficiente
- GPU acceleration con PyTorch CUDA
- Early stopping per prevenire overfitting

### Scalabilità
- Support dataset fino a milioni di record
- Memory-efficient data loading
- Parallel processing dove possibile
- Progressive training per dataset grandi

## Limitazioni

### Hardware
- GPU consigliata per training efficiente
- Memoria RAM proporzionale a dataset size
- Storage per modelli e risultati intermedi

### Dati
- Richiede coordinate geografiche valide
- Formato timestamp standardizzato
- Qualità dipende da completezza dataset

## Note Tecniche

- Framework: PyTorch per deep learning
- Coordinate: Supporto WKT e proiezioni standard
- Clustering: Implementazione scalabile con scikit-learn
- Visualizzazione: Folium per mappe interattive web
- Storage: Compatibilità Google Drive e storage locali


# UnisciFile.py 

## Descrizione

Script Python per l'analisi di file CSV di grandi dimensioni con rilevamento automatico dei formati datetime. Processa dataset voluminosi utilizzando chunk processing per identificare i formati delle colonne temporali e fornire statistiche sui pattern di data/ora presenti nei dati.

## Requisiti

- Python 3.x
- Pandas
- Collections (libreria standard)


## Configurazione

Modifica il percorso del file nel codice:
```python
file_path = "/percorso/al/tuo/file/gigante.csv"
```

## Funzionalità Principali

### Rilevamento Formati DateTime
Lo script supporta il riconoscimento automatico di numerosi formati datetime:

#### Formati ISO e Standard
- `%Y-%m-%d %H:%M:%S.%f` - 2023-12-25 14:30:15.123456
- `%Y-%m-%d %H:%M:%S` - 2023-12-25 14:30:15
- `%Y-%m-%dT%H:%M:%SZ` - 2023-12-25T14:30:15Z
- `%Y-%m-%dT%H:%M:%S.%fZ` - 2023-12-25T14:30:15.123Z

#### Formati Locali
- `%d/%m/%Y %H:%M:%S` - 25/12/2023 14:30:15
- `%d.%m.%Y %H:%M:%S` - 25.12.2023 14:30:15
- `%m-%d-%Y %I:%M:%S %p` - 12-25-2023 02:30:15 PM

#### Formati Estesi
- `%d %b %Y %H:%M:%S` - 25 Dec 2023 14:30:15
- `%d %B %Y %H:%M:%S` - 25 December 2023 14:30:15

#### Formati Speciali
- `%s` - Unix timestamp (secondi da epoch)
- `%Y-%m-%d %H:%M:%S %Z` - Con timezone
- `%Y-%m-%dT%H:%M:%S%z` - Con offset timezone

### Chunk Processing
- Processamento a blocchi per file di grandi dimensioni
- Gestione memoria ottimizzata
- Configurabile dimensione chunk

### Analisi Statistica
- Conteggio occorrenze per formato
- Identificazione pattern dominanti
- Rilevamento formati sconosciuti

## Utilizzo

### Esecuzione Base
```bash
python Unisci_file.py
```

### Personalizzazione Chunk Size
```python
chunk_size = 100000  # Modifica dimensione chunk
```

## Colonne Analizzate

Lo script cerca specificamente le colonne:
- `local_ts_start`: Timestamp di inizio
- `local_ts_end`: Timestamp di fine

## Output

### Formato Report
```
📊 Formati rilevati per 'local_ts_start':
  %Y-%m-%d %H:%M:%S: 50000 occorrenze
  %d/%m/%Y %H:%M:%S: 25000 occorrenze
  UNKNOWN: 1000 occorrenze

📊 Formati rilevati per 'local_ts_end':
  %Y-%m-%d %H:%M:%S: 48000 occorrenze
  %d/%m/%Y %H:%M:%S: 27000 occorrenze
  INVALID: 500 occorrenze
```

### Categorie Speciali
- **INVALID**: Valori NaN, None, NaT
- **UNKNOWN**: Formati non riconosciuti
- **Formati Standard**: Pattern identificati con successo

## Funzioni Principali

### `detect_date_format(date_str)`
Rileva automaticamente il formato datetime di una stringa:
- Input: Stringa contenente data/ora
- Output: Formato datetime corrispondente
- Gestisce valori nulli e invalidi

### Chunk Processing Loop
```python
for chunk in pd.read_csv(file_path, chunksize=chunk_size):
    # Processa ogni chunk separatamente
    # Accumula statistiche formato
```

## Gestione Errori

### Valori Problematici
- **NaN/None/NaT**: Categorizzati come INVALID
- **Formati sconosciuti**: Etichettati come UNKNOWN
- **Errori parsing**: Gestiti con try/except

### Memoria e Performance
- Chunk processing per file grandi
- Evita caricamento completo in memoria
- Progress implicito tramite chunk

## Personalizzazione

### Aggiungere Nuovi Formati
```python
possible_formats = [
    # Formati esistenti...
    "%d-%m-%Y %H:%M",      # Nuovo formato personalizzato
    "%Y%m%d%H%M%S",        # Formato compatto
]
```

### Modificare Colonne Target
```python
# Cambia colonne da analizzare
timestamp_cols = ['start_time', 'end_time', 'created_at']
```

### Dimensione Chunk Dinamica
```python
import os
file_size = os.path.getsize(file_path)
chunk_size = min(100000, file_size // 1000)  # Adatta a dimensione file
```

## Casi d'Uso

### Data Quality Assessment
- Identificazione inconsistenze formato
- Validazione integrità temporale
- Preparazione normalizzazione dati

### Data Migration
- Analisi formato prima conversione
- Identificazione pattern specifici
- Pianificazione strategie parsing

### ETL Pipeline
- Preprocessing automatico formati
- Validazione dati temporali
- Standardizzazione datetime

## Limitazioni

### Performance
- Velocità dipende da dimensione file
- CPU intensive per molti formati
- Memoria limitata da chunk size

### Formati Supportati
- Solo formati in lista predefinita
- Non rileva formati custom automaticamente
- Sensibile a variazioni minori formato

## Estensioni Possibili

### Report Dettagliato
```python
# Aggiungi statistiche aggiuntive
print(f"Total rows processed: {total_rows}")
print(f"Invalid values percentage: {invalid_pct}%")
```

### Auto-Fix Formati
```python
# Conversione automatica formato dominante
dominant_format = formats_start.most_common(1)[0][0]
df['local_ts_start'] = pd.to_datetime(df['local_ts_start'], format=dominant_format)
```

### Export Risultati
```python
# Salva risultati analisi
results = {
    'start_formats': dict(formats_start),
    'end_formats': dict(formats_end)
}
import json
with open('format_analysis.json', 'w') as f:
    json.dump(results, f, indent=2)
```

## Note Tecniche

- Utilizza pandas.read_csv con chunksize per efficienza memoria
- Counter per aggregazione veloce statistiche
- Gestione robust errori parsing datetime
- Compatibile con file CSV standard e varianti
- Performance ottimizzata per dataset multi-gigabyte


