
"""
Spatial enrichment for Berlin libraries.

- Assigns districts using spatial joins
- Attaches district_id
- Adds neighborhood names
"""

import geopandas as gpd
import pandas as pd


def enrich_with_districts(
    libraries_gdf: gpd.GeoDataFrame,
    districts_gdf: gpd.GeoDataFrame,
    district_lookup: pd.DataFrame,
) -> gpd.GeoDataFrame:
    """
    Spatially join libraries with Berlin districts.
    """

    # Ensure CRS alignment (Make sure all GeoDataFrames use the same coordinate system (WGS84))
    libraries_gdf = libraries_gdf.set_geometry("geom_point").to_crs(epsg=4326)
    districts_gdf = districts_gdf.to_crs(epsg=4326)

    # Spatial join (Join library points to districts polygons via spatial join ("within" means point within polygon)
    joined = gpd.sjoin()
    joined = gpd.sjoin(
        libraries_gdf,
        districts_gdf[["district", "geometry"]],
        how="left",
        predicate="within",
    )

    # Map district_id (Attach district_id and neighborhood names by matching on 'district')
    joined = joined.merge(
        district_lookup,
        on="district",
        how="left",
    )

    return joined


if __name__ == "__main__":
    # This is a simple status check for running the script directly
    print("Spatial enrichment module ready.")
    print("Spatial enrichment module ready.")
