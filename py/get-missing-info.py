import requests
import pandas as pd
import json

with open("./api_key.json") as f:
    secrets_file = json.load(f)

root = "https://www.courtlistener.com/api/rest/v3"
pacer_username = secrets_file['pacer_username']
pacer_pw = secrets_file['pacer_password']
my_headers = {'Authorization': secrets_file['auth_token'] }
missing_dat = pd.read_csv('/Users/hope/UCLA/code/compassionate-releases/compassionate-release-denials/data/missings_crs.csv')

def create_recap_fetch_endpoint(docket_number, court):
    search_http_endpoint = ('{0}/recap-fetch'
        '?request_type=1'     
        '&pacer_username={1}'
        '&pacer_password={2}'
        '&docket_number={3}' 
        '&court={4}'
        '&show_parties_and_counsel=true'.format(root, pacer_username, pacer_pw, docket_number, court))
    return search_http_endpoint

def get_missing_info(docket_number, court):
    fetch_http_endpoint = create_recap_fetch_endpoint(docket_number, court)
    # print(fetch_http_endpoint)
    r = requests.get(fetch_http_endpoint, headers=my_headers)
    print(r)
    r.raise_for_status()
    json_data = r.json()
    return json_data

## look into the number of dockets to fetch
missing_dat['docket_num'] = missing_dat['Docket Number'].str.slice(0, 13) 
missing_dat['dNum,Court'] = missing_dat['docket_num'] + "_" + missing_dat['court_exact']
print("nDocket entries", len(missing_dat))
print("nCases", missing_dat['Docket ID'].nunique())
print("nDockets", missing_dat['docket_num'].nunique())
print("n {docket num, court}:", missing_dat['dNum,Court'].nunique())
print("nCases", missing_dat['Docket ID'].nunique())

## test on one or two
get_missing_info('5:18-cr-00765', 'ohnd')
# get_missing_info('1:16-cr-00106', 'med')


all_missed_items = []
for index, row in missing_dat.iterrows():
    print(row['docket_num'], row['court_exact'])
    # out_data = get_missing_info(row['docket_num'], row['court_exact'])
    # all_missing_items += out_data
    # return(all_missing_items)


with open('data/missing_info.json', 'w') as outfile:
    json.dump(all_missing_items, outfile, sort_keys = True)


