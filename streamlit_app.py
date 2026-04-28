import streamlit as st
import requests

API_URL = "https://dinosaur-api-xe77.onrender.com"

st.set_page_config(page_title="🦕 Dinosaur Facts", layout="wide")
st.title("🦕 Dinosaur Facts Explorer")
st.markdown("A full SCRUD frontend consuming the Dinosaur Facts REST API on Render.")

# ── AUTH ──────────────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("🔐 Login Required")
    st.markdown("Enter your API secret key to access the app.")
    key_input = st.text_input("Secret Key", type="password", placeholder="your-super-secret-key")
    if st.button("Login"):
        test = requests.delete(f"{API_URL}/dinosaurs/99999",
                               headers={"Authorization": f"Bearer {key_input}"})
        if test.status_code in [200, 404]:
            st.session_state.authenticated = True
            st.session_state.secret_key = key_input
            st.rerun()
        else:
            st.error("❌ Invalid key. Try again.")
    st.stop()

HEADERS = {"Authorization": f"Bearer {st.session_state.secret_key}"}

# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.success("🔓 Logged in")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.secret_key = ""
        st.rerun()
    st.divider()
    menu = st.selectbox("Choose Operation", [
        "🔍 Search / List",
        "📖 Get by ID",
        "➕ Create",
        "✏️ Update",
        "🗑️ Delete"
    ])

# ── SEARCH ────────────────────────────────────────────────────
if menu == "🔍 Search / List":
    st.header("🔍 Search Dinosaurs")
    col1, col2 = st.columns(2)
    with col1:
        diet = st.selectbox("Filter by Diet", ["", "Carnivore", "Herbivore", "Omnivore", "Piscivore"])
    with col2:
        period = st.selectbox("Filter by Period", ["", "Late Cretaceous", "Early Cretaceous", "Late Jurassic"])

    if st.button("Search"):
        params = {}
        if diet:
            params["diet"] = diet
        if period:
            params["period"] = period
        response = requests.get(f"{API_URL}/dinosaurs", params=params)
        if response.status_code == 200:
            data = response.json()
            if data:
                st.success(f"Found {len(data)} dinosaur(s)")
                for dino in data:
                    with st.expander(f"🦖 {dino['name']} — {dino['diet']} | {dino['period']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**ID:** {dino['id']}")
                            st.write(f"**Period:** {dino['period']}")
                            st.write(f"**Diet:** {dino['diet']}")
                            st.write(f"**Length:** {dino['length_m']} m")
                            st.write(f"**Weight:** {dino['weight_kg']} kg")
                        with col2:
                            st.write(f"**Discovered:** {dino['discovered_year']}")
                            st.write(f"**Found in:** {dino['found_in']}")
                            st.info(f"💡 {dino['fun_fact']}")
            else:
                st.warning("No dinosaurs found for that filter.")
        else:
            st.error("Failed to fetch dinosaurs.")

# ── GET BY ID ─────────────────────────────────────────────────
elif menu == "📖 Get by ID":
    st.header("📖 Get Dinosaur by ID")
    dino_id = st.number_input("Enter Dinosaur ID", min_value=1, step=1)
    if st.button("Get"):
        response = requests.get(f"{API_URL}/dinosaurs/{int(dino_id)}")
        if response.status_code == 200:
            dino = response.json()
            st.success(f"Found: {dino['name']}")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**ID:** {dino['id']}")
                st.write(f"**Period:** {dino['period']}")
                st.write(f"**Diet:** {dino['diet']}")
                st.write(f"**Length:** {dino['length_m']} m")
                st.write(f"**Weight:** {dino['weight_kg']} kg")
            with col2:
                st.write(f"**Discovered:** {dino['discovered_year']}")
                st.write(f"**Found in:** {dino['found_in']}")
                st.info(f"💡 {dino['fun_fact']}")
        elif response.status_code == 404:
            st.error(f"No dinosaur found with ID {int(dino_id)}")
        else:
            st.error("Something went wrong.")

# ── CREATE ────────────────────────────────────────────────────
elif menu == "➕ Create":
    st.header("➕ Add a New Dinosaur")
    with st.form("create_form"):
        name            = st.text_input("Name *", placeholder="e.g. Allosaurus")
        period          = st.selectbox("Period *", ["Late Cretaceous", "Early Cretaceous", "Late Jurassic", "Early Jurassic", "Triassic"])
        diet            = st.selectbox("Diet *", ["Carnivore", "Herbivore", "Omnivore", "Piscivore"])
        col1, col2      = st.columns(2)
        with col1:
            length_m        = st.number_input("Length (m)", min_value=0.0, step=0.1)
            discovered_year = st.number_input("Discovered Year", min_value=1800, max_value=2100, step=1, value=1900)
        with col2:
            weight_kg       = st.number_input("Weight (kg)", min_value=0, step=100)
            found_in        = st.text_input("Found In", placeholder="e.g. Montana, USA")
        fun_fact        = st.text_area("Fun Fact", placeholder="Something interesting...")
        submitted       = st.form_submit_button("➕ Create Dinosaur")

    if submitted:
        if not name:
            st.error("Name is required.")
        else:
            payload = {
                "name": name,
                "period": period,
                "diet": diet,
                "length_m": length_m,
                "weight_kg": weight_kg,
                "discovered_year": discovered_year,
                "found_in": found_in,
                "fun_fact": fun_fact
            }
            response = requests.post(f"{API_URL}/dinosaurs", json=payload, headers=HEADERS)
            if response.status_code == 201:
                dino = response.json()
                st.success(f"✅ Created {dino['name']} with ID {dino['id']}!")
            else:
                st.error(f"Failed to create: {response.text}")

# ── UPDATE ────────────────────────────────────────────────────
elif menu == "✏️ Update":
    st.header("✏️ Update a Dinosaur")
    dino_id = st.number_input("Enter Dinosaur ID to update", min_value=1, step=1)

    if st.button("Load"):
        response = requests.get(f"{API_URL}/dinosaurs/{int(dino_id)}")
        if response.status_code == 200:
            st.session_state.loaded_dino = response.json()
            st.success(f"Loaded: {st.session_state.loaded_dino['name']}")
        else:
            st.error(f"Dinosaur with ID {int(dino_id)} not found.")

    if "loaded_dino" in st.session_state:
        dino = st.session_state.loaded_dino
        with st.form("update_form"):
            name            = st.text_input("Name", value=dino["name"])
            period          = st.text_input("Period", value=dino["period"])
            diet            = st.text_input("Diet", value=dino["diet"])
            col1, col2      = st.columns(2)
            with col1:
                length_m        = st.number_input("Length (m)", value=float(dino["length_m"] or 0), step=0.1)
                discovered_year = st.number_input("Discovered Year", value=int(dino["discovered_year"] or 1900), step=1)
            with col2:
                weight_kg       = st.number_input("Weight (kg)", value=int(dino["weight_kg"] or 0), step=100)
                found_in        = st.text_input("Found In", value=dino["found_in"] or "")
            fun_fact        = st.text_area("Fun Fact", value=dino["fun_fact"] or "")
            submitted       = st.form_submit_button("✏️ Update Dinosaur")

        if submitted:
            payload = {
                "name": name,
                "period": period,
                "diet": diet,
                "length_m": length_m,
                "weight_kg": weight_kg,
                "discovered_year": discovered_year,
                "found_in": found_in,
                "fun_fact": fun_fact
            }
            response = requests.put(f"{API_URL}/dinosaurs/{dino['id']}", json=payload, headers=HEADERS)
            if response.status_code == 200:
                st.success(f"✅ Updated {response.json()['name']} successfully!")
                del st.session_state.loaded_dino
            else:
                st.error(f"Failed to update: {response.text}")

# ── DELETE ────────────────────────────────────────────────────
elif menu == "🗑️ Delete":
    st.header("🗑️ Delete a Dinosaur")
    dino_id = st.number_input("Enter Dinosaur ID to delete", min_value=1, step=1)

    if st.button("Load Dinosaur"):
        response = requests.get(f"{API_URL}/dinosaurs/{int(dino_id)}")
        if response.status_code == 200:
            dino = response.json()
            st.warning(f"You are about to delete: **{dino['name']}** (ID {dino['id']})")
            st.session_state.dino_to_delete = dino
        else:
            st.error("Dinosaur not found.")

    if "dino_to_delete" in st.session_state:
        if st.button("🗑️ Confirm Delete", type="primary"):
            dino = st.session_state.dino_to_delete
            response = requests.delete(f"{API_URL}/dinosaurs/{dino['id']}", headers=HEADERS)
            if response.status_code == 200:
                st.success(f"✅ Deleted {dino['name']} successfully!")
                del st.session_state.dino_to_delete
            else:
                st.error(f"Failed to delete: {response.text}")
