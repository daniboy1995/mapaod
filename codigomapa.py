import pandas as pd
import pydeck as pdk
import streamlit as st

url = "https://raw.githubusercontent.com/daniboy1995/mapaod/main/dadosmapa.csv"
df = pd.read_csv(url)

def plotar_mapa(zonas_selecionadas, ticketdate_selecionada, route_selecionada):
    df_filtrado = df[df['trafficzoneidorign'].isin(zonas_selecionadas) &
                     (df['ticketdate'] == ticketdate_selecionada) &
                     (df['route'] == route_selecionada)]

    if not df_filtrado.empty:
        origens = df_filtrado[['lonorigem', 'latorigem']]
        destinos = df_filtrado[['londestino', 'latdestino']]
        linhas = origens.join(destinos, lsuffix='_origem', rsuffix='_destino')

        layers = [
            pdk.Layer(
                "ScatterplotLayer",
                data=origens,
                get_position=['lonorigem', 'latorigem'],
                get_color='[0, 255, 0]',
                get_radius=50,
            ),
            pdk.Layer(
                "ScatterplotLayer",
                data=destinos,
                get_position=['londestino', 'latdestino'],
                get_color='[0, 0, 255]',
                get_radius=50,
            ),
            pdk.Layer(
                "PathLayer",
                data=linhas,
                get_path=['lonorigem', 'latorigem', 'londestino', 'latdestino'],
                get_color='[255, 0, 0]',
                get_width=5,
            ),
        ]

        view_state = pdk.ViewState(
            latitude=df_filtrado['latorigem'].mean(),
            longitude=df_filtrado['lonorigem'].mean(),
            zoom=10
        )

        map = pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=view_state,
            layers=layers,
        )

        st.pydeck_chart(map)
    else:
        st.write("Nenhum dado encontrado para as seleções feitas.")

zonas_de_trafego = df['trafficzoneidorign'].unique()
filtro_zona_trafego = st.multiselect('Zona de Tráfego:', zonas_de_trafego, default=(1,))

ticketdates = df['ticketdate'].unique()
filtro_ticketdate = st.selectbox('Ticket Date:', ticketdates)

filtro_route = st.selectbox('Route:', df['route'].unique())

plotar_mapa(filtro_zona_trafego, filtro_ticketdate, filtro_route)
