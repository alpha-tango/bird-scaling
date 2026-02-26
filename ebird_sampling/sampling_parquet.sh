"""
Take the unzipped sampling file, and rewrite it as a parquet file
using DuckDB. Normalize the column names so there are no spaces;
manually set the type of the `PROJECT IDENTIFIER` column to VARCHAR
so it doesn't autodetect int.
"""
set -x

sql=$(cat << END
set memory_limit='10GB';
PRAGMA temp_directory='temp';
COPY (
    SELECT * from read_csv(
        'data/ebd_sampling_relDec-2025/ebd_sampling_relDec-2025.txt',
        header=true,
        normalize_names=True,
        auto_detect=True,
        types={'project_identifiers': 'VARCHAR'}
    )
) to 'data/ebd_sampling_relDec-2025/ebd_sampling_relDec-2025.parquet' (FORMAT PARQUET);
END
)

time duckdb :memory: "$sql"
