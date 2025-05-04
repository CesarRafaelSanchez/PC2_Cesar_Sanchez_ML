# Importar las librerías necesarias
import networkx as nx
import pandas as pd
import random
# Importar pyvis para visualización interactiva (recomendado)
# Si obtienes un error "ModuleNotFoundError: No module named 'pyvis'",
# instala la librería ejecutando en tu terminal: pip install pyvis
from pyvis.network import Network
# Importar matplotlib para visualización estática (alternativa)
import matplotlib.pyplot as plt

# --- 1. Simulación de Adquisición de Datos ---
# En un escenario real, aquí iría el código para obtener datos de APIs (CoinMarketCap, CoinGecko)
# o realizar web scraping para las categorías (IA, Videojuegos, RWA, Memes)
# y sus atributos (precio, market cap, volumen, etc.) y relaciones (co-listing, comunidad, etc.).

# Para este ejemplo, crearemos datos simulados para 100 nodos (proyectos)
# y algunas aristas simuladas.
num_nodos = 100
categorias = ['Inteligencia Artificial', 'Videojuegos', 'RWA', 'Memes']

# Generar datos de nodos simulados
nodos_data = []
for i in range(num_nodos):
    nodo_id = f'PROYECTO_{i+1}'
    categoria = random.choice(categorias)
    # Atributos simulados (simplificado)
    market_cap = random.uniform(1e6, 1e9) # Capitalización de mercado simulada
    volumen_24h = random.uniform(market_cap * 0.01, market_cap * 0.1) # Volumen 24h simulado
    precio = random.uniform(0.01, 100) # Precio simulado
    circulating_supply = random.uniform(1e6, 1e10) # Suministro circulante simulado
    total_supply = circulating_supply * random.uniform(1, 5) # Suministro total simulado
    max_supply = total_supply * random.uniform(1, 10) if random.random() > 0.2 else None # Suministro máximo simulado (algunos pueden no tener)
    ranking = random.randint(1, 2000) # Posición en el ranking simulada
    halving_previo = random.choice([True, False]) # Indicador de halving simulado
    multichain = random.choice([True, False]) # Indicador multichain simulado
    listed_cex = random.choice([True, False]) # Indicador listado en CEX simulado
    contract_address = f'0x{random.getrandbits(160):040x}' # Dirección de contrato simulada
    supported_wallets = random.sample(['MetaMask', 'Trust Wallet', 'Ledger', 'Trezor', 'Phantom'], k=random.randint(1, 4)) # Billeteras soportadas simuladas
    explorer_url = f'https://explorer.example.com/{nodo_id}' # Enlace a explorador simulado
    website_url = f'https://{nodo_id.lower()}.com' # URL de sitio web simulada
    twitter_url = f'https://twitter.com/{nodo_id.lower()}' # URL de Twitter simulada
    diffusion_factor = random.uniform(0.1, 10.0) # Factor de difusión simulado
    rating = random.uniform(1.0, 5.0) # Calificación simulada

    nodos_data.append({
        'id': nodo_id,
        'categoria': categoria,
        'market_cap': market_cap,
        'volumen_24h': volumen_24h,
        'precio': precio,
        'circulating_supply': circulating_supply,
        'total_supply': total_supply,
        'max_supply': max_supply,
        'ranking': ranking,
        'halving_previo': halving_previo,
        'multichain': multichain,
        'listed_cex': listed_cex,
        'contract_address': contract_address,
        'supported_wallets': supported_wallets,
        'explorer_url': explorer_url,
        'website_url': website_url,
        'twitter_url': twitter_url,
        'diffusion_factor': diffusion_factor,
        'rating': rating,
        # Agregar aquí más atributos según la lista del Canvas
    })

df_nodos = pd.DataFrame(nodos_data)

# Generar datos de aristas simuladas
# Crearemos aristas basadas en una similitud de categoría simulada o conexión aleatoria
aristas_data = []
for i in range(num_nodos):
    for j in range(i + 1, num_nodos):
        # Simular una conexión aleatoria con cierta probabilidad
        if random.random() < 0.05: # 5% de probabilidad de conexión aleatoria
            nodo1 = df_nodos.iloc[i]['id']
            nodo2 = df_nodos.iloc[j]['id']
            # Ponderación simulada (ejemplo: basada en la suma de market caps)
            peso = df_nodos.iloc[i]['market_cap'] + df_nodos.iloc[j]['market_cap']
            aristas_data.append({'source': nodo1, 'target': nodo2, 'weight': peso})
        # Simular una conexión más probable si son de la misma categoría
        elif df_nodos.iloc[i]['categoria'] == df_nodos.iloc[j]['categoria'] and random.random() < 0.2: # 20% si misma categoría
             nodo1 = df_nodos.iloc[i]['id']
             nodo2 = df_nodos.iloc[j]['id']
             peso = (df_nodos.iloc[i]['market_cap'] + df_nodos.iloc[j]['market_cap']) * 2 # Mayor peso si misma categoría
             aristas_data.append({'source': nodo1, 'target': nodo2, 'weight': peso})


