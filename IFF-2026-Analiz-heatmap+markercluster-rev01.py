#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import folium
from folium import IFrame
from folium.plugins import MarkerCluster, HeatMap


# In[2]:


df = pd.read_csv("iff.csv", sep=";")


# In[3]:


df.columns=df.columns.str.strip()
df.head(2)


# In[4]:


coords={
    "Atlas 1948":[41.034213819267414, 28.979258273884174],
    "Kadıköy Sineması": [40.98839794899813, 29.02879876774457],
    "Sinematek/Sinemaevi": [40.986772147157325, 29.03273114123157],
    "Beyoğlu Sineması": [41.03443498014413, 28.979207202571917],
    "Paribu Cineverse Nautilus": [40.999865209375656, 29.031124097054416],
    "Cinewam City's 3": [41.05120760500985, 28.992807022113393],
    "Cinewam City's 7": [41.05120760500985, 28.992807022113393],
}


# In[5]:


def build_map(df, coords, start=(41.014, 29.007), zoom=12):

    harita = folium.Map(location=start, zoom_start=zoom, tiles="CartoDB Voyager")

    marker_cluster = MarkerCluster().add_to(harita)

    heat_data = []

    # Salon bazlı grupla
    for salon, data in df.groupby("Yer"):

        coord = coords.get(salon)
        if coord is None:
            continue

        data = data.sort_values(by=["Tarih", "Saat"])

        # Popup içeriği
        film_listesi = f"<h4 style='color:darkred'>{salon}</h4>"

        for row in data.itertuples():
            film_listesi += (
                f"<b>{row.Film}</b><br>"
                f"Tarih: {row.Tarih}<br>"
                f"Saat: {row.Saat}<br><hr>"
            )

        popup_html = f"""
        <div style='width:300px; height:300px; overflow:auto;'>
            {film_listesi}
        </div>
        """

        iframe = IFrame(popup_html, width=320, height=320)
        popup = folium.Popup(iframe, max_width=350)

        folium.Marker(
            location=coord,
            popup=popup,
            tooltip=salon
        ).add_to(marker_cluster)

        heat_data.append([coord[0], coord[1], len(data)])

    HeatMap(heat_data).add_to(harita)

    return harita


# In[6]:


harita = build_map(df, coords)
harita.save("map.html")

import webbrowser
import os

webbrowser.open(os.path.abspath("map.html"))


# In[7]:


import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))

sns.countplot(data=df, x="Yer")

plt.title("Salon Bazlı Film Dağılımı")
plt.xticks(rotation=45)

plt.show()


# In[8]:


import seaborn as sns
import matplotlib.pyplot as plt

ax = sns.countplot(data=df, x="Yer")

# sayı ekleme
for p in ax.patches:
    ax.annotate(
        int(p.get_height()),
        (p.get_x() + p.get_width()/2, p.get_height()),
        ha="center",
        va="bottom"
    )

plt.xticks(rotation=45)
plt.show()


# In[9]:


import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("Sinema Haritası")

harita = build_map(df, coords)

st_data = st_folium(harita, width=900, height=600)


# In[ ]:




