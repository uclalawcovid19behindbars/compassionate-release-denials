import pandas as pd
import json
import numpy as np

# with open('/Users/hope/UCLA/code/compassionate-releases/compassionate-release-denials/data/doc_details.json') as f:
#     test = json.load(f)

with open('/Users/hope/UCLA/code/compassionate-releases/compassionate-release-denials/data/denied_archive.json') as f:
    denied_archive = json.load(f)

with open('/Users/hope/UCLA/code/compassionate-releases/compassionate-release-denials/data/granted_archive.json') as f:
    granted_archive = json.load(f)

def filter_data(json_dat):
    rows = []
    for item in json_dat:
        rows.append(item)
    df = pd.DataFrame(rows)
    df['dateFiled_clean'] = df['dateFiled'].str[5:7] + '/' + df['dateFiled'].str[8:10] + '/' + df['dateFiled'].str[2:4]
    df['citation'] = df['caseName'] + ', No. ' + df['docketNumber'].astype(str) + ', Dkt. No. ' + df['entry_number'].astype(str) + ' ([' + df['dateFiled_clean'] + '])'
    df['url'] = 'https://www.courtlistener.com/' + df['absolute_url']
    df['reviewed']  = 'No'
    columns = ['caseName', 'docketNumber', 'court', 'dateFiled_clean', 'entry_number', 'description', 'status',
                'assignedTo', 'referredTo', 'suitNature', 'cause', 'attorney', 'citation', 'url', 'reviewed']
    out = df[columns]
    out = out.rename(columns = {'caseName': 'Case Name',
                               'docketNumber': 'Docket Number',
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

# expected 485 total
granted = filter_data(granted_archive) # expect 106
denied = filter_data(denied_archive) # expect 114

archive = denied.append(granted)
dups = archive.duplicated(subset = ['Citation'])
archive['Duplicate citation?'] = np.where(dups, 'Yes', '')

archive.to_csv('/Users/hope/UCLA/code/compassionate-releases/compassionate-release-denials/data/archive_crs.csv')
