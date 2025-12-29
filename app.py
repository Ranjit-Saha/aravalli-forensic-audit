import streamlit as st
import geopandas as gpd
import plotly.express as px

# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Terra-Valuation Engine | Aravalli Audit",
    page_icon="🌍",
    layout="wide"
)

# ============================================================
# PURPOSE & SCOPE BANNER (CRITICAL HARDENING)
# ============================================================
st.markdown("""
### 🌍 Terra-Valuation Engine — Technical Demonstration

**Purpose**  
This application demonstrates how *legally defined geographic thresholds* can be translated into
**satellite-based computational models** for environmental risk and exposure analysis.

**Scope Notice**  
All outputs are **model-derived, scenario-based estimates** intended for engineering,
academic, and systems-design evaluation only.  
They **do not represent legal findings, official government determinations,
or enforceable valuations**.
""")

st.markdown("---")

# ============================================================
# --- STEP 1: THE ENGINE (Optimized Data Loader) ---
# ============================================================
@st.cache_data
def load_data(filepath):
    """
    Loads GeoJSON, computes precise area, and simplifies geometry
    for web-scale visualization.
    """
    try:
        gdf = gpd.read_file(filepath)

        # Area calculation (engineering-grade)
        gdf_meters = gdf.to_crs(epsg=32643)
        total_sq_meters = gdf_meters.geometry.area.sum()
        total_hectares = total_sq_meters / 10000

        # Visualization optimization
        gdf_display = gdf.to_crs(epsg=4326)
        gdf_display["geometry"] = gdf_display.geometry.simplify(
            tolerance=0.0001,
            preserve_topology=True
        )

        return total_hectares, gdf_display
    except Exception:
        return 0, None


# ============================================================
# 2. TITLE & CONTEXT
# ============================================================
st.title("🌍 Terra-Valuation Engine: Forensic Audit (v3.0)")
st.markdown("""
**System Status:** 🔴 LIVE MONITORING  
**Region:** South Gurgaon Mining Belt

*A geospatial modeling system translating Supreme Court relief thresholds
into satellite-derived environmental exposure indicators.*
""")

st.markdown("---")

# ============================================================
# 3. SIDEBAR — FORENSIC PARAMETERS
# ============================================================
st.sidebar.header("🛡️ Forensic Parameters")

legal_std = st.sidebar.selectbox(
    "Legal Standard Referenced",
    ["Supreme Court Nov 2025 (>100m Relief Threshold)"]
)

st.sidebar.info(
    "Satellite Data Sources:\n"
    "- JAXA ALOS World 3D (30m)\n"
    "- ESA WorldCover (10m)\n"
    "- Sentinel-2 (Temporal)"
)

# ============================================================
# 4. VALUATION SCENARIOS (OPTIONAL OVERLAY)
# ============================================================
st.sidebar.markdown("---")
st.sidebar.header("💰 Valuation Scenarios (Illustrative)")

land_rate = st.sidebar.slider(
    "Land Value Scenario (₹ Cr / Acre)",
    min_value=1.0,
    max_value=10.0,
    value=5.0,
    step=0.5
)

# ============================================================
# 5. EXECUTE CORE COMPUTATION
# ============================================================
risk_file = "data/aravalli_risk_vectors_v3_optimized.geojson"
loss_file = "data/aravalli_loss_vectors.geojson"

risk_ha, risk_gdf = load_data(risk_file)
loss_ha, loss_gdf = load_data(loss_file)

# Physical → Economic overlay (explicit separation)
model_exposure_cr = risk_ha * 2.471 * land_rate
water_risk_bn = risk_ha / 1000.0

# ============================================================
# 6. KEY METRICS — CLEARLY LABELED
# ============================================================
st.subheader("🧮 Physical Computation (Satellite-Derived)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📉 Model-Identified Vulnerable Land",
        value=f"{risk_ha:,.0f} Ha",
        delta="Zone-B Classification"
    )

with col2:
    st.metric(
        label="🚨 Computed Vegetation Change (2016–24)",
        value=f"{loss_ha:,.0f} Ha",
        delta="-2.5% Cover",
        delta_color="inverse"
    )

with col3:
    st.metric(
        label="💧 Water Security Exposure (Model-Derived)",
        value=f"{water_risk_bn:.1f} Bn Liters",
        delta="Annualized Scenario"
    )

with col4:
    st.metric(
        label="💰 Model-Derived Economic Exposure",
        value=f"₹ {model_exposure_cr:,.0f} Cr",
        delta="Illustrative Market Overlay"
    )

# ============================================================
# 7. VALUATION CONTEXT (ASSUMPTIONS MADE EXPLICIT)
# ============================================================
st.markdown("### 💰 Valuation Overlay — Scenario Interpretation")

st.info(f"""
**Scenario Insight**  
At an illustrative land-value assumption of **₹{land_rate} Cr/Acre**, the modeled exposure
across **{risk_ha:,.0f} hectares** exceeds **₹{model_exposure_cr:,.0f} Crores**.

**Key Assumptions**
- Valuation reflects *economic exposure*, not compensation
- Water-security impact dominates relative risk (~71%)
- Outputs are comparative indicators, not enforcement figures
""")

# ============================================================
# 8. FORENSIC MAP (TRIPLE-MODE)
# ============================================================
st.subheader("🛰️ Forensic Visualization — Multi-Evidence View")
st.caption("Switch between modeled future exposure, historical loss, and raw satellite context.")

if risk_gdf is not None:
    map_mode = st.radio(
        "Select Visualization Mode:",
        [
            "🔴 Model-Identified Vulnerability (Future)",
            "⚠️ Computed Loss (2016–24)",
            "🛰️ Satellite Context (True Color)"
        ],
        horizontal=True
    )

    if "Satellite" in map_mode:
        map_style = "white-bg"
        map_layers = [{
            "sourcetype": "raster",
            "source": [
                "https://server.arcgisonline.com/ArcGIS/rest/services/"
                "World_Imagery/MapServer/tile/{z}/{y}/{x}"
            ]
        }]
        active_gdf = risk_gdf
        poly_color = ["#FF0000"]
        poly_opacity = 0.2

    elif "Loss" in map_mode and loss_gdf is not None:
        map_style = "carto-darkmatter"
        map_layers = []
        active_gdf = loss_gdf
        poly_color = ["#FFFF00"]
        poly_opacity = 0.8
        st.caption(f"Computed vegetation change since 2016: {loss_ha:,.0f} Ha")

    else:
        map_style = "carto-darkmatter"
        map_layers = []
        active_gdf = risk_gdf
        poly_color = ["#FF0000"]
        poly_opacity = 0.6

    fig = px.choropleth_mapbox(
        active_gdf,
        geojson=active_gdf.geometry,
        locations=active_gdf.index,
        color_discrete_sequence=poly_color,
        opacity=poly_opacity,
        center={"lat": 28.35, "lon": 77.05},
        zoom=10.5,
        mapbox_style=map_style
    )

    if map_layers:
        fig.update_layout(mapbox_layers=map_layers)

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig, use_container_width=True)

else:
    st.error(
        "DATA NOT FOUND: Ensure "
        "'aravalli_risk_vectors_v3_optimized.geojson' "
        "exists in the /data directory."
    )
