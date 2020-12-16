import requests
import json
import math
from datetime import datetime

# GET DATE
current_date = datetime.now().date()
formatted_date = current_date.strftime("%m/%d/%Y")
sheet_title_date = current_date.strftime("%m/%d/%y")

# CONFIG API REQUESTER
with open("./api_key.json") as f:
    secrets_file = json.load(f)

root = "https://www.courtlistener.com/api/rest/v3"
my_headers = {'Authorization': secrets_file['auth_token'] }

main_query = '(coronavirus OR covid-19 OR covid) AND ("compassionate release" OR 3582! OR "first step act" OR "reduce sentence" OR "home confinement")'

def create_description(outcome):
    base_description = '(release OR ("compassionate release" OR 3582! OR "first step act" OR "reduce sentence" OR "home confinement" OR "supervised release")) AND (order OR decision OR opinion OR ruling OR "signed by" OR judgment)'
    denial_desc = ' AND (deny! OR denial or dismiss!)'
    granted_desc = ' AND (grant! OR sustain!)'
    possible_outcomes = {
        "main": '',
        "granted": granted_desc,
        "denied": denial_desc
    }
    description = possible_outcomes.get(outcome, lambda x: x)
    return base_description + description

# date format: '10/26/2020' 
def create_search_endpoint(granted_or_denied, date_filed = None):
    description = create_description(granted_or_denied)
    if date_filed:
        search_http_endpoint = ('{0}/search'
            '?q={1}'
            '&type=r'
            '&order_by=score%20desc'
            '&maxResults=50'
            '&description={2}'
            '&filed_after={3}' # need to change this to reference "entry_date_filed"
            '&docket_number=cr'.format(root, main_query, description, date_filed))
    else:
        search_http_endpoint = ('{0}/search'
            '?q={1}'
            '&type=r'
            '&order_by=score%20desc'
            '&maxResults=50'
            '&description={2}'
            '&docket_number=cr'.format(root, main_query, description))
    return search_http_endpoint

def get_CRs(granted_or_denied, date_filed = None, nextPage = None):
    search_http_endpoint = create_search_endpoint(granted_or_denied, date_filed)
    if nextPage:
        r = requests.get(nextPage, headers=my_headers)
        print(r)
        r.raise_for_status()
    else: 
        r = requests.get(search_http_endpoint, headers=my_headers)
        print(r)
        r.raise_for_status()
    json_data = r.json()
    docket_entries = [doc['absolute_url'] for doc in json_data['results']]
    res = [doc for doc in json_data['results']]
    for doc in res:
        doc['status'] = granted_or_denied
    npages = math.ceil(json_data['count'] / len(docket_entries))
    nextPage = json_data.get('next') 
    return res, npages, nextPage

def get_all_pages(granted_or_denied, date_filed = None):
    all_items = []
    first_items, npages, nextPage = get_CRs(granted_or_denied, date_filed)
    all_items.extend(first_items)
    page_number = 2
    while page_number <= npages:
            items, n, nextPages = get_CRs(granted_or_denied, date_filed, nextPage)
            all_items += items
            page_number += 1
            nextPage = nextPages
    return all_items

granted_docs = get_all_pages('granted')
denied_docs = get_all_pages('denied')
main_docs = get_all_pages('main')

# save raw .json file 
with open('data/granted_archive.json', 'w') as outfile:
    json.dump(granted_docs, outfile, sort_keys = True)

with open('data/denied_archive.json', 'w') as outfile:
    json.dump(denied_docs, outfile, sort_keys = True)

with open('data/main_archive.json', 'w') as outfile:
    json.dump(main_docs, outfile, sort_keys = True)

