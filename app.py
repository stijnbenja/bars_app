import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from folium.plugins import LocateControl
import pandas as pd
import numpy as np

st.set_page_config(page_title="Bar Heatmap Utrecht", layout="wide")
st.title("🍺 Bar heatmap Utrecht")

df = pd.read_csv("bars_utrecht_full.csv")

# Sidebar filters
min_rating = st.sidebar.slider("Minimale rating", 1.0, 5.0, 3.0, 0.1)
min_reviews = st.sidebar.slider("Minimaal aantal reviews", 0, 500, 0, 10)

df = df[df["rating"] >= min_rating]
df = df[df["rating_count"] >= min_reviews]

st.sidebar.markdown(f"**{len(df)} bars** zichtbaar")

# Gewichten
rating_weight = (df["rating"] - 3).clip(lower=0) ** 2
log_reviews = np.log1p(df["rating_count"])
log_reviews_norm = (log_reviews - log_reviews.min()) / (log_reviews.max() - log_reviews.min())
df["weight"] = rating_weight * (0.3 + 0.7 * log_reviews_norm)

# Kaart
m = folium.Map(location=[52.0907, 5.1214], zoom_start=14, tiles="CartoDB positron")

LocateControl(auto_start=False).add_to(m)

heat_data = df[["latitude", "longitude", "weight"]].values.tolist()
HeatMap(heat_data, radius=35, blur=25, min_opacity=0.3, max_zoom=16).add_to(m)



for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=8,
        color="transparent",
        fill=True,
        fill_color="transparent",
        fill_opacity=0,
        tooltip=folium.Tooltip(f"{row['name']} — ⭐ {row['rating']} ({int(row['rating_count'])} reviews)")
    ).add_to(m)

st_folium(m, use_container_width=True, height=700)