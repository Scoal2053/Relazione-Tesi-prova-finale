import pandas as pd
import folium
from folium.plugins import MarkerCluster
import branca
final_path = "" # Inserisci il percorso del file CSV qui del tensore con i cluster
def start():
    df = pd.read_csv(final_path, sep=";")

    # Parametri
    cluster_column = 'kmeans_labels_10000'
    clusters = sorted(df[cluster_column].unique())
    colori = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred',
            'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white',
            'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']

    # Mappa
    m = folium.Map(location=[df['latitude_start'].mean(), df['longitude_start'].mean()],
                zoom_start=12, control_scale=True)

    # MarkerCluster per ogni cluster
    for i, cluster in enumerate(clusters):
        cluster_df = df[df[cluster_column] == cluster]
        fg = folium.FeatureGroup(name=f"Cluster {cluster}", show=False)
        marker_cluster = MarkerCluster()

        for _, row in cluster_df.iterrows():
            folium.Marker(
                location=[row['latitude_start'], row['longitude_start']],
                popup=f"ID: {row['id']}<br>Cluster: {cluster}",
                icon=folium.Icon(color=colori[i % len(colori)])
            ).add_to(marker_cluster)

        marker_cluster.add_to(fg)
        fg.add_to(m)

    # Layer control
    folium.LayerControl(collapsed=False).add_to(m)

    # JavaScript per controlli
    js_code = """
    <script>
    window.onload = function() {
        let interval = null;
        let currentIndex = 0;
        let paused = false;
        let speedLevels = [2000, 1000, 400, 200];
        let currentSpeedIndex = 0;
        let checkboxes = [];

        function setAllLayers(checked) {
            checkboxes = document.querySelectorAll('.leaflet-control-layers-overlays input');
            checkboxes.forEach(function(cb) {
                if (cb.checked !== checked) cb.click();
            });
        }

        function updateInterval() {
            if (interval) {
                clearInterval(interval);
                interval = setInterval(() => {
                    if (paused) return;
                    setAllLayers(false);
                    if (currentIndex >= checkboxes.length) {
                        clearInterval(interval);
                        return;
                    }
                    checkboxes[currentIndex].click();
                    currentIndex++;
                }, speedLevels[currentSpeedIndex]);
            }
        }

        function startAnimation() {
            checkboxes = document.querySelectorAll('.leaflet-control-layers-overlays input');
            const startCluster = prompt(`Da quale cluster vuoi iniziare? Inserisci un numero da 0 a ${checkboxes.length - 1}:`);
            if (!startCluster || isNaN(startCluster) || startCluster < 0 || startCluster >= checkboxes.length) {
                alert("Cluster non valido.");
                return;
            }

            currentIndex = parseInt(startCluster);
            setAllLayers(false);
            paused = false;

            if (interval) clearInterval(interval);

            interval = setInterval(() => {
                if (paused) return;
                setAllLayers(false);
                if (currentIndex >= checkboxes.length) {
                    clearInterval(interval);
                    return;
                }
                checkboxes[currentIndex].click();
                currentIndex++;
            }, speedLevels[currentSpeedIndex]);
        }

        function pauseAnimation() {
            paused = !paused;
        }

        function stopAnimation() {
            if (interval) {
                clearInterval(interval);
                interval = null;
            }
            currentIndex = 0;
            paused = false;
            setAllLayers(false);
        }

        function toggleSpeed() {
            currentSpeedIndex = (currentSpeedIndex + 1) % speedLevels.length;
            updateInterval();
            speedButton.innerHTML = `⏩ Velocità ${getSpeedLabel()}`;
        }

        function getSpeedLabel() {
            switch (currentSpeedIndex) {
                case 0: return "1x";
                case 1: return "2x";
                case 2: return "5x";
                case 3: return "10x";
                default: return "1x";
            }
        }

        var buttonBox = document.createElement('div');
        buttonBox.style.position = 'absolute';
        buttonBox.style.bottom = '20px';
        buttonBox.style.left = '20px';
        buttonBox.style.backgroundColor = 'white';
        buttonBox.style.border = '1px solid #ccc';
        buttonBox.style.borderRadius = '8px';
        buttonBox.style.padding = '10px';
        buttonBox.style.zIndex = 1000;
        buttonBox.style.boxShadow = '2px 2px 8px rgba(0,0,0,0.3)';
        buttonBox.style.display = 'flex';
        buttonBox.style.flexDirection = 'column';
        buttonBox.style.gap = '5px';
        buttonBox.style.fontFamily = 'Arial, sans-serif';
        buttonBox.style.fontSize = '13px';

        function makeButton(label, onClick) {
            var btn = document.createElement('button');
            btn.innerHTML = label;
            btn.onclick = onClick;
            btn.style.padding = '6px 10px';
            btn.style.cursor = 'pointer';
            btn.style.border = '1px solid #888';
            btn.style.borderRadius = '5px';
            btn.style.background = '#f0f0f0';
            btn.onmouseover = () => btn.style.background = '#e0e0e0';
            btn.onmouseout = () => btn.style.background = '#f0f0f0';
            return btn;
        }

        buttonBox.appendChild(makeButton('▶️ Play', startAnimation));
        buttonBox.appendChild(makeButton('⏸️ Pause', pauseAnimation));
        buttonBox.appendChild(makeButton('⏹️ Stop', stopAnimation));
        buttonBox.appendChild(makeButton('Seleziona tutti', () => setAllLayers(true)));
        buttonBox.appendChild(makeButton('Deseleziona tutti', () => setAllLayers(false)));

        const speedButton = makeButton(`⏩ Velocità ${getSpeedLabel()}`, toggleSpeed);
        buttonBox.appendChild(speedButton);

        document.body.appendChild(buttonBox);
    };
    </script>
    """

    # Aggiungi lo script alla mappa
    m.get_root().html.add_child(folium.Element(js_code))

    # Salva HTML
    output_path = "/mnt/c/Users/hp/Desktop/AI STAGE/mappe/mappa_cluster_start.html"
    m.save(output_path)
    print(f"✅ Mappa salvata in '{output_path}' — aprila in un browser.")



