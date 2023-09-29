import pandas as pd
import folium
from folium import PolyLine, Marker
import ipywidgets as widgets
from IPython.display import display
from urllib.parse import quote_plus
import requests
from io import StringIO

# URL do arquivo CSV no repositório do Git
url = "https://raw.githubusercontent.com/daniboy1995/mapaod/main/dadosmapa.csv"

# Função para obter dados do CSV e lidar com erros
def obter_dados_do_git():
    try:
        # Obter dados do CSV usando requests
        response = requests.get(url)
        response.raise_for_status()  # Lança uma exceção se a requisição não for bem-sucedida
        
        # Criar DataFrame a partir dos dados do CSV
        df = pd.read_csv(StringIO(response.text))
        return df
    
    except Exception as e:
        print("Erro ao obter dados do Git:", e)
        return None

# Obter dados do Git
df = obter_dados_do_git()

# Se df não for None, continue com o restante do seu código
if df is not None:
    # Crie uma função para atualizar as opções do filtro de rota com base na seleção de zona de tráfego
    def atualizar_rotas(change):
        if change.new:
            filtro_route.options = df[df['trafficzoneidorign'].isin(change.new)]['route'].unique()

    # Crie uma função para plotar o mapa com base nas seleções feitas
    def plotar_mapa(zonas_selecionadas, ticketdate_selecionada, route_selecionada):
        # Filtra o DataFrame com base nas seleções
        df_filtrado = df[df['trafficzoneidorign'].isin(zonas_selecionadas) &
                         (df['ticketdate'] == ticketdate_selecionada) &
                         (df['route'] == route_selecionada)]

        # Verifique se há pelo menos uma linha válida no DataFrame filtrado
        if not df_filtrado.empty:
            # Crie um mapa centralizado nas coordenadas médias das origens
            mapa = folium.Map(location=[df_filtrado['latorigem'].mean(), df_filtrado['lonorigem'].mean()], zoom_start=10)

            for index, row in df_filtrado.iterrows():
                origem = (row['latorigem'], row['lonorigem'])
                destino = (row['latdestino'], row['londestino'])
                rota = row['route']
                zona = row['trafficzoneidorign']
                
                # Obtenha a contagem de usercards para esta rota
                usercards_count = df_filtrado[df_filtrado['route'] == rota]['usercard'].count()
                
                # Crie um pop-up com informações sobre a rota e o número de usercards
                popup_text = f"Origem: {origem}<br>Destino: {destino}<br>Rota: {rota}<br>Usercards: {usercards_count}"
                
                # Defina a cor do marcador da origem para ser diferente da cor do destino
                cor = 'green' if origem == (row['latorigem'], row['lonorigem']) else 'red'
                
                # Adicione marcadores de origem e destino com a cor apropriada
                folium.Marker(location=origem, icon=folium.Icon(color=cor), tooltip=popup_text).add_to(mapa)
                folium.Marker(location=destino, icon=folium.Icon(color='blue'), tooltip=popup_text).add_to(mapa)

                linha = PolyLine(locations=[origem, destino], color='blue', tooltip=popup_text)
                linha.add_to(mapa)

            display(mapa)
        else:
            print("Nenhum dado encontrado para as seleções feitas.")

    # Crie widgets de seleção para a zona de tráfego de origem, ticketdate e rota
    zonas_de_trafego = df['trafficzoneidorign'].unique()
    filtro_zona_trafego = widgets.SelectMultiple(
        options=zonas_de_trafego,
        description='Zona de Tráfego:',
        disabled=False,
    )
    
    ticketdates = df['ticketdate'].unique()
    filtro_ticketdate = widgets.Dropdown(
        options=ticketdates,
        description='Ticket Date:',
        disabled=False,
    )
    
    filtro_route = widgets.Dropdown(
        options=df['route'].unique(),
        description='Route:',
        disabled=False,
    )

    # Defina um observador para atualizar as opções do filtro de rota com base na seleção de zona de tráfego
    filtro_zona_trafego.observe(atualizar_rotas, 'value')

    # Exiba os widgets de seleção
    widgets.interactive(plotar_mapa, zonas_selecionadas=filtro_zona_trafego, 
                        ticketdate_selecionada=filtro_ticketdate, route_selecionada=filtro_route)
else:
    print("Não foi possível obter os dados do Git. Verifique a URL do arquivo CSV.")
