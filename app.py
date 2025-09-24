
import streamlit as st
import os
from datetime import datetime

CONFIG_FILE = "config.txt"

def load_config():
    config = {
        "sources": "",
        "keywords": "",
        "oldest_date": "",
        "newest_date": "",
    }
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    config[key] = value
    return config

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")

def main():
    st.set_page_config(layout="wide")
    st.title("📰 Můj AI Digest")

    config = load_config()

    with st.form("config_form"):
        sources = st.text_area("Zdroje (URL adresy oddělené novým řádkem)", value=config.get("sources", ""), height=150)
        keywords = st.text_input("Klíčová slova", value=config.get("keywords", ""))
        col1, col2 = st.columns(2)
        with col1:
            oldest_date = st.date_input("Nejstarší datum článku", value=datetime.strptime(config.get("oldest_date"), "%Y-%m-%d") if config.get("oldest_date") else None)
        with col2:
            newest_date = st.date_input("Nejnovější datum článku", value=datetime.strptime(config.get("newest_date"), "%Y-%m-%d") if config.get("newest_date") else None)

        submitted = st.form_submit_button("💾 Uložit konfiguraci")
        if submitted:
            config["sources"] = sources
            config["keywords"] = keywords
            config["oldest_date"] = oldest_date.strftime("%Y-%m-%d") if oldest_date else ""
            config["newest_date"] = newest_date.strftime("%Y-%m-%d") if newest_date else ""
            save_config(config)
            st.success("Konfigurace byla uložena.")

    st.markdown("---")
    st.subheader("📄 Výsledky")

    # Simulace výsledků pro demonstraci
    results = [f"Článek {i+1}" for i in range(50)]
    page_size = 5
    if "page" not in st.session_state:
        st.session_state.page = 0

    start = st.session_state.page * page_size
    end = start + page_size
    for result in results[start:end]:
        st.write(result)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Předchozí") and st.session_state.page > 0:
            st.session_state.page -= 1
    with col2:
        if st.button("➡️ Další") and end < len(results):
            st.session_state.page += 1

if __name__ == "__main__":
    main()
