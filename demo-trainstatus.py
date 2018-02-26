#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import datetime
from TrainMonitor import viaggiatreno

def is_valid_timestamp(ts):
    return (ts is not None) and (ts > 0) and (ts < 2147483648000)
    
def format_timestamp(ts, fmt='%H:%M:%S'):
    if is_valid_timestamp(ts):
        return datetime.datetime.fromtimestamp(ts/1000).strftime(fmt)
    else:
        return 'N/A'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ("Usage: trainstatus.py <trainNumber>")
        sys.exit()
        
    trainNumber = int(sys.argv[1])
    api = viaggiatreno.API()

    # "cercaNumeroTrenoTrenoAutocomplete is the viaggiatreno API call that returns the starting station
    # for the train number specified as its argument.
    # Unfortunately that could return more than one station.
    departures = api.call('cercaNumeroTrenoTrenoAutocomplete', trainNumber)
    
    if len(departures) == 0:
        print ("Train {0} does not exists.".format(trainNumber))
        sys.exit()
        
    # TODO: handle not unique train numbers, when len(departures) > 1

    # each result has two elements, the name of the station [0] and its ID [1].
    # we only care about the first result here (TODO)
    # Therefore, departures[0][1] is the station ID element #1 of the first result [0].
    departure_ID = departures[0][1]

    # This fetches the status for that train number from that departure_ID we just fetched.
    # It is required by viaggiatreno.it APIs.
    train_status = api.call('andamentoTreno', departure_ID, trainNumber)

    if train_status['tipoTreno'] == 'ST' or train_status['provvedimento'] == 1:
        print ("Train {0} cancelled".format(trainNumber))
        
    elif train_status['oraUltimoRilevamento'] is None:
        print ("Train {0} has not yet departed".format(trainNumber))
        print ("Scheduled departure {0} from {1}".format(
            format_timestamp (train_status['orarioPartenza']),
            train_status['origine']
        ))
        
    else:
        if train_status['tipoTreno'] in ('PP', 'SI', 'SF'):
            print ("Train partially cancelled: ", train_status['subTitle'])
            
        print ('Last tracking in {0} at {1}'.format(
            train_status['stazioneUltimoRilevamento'],
            format_timestamp(train_status['oraUltimoRilevamento'])
        ))

        for f in train_status['fermate']:
            station   = f['stazione']
            scheduled = format_timestamp(f['programmata'])
            if f['tipoFermata'] == 'P':
                actual = format_timestamp(f['partenzaReale'])
                delay  = f['ritardoPartenza']
                descr  = 'Departure'
            else:
                actual = format_timestamp(f['arrivoReale'])
                delay  = f['ritardoArrivo']
                descr  = 'Arrival'
            
            description  = '{0} {1}: {2} (scheduled {3} - delay: {4})'.format(station, descr, actual, scheduled, delay)
                
            if f['actualFermataType'] == 3:
                print (station, "cancelled")
            elif f['actualFermataType'] == 0:
                print (station, "data not available")
            else:
                print (description)
                
