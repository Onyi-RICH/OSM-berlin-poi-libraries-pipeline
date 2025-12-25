"""
Transform raw OSM library data.

- Selects relevant columns
- Standardizes naming and contact fields
- Converts geometry to Point
- Extracts latitude & longitude
- Removes duplicates
"""

import geopandas as gpd
import pandas as pd


KEEP_COLUMNS = [
    "name",
    "amenity",
    "operator:type",
    "operator",
    "addr:street",
    "addr:housenumber",
    "addr:postcode",
    "addr:city",
    "addr:country",
    "opening_hours",
    "wheelchair",
    "toilets:wheelchair",
    "level",
    "internet_access",
    "ref:isil",
    "email",
    "contact:email",
    "phone",
    "contact:phone",
    "website",
    "contact:website",
    "geometry",
]


def clean_libraries(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Clean and normalize OSM libraries dataset.
    """

    # Keep only expected columns
    gdf = gdf[[col for col in KEEP_COLUMNS if col in gdf.columns]].copy()

    # Rename columns to final schema
    gdf = gdf.rename(
        columns={
            "operator:type": "operator_type",
            "addr:street": "street",
            "addr:housenumber": "housenumber",
            "addr:postcode": "postcode",
            "addr:city": "city",
            "addr:country": "country",
            "wheelchair": "wheelchair_accessible",
            "toilets:wheelchair": "toilets_wheelchair",
            "ref:isil": "isil_code",
            "contact:email": "contact_email",
            "contact:phone": "contact_phone",
            "contact:website": "contact_website",
        }
    )

    # Merge email / phone fields
    gdf["final_email"] = gdf["email"].fillna(gdf.get("contact_email"))
    gdf["final_phone"] = gdf["phone"].fillna(gdf.get("contact_phone"))
    gdf["website_url"] = gdf["website"].fillna(gdf.get("contact_website"))

    # Convert geometry to Point (centroid if polygon)
    gdf["geom_point"] = gdf.geometry.centroid

    # Extract coordinates
    gdf["longitude"] = gdf["geom_point"].x
    gdf["latitude"] = gdf["geom_point"].y

    # Fill missing names
    gdf["name"] = gdf["name"].fillna("unknown")

    # Drop duplicates
    gdf = gdf.drop_duplicates(subset=["name", "street", "housenumber"])

    return gdf


if __name__ == "__main__":
    print("This module is intended to be imported and used in the pipeline.")

