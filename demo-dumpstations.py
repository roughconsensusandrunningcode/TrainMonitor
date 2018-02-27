#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import datetime
import os
import json
import string
import csv
from operator import itemgetter
from TrainMonitor import viaggiatreno

region_codes = {
    1:  "Lombardia",
    2:  "Liguria",
    3:  "Piemonte",
    4:  "Valle d'Aosta",
    5:  "Lazio",
    6:  "Umbria",
    7:  "Molise",
    8:  "Emilia Romagna",
    10: "Friuli-Venezia Giulia",
    11: "Marche",
    12: "Veneto",
    13: "Toscana",
    14: "Sicilia",
    15: "Basilicata",
    16: "Puglia",
    17: "Calabria",
    18: "Campania",
    19: "Abruzzo",
    20: "Sardegna",
    22: "Trentino Alto Adige"
}

destdir = os.path.join('data', 'stations-dump')
if not os.path.exists(destdir):
    os.makedirs(destdir)

as_csv = []
as_geojson = {
    'type': 'FeatureCollection',
    'features': []
}

api = viaggiatreno.API()
sortkey = itemgetter(0)

num_stations = 0
for letter in string.ascii_uppercase:
    #Get all stations which name starts with 'letter'
    stations = api.call('autocompletaStazione', letter)
    num_stations += len(stations)
    print(letter, len(stations), num_stations)
    for s in sorted(stations, key=sortkey):
        station_name, station_id = s
        station = {
            'name':        station_name,
            'id':          station_id,
            'region':      'N/A',
            'region_code': 'N/A',
            'lat':         'N/A',
            'lon':         'N/A',
            'city':        'N/A'
        }
        
        #Get region code, needed to obtain station details
        reg_code = api.call('regione', station_id)
        if reg_code is not None:
            station['region_code'] = int(reg_code)
            station['region'] = region_codes.get(int(reg_code), 'N/A')
            #Get station details
            details = api.call('dettaglioStazione', station_id, reg_code)
            if details is not None:
                station['city'] = details['nomeCitta']
                station['lat']  = details['lat']
                station['lon']  = details['lon']
                
                as_geojson['features'].append ({
                    'type': 'Feature',
                    'properties': {
                        'name': station['name'],
                        'id': station['id'],
                        'region_code': station['region_code'],
                        'region': station['region'],
                        'city': station['city']
                    },
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [details['lon'], details['lat']]
                    }
                })
                
        as_csv.append(station)
        
with open(os.path.join(destdir, 'stations.geojson'), 'w') as fp:
    json.dump(as_geojson, fp)
    
with open(os.path.join(destdir, 'stations.csv'), 'w') as fp:
    csv_fields = itemgetter('name', 'id', 'region', 'region_code', 'city', 'lat', 'lon')
    wr = csv.writer(fp, delimiter=',', lineterminator='\n')
    wr.writerow(('name', 'id', 'region', 'region_code', 'city', 'lat', 'lon'))
    for row in as_csv:
        wr.writerow(csv_fields(row))
        
