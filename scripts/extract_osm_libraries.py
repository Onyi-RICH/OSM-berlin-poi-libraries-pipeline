
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
    tags = {"amenity": "library"}
    gdf = ox.features_from_place(place, tags)

    # Ensure WGS84
    gdf = gdf.to_crs(epsg=4326)

    # Reset index to expose OSM IDs
    gdf = gdf.reset_index()

    return gdf


if __name__ == "__main__":
    libraries_gdf = extract_osm_libraries()
    print(f"Extracted {len(libraries_gdf)} library records from OSM")
