import pandas as pd
import folium
import streamlit as st

url = "https://raw.githubusercontent.com/daniboy1995/mapaod/main/dadosmapa.csv"
df = pd.read_csv(url)

# Crie uma função para plotar o mapa com base nas seleções feitas
def plotar_mapa(zonas_selecionadas, ticketdate_selecionada, route_selecionada):
    # Filtra o DataFrame com base nas seleções
    df_filtrado = df[df['trafficzoneidorign'].isin(zonas_selecionadas) &
                     (df['ticketdate'] == ticketdate_selecionada) &
                     (df['route'] == route_selecionada)]

    # Verifique se há pelo menos uma linha válida no DataFrame filtrado
    if not df_filtrado.empty:
        # Calcula as coordenadas médias das origens
        lat_media = df_filtrado['latorigem'].mean()
        lon_media = df_filtrado['lonorigem'].mean()

        # Crie um mapa centralizado nas coordenadas médias das origens
        mapa = folium.Map(location=[lat_media, lon_media], zoom_start=10)

        for _, row in df_filtrado.iterrows():
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

            linha = folium.PolyLine(locations=[origem, destino], color='blue', tooltip=popup_text)
            linha.add_to(mapa)

        # Exiba o mapa no Streamlit usando st.write()
        st.write(mapa)
    else:
        st.write("Nenhum dado encontrado para as seleções feitas.")

# Crie um widget de seleção múltipla para a zona de tráfego de origem
zonas_de_trafego = df['trafficzoneidorign'].unique()
filtro_zona_trafego = st.multiselect('Zona de Tráfego:', zonas_de_trafego, default=(1,))

# Crie widgets de seleção para o ticketdate e a rota
ticketdates = df['ticketdate'].unique()
filtro_ticketdate = st.selectbox('Ticket Date:', ticketdates)
filtro_route = st.selectbox('Route:', df['route'].unique())

# Exiba os widgets de seleção e o mapa
plotar_mapa(filtro_zona_trafego, filtro_ticketdate, filtro_route)
