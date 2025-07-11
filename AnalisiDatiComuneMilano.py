import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import Point

# Caricamento dei file CSV
def load_data():
    try:
        stazioni = pd.read_csv("/mnt/c/Users/hp/Desktop/DatiMezziPubblici/sistema_ferroviario_urbano_layer_0_stazioni__final.csv", sep=";", quotechar='"')
        fermate = pd.read_csv("/mnt/c/Users/hp/Desktop/DatiMezziPubblici/tpl_fermate.csv", sep=";", quotechar='"')
        metro_fermate = pd.read_csv("/mnt/c/Users/hp/Desktop/DatiMezziPubblici/tpl_metrofermate.csv", sep=";", quotechar='"')
        return stazioni, fermate, metro_fermate
    except Exception as e:
        print(f"Errore nel caricamento dei dati: {e}")
        return None, None, None

# Creazione di GeoDataFrame
def create_geodataframes(stazioni, fermate, metro_fermate):
    try:
        stazioni_gdf = gpd.GeoDataFrame(stazioni, geometry=gpd.points_from_xy(stazioni['LONG_X_4326'], stazioni['LAT_Y_4326']), crs="EPSG:4326")
        fermate_gdf = gpd.GeoDataFrame(fermate, geometry=gpd.points_from_xy(fermate['LONG_X_4326'], fermate['LAT_Y_4326']), crs="EPSG:4326")
        metro_fermate_gdf = gpd.GeoDataFrame(metro_fermate, geometry=gpd.points_from_xy(metro_fermate['LONG_X_4326'], metro_fermate['LAT_Y_4326']), crs="EPSG:4326")
        return stazioni_gdf, fermate_gdf, metro_fermate_gdf
    except KeyError as e:
        print(f"Errore nelle colonne dei dati: {e}")
        return None, None, None

# Creazione della mappa
def create_map(stazioni_gdf, fermate_gdf, metro_fermate_gdf):
    m = folium.Map(location=[stazioni_gdf.geometry.y.mean(), stazioni_gdf.geometry.x.mean()], zoom_start=12)

    # Aggiunta dei marker per le stazioni
    for _, row in stazioni_gdf.iterrows():
        folium.Marker([row.geometry.y, row.geometry.x], popup=row['Stazione'], icon=folium.Icon(color='blue')).add_to(m)

    # Aggiunta dei marker per le fermate bus
    for _, row in fermate_gdf.iterrows():
        folium.CircleMarker([row.geometry.y, row.geometry.x], radius=3, color='red', fill=True, fill_color='red').add_to(m)

    # Aggiunta dei marker per le fermate metro
    for _, row in metro_fermate_gdf.iterrows():
        folium.CircleMarker([row.geometry.y, row.geometry.x], radius=4, color='green', fill=True, fill_color='green').add_to(m)

    return m

# Esecuzione
stazioni, fermate, metro_fermate = load_data()
if stazioni is not None:
    stazioni_gdf, fermate_gdf, metro_fermate_gdf = create_geodataframes(stazioni, fermate, metro_fermate)
    if stazioni_gdf is not None:
        mappa = create_map(stazioni_gdf, fermate_gdf, metro_fermate_gdf)
        mappa.save("mappa_trasporti.html")
        print("Mappa salvata con successo!")

# Blu stazioni ferroviarie
# Rosso fermate bus
# Verde fermate metro

# fare 3 mappe distinte