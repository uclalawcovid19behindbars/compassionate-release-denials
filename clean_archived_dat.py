import pandas as pd
import json
import numpy as np

# with open('/Users/hope/UCLA/code/compassionate-releases/compassionate-release-denials/data/doc_details.json') as f:
#     test = json.load(f)

with open('/Users/hope/UCLA/code/compassionate-releases/compassionate-release-denials/data/granted_archive.json') as f:
    granted_archive = json.load(f)

with open('/Users/hope/UCLA/code/compassionate-releases/compassionate-release-denials/data/denied_archive.json') as f:
    denied_archive = json.load(f)

with open('/Users/hope/UCLA/code/compassionate-releases/compassionate-release-denials/data/main_archive.json') as f:
    main_archive = json.load(f)

def filter_data(json_dat):
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

granted = filter_data(granted_archive) 
len(granted)                  # nDocket Entries
granted['Docket ID'].nunique() # nCases

denied = filter_data(denied_archive) 
len(denied)
denied['Docket ID'].nunique()

main = filter_data(main_archive) 
len(main)
main['Docket ID'].nunique() 

archive = denied.append(granted)
archive = archive.append(main)
dups = archive.duplicated(subset = ['Citation'])
archive['Duplicate citation?'] = np.where(dups, 'Yes', '')

# find dockets with missing attorney / judge information
# Judge (initial) 
# Prosecutor Name
missing_pros = archive[~archive['Prosecutor Name'].isnull()]
missing_judge = archive[~archive['Judge (initial)'].isnull()]
missing = missing_pros.append(missing_judge)
missing_out = missing.drop_duplicates(subset=['Citation'])
len(missing_out)
missing_out['Docket ID'].nunique()

archive.to_csv('/Users/hope/UCLA/code/compassionate-releases/compassionate-release-denials/data/archive_crs.csv')
