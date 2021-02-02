# fetch all data from courtlistener
python get-cases.py
python clean_archived_dat.py

# filter and update data
Rscript filter-newest-data.r

# post data on google sheet in a new tab