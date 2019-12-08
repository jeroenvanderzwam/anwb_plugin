import requests
import pandas as pd

def anwb_opstoppingtype_csv(data, type_):
    #kolommen = list(wegen[1]['events']['trafficJams'][0].keys())
    # kan niet dynamisch omdat je niet weet welke wegen files hebben
    kolommen = ['msgNr', 'from', 'fromLoc', 'to', 'toLoc', 'location', 'segStart', 'segEnd',
                'start', 'startDate', 'stop', 'stopDate', 'delay', 'distance', 'reason',
                'description', 'events']

    data_df = []
    wegen = data['roadEntries']
    for weg in wegen:
        opstoppingen = weg['events'][type_]
        for opstopping in opstoppingen:
            #werkzaamheden, opstopping, radars
            regel = {}
            # moet door vaste kolommen heen om dat de data niet in alle files zit (ik weet niet waarom)
            for kolom in kolommen:
                waarde = opstopping.get(kolom, 'Nan')
                if waarde == 'Nan':
                    regel[kolom] = 'Nan'
                    continue
                if kolom == 'fromLoc':
                    lat, lon = opstopping[kolom].values()
                    regel['from_lat'] = lat
                    regel['from_lon'] = lon
                    continue
                if kolom == 'toLoc':
                    lat, lon = opstopping[kolom].values()
                    regel['to_lat'] = lat
                    regel['to_lon'] = lon
                    continue
                if kolom == 'events':
                    continue

                regel[kolom] = opstopping[kolom]
            data_df.append(regel)

    df = pd.DataFrame(data_df)
    df.to_csv(f'anwb_{type_}.csv')

url = requests.get('https://www.anwb.nl/feeds/gethf').json()
anwb_opstoppingtype_csv(url, 'trafficJams')
anwb_opstoppingtype_csv(url, 'roadWorks')
anwb_opstoppingtype_csv(url, 'radars')
