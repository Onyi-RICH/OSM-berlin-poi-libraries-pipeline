# 📚 Berlin Libraries — OSM ETL & Geospatial Data Layer

**End-to-End ETL Pipeline for OpenStreetMap Libraries in Berlin**

This project implements a full **extract–transform–load (ETL) pipeline** for integrating **Berlin public library data** from OpenStreetMap (OSM) into a **clean, enriched, and database-ready unified table**.  
The pipeline is designed for **analytics, spatial queries, and downstream data products**, and follows data engineering best practices for reproducibility and scalability.

---

## 📓 Notebook Overview

### `01_extract_osm_libraries.ipynb`  
Extracts all library Points of Interest (POIs) in Berlin from OpenStreetMap using **OSMnx**.

This notebook:
- Queries OSM using `amenity=library`
- Retrieves raw OSM attributes and geometries
- Reprojects data to WGS84 (EPSG:4326)
- Outputs a raw GeoJSON file used for downstream transformation

---

### `02_transform_libraries.ipynb`  
Cleans and normalizes raw OSM library data into a consistent analytical schema.

This notebook:
- Selects and standardizes relevant OSM attributes
- Normalizes column names to snake_case
- Merges duplicated contact fields (`email`, `contact:email`, etc.)
- Converts polygon geometries to point centroids
- Extracts latitude and longitude
- Handles missing names and removes duplicates
- Produces a cleaned libraries dataset aligned with the unified schema

---

### `03_spatial_enrichment.ipynb`  
Adds administrative and spatial context to the libraries dataset.

This notebook:
- Performs spatial joins between library points and Berlin district polygons
- Assigns district names and `district_id`
- Enriches records with neighborhood information
- Ensures CRS consistency across all spatial layers
- Outputs a fully enriched GeoJSON dataset

---

### `04_load_libraries_to_db.ipynb`  
Handles database integration and final loading into Postgres/PostGIS.

This notebook:
- Connects to a PostgreSQL/PostGIS database
- Inserts records into `berlin_source_data.libraries`
- Applies schema constraints
- Uses `ON CONFLICT DO NOTHING` to prevent duplicate inserts
- Is safe to re-run for incremental or recovery loads

---

## 🔄 Applied Data Transformation Steps

- Column normalization (snake_case, standardized field names)
- Source harmonization of OSM tags into a unified schema
- Geometry validation and conversion to Point geometries
- CRS reprojection to WGS84 (EPSG:4326)
- Spatial joins for district and neighborhood assignment
- Deduplication based on name and address fields
- Contact field consolidation (email, phone, website)
- Schema enforcement prior to database insertion

---

## ✅ Data Validation

- **CRS Consistency**  
  All geometries are reprojected to WGS84 (EPSG:4326).

- **Geometry Validity**  
  Polygon and multipolygon features are converted to point centroids for spatial joins and analytics.

- **Spatial Extent**  
  All library records are verified to fall within the Berlin administrative boundary.

- **Duplicate Handling**  
  Duplicate libraries are removed using a composite key of name and address.

- **Null Handling**  
  Missing library names are filled with `"unknown"` to preserve record integrity.

---

## 🧠 Architecture Decision: One Unified Libraries Table

During development, we evaluated whether to:
- Maintain multiple source-specific tables (raw OSM, cleaned OSM, enriched OSM), or
- Produce a **single harmonized libraries table** for analytics and application use.

### Exploration Summary

- OpenStreetMap exposes highly flexible and inconsistent tagging
- Many attributes overlap semantically across records
- Libraries can appear as points or polygons
- District and neighborhood information must be spatially derived
- Downstream analytics benefit from a single, stable schema

---

### ✅ Final Decision: One Unified Libraries Table

A single integrated libraries table was chosen because it provides:

- A consistent schema across all library records
- Simplified spatial querying and analytics
- Easier QA and validation
- Cleaner integration into unified city-wide data models
- Compatibility with scalable POI layer ingestion pipelines

Source lineage is preserved through OSM identifiers and raw attributes, without fragmenting the data model.

---

## 🗂️ Final Libraries Table Schema

| Field Name | Description |
|-----------|------------|
| library_id | Unique library identifier (PK) |
| name | Library name |
| amenity | OSM amenity type (`library`) |
| operator_type | Type of operating organization |
| operator | Library operator |
| street | Street name |
| housenumber | House number |
| postcode | Postal code |
| city | City name |
| country | Country code |
| latitude | Latitude (EPSG:4326) |
| longitude | Longitude (EPSG:4326) |
| opening_hours | Opening hours (OSM format) |
| wheelchair_accessible | Wheelchair accessibility flag |
| toilets_wheelchair | Wheelchair accessible toilets |
| level | Floor level |
| internet_access | Internet availability |
| isil_code | International library identifier |
| final_email | Consolidated email contact |
| final_phone | Consolidated phone contact |
| website_url | Library website |
| district | Berlin district name |
| neighbourhood | Neighborhood name |
| district_id | District identifier (FK) |
| geometry | Geometry (Point, EPSG:4326) |


---

## 🛠️ Tools & Technologies

- **Languages**: Python, SQL  
- **Libraries**: pandas, geopandas, osmnx, psycopg2  
- **Databases**: PostgreSQL, PostGIS  
- **Environment**: Jupyter Notebook 

---