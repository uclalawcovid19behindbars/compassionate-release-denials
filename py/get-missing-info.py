import requests
import pandas as pd
import json
import time

with open("./api_key.json") as f:
    secrets_file = json.load(f)

root = "https://www.courtlistener.com/api/rest/v3"
pacer_username = secrets_file['pacer_username']
pacer_pw = secrets_file['pacer_password']
my_headers = {'Authorization': secrets_file['auth_token'] }
missing_dat = pd.read_csv('/Users/hope/UCLA/code/compassionate-releases/compassionate-release-denials/data/missings_crs.csv')

#######
####### STEP 1: 
####### USE RECAP-FETCH TO MAKE A PURCHASE 
#######

def create_recap_fetch_post(docket_ID):
    recap_data = {"request_type": 1,
        "pacer_username": pacer_username,
        "pacer_password": pacer_pw,
        "docket": docket_ID,
        "show_parties_and_counsel": "true"}
    return recap_data

def post_recap_fetch(docket_ID):
    fetch_http_post_data = create_recap_fetch_post(docket_ID)
    r = requests.post('https://www.courtlistener.com/api/rest/v3/recap-fetch/', headers=my_headers, data=fetch_http_post_data)
    r.raise_for_status()
    return(r.text)

## Example cURL POST
curl -X POST --data 'request_type=1' --data 'pacer_username=USERNAME' --data 'pacer_password=PASSWORD' --data 'docket_number=5:18-cr-00765' --data 'court=ohnd' --data 'show_parties_and_counsel=true' --header 'Authorization: Token MYTOKEN' https://www.courtlistener.com/api/rest/v3/recap-fetch/

## look into the number of dockets to fetch
missing_dat['dNum,Court'] = missing_dat['docket_num'] + "_" + missing_dat['court_exact']
print("nDocket entries", len(missing_dat))
print("nCases", missing_dat['Docket ID'].nunique())
print("nDockets", missing_dat['docket_num'].nunique())
print("n {docket num, court}:", missing_dat['dNum,Court'].nunique())
print("nCases", missing_dat['Docket ID'].nunique())

## test on one or two
# post_recap_fetch('5:18-cr-00765', 'ohnd')
# post_recap_fetch('1:16-cr-00106', 'med')

## DANGER ZONE 
# for i in missing_dat.index:
#     post_recap_fetch(missing_dat['docket_num'][i], missing_dat['court_exact'][i])
#     time.sleep(2)

#######
####### STEP 2: 
####### FETCH MISSING INFO FROM DOCKET
#######

def create_docket_endpoint(docket_number, court):
    search_http_endpoint = ('{0}/docket'
        '?request_type=1'     
        '&pacer_username={1}'
        '&pacer_password={2}'
        '&docket_number={3}' 
        '&court={4}'
        '&show_parties_and_counsel=true'.format(root, pacer_username, pacer_pw, docket_number, court))
    return search_http_endpoint

def get_missing_info(docket_number, court):
    docket_http_endpoint = create_docket_endpoint(docket_number, court)
    print(docket_http_endpoint)
    # r = requests.get(fetch_http_endpoint, headers=my_headers)
    # print(r)
    # r.raise_for_status()
    # json_data = r.json()
    # return json_data

with open('data/missing_info.json', 'w') as outfile:
    json.dump(all_missing_items, outfile, sort_keys = True)
