
# editables
infile='ebd_US_relSep-2023.txt.gz'
outfile='2022_fl_hillsborough.txt'
statename='Florida'
countyname='Hillsborough'
year='2022'

# start with column names
gunzip $infile --stdout | head -1 > $outfile

# pipe requested data to a new file
# column 18 is state name
# column 20 is county name
# column 31 is observation date
time gunzip $infile --stdout | 
awk -F'\t' -v var1=$statename -v var2=$countyname -v var3=$year '($18 == var1) && ($20 == var2) && ($31~var3) {print $0}' >> $outfile