
"""
Extract libraries in Berlin from OpenStreetMap using OSMnx.

- Filters by amenity=library
- Returns raw GeoDataFrame with OSM attributes
- Output is used for downstream transformation
"""

import osmnx as ox
import geopandas as gpd


def extract_osm_libraries(place: str = "Berlin, Germany") -> gpd.GeoDataFrame:
    """
    Fetch libraries from OSM for a given place.

    Args:
        place (str): Place name used by OSMnx

    Returns:
        GeoDataFrame: Raw OSM libraries data
    """
    
    # Define filter for OSM to get only libraries
    tags = {"amenity": "library"}
    
    # Query OSM for features matching tags in the target place
    gdf = ox.features_from_place(place, tags)
    
    # Convert coordinate system to standard WGS84 (lat/lon)
    gdf = gdf.to_crs(epsg=4326)
    
    # Reset index to expose OSM IDs as columns
    gdf = gdf.reset_index()
    
    return gdf

if __name__ == "__main__":
    # Extract library features in Berlin
    libraries_gdf = extract_osm_libraries()
    # Print how many records were found
    print(f"Extracted {len(libraries_gdf)} library records from OSM")
