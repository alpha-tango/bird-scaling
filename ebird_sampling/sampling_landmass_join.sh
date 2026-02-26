"""
Take the parquet file of sampling data, with a coordinate column already added,
and join it to the landmass area data.
"""
set -x

sql=$(cat << END
SET memory_limit='10GB';
PRAGMA temp_directory='temp';

INSTALL spatial;
LOAD spatial;

CREATE TABLE landmass_areas AS
    SELECT *
    FROM ST_Read('data/landmass_areas/albers_projection_areas.shp');

CREATE INDEX geom_idx ON landmass_areas USING RTREE (geom);

CREATE TABLE sampling_events AS
    SELECT *,
    ST_Point(longitude, latitude) AS coordinates
    FROM 'data/ebd_sampling_relDec-2025/ebd_sampling_relDec-2025.parquet'
    WHERE observation_date >= '2024-01-01'
        AND observation_date < '2025-01-01';

COPY (
    SELECT sampling_events.*,
    landmass_areas.FID
    FROM sampling_events
    LEFT JOIN landmass_areas 
        ON ST_CONTAINS(landmass_areas.geom, sampling_events.coordinates)
) to 'data/ebd_sampling_relDec-2025/ebd_sampling_relDec-2025_landmasses_2024.parquet' (FORMAT PARQUET);

END
)

time duckdb :memory: "$sql"


