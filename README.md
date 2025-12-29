# 🌍 Terra-Valuation Engine: Geospatial Compliance Methodology (v3.0)
### *A Technical Demonstration of Real-Time Legal-Geographic Threshold Translation*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://aravalli-forensic-audit-2025.streamlit.app)
![Status](https://img.shields.io/badge/Status-Technical%20Demo-blue?style=for-the-badge)
![Stack](https://img.shields.io/badge/Stack-Python%20%7C%20GEE-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)

> **"Demonstrating how judicial thresholds can be translated into executable geospatial queries."**
> This project is a technical proof-of-concept for satellite-based compliance mapping, using the November 2025 Aravalli ruling as a demonstrative case study.

---

## ⚠️ IMPORTANT DISCLAIMERS
**This is an educational demonstration and software engineering portfolio project.**
* ❌ **NOT** legal advice or official environmental assessment.
* ❌ **NOT** a policy recommendation or government-approved mapping.
* ✅ **IS** a technical demonstration of satellite data processing capabilities.
* ✅ **IS** a reproducible methodology for academic reference.

---

## 🔬 Project Purpose & Methodology
This project demonstrates the technical pipeline required to operationalize legal definitions—specifically the November 2025 "100m local relief" threshold—into real-time satellite queries.

### 1. Relief Calculation (Legal Translation)
* **Input:** JAXA ALOS World 3D (30m resolution DEM).
* **Logic:** `Relief = Pixel_Elevation - Focal_Min(2km_Kernel)`.
* **Classification:** Differentiating Zone A (>100m) and Zone B (<100m) based on judicial benchmarks.

### 2. Temporal Change Detection
* **Input:** Sentinel-2 SR Harmonized (2016-2024).
* **Logic:** `NDVI_Loss = (NDVI_2016 > 0.3) AND (NDVI_2024 < 0.2)`.
* **Purpose:** Demonstrates irreversible vegetation change detection while filtering seasonal noise.

---

## 📊 Illustrative Findings (Demonstration Study Area)
*Outputs generated for the South Gurgaon Sector to illustrate model capabilities.*

| Metric | Computed Value | Technical Basis |
| :--- | :--- | :--- |
| **Threshold Output** | **34,358 Hectares** | Pixels where computed relief < 100m. |
| **Change Detection** | **4,685 Hectares** | Irreversible NDVI loss (Sentinel-2). |
| **Water Risk Model** | **34.4 Billion Liters** | Calculated via published CGWB coefficients. |
| **Economic Exposure**| **₹4.2 Lakh Crore** | Illustrative model using regional market data. |

* **Valuation Note:** The ₹4.2 Lakh Crore figure is an illustrative economic exposure model and does not represent an official valuation or legal claim.

---

## 👨‍💻 Developed By
**Ranjit Saha**

*Geospatial Systems Architect | Python • Google Earth Engine • Remote Sensing*
* 💡 **Project Status:** Independent Research / Original Intellectual Property.
* 📜 **License:** [MIT License](https://opensource.org/licenses/MIT).

---

## 🚀 Installation & Usage
**Prerequisites**
- Python 3.8+
- Basic understanding of GeoJSON/Geospatial data.

### 1. Clone the Repository
```bash 
   git clone https://github.com/Ranjit-Saha/aravalli-forensic-audit.git
   cd aravalli-forensic-audit
```
 

### 2.Install Dependencies   
```bash
pip install -r requirements.txt
```
  
  
### 3.Run the Forensic Engine
```bash
streamlit run app.py
```  
 
  
*The dashboard will launch automatically in your browser at* http://localhost:8501

 