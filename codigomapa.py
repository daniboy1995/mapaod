import pandas as pd
import folium
from folium import PolyLine, Marker
import streamlit as st

url = "https://raw.githubusercontent.com/daniboy1995/mapaod/main/dadosmapa.csv"
df = pd.read_csv(url)

zonas_de_trafego = df['trafficzoneidorign'].unique()
filtro_zona_trafego = st.multiselect('Zona de Tráfego:', zonas_de_trafego, default=(1,))

ticketdates = df['ticketdate'].unique()
filtro_ticketdate = st.selectbox('Ticket Date:', ticketdates)

rotas_disponiveis = df[df['trafficzoneidorign'].isin(filtro_zona_trafego) & (df['ticketdate'] == filtro_ticketdate)]['route'].unique()
filtro_route = st.selectbox('Route:', rotas_disponiveis)

df_filtrado = df[(df['trafficzoneidorign'].isin(filtro_zona_trafego)) & (df['ticketdate'] == filtro_ticketdate) & (df['route'] == filtro_route)]

if not df_filtrado.empty:
    mapa = folium.Map(location=[df_filtrado['latorigem'].mean(), df_filtrado['lonorigem'].mean()], zoom_start=10)

    for index, row in df_filtrado.iterrows():
        origem = (row['latorigem'], row['lonorigem'])
        destino = (row['latdestino'], row['londestino'])
        rota = row['route']
        zona = row['trafficzoneidorign']
        
        usercards_count = df_filtrado[df_filtrado['route'] == rota]['usercard'].count()
        
        popup_text = f"Origem: {origem}<br>Destino: {destino}<br>Rota: {rota}<br>Usercards: {usercards_count}"
        
        cor = 'green' if origem == (row['latorigem'], row['lonorigem']) else 'red'
        
        folium.Marker(location=origem, icon=folium.Icon(color=cor), tooltip=popup_text).add_to(mapa)
        folium.Marker(location=destino, icon=folium.Icon(color='blue'), tooltip=popup_text).add_to(mapa)

        linha = PolyLine(locations=[origem, destino], color='blue', tooltip=popup_text)
        linha.add_to(mapa)

    # Use folium_static para renderizar o mapa no Streamlit
    st.write(folium_static(mapa))
else:
    st.write("Nenhum dado encontrado para as seleções feitas.")