def end():
    final_path = "/mnt/c/Users/hp/Desktop/AI STAGE/Tensore/tensore_5_1_with_clusters_2-1.csv"
    df = pd.read_csv(final_path, sep=";")

    # Parametri
    cluster_column = 'kmeans_labels_10000'
    clusters = sorted(df[cluster_column].unique())
    colori = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred',
              'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white',
              'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']

    # Mappa
    m = folium.Map(location=[df['latitude_end'].mean(), df['longitude_end'].mean()],
                   zoom_start=12, control_scale=True)

    # MarkerCluster per ogni cluster
    for i, cluster in enumerate(clusters):
        cluster_df = df[df[cluster_column] == cluster]
        fg = folium.FeatureGroup(name=f"Cluster {cluster}", show=False)
        marker_cluster = MarkerCluster()

        for _, row in cluster_df.iterrows():
            folium.Marker(
                location=[row['latitude_end'], row['longitude_end']],
                popup=f"ID: {row['id']}<br>Cluster: {cluster}",
                icon=folium.Icon(color=colori[i % len(colori)])
            ).add_to(marker_cluster)

        marker_cluster.add_to(fg)
        fg.add_to(m)

    # Layer control
    folium.LayerControl(collapsed=False).add_to(m)

    # JavaScript per controlli
    js_code = """
    <script>
    window.onload = function() {
        let interval = null;
        let currentIndex = 0;
        let paused = false;
        let speedLevels = [2000, 1000, 400, 200];
        let currentSpeedIndex = 0;
        let checkboxes = [];

        function setAllLayers(checked) {
            checkboxes = document.querySelectorAll('.leaflet-control-layers-overlays input');
            checkboxes.forEach(function(cb) {
                if (cb.checked !== checked) cb.click();
            });
        }

        function updateInterval() {
            if (interval) {
                clearInterval(interval);
                interval = setInterval(() => {
                    if (paused) return;
                    setAllLayers(false);
                    if (currentIndex >= checkboxes.length) {
                        clearInterval(interval);
                        return;
                    }
                    checkboxes[currentIndex].click();
                    currentIndex++;
                }, speedLevels[currentSpeedIndex]);
            }
        }

        function startAnimation() {
            checkboxes = document.querySelectorAll('.leaflet-control-layers-overlays input');
            const startCluster = prompt(`Da quale cluster vuoi iniziare? Inserisci un numero da 0 a ${checkboxes.length - 1}:`);
            if (!startCluster || isNaN(startCluster) || startCluster < 0 || startCluster >= checkboxes.length) {
                alert("Cluster non valido.");
                return;
            }

            currentIndex = parseInt(startCluster);
            setAllLayers(false);
            paused = false;

            if (interval) clearInterval(interval);

            interval = setInterval(() => {
                if (paused) return;
                setAllLayers(false);
                if (currentIndex >= checkboxes.length) {
                    clearInterval(interval);
                    return;
                }
                checkboxes[currentIndex].click();
                currentIndex++;
            }, speedLevels[currentSpeedIndex]);
        }

        function pauseAnimation() {
            paused = !paused;
        }

        function stopAnimation() {
            if (interval) {
                clearInterval(interval);
                interval = null;
            }
            currentIndex = 0;
            paused = false;
            setAllLayers(false);
        }

        function toggleSpeed() {
            currentSpeedIndex = (currentSpeedIndex + 1) % speedLevels.length;
            updateInterval();
            speedButton.innerHTML = `⏩ Velocità ${getSpeedLabel()}`;
        }

        function getSpeedLabel() {
            switch (currentSpeedIndex) {
                case 0: return "1x";
                case 1: return "2x";
                case 2: return "5x";
                case 3: return "10x";
                default: return "1x";
            }
        }

        var buttonBox = document.createElement('div');
        buttonBox.style.position = 'absolute';
        buttonBox.style.bottom = '20px';
        buttonBox.style.left = '20px';
        buttonBox.style.backgroundColor = 'white';
        buttonBox.style.border = '1px solid #ccc';
        buttonBox.style.borderRadius = '8px';
        buttonBox.style.padding = '10px';
        buttonBox.style.zIndex = 1000;
        buttonBox.style.boxShadow = '2px 2px 8px rgba(0,0,0,0.3)';
        buttonBox.style.display = 'flex';
        buttonBox.style.flexDirection = 'column';
        buttonBox.style.gap = '5px';
        buttonBox.style.fontFamily = 'Arial, sans-serif';
        buttonBox.style.fontSize = '13px';

        function makeButton(label, onClick) {
            var btn = document.createElement('button');
            btn.innerHTML = label;
            btn.onclick = onClick;
            btn.style.padding = '6px 10px';
            btn.style.cursor = 'pointer';
            btn.style.border = '1px solid #888';
            btn.style.borderRadius = '5px';
            btn.style.background = '#f0f0f0';
            btn.onmouseover = () => btn.style.background = '#e0e0e0';
            btn.onmouseout = () => btn.style.background = '#f0f0f0';
            return btn;
        }

        buttonBox.appendChild(makeButton('▶️ Play', startAnimation));
        buttonBox.appendChild(makeButton('⏸️ Pause', pauseAnimation));
        buttonBox.appendChild(makeButton('⏹️ Stop', stopAnimation));
        buttonBox.appendChild(makeButton('Seleziona tutti', () => setAllLayers(true)));
        buttonBox.appendChild(makeButton('Deseleziona tutti', () => setAllLayers(false)));

        const speedButton = makeButton(`⏩ Velocità ${getSpeedLabel()}`, toggleSpeed);
        buttonBox.appendChild(speedButton);

        document.body.appendChild(buttonBox);
    };
    </script>
    """

    # Aggiungi lo script alla mappa
    m.get_root().html.add_child(folium.Element(js_code))

    # Salva HTML
    output_path = "/mnt/c/Users/hp/Desktop/AI STAGE/mappe/mappa_cluster_end.html"
    m.save(output_path)
    print(f"✅ Mappa salvata in '{output_path}' — aprila in un browser.")

    
    
    
x = input("Vuoi visualizzare la mappa di partenza (1) o di arrivo (2) o entrambe (3)? ")
if x == "1":
    print("Mappa di partenza")
    start()
elif x == "2":
    print("Mappa di arrivo")
    end()
elif x == "3":
    print("Mappa di partenza e arrivo")
    start()
    end()
else:
    print("Opzione non valida. Inserisci 1, 2 o 3.")
