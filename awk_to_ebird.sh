# column 31 is observation date
set -x
infile='ebd_US_relSep-2023.txt.gz'
# infile='ebd_US_relSep-2023_head1000.txt.gz'

sql=$(cat << END
set memory_limit='10GB';
PRAGMA temp_directory='temp';
COPY (
    SELECT * from read_csv(
        '/dev/stdin',        delim='\t',
        header=true,
        columns={'GLOBAL_UNIQUE_IDENTIFIER': 'VARCHAR',
                'LAST_EDITED_DATE': 'TIMESTAMP',
                'TAXONOMIC_ORDER': 'INTEGER',
                'CATEGORY': 'VARCHAR',
                'TAXON_CONCEPT_ID': 'VARCHAR',
                'COMMON_NAME': 'VARCHAR',
                'SCIENTIFIC_NAME': 'VARCHAR',
                'SUBSPECIES_COMMON_NAME': 'VARCHAR',
                'SUBSPECIES_SCIENTIFIC_NAME': 'VARCHAR',
                'EXOTIC_CODE': 'VARCHAR',
                'OBSERVATION_COUNT': 'VARCHAR',
                'BREEDING_CODE': 'VARCHAR',
                'BREEDING_CATEGORY': 'VARCHAR',
                'BEHAVIOR_CODE': 'VARCHAR',
                'AGE_SEX': 'VARCHAR',
                'COUNTRY': 'VARCHAR',
                'COUNTRY_CODE': 'VARCHAR',
                'STATE': 'VARCHAR',
                'STATE_CODE': 'VARCHAR',
                'COUNTY': 'VARCHAR',
                'COUNTY_CODE': 'VARCHAR',
                'IBA_CODE': 'VARCHAR',
                'BCR_CODE': 'INTEGER',
                'USFWS_CODE': 'VARCHAR',
                'ATLAS_BLOCK': 'VARCHAR',
                'LOCALITY': 'VARCHAR',
                'LOCALITY_ID': 'VARCHAR',
                'LOCALITY_TYPE': 'VARCHAR',
                'LATITUDE': 'DOUBLE',
                'LONGITUDE': 'DOUBLE',
                'OBSERVATION_DATE': 'DATE',
                'TIME_OBSERVATIONS_STARTED': 'VARCHAR',
                'OBSERVER_ID': 'VARCHAR',
                'SAMPLING_EVENT_IDENTIFIER': 'VARCHAR',
                'PROTOCOL_TYPE': 'VARCHAR',
                'PROTOCOL_CODE': 'VARCHAR',
                'PROJECT_CODE': 'VARCHAR',
                'DURATION_MINUTES': 'DOUBLE',
                'EFFORT_DISTANCE_KM': 'DOUBLE',
                'EFFORT_AREA_HA': 'DOUBLE',
                'NUMBER_OBSERVERS': 'INTEGER',
                'ALL_SPECIES_REPORTED': 'BOOLEAN',
                'GROUP_IDENTIFIER': 'VARCHAR',
                'HAS_MEDIA': 'BOOLEAN',
                'APPROVED': 'BOOLEAN',
                'REVIEWED': 'BOOLEAN',
                'REASON': 'VARCHAR',
                'TRIP_COMMENTS': 'VARCHAR',
                'SPECIES_COMMENTS': 'VARCHAR'
                }
    )
) to 'ebird_2020.parquet' (FORMAT PARQUET);
END
)

time gunzip $infile --stdout | awk -F'\t' '$31>="2020-01-01" && $31<"2021-01-01" {print $0}' | duckdb :memory: "$sql"