# column 31 is observation date
set -x
infile="/Volumes/Expansion/ebird/ebd_relOct-2025/ebd_relOct-2025.txt.gz"
# infile="/Volumes/Expansion/ebird/ebd_relOct-2025/ebd_relOct-2025.txt"

# time gunzip $infile --stdout | awk -F'\t' '$31>="2023-01-01" && $31<"2024-01-01" {print $0}' > $outfile
time gunzip $infile --stdout | awk -F'\t' '$31>="2023-01-01" && $31<"2024-01-01" {print $0}' > /Volumes/Expansion/ebird/ebd_relOct-2025/ebd_relOct-2025_2023.txt


