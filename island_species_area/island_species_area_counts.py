import duckdb
import island_species_area_counts_config as config

def create_sampling_events_table():
    # next load the sampling events with landmass fid

    duckdb.sql(f"""
    CREATE TABLE sampling_events AS
        SELECT *
        FROM '{config.sampling_events_file}'
    """)
    return

def create_landmass_table():
    duckdb.sql(f"""CREATE TABLE landmass_areas AS
    SELECT fid, area_km2, geom, ST_CENTROID(geom) AS centroid
    FROM ST_Read('{config.area_shapefile}')""")
    return


def main():

    # duckdb spatial settings
    duckdb.sql(
        """
        INSTALL SPATIAL;
        LOAD SPATIAL;
        """
    )

    # create tables for running joins
    create_sampling_events_table()
    create_landmass_table()

    # create a table of landmass counts
    duckdb.sql(
        f"""
        CREATE TABLE landmass_counts AS
        SELECT sampling_events.FID AS landmass_fid,
            COUNT(distinct scientific_name) as species_count,
            COUNT(distinct sampling_events.sampling_event_identifier) as checklists_submitted,
            SUM(sampling_events.duration_minutes) AS total_minutes,
            SUM(sampling_events.effort_distance_km) AS total_effort_km,
            COUNT(distinct sampling_events.observer_id) as observer_count
        FROM '{config.ebird_observation_file}' AS ebird_observations
        INNER JOIN sampling_events on ebird_observations.sampling_event_identifier = sampling_events.sampling_event_identifier
        where SAMPLING_EVENTS.fid is not null
        GROUP BY 1
        """
    )

    # write plain counts and areas
    areas_and_counts = duckdb.sql("""
    SELECT
        landmass_fid,
        ST_X(centroid) AS centroid_x,
        ST_Y(centroid) AS centroid_y,
        species_count,
        checklists_submitted,
        total_minutes,
        total_effort_km,
        observer_count,
        area_km2,
        checklists_submitted/area_km2 AS checklists_per_km2,
        observer_count/area_km2 AS observers_per_km2,
        row_number() OVER (ORDER BY area_km2) // 50 as rank_group_50,
        row_number() OVER (ORDER BY area_km2) // 100 as rank_group_100,
        row_number() OVER (ORDER BY area_km2) // 500 as rank_group_500,
        row_number() OVER (ORDER BY area_km2) // 1000 as rank_group_1000,
        row_number() OVER (ORDER BY area_km2) // 5000 as rank_group_5000,
        row_number() OVER (ORDER BY area_km2) // 10000 as rank_group_10000
    FROM landmass_counts
    LEFT JOIN landmass_areas ON landmass_counts.landmass_fid = landmass_areas.fid
    """).to_df()

    print("areas with checklists and counts shape: ", areas_and_counts.shape)
    print(areas_and_counts.count())
    
    areas_and_counts.sort_values(by='area_km2', ascending=True)
    areas_and_counts.to_csv(f'island_species_area/outputs/areas_and_counts_{config.run_label}.csv')

    # repeat with full outer join
    areas_and_counts_2 = duckdb.sql("""
    SELECT
        landmass_areas.fid,
        ST_X(centroid) AS centroid_x,
        ST_Y(centroid) AS centroid_y,
        species_count,
        checklists_submitted,
        total_minutes,
        total_effort_km,
        observer_count,
        area_km2,
        checklists_submitted/area_km2 AS checklists_per_km2,
        observer_count/area_km2 AS observers_per_km2,
        row_number() OVER (ORDER BY area_km2) // 50 as rank_group_50,
        row_number() OVER (ORDER BY area_km2) // 100 as rank_group_100,
        row_number() OVER (ORDER BY area_km2) // 500 as rank_group_500,
        row_number() OVER (ORDER BY area_km2) // 1000 as rank_group_1000,
        row_number() OVER (ORDER BY area_km2) // 5000 as rank_group_5000,
        row_number() OVER (ORDER BY area_km2) // 10000 as rank_group_10000
    FROM landmass_counts
    FULL OUTER JOIN landmass_areas ON landmass_counts.landmass_fid = landmass_areas.fid
    """).to_df()

    print("all areas and counts shape: ", areas_and_counts_2.shape)
    print(areas_and_counts_2.count())
    areas_and_counts_2.sort_values(by='area_km2', ascending=True)
    areas_and_counts_2.to_csv(f'island_species_area/outputs/all_areas_and_counts_{config.run_label}.csv')


    return 0


if __name__=="__main__":
    main()
