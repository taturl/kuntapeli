import folium
import streamlit as st

from streamlit_folium import st_folium
from shapely.geometry import shape
import json


prompt = str(st.text_input('Kirjoita kunnan nimi ja paina enter. Niitä on yhteensä 309.'))

if 'correct_quesses' not in st.session_state:
    st.session_state['correct_quesses'] = []

if 'kuntarajat' not in st.session_state:
    st.session_state['kuntarajat'] = json.loads(open('Kuntarajat.geojson').read())['features']

if 'm' not in st.session_state:
    st.session_state['m'] = folium.Map(
        location=[65.192059,  24.945831],
        zoom_start=5,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}",
        attr='Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ'
    )

    def style_function(x): return {'fillOpacity': 0, 'weight': 0.1}

    folium.GeoJson(
        'Kuntarajat.geojson',
        name='geojson',
        style_function=style_function
    ).add_to(st.session_state.m)

if prompt:
    prompt = prompt.casefold().capitalize()
    names = [kunta['properties']['Name'] for kunta in st.session_state.kuntarajat]
    if prompt in names:
        if prompt in st.session_state.correct_quesses:
            st.write(prompt, '...on kunta ja tiesit sen jo.', )
        else:
            st.write(prompt, '...on kunta.', )
        
            # Add to results
            st.session_state.correct_quesses.append(prompt)
            print(st.session_state.correct_quesses)

            # Add all known kuntas to map
            # for known_kunta in st.session_state.correct_quesses:
            kunta = next(kunta for kunta in st.session_state.kuntarajat if kunta['properties']['Name'] == prompt)
            kunta_geo = shape(kunta["geometry"])
            folium.GeoJson(kunta_geo, tooltip=prompt).add_to(st.session_state.m)

if len(st.session_state.correct_quesses) >= 309:
    st.title("TIESIT KAIKKI KUNNAT! ONNEKSI OLKOON")

# folium.LayerControl().add_to(st.session_state.m)
st_data = st_folium(st.session_state.m, width=725)
