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
    api_file = json.load(f)

root = "https://www.courtlistener.com/api/rest/v3/"
key = api_file['key']
headers = {'Authorization': api_file['auth_token'] }

search_terms = '(coronavirus OR covid-19) AND (incarcerat* OR correctional OR prison OR jail OR detention)'

def create_description(outcome):
    desc_beginning = '(order OR opinion OR decision) NOT (scheduling OR "standing order" OR "administrative order" OR "general order")'
    possible_outcomes = {
        "granted": ' AND grant*',
        "denied": ' AND (deny* OR deni*)'
    }
    description = possible_outcomes.get(outcome, lambda x: x)
    return desc_beginning + description

# date format: '10/26/2020' 
def create_endpoint(granted_or_denied, date_filed = None):
    description = create_description(granted_or_denied)
    if date_filed:
        search_http_endpoint = ('{0}/search'
            '?q={1}'
            '&type=r'
            '&order_by=score%20desc'
            '&maxResults=50'
            '&description={2}'
            '&filed_after={3}'
            '&docket_number=cr'
            '&key={4}'.format(root, search_terms, description, date_filed, key))
    else:
        search_http_endpoint = ('{0}/search'
                '?q={1}'
                '&type=r'
                '&order_by=score%20desc'
                '&description={2}'
                '&docket_number=cr'
                '''&fields=page,docket_number,court,assigned_to,referred_to,nature_of_suit,resource_uri,
                            case_name,cause,pageToken'''
                # '&nature_of_suit='
                '&key={3}'.format(root, search_terms, description, key))
    return search_http_endpoint

def get_CRs(granted_or_denied, date_filed = None, nextPage = None):
    search_http_endpoint = create_endpoint(granted_or_denied, date_filed)
    if nextPage:
        r = requests.get(nextPage)
        r.raise_for_status()
    else: 
        r = requests.get(search_http_endpoint, headers=headers)
        r.raise_for_status()
    json_data = r.json()
    docket_entries = [doc['absolute_url'] for doc in json_data['results']]
    res = [doc for doc in json_data['results']]
    for doc in res:
        doc['status'] = granted_or_denied
    npages = math.ceil(json_data['count'] / len(docket_entries))
    nextPage = json_data.get('next') 
    return res, npages, nextPage

def get_all_pages(granted_or_denied, date_filed):
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

granted_docs = get_all_pages('granted', '02/01/20')
denied_docs = get_all_pages('denied', '02/01/20')

# save raw .json file 
with open('data/granted_archive.json', 'w') as outfile:
    json.dump(granted_docs, outfile, sort_keys = True)

with open('data/denied_archive.json', 'w') as outfile:
    json.dump(denied_docs, outfile, sort_keys = True)
