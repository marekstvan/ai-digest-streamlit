
import streamlit as st
import configparser
import os

# Load configuration
config = configparser.ConfigParser()
config.read("config.txt", encoding="utf-8")

settings = config["Settings"]
sources = [s.strip() for s in settings.get("sources", "").split(",")]
keywords = [k.strip() for k in settings.get("keywords", "").split(",")]
blacklist = [b.strip() for b in settings.get("blacklist", "").split(",")]
date_from = settings.get("date_from", "")
date_to = settings.get("date_to", "")
articles_per_page = int(settings.get("articles_per_page", 10))
layout_width = settings.get("layout_width", "1280")

# Set page config
st.set_page_config(layout="wide")

# Display configuration summary
st.title("Můj AI Digest – Pojišťovnictví")
st.markdown(f"**Zdroje:** {', '.join(sources)}")
st.markdown(f"**Klíčová slova:** {', '.join(keywords)}")
st.markdown(f"**Blacklist:** {', '.join(blacklist)}")
st.markdown(f"**Období:** {date_from} až {date_to}")
st.markdown(f"**Počet článků na stránku:** {articles_per_page}")
st.markdown(f"**Šířka layoutu:** {layout_width}px")

# Placeholder for article loading
st.info("Načítání článků z reálných zdrojů zatím není implementováno.")
