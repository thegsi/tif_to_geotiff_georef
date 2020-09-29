import csv
import requests
import pickle
import config

with open('OSDs_with_paths.csv', newline='') as f:
    reader = csv.reader(f)
    maps = list(reader)[1:]

headers = {'Authorization': 'Token ' + config.georef_key}

mapids = []
for map in maps:
    r = requests.get('http://api.oldmapsonline.org/1.0/maps/external/' + map[0], headers=headers)
    map.append(r.json()['id'])
    mapids.append(map)

georefs = []
for mapid in mapids:
    r = requests.get('http://api.oldmapsonline.org/1.0/maps/' + mapid[4] + '/georeferences', headers=headers)
    georef = r.json()['items'][0]
    georef['external_id'] = mapid[0]
    georefs.append(georef)

with open(f'./osd_georefs.pickle','wb') as out_pickle:
  pickle.dump(georefs,out_pickle)