df_aristas = pd.DataFrame(aristas_data)

# --- 2. Construcción del Grafo ---
# Crear un objeto grafo no dirigido (puedes usar nx.DiGraph() para un grafo dirigido)
G = nx.Graph()

# Añadir nodos con sus atributos
for index, row in df_nodos.iterrows():
    G.add_node(row['id'],
               categoria=row['categoria'],
               market_cap=row['market_cap'],
               volumen_24h=row['volumen_24h'],
               precio=row['precio'],
               circulating_supply=row['circulating_supply'],
               total_supply=row['total_supply'],
               max_supply=row['max_supply'],
               ranking=row['ranking'],
               halving_previo=row['halving_previo'],
               multichain=row['multichain'],
               listed_cex=row['listed_cex'],
               contract_address=row['contract_address'],
               supported_wallets=row['supported_wallets'],
               explorer_url=row['explorer_url'],
               website_url=row['website_url'],
               twitter_url=row['twitter_url'],
               diffusion_factor=row['diffusion_factor'],
               rating=row['rating'])
               # Añadir aquí más atributos

# Añadir aristas con sus ponderaciones
for index, row in df_aristas.iterrows():
    G.add_edge(row['source'], row['target'], weight=row['weight'])

# --- 3. Visualización del Grafo ---

# Opción 1: Visualización interactiva con Pyvis (Recomendado para explorar la red)
# Crear un objeto Network de Pyvis
net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", notebook=True)

# Añadir nodos y aristas desde el grafo NetworkX
# Puedes personalizar la apariencia de los nodos (tamaño, color, etc.)
# basándote en sus atributos.
for node in G.nodes():
    # Ejemplo: tamaño del nodo basado en market cap (escalado)
    size = G.nodes[node]['market_cap'] / 1e7 + 5 # Escalar para visualización
    # Ejemplo: color del nodo basado en categoría
    color_map = {'Inteligencia Artificial': 'red', 'Videojuegos': 'blue', 'RWA': 'green', 'Memes': 'purple'}
    color = color_map.get(G.nodes[node]['categoria'], 'gray')

    # Crear un título más detallado para el tooltip
    title_html = f"""
    <b>{node}</b><br>
    Categoría: {G.nodes[node]['categoria']}<br>
    Market Cap: ${G.nodes[node]['market_cap']:.2f}<br>
    Volumen 24h: ${G.nodes[node]['volumen_24h']:.2f}<br>
    Precio: ${G.nodes[node]['precio']:.4f}<br>
    Ranking: {G.nodes[node]['ranking']}<br>
    Halving Previo: {'Sí' if G.nodes[node]['halving_previo'] else 'No'}<br>
    Multichain: {'Sí' if G.nodes[node]['multichain'] else 'No'}<br>
    Listado CEX: {'Sí' if G.nodes[node]['listed_cex'] else 'No'}<br>
    Difusión: {G.nodes[node]['diffusion_factor']:.2f}<br>
    Rating: {G.nodes[node]['rating']:.2f}
    """

    net.add_node(node, label=node, size=size, color=color, title=title_html)


for edge in G.edges(data=True):
    # Ejemplo: grosor de la arista basado en el peso
    width = edge[2]['weight'] / 1e9 # Escalar para visualización
    net.add_edge(edge[0], edge[1], width=width)

# Configurar opciones de física para una mejor distribución del grafo
net.repulsion(node_distance=100, central_gravity=0.2, spring_length=200, spring_strength=0.05, damping=0.09)

# Guardar la visualización interactiva en un archivo HTML
net.show("crypto_network_interactive.html", notebook=False)
print("Visualización interactiva guardada en crypto_network_interactive.html")


# Opción 2: Visualización estática con Matplotlib (Más simple, menos interactiva)
"""
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, k=0.5, iterations=50) # Algoritmo de layout para posicionar nodos

# Dibujar nodos
# Puedes ajustar el tamaño y color de los nodos aquí también
node_colors = [color_map.get(G.nodes[node]['categoria'], 'gray') for node in G.nodes()]
node_sizes = [G.nodes[node]['market_cap'] / 1e7 + 5 for node in G.nodes()]
nx.draw(G, pos, with_labels=False, node_size=node_sizes, node_color=node_colors, edge_color='gray', alpha=0.6)

# Dibujar etiquetas de nodos (opcional, puede ser denso para muchos nodos)
# nx.draw_networkx_labels(G, pos, font_size=8, font_color='black')

# Dibujar aristas (opcional, puede ser denso)
# edge_weights = [data['weight'] / 1e9 for u, v, data in G.edges(data=True)]
# nx.draw_networkx_edges(G, pos, width=edge_weights, alpha=0.5, edge_color='gray')


plt.title("Modelo de Grafo del Mercado Cripto (Simulado)")
plt.show()
"""

# --- Contenido para requirements.txt ---
# Este archivo lista las librerías necesarias para ejecutar el script.
# Para instalarlas, ejecuta en tu terminal: pip install -r requirements.txt

# networkx
# pandas
# pyvis # Añadido pyvis explícitamente
# matplotlib