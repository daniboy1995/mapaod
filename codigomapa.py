import pandas as pd
import folium
from folium import PolyLine, Marker
import ipywidgets as widgets
import streamlit as st

url = "https://raw.githubusercontent.com/daniboy1995/mapaod/main/dadosmapa.csv"
df = pd.read_csv(url)

# Função para criar o DataFrame do mapa
def criar_dataframe_mapa(zonas_selecionadas, ticketdate_selecionada, route_selecionada):
    df_filtrado = df[df['trafficzoneidorign'].isin(zonas_selecionadas) &
                     (df['ticketdate'] == ticketdate_selecionada) &
                     (df['route'] == route_selecionada)]

    data = []
    for index, row in df_filtrado.iterrows():
        origem = (row['latorigem'], row['lonorigem'])
        destino = (row['latdestino'], row['londestino'])
        rota = row['route']
        zona = row['trafficzoneidorign']
        usercards_count = df_filtrado[df_filtrado['route'] == rota]['usercard'].count()

        data.append({
            'Origem': origem,
            'Destino': destino,
            'Rota': rota,
            'Zona': zona,
            'Usercards': usercards_count
        })

    return pd.DataFrame(data)

# Widgets de seleção
zonas_de_trafego = df['trafficzoneidorign'].unique()
filtro_zona_trafego = st.multiselect('Zona de Tráfego:', zonas_de_trafego, default=(1,))

ticketdates = df['ticketdate'].unique()
filtro_ticketdate = st.selectbox('Ticket Date:', ticketdates)

filtro_route = st.selectbox('Route:', df['route'].unique())

# Atualiza o DataFrame com base nas seleções
df_mapa = criar_dataframe_mapa(filtro_zona_trafego, filtro_ticketdate, filtro_route)

# Crie o mapa Folium com base no DataFrame filtrado
mapa = folium.Map(location=[df_mapa['Origem'].mean()[0], df_mapa['Origem'].mean()[1]], zoom_start=10)

for _, row in df_mapa.iterrows():
    origem = list(row['Origem'])
    destino = list(row['Destino'])
    rota = row['Rota']
    zona = row['Zona']
    usercards_count = row['Usercards']

    popup_text = f"Origem: {origem}<br>Destino: {destino}<br>Rota: {rota}<br>Usercards: {usercards_count}"
    folium.Marker(location=origem, icon=folium.Icon(color='green'), tooltip=popup_text).add_to(mapa)
    folium.Marker(location=destino, icon=folium.Icon(color='red'), tooltip=popup_text).add_to(mapa)
    linha = PolyLine(locations=[origem, destino], color='blue', tooltip=popup_text)
    linha.add_to(mapa)

# Exibe o mapa no Streamlit
st.folium_chart(mapa)
