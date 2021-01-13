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

#######
####### STEP 1: 
####### USE RECAP-FETCH TO MAKE A PURCHASE 
#######

def create_recap_fetch_post(docket_number, court):
    recap_data = {"request_type": 1,
        "pacer_username": {0},
        "pacer_password": {1},
        "docket_number": {2},
        "court": {3},
        "show_parties_and_counsel": "true"}.format(pacer_username, pacer_pw, docket_number, court)
    return recap_data

    # recap_request = ('{0}/recap-fetch'
    #     '?request_type=1'     
    #     '&pacer_username={1}'
    #     '&pacer_password={2}'
    #     '&docket_number={3}' 
    #     '&court={4}'
    #     '&show_parties_and_counsel=true'.format(root, pacer_username, pacer_pw, docket_number, court))
    # return recap_request

def post_recap_fetch(docket_number, court):
    fetch_http_post = create_recap_fetch_post(docket_number, court)
    r = requests.post(fetch_http_post, headers=my_headers)
    r.raise_for_status()
    print(r.text)

## Share-able CURL POSTS

curl -X POST --data 'request_type=1' --data 'pacer_username=USERNAME' --data 'pacer_password=PASSWORD' --data 'docket_number=5:18-cr-00765' --data 'court=ohnd' --data 'show_parties_and_counsel=true' --header 'Authorization: Token MYTOKEN' https://www.courtlistener.com/api/rest/v3/recap-fetch/

# post_recap_fetch('1:16-cr-00106', 'med')
https://www.courtlistener.com/api/rest/v3/search/?type=d&q=5%3A18-cr-00765+ohnd&order_by=score+desc

## look into the number of dockets to fetch
missing_dat['docket_num'] = missing_dat['Docket Number'].str.slice(0, 13) 
missing_dat['dNum,Court'] = missing_dat['docket_num'] + "_" + missing_dat['court_exact']
print("nDocket entries", len(missing_dat))
print("nCases", missing_dat['Docket ID'].nunique())
print("nDockets", missing_dat['docket_num'].nunique())
print("n {docket num, court}:", missing_dat['dNum,Court'].nunique())
print("nCases", missing_dat['Docket ID'].nunique())

## test on one or two
post_recap_fetch('5:18-cr-00765', 'ohnd')
# post_recap_fetch('1:16-cr-00106', 'med')

all_missed_items = []
for index, row in missing_dat.iterrows():
    print(row['docket_num'], row['court_exact'])
    # out_data = post_recap_fetch(row['docket_num'], row['court_exact'])
    # all_missing_items += out_data
    # return(all_missing_items)

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


