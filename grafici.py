import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

final_path = "/mnt/c/Users/hp/Desktop/AI STAGE/Tensore/tensore_5_1_with_clusters_2-1.csv"
df = pd.read_csv(final_path, sep=";")

print(df.columns)





import matplotlib.pyplot as plt
import seaborn as sns

def plot_temporal_patterns(df, cluster_col, labels, title_suffix):
    # Mappa numerica dei giorni della settimana (0 = lunedì)
    weekday_map = {
        0: 'Lunedì', 1: 'Martedì', 2: 'Mercoledì', 3: 'Giovedì',
        4: 'Venerdì', 5: 'Sabato', 6: 'Domenica'
    }

    # Palette di colori diversa per ogni cluster
    palette = sns.color_palette("hsv", len(labels))

    plt.figure(figsize=(12, 6))

    # Prepara i dati per tutti i cluster insieme
    plot_data = []
    for label in labels:
        subset = df[df[cluster_col] == label].copy()
        if 'start_hour' in subset.columns and len(subset) > 0:
            subset['cluster_label'] = f'Cluster {label}'
            plot_data.append(subset[['start_hour', 'cluster_label']])
        else:
            print(f"[!] 'start_hour' non trovato o cluster vuoto per {label} ({title_suffix}), salto...")
            continue
    
    if plot_data:
        combined_data = pd.concat(plot_data, ignore_index=True)
        print(f"[INFO] Dati trovati per {len(plot_data)} cluster: {combined_data['cluster_label'].unique()}")
        
        # Verifica che ci siano effettivamente dati da plottare
        if len(combined_data) == 0:
            print(f"[!] Dataset combinato vuoto per i cluster {labels} ({title_suffix})")
            plt.close()
            return
        
        # Grafico con barre affiancate per ciascun cluster
        sns.histplot(
            data=combined_data,
            x='start_hour', 
            hue='cluster_label',
            bins=range(0, 25),  # 0-24 per avere le etichette 0–23
            kde=False, 
            multiple='dodge',  # Affiancare le barre invece di sovrapporle
            palette=palette[:len(plot_data)],
            alpha=0.8  # Ridotto la trasparenza visto che non si sovrappongono più
        )
        
        plt.title(f'Distribuzione ore di partenza ({title_suffix})')
        plt.xlabel('Ora del giorno (Da Mezzanotte alle 23 di Sera)')
        plt.ylabel('Frequenza')
        plt.xticks(range(0, 24))
        
        # Gestione più robusta della legenda
        handles, labels_legend = plt.gca().get_legend_handles_labels()
        if handles:
            plt.legend()
        else:
            print(f"[!] Nessuna etichetta trovata per la legenda ({title_suffix})")
        
        plt.tight_layout()
    else:
        print(f"[!] Nessun dato valido trovato per i cluster {labels} ({title_suffix})")
        plt.close()
        return

    # Salvataggio con nome coerente
    filename = f"temporal_pattern_combined_{'_'.join(map(str, labels))}_{title_suffix.replace(' ', '_')}.jpg"
    plt.savefig(filename, dpi=300)
    plt.close()
    print("fatto")





# Esegui
plot_temporal_patterns(df, 'kmeans_labels_UMAP2D', [2, 9], 'k=12')

import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt

def plot_cluster_map(df, cluster_col, labels, title_suffix):
    subset = df[df[cluster_col].isin(labels)].copy()
    gdf = gpd.GeoDataFrame(
        subset,
        geometry=gpd.points_from_xy(subset.longitude_start, subset.latitude_start),
        crs="EPSG:4326"
    ).to_crs(epsg=3857)

    # Palette di colori per i cluster
    colors = plt.cm.Set1(range(len(labels)))
    
    fig, ax = plt.subplots(figsize=(10, 10))
    for i, label in enumerate(labels):
        cluster_data = gdf[gdf[cluster_col] == label]
        cluster_data.plot(
            ax=ax,
            markersize=2,
            color=colors[i],
            alpha=0.6,
            label=f'Cluster {label}'
        )
    
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)
    ax.set_title(f'Mappa start - Clusters {labels} ({title_suffix})')
    ax.axis('off')
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"map_combined_clusters_{'_'.join(map(str, labels))}_{title_suffix.replace(' ', '_')}.jpg", dpi=300)
    plt.close()
    print("fatto")

