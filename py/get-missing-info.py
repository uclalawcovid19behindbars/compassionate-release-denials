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

## to do: need to figure out a way to filter on date

def create_recap_fetch_endpoint(docket_number, court):
    search_http_endpoint = ('{0}/recap-fetch'
        '?request_type=1'     
        '&pacer_username={1}'
        '&pacer_password={2}'
        '&docket_number={3}' 
        '&court={4}'
        'show_parties_and_counsel=true'.format(root, pacer_username, pacer_pw, docket_number, court))
    return search_http_endpoint

def get_missing_info(docket_number, court):
    fetch_http_endpoint = create_recap_fetch_endpoint(docket_number, court)
    r = requests.get(fetch_http_endpoint, headers=my_headers)
    print(r)
    r.raise_for_status()
    json_data = r.json()
    return json_data

## look into the number of dockets to fetch

missing_dat['dNum,Court'] = missing_dat['docket_num'] + "_" + missing_dat['court_exact']
print("nDocket entries", len(missing_dat))
print("nCases", missing_dat['Docket ID'].nunique())
print("nDockets", missing_dat['docket_num'].nunique())
print("n {docket num, court}:", missing_dat['dNum,Court'].nunique())
print("nCases", missing_dat['Docket ID'].nunique())



all_missed_items = []
for i in missing_dat:
    out_data = get_missing_info(missing_dat['docket_num'][i], missing_dat['court_exact'][i])
    all_missing_items += out_data
    return(all_missing_items)




with open('data/missing_info.json', 'w') as outfile:
    json.dump(all_missing_items, outfile, sort_keys = True)

## EXAMPLE RECAP-FETCH CALL
# this request identifies a case by docket number and court:
curl -X POST \
  --data 'request_type=1' \
  --data 'pacer_username=xxx' \
  --data 'pacer_password=yyy' \
  --data 'docket_number=5:16-cv-00432' \
  --data 'court=okwd' \
  --data 'show_parties_and_counsel=true' \
  --header '' # auth here \ 
  https://www.courtlistener.com/api/rest/v3/recap-fetch/

# this request updates an existing docket in CourtListener by its ID, but only gets the parties and counsel
curl -X POST \
  --data 'request_type=1' \
  --data 'pacer_username=xxx' \
  --data 'pacer_password=yyy' \
  --data 'docket=5' \
  --data 'show_parties_and_counsel=true' \
  --data 'de_date_end=1980-01-01' \
  --header '' # auth here \
  https://www.courtlistener.com/api/rest/v3/recap-fetch/

