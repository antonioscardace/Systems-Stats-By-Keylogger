from deep_translator import GoogleTranslator

from elasticsearch import Elasticsearch

import requests
import json


ES_URL = 'http://elasticsearch:9200'
ES_INDEX = 'keylogger_stats'
ES_MAPPING = {
    "mappings": {
        "properties": {
            "location": {
                "type": "geo_point"
            }
        }
    }
}

es = Elasticsearch(
    ES_URL,
    verify_certs=False
)  

es.indices.create(
    index=ES_INDEX,
    body=ES_MAPPING, # we overwrite the mapping because otherwise, ES sees the "location" field as text
    ignore=400 # ignore error of "index already exists"
)


def load_window_titles(path):
    with open(path, 'r') as fd:
        titles = fd.read().split('\n')
        return set(titles)


def get_delta_timestamps(t_begin, t_end):
    tdelta = t_end - t_begin
    delta_secs = tdelta.total_seconds()
    return {'delta_secs': delta_secs}

def get_geo_ip_coords(ip_address):
    api = requests.get('https://geolocation-db.com/jsonp/' + ip_address)
    geoip = json.loads(api.content.decode().split('(')[1][:-1])
    coords = str(geoip['latitude']) + ', ' + str(geoip['longitude'])
    return { 'location': coords }
    
def get_window_classification(window):
    classes = {
        'Social': load_window_titles('titles/social.txt'),
        'Utility': load_window_titles('titles/utilities.txt'),
        'Entertainment': load_window_titles('titles/entertainment.txt'),
        'Web Browsing': load_window_titles('titles/web.txt'),
        'Office & Study': load_window_titles('titles/office_study.txt')
    }

    for label in classes.keys():
        for title in classes[label]:
            if title in window:
                return {'window': title.title(), 'window_category': label}

    return {'window_category': 'Other'}


def process_batch(df, id):
    for idx, row in enumerate(df.collect()):
        
        doc = row.asDict()
        doc['window'] = GoogleTranslator(source='auto', target='en').translate(doc['window']).lower()
    
        doc.update(get_delta_timestamps(doc['timestamp_begin'], doc['timestamp_end']))
        doc.update(get_window_classification(doc['window']))

        if doc['ip_address'] != "Unknown":
            doc.update(get_geo_ip_coords(doc['ip_address']))

        print(doc)

        id_str = '{}-{}-1'
        id = id_str.format(id, idx)

        response = es.index(index=ES_INDEX, id=id, document=doc)
        print(response)