def plot_cluster_map_k2000_large(df, cluster_col, labels, title_suffix):
    """
    Funzione specializzata per plottare i cluster 231 e 511 di k=2000 
    con punti più grandi e visibili sulla mappa
    """
    subset = df[df[cluster_col].isin(labels)].copy()
    gdf = gpd.GeoDataFrame(
        subset,
        geometry=gpd.points_from_xy(subset.longitude_start, subset.latitude_start),
        crs="EPSG:4326"
    ).to_crs(epsg=3857)

    # Palette di colori per i cluster - colori più vivaci
    colors = ["#FF7300", '#4444FF']  # Rosso e blu intensi per migliore visibilità
    
    fig, ax = plt.subplots(figsize=(12, 12))  # Figura più grande
    
    for i, label in enumerate(labels):
        cluster_data = gdf[gdf[cluster_col] == label]
        cluster_data.plot(
            ax=ax,
            markersize=16,  # Punti molto più grandi (era 2)
            color=colors[i],
            alpha=0.8,  # Più opaco per migliore visibilità
            label=f'Cluster {label}',
            edgecolors='black',  # Bordo nero per definire meglio i punti
            linewidth=0.5  # Spessore del bordo
        )
    
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)
    ax.set_title(f'Mappa start - Clusters {labels} ({title_suffix}) - Punti Ingranditi', fontsize=14)
    ax.axis('off')
    
    # Legenda più grande e visibile
    legend = ax.legend(fontsize=12, markerscale=1.5)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_alpha(0.9)
    
    plt.tight_layout()
    plt.savefig(f"map_large_points_clusters_{'_'.join(map(str, labels))}_{title_suffix.replace(' ', '_')}.jpg", dpi=300, bbox_inches='tight')
    plt.close()
    print("Mappa con punti ingranditi creata!")



# Esegui

def plot_weekday_patterns(df, cluster_col, labels, title_suffix):
    # Mappa numerica dei giorni della settimana (0 = lunedì)
    weekday_map = {
        0: 'Lunedì', 1: 'Martedì', 2: 'Mercoledì', 3: 'Giovedì',
        4: 'Venerdì', 5: 'Sabato', 6: 'Domenica'
    }

    # Palette di colori diversa per ogni cluster
    palette = sns.color_palette("hsv", len(labels))

    plt.figure(figsize=(12, 6))

    # Prepara i dati per tutti i cluster insieme
    plot_data = []
    for label in labels:
        subset = df[df[cluster_col] == label].copy()
        if 'weekday_num_start' in subset.columns and len(subset) > 0:
            subset['cluster_label'] = f'Cluster {label}'
            # Aggiungi il nome del giorno per una migliore visualizzazione
            subset['weekday_name'] = subset['weekday_num_start'].map(weekday_map)
            plot_data.append(subset[['weekday_num_start', 'weekday_name', 'cluster_label']])
        else:
            print(f"[!] 'weekday_num_start' non trovato o cluster vuoto per {label} ({title_suffix}), salto...")
            continue
    
    if plot_data:
        combined_data = pd.concat(plot_data, ignore_index=True)
        print(f"[INFO] Dati trovati per {len(plot_data)} cluster: {combined_data['cluster_label'].unique()}")
        
        # Verifica che ci siano effettivamente dati da plottare
        if len(combined_data) == 0:
            print(f"[!] Dataset combinato vuoto per i cluster {labels} ({title_suffix})")
            plt.close()
            return
        
        # Grafico con barre affiancate per ciascun cluster
        sns.histplot(
            data=combined_data,
            x='weekday_num_start', 
            hue='cluster_label',
            bins=range(0, 8),  # 0-7 per i giorni della settimana (0-6)
            kde=False, 
            multiple='dodge',  # Affiancare le barre invece di sovrapporle
            palette=palette[:len(plot_data)],
            alpha=0.8
        )
        
        plt.title(f'Distribuzione giorni della settimana ({title_suffix})')
        plt.xlabel('Giorno della settimana')
        plt.ylabel('Frequenza')
        
        # Imposta le etichette dei giorni della settimana sull'asse x
        plt.xticks(range(0, 7), [weekday_map[i] for i in range(7)], rotation=45)
        
        # Gestione più robusta della legenda
        handles, labels_legend = plt.gca().get_legend_handles_labels()
        if handles:
            plt.legend()
        else:
            print(f"[!] Nessuna etichetta trovata per la legenda ({title_suffix})")
        
        plt.tight_layout()
    else:
        print(f"[!] Nessun dato valido trovato per i cluster {labels} ({title_suffix})")
        plt.close()
        return

    # Salvataggio con nome coerente
    filename = f"weekday_pattern_combined_{'_'.join(map(str, labels))}_{title_suffix.replace(' ', '_')}.jpg"
    plt.savefig(filename, dpi=300)
    plt.close()
    print("fatto")



