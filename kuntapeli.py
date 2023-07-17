import json
import folium
import streamlit as st
from streamlit_folium import st_folium
from shapely.geometry import shape


@st.cache_data
def load_geojson_to_memory():
    return(
        json.loads(open('Kuntarajat.geojson').read())['features']
    )

KUNTARAJAT = load_geojson_to_memory()

if 'correct_guesses' not in st.session_state:
    st.session_state['correct_guesses'] = []

if 'fg' not in st.session_state:
    st.session_state['fg'] = folium.FeatureGroup(name="Kuntarajat")

def check_guess():
    prompt = st.session_state.prompt.casefold().capitalize()
    names = [kunta['properties']['Name'] for kunta in KUNTARAJAT]
    if prompt in names:
        if prompt in st.session_state.correct_guesses:
            st.write(prompt, '...on kunta ja kirjoitit sen jo :-)', )
        else:
            st.write(prompt, '...on kunta. Lisätään se kartalle!', )
            st.session_state.correct_guesses.append(prompt)

            kunta = next(kunta for kunta in KUNTARAJAT if kunta['properties']['Name'] == prompt)
            kunta_geo = shape(kunta["geometry"])
            st.session_state.fg.add_child( 
                folium.GeoJson(kunta_geo, tooltip=prompt)
            )
    else:
        st.write(prompt, '... ei ole kunta.')

st.text_input(
    'Suomessa on 309 kuntaa. Muistatko ne kaikki?',
    key='prompt',
    placeholder='Kirjoita tähän kunnannimi',
    on_change=check_guess
)

if len(st.session_state.correct_guesses) >= 309:
    st.title("TIESIT KAIKKI KUNNAT! ONNEKSI OLKOON")

m = folium.Map(
    location=[65.192059,  24.945831],
    zoom_start=5,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}",
    attr='Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ'
)

def style_function(x): return {'fillOpacity': 0, 'weight': 0.1}

out = st_folium(
    m,
    feature_group_to_add=st.session_state.fg,
    height=600,
    use_container_width=True
)
