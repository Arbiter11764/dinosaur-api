import streamlit as st
import requests

API_URL = "https://dinosaur-api-xe77.onrender.com"

st.set_page_config(page_title="🦕 Dinosaur Gallery", layout="wide")
st.title("🦕 Dinosaur Gallery")
st.markdown("Dinosaur facts with images pulled automatically from Wikipedia.")

# ── IMAGE HELPER ──────────────────────────────────────────────
def get_dino_image(name):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{name.replace(' ', '_')}"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            return data.get("thumbnail", {}).get("source", None)
    except:
        return None

# ── FETCH ALL DINOS ───────────────────────────────────────────
response = requests.get(f"{API_URL}/dinosaurs")

if response.status_code == 200:
    dinosaurs = response.json()
    st.success(f"Loaded {len(dinosaurs)} dinosaurs")

    for dino in dinosaurs:
        st.divider()
        col1, col2 = st.columns([1, 2])

        with col1:
            img = get_dino_image(dino["name"])
            if img:
                st.image(img, caption=dino["name"], use_column_width=True)
            else:
                st.caption("No image found")

        with col2:
            st.subheader(f"🦖 {dino['name']}")
            st.write(f"**Period:** {dino['period']}")
            st.write(f"**Diet:** {dino['diet']}")
            st.write(f"**Length:** {dino['length_m']} m")
            st.write(f"**Weight:** {dino['weight_kg']} kg")
            st.write(f"**Discovered:** {dino['discovered_year']}")
            st.write(f"**Found in:** {dino['found_in']}")
            st.info(f"💡 {dino['fun_fact']}")
else:
    st.error("Could not connect to the API.")
