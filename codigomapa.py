import pandas as pd
import osmnx as ox
import folium
from folium import PolyLine, Marker
import streamlit as st

# Carregando os dados
url = "https://raw.githubusercontent.com/daniboy1995/mapaod/main/dadosmapa.csv"
df = pd.read_csv(url)

def plotar_mapa(zonas_selecionadas, ticketdate_selecionada, route_selecionada):
    df_filtrado = df[df['trafficzoneidorign'].isin(zonas_selecionadas) &
                     (df['ticketdate'] == ticketdate_selecionada) &
                     (df['route'] == route_selecionada)]

    if not df_filtrado.empty:
        # Obtendo os pontos de origem e destino
        origens = list(zip(df_filtrado['latorigem'], df_filtrado['lonorigem']))
        destinos = list(zip(df_filtrado['latdestino'], df_filtrado['londestino']))

        # Criando um mapa base usando OpenStreetMap
        mapa = folium.Map(location=[df_filtrado['latorigem'].mean(), df_filtrado['lonorigem'].mean()], zoom_start=10)

        # Adicionando marcadores de origem e destino ao mapa
        for origem, destino in zip(origens, destinos):
            folium.Marker(location=origem, icon=folium.Icon(color='green')).add_to(mapa)
            folium.Marker(location=destino, icon=folium.Icon(color='blue')).add_to(mapa)
            PolyLine([origem, destino], color="red", weight=2.5, opacity=1).add_to(mapa)

        # Exibindo o mapa
        st.write(mapa)
    else:
        st.write("Nenhum dado encontrado para as seleções feitas.")

zonas_de_trafego = df['trafficzoneidorign'].unique()
filtro_zona_trafego = st.multiselect('Zona de Tráfego:', zonas_de_trafego, default=(1,))

ticketdates = df['ticketdate'].unique()
filtro_ticketdate = st.selectbox('Ticket Date:', ticketdates)

filtro_route = st.selectbox('Route:', df['route'].unique())

plotar_mapa(filtro_zona_trafego, filtro_ticketdate, filtro_route)
