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
        import os
        print ("Usage: " + os.path.basename(__file__) + " <trainNumber>")
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
    midnight_of_today = departures[0][2]
    # This fetches the status for that train number from that departure_ID we just fetched.
    # It is required by viaggiatreno.it APIs.
    # train_status also includes the whole list of stops for that train (used a few lines later on).
    train_status = api.call('andamentoTreno', departure_ID, trainNumber, midnight_of_today)
    
    # in these cases, the train has been cancelled.
    if train_status['tipoTreno'] == 'ST' or train_status['provvedimento'] == 1:
        print ("Train {0} cancelled".format(trainNumber))

    # otherwise, it is checked whether the train is running or if it's not yet.
    elif train_status['oraUltimoRilevamento'] is None:
        print ("Train {0} has not yet departed".format(trainNumber))
        print ("Scheduled departure {0} from {1}".format(
            format_timestamp (train_status['orarioPartenza']),
            train_status['origine']
        ))

    # finally, if the train is up and running
    else:
        if train_status['tipoTreno'] in ('PP', 'SI', 'SF'):
            print ("Train partially cancelled: ", train_status['subTitle'])
            
        print ('Last tracking in {0} at {1}'.format(
            train_status['stazioneUltimoRilevamento'],
            format_timestamp(train_status['oraUltimoRilevamento'])
        ))

        # each stop is processed and outputted on the console with the relevant informations.
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

            # the output line is formatted according to the available data:
            if f['actualFermataType'] == 3:
                station_output  = '{:40} cancelled'.format(station)
            elif f['actualFermataType'] == 0:
                station_output  = '{:40} data not available'.format(station)
            else:
                station_output  = '{:40} {}: {} (scheduled {} - delay: {})'.format(station, descr, actual, scheduled, delay)

            # there we go
            print (station_output)
                
