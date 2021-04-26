import pandas as pd
import json
import numpy as np
import pathlib
from datetime import datetime

# GET DATE
current_date = datetime.now().date()
formatted_date = current_date.strftime("%m-%d-%Y")

# set up paths + files names
data_path = pathlib.Path.home() / 'UCLA' / 'code' / 'compassionate-releases' / 'compassionate-release-denials' / 'data'
archive_file_name = 'archive_' + formatted_date + '.csv'
outfile_loc = data_path / archive_file_name

# open most recently fetched data
with open(data_path / 'granted_archive.json', mode = 'r') as f:
    granted_archive = json.load(f)

with open(data_path / 'denied_archive.json', mode = 'r') as f:
    denied_archive = json.load(f)

with open(data_path / 'main_archive.json', mode = 'r') as f:
    main_archive = json.load(f)

# clean it up
def filter_data(json_dat, all_columns):
    rows = []
    for item in json_dat:
        rows.append(item)
    df = pd.DataFrame(rows)
    df['dateFiled_clean'] = df['entry_date_filed'].str[5:7] + '/' + df['entry_date_filed'].str[8:10] + '/' + df['entry_date_filed'].str[2:4]
    df['citation'] = df['caseName'] + ', No. ' + df['docketNumber'].astype(str) + ', Dkt. No. ' + df['entry_number'].astype(str) + ' ([' + df['dateFiled_clean'] + '])'
    df['url'] = 'https://www.courtlistener.com' + df['absolute_url']
    df['reviewed']  = 'No'
    columns = ['caseName', 'docketNumber', 'docket_id', 'court', 'dateFiled_clean', 'entry_number', 'description', 'status', 
                'assignedTo', 'referredTo', 'suitNature', 'cause', 'attorney', 'citation', 'url', 'reviewed']
    if all_columns: 
        out = df
    else:
        out = df[columns]
    out = out.rename(columns = {'caseName': 'Case Name',
                                    'docketNumber': 'Docket Number',
                                    'docket_id': "Docket ID",
                                    'court': 'Federal Court Name',
                                    'dateFiled_clean': 'Date Filed',
                                    'entry_number': 'Document Number',
                                    'description': 'Document Description',
                                    'status': 'Granted or denied',
                                    'assignedTo': 'Judge (initial)',
                                    'referredTo': 'Judge (referred)',
                                    'suitNature': 'Nature of Suit',
                                    'cause': 'Cause',
                                    'attorney': 'Prosecutor Name',
                                    'citation': 'Citation',
                                    'url': 'URL',
                                    'reviewed': 'Reviewed?'})
    return out

def process_archive(denied_archive, granted_archive, main_archive, all_columns):
    granted = filter_data(granted_archive, all_columns) 
    print("nDocket entries (granted)", len(granted))
    print("nCases (granted)", granted['Docket ID'].nunique())

    denied = filter_data(denied_archive, all_columns) 
    print("nDocket entries (denied)", len(denied))
    print("nCases (denied)", denied['Docket ID'].nunique())

    main = filter_data(main_archive, all_columns) 
    print("nDocket entries (main)", len(main))
    print("nCases (main)", main['Docket ID'].nunique())

    archive = denied.append(granted)
    archive = archive.append(main)
    print("total nDocket entries", len(archive))

    dups = archive.duplicated(subset = ['Citation'])
    archive['Duplicate citation?'] = np.where(dups, 'Yes', '')
    if not all_columns:
        archive.to_csv(outfile_loc)
        return(archive)
    else: 
        archive['docket_num'] = archive['Docket Number'].str.slice(0, 13) 
        archive.to_csv(outfile_loc)
        return(archive)

archive = process_archive(denied_archive, granted_archive, main_archive, all_columns = False)
# missings = process_archive(denied_archive, granted_archive, main_archive, all_columns = True)


