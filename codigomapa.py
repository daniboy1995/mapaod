import pandas as pd
import folium
from folium import PolyLine, Marker
import streamlit as st

# Carregue os dados
url = "https://raw.githubusercontent.com/daniboy1995/mapaod/main/dadosmapa.csv"
df = pd.read_csv(url)

# Função para filtrar e plotar o mapa
def plotar_mapa(zonas_selecionadas, ticketdate_selecionada, route_selecionada):
    # Filtra o DataFrame com base nas seleções
    df_filtrado = df[df['trafficzoneidorign'].isin(zonas_selecionadas) &
                     (df['ticketdate'] == ticketdate_selecionada) &
                     (df['route'] == route_selecionada)]

    # Verifica se há pelo menos uma linha válida no DataFrame filtrado
    if not df_filtrado.empty:
        # Cria um mapa centralizado nas coordenadas médias das origens
        mapa = folium.Map(location=[df_filtrado['latorigem'].mean(), df_filtrado['lonorigem'].mean()], zoom_start=10)

        for index, row in df_filtrado.iterrows():
            origem = (row['latorigem'], row['lonorigem'])
            destino = (row['latdestino'], row['londestino'])
            rota = row['route']
            zona = row['trafficzoneidorign']
            
            # Obtém a contagem de usercards para esta rota
            usercards_count = df_filtrado[df_filtrado['route'] == rota]['usercard'].count()
            
            # Cria um pop-up com informações sobre a rota e o número de usercards
            popup_text = f"Origem: {origem}<br>Destino: {destino}<br>Rota: {rota}<br>Usercards: {usercards_count}"
            
            # Define a cor do marcador da origem para ser diferente da cor do destino
            cor = 'green' if origem == (row['latorigem'], row['lonorigem']) else 'red'
            
            # Adiciona marcadores de origem e destino com a cor apropriada
            folium.Marker(location=origem, icon=folium.Icon(color=cor), tooltip=popup_text).add_to(mapa)
            folium.Marker(location=destino, icon=folium.Icon(color='blue'), tooltip=popup_text).add_to(mapa)

            linha = PolyLine(locations=[origem, destino], color='blue', tooltip=popup_text)
            linha.add_to(mapa)

        # Exibe o mapa no Streamlit
        st.map(mapa)
    else:
        st.write("Nenhum dado encontrado para as seleções feitas.")

# Widget para seleção de zona de tráfego
zonas_de_trafego = df['trafficzoneidorign'].unique()
zonas_selecionadas = st.multiselect("Selecione as Zonas de Tráfego:", zonas_de_trafego, default=(1,))

# Widget para seleção de data do ticket
ticketdates = df['ticketdate'].unique()
ticketdate_selecionada = st.selectbox("Selecione a Data do Ticket:", ticketdates)

# Widget para seleção de rota
routes = df['route'].unique()
route_selecionada = st.selectbox("Selecione a Rota:", routes)

# Botão para plotar o mapa
if st.button("Plotar Mapa"):
    plotar_mapa(zonas_selecionadas, ticketdate_selecionada, route_selecionada)
