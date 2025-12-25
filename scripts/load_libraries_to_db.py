"""
Load cleaned and enriched Berlin libraries data into Postgres/PostGIS.

- Inserts into berlin_source_data.libraries
- Uses ON CONFLICT DO NOTHING to avoid duplicates
- Safe to re-run
"""

import psycopg2
import psycopg2.extras
import geopandas as gpd
from typing import List


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "berlin",
    "user": "postgres",
    "password": "postgres",
}


TARGET_TABLE = "berlin_source_data.libraries"


COLUMNS = [
    "name",
    "amenity",
    "operator_type",
    "operator",
    "street",
    "housenumber",
    "postcode",
    "city",
    "country",
    "latitude",
    "longitude",
    "opening_hours",
    "wheelchair_accessible",
    "toilets_wheelchair",
    "level",
    "internet_access",
    "isil_code",
    "final_email",
    "final_phone",
    "website_url",
    "district",
    "neighbourhood",
    "district_id",
]


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def insert_libraries(gdf: gpd.GeoDataFrame):
    """
    Insert library records into Postgres.
    """

    conn = get_connection()
    cur = conn.cursor()

    insert_sql = f"""
        INSERT INTO {TARGET_TABLE} (
            {", ".join(COLUMNS)}
        )
        VALUES %s
        ON CONFLICT DO NOTHING;
    """

    values = [
        tuple(row[col] for col in COLUMNS)
        for _, row in gdf.iterrows()
    ]

    psycopg2.extras.execute_values(
        cur,
        insert_sql,
        values,
        page_size=1000
    )

    conn.commit()
    cur.close()
    conn.close()

    print(f"Inserted {len(values)} records into {TARGET_TABLE}")


if __name__ == "__main__":
    print("This script should be imported and called from the pipeline.")