# Esegui

def main(): 
    plot_temporal_patterns(df, 'kmeans_labels_UMAP2D', [2, 9], 'k=12')
    plot_weekday_patterns(df, 'kmeans_labels_UMAP2D', [2, 9], 'k=12')
    plot_cluster_map(df, 'kmeans_labels_UMAP2D', [2, 9], 'k=12')
    plot_cluster_map(df, 'kmeans_labels_50', [38, 39], 'k=50')
    plot_weekday_patterns(df, 'kmeans_labels_50', [38, 39], 'k=50')
    plot_cluster_map(df, 'kmeans_labels_100', [20], 'k=100')
    plot_weekday_patterns(df, 'kmeans_labels_100', [20], 'k=100')
    plot_cluster_map(df, 'kmeans_labels_1000', [328, 810], 'k=1000')
    plot_weekday_patterns(df, 'kmeans_labels_1000', [328, 810], 'k=1000')
    plot_weekday_patterns(df, 'kmeans_labels_2000', [231, 511], 'k=2000')
    plot_cluster_map(df, 'kmeans_labels_2000', [231, 511], 'k=2000')
    # Mappa specializzata con punti più grandi per i cluster 231 e 511
    plot_cluster_map_k2000_large(df, 'kmeans_labels_2000', [231, 511], 'k=2000')


plot_cluster_map(df, 'kmeans_labels_500', [50, 56, 237], 'k=500')


def plot_cluster_map_k500_optimized(df, cluster_col, labels, title_suffix):
    """
    Funzione specializzata per k=500 che gestisce meglio gli outlier geografici
    usando matplotlib/geopandas senza dipendenze di Plotly/Kaleido
    """
    subset = df[df[cluster_col].isin(labels)].copy()
    
    # Calcola i percentili per limitare la vista e ridurre l'effetto degli outlier
    lat_min, lat_max = subset['latitude_start'].quantile([0.01, 0.99])
    lon_min, lon_max = subset['longitude_start'].quantile([0.01, 0.99])
    
    # Filtra i dati per rimuovere outlier estremi usando .loc per evitare warning
    subset_filtered = subset.loc[
        (subset['latitude_start'] >= lat_min) & 
        (subset['latitude_start'] <= lat_max) &
        (subset['longitude_start'] >= lon_min) & 
        (subset['longitude_start'] <= lon_max)
    ].copy()
    
    # Crea il GeoDataFrame
    gdf = gpd.GeoDataFrame(
        subset_filtered,
        geometry=gpd.points_from_xy(subset_filtered.longitude_start, subset_filtered.latitude_start),
        crs="EPSG:4326"
    ).to_crs(epsg=3857)
    
    # Colori vivaci e distinti per ogni cluster
    colors = ["#FF0000", "#0011FF", "#48FF00"]  # Rosso, Teal, Blu
    
    fig, ax = plt.subplots(figsize=(14, 10))  # Figura più grande
    
    for i, label in enumerate(labels):
        cluster_data = gdf[gdf[cluster_col] == label]
        if len(cluster_data) > 0:
            cluster_data.plot(
                ax=ax,
                markersize=16,  # Punti più grandi per migliore visibilità
                color=colors[i],
                alpha=0.7,
                label=f'Cluster {label}',
                edgecolors='white',  # Bordo bianco per distinguere meglio
                linewidth=0.3
            )
    
    # Aggiungi basemap centrata sui dati filtrati
    try:
        ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom='auto')
    except:
        # Fallback se non riesce a scaricare la mappa
        print("Warning: Impossibile scaricare la basemap, continuo senza...")
        ax.set_facecolor('lightgray')
    
    ax.set_title(f'Mappa Clusters {labels} ({title_suffix})', 
                fontsize=16)
    ax.axis('off')
    
    # Legenda migliorata
    legend = ax.legend(fontsize=12, markerscale=2, 
                      loc='upper right', frameon=True, 
                      fancybox=True, shadow=True)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_alpha(0.9)
    
    plt.tight_layout()
    
    # Salva l'immagine
    filename = f"map_optimized_clusters_{'_'.join(map(str, labels))}_{title_suffix.replace(' ', '_')}.jpg"
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"Mappa ottimizzata salvata: {filename}")
    print(f"Punti visualizzati: {len(subset_filtered)} / {len(subset)} totali")
    print(f"Outlier rimossi: {len(subset) - len(subset_filtered)}")

# Esegui la funzione ottimizzata
plot_cluster_map_k500_optimized(df, 'kmeans_labels_500', [50, 56, 237], 'k=500')

