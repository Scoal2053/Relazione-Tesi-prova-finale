import geopandas as gpd
import folium

# Caricamento del file GeoJSON
def load_geojson(file_path):
    try:
        gdf = gpd.read_file(file_path)
        return gdf
    except Exception as e:
        print(f"Errore nel caricamento del file GeoJSON: {e}")
        return None

# Creazione della mappa interattiva
def create_map(gdf):
    # Calcola il centro della mappa
    center = [gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()]
    
    # Crea la mappa
    m = folium.Map(location=center, zoom_start=12)
    
    # Aggiungi i dati GeoJSON alla mappa
    folium.GeoJson(gdf).add_to(m)
    
    return m

# Esecuzione
file_path = r"c:\Users\hp\Desktop\NIL\ds964_nil_wm.geojson"  # Sostituisci con il nome del tuo file GeoJSON
gdf = load_geojson(file_path)
if gdf is not None:
    mappa = create_map(gdf)
    # Mostra la mappa
    mappa