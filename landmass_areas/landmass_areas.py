import geopandas as gpd
import landmass_areas_config
import pandas as pd

def main():
    polygon_df = gpd.read_file(landmass_areas_config.LAND_POLYGON_FILE)

    print(landmass_areas_config.LAND_POLYGON_FILE)
    print(polygon_df.head(20))
    print("\nAre there invalid geometries?: ", polygon_df[~polygon_df.is_valid])
    print("\n Are there empty geometries: ", polygon_df[polygon_df.is_empty])

    # Calculating area with WGS84 (EPSG:4326) directly is not recommended 
    # for accuracy because it uses latitude/longitude (degrees) rather than planar units (meters). 
    # As a geographic coordinate system, degrees of longitude vary in width depending on latitude.
    # Thus we convert to an coordinate system with meters as the unit.

    sq_m_per_sq_km = 1000000

    #### calculate area for antarctic polygon ####
    ##############################################

    # convert antarctic polygon only to an antarctic-specific CRS
    antarctic_area = polygon_df[polygon_df['FID']==306888].to_crs(landmass_areas_config.ANTARCTIC_AREA_CRS)
    # calculate the area
    antarctic_area['area_km2'] = antarctic_area['geometry'].area / sq_m_per_sq_km
    # convert to our default CRS so we can concatenate with the rest of the data
    # this results in a weird geometry, which we will handle later
    antarctic_area = antarctic_area.to_crs(landmass_areas_config.DEFAULT_AREA_CRS)
    
    #### calculate area for all other polygons ####
    ###############################################

    # convert everything EXCEPT antarctic polygon to specified CRS
    other_area = polygon_df[polygon_df['FID'] != 306888].to_crs(landmass_areas_config.DEFAULT_AREA_CRS)
    # calculate the area
    other_area['area_km2'] = other_area['geometry'].area / sq_m_per_sq_km
    
    #### now concatenate these two area dfs ####
    ############################################
    areas_df = pd.concat([antarctic_area, other_area])

    print("NEW AREAS DF")
    print(areas_df.head(20))
    print("\nArea DF - are there invalid geometries? (expect 1, FID=306888): ", areas_df[~areas_df.is_valid])
    # expect one invalid geometry from antarctica
    print("\nArea DF - are there empty geometries? ", areas_df[areas_df.is_empty])

    #### join original polygon df to area df ####
    #############################################

    # we want to move back to polygons of latitude/longitude,
    # but reprojecting back and forth results in invalid geometries
    joined = polygon_df.merge(areas_df, on='FID', how='left')
    final_areas_df = joined[['FID', 'geometry_x', 'area_km2']].copy()
    final_areas_df.rename(columns={'geometry_x': 'geometry'}, inplace=True)

    print("FINAL_AREAS_DF")
    print(final_areas_df.head(20))
    print("\nFinal Area DF - are there invalid geometries?: ", final_areas_df[~final_areas_df.is_valid])
    print("\nFinal Area DF - are there empty geometries? ", final_areas_df[final_areas_df.is_empty])

    final_areas_df.to_file('landmass_areas/outputs/shapefiles/albers_antarctic_areas.shp')

    return 0

if __name__ == "__main__":
    main()

