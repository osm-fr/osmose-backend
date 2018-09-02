import requests
import json
import csv
import time

traffic_signs = []
reader = json.loads(open('mapillary-traffic-signs.mapping.json', 'r').read())
try:
  for row in reader:
      traffic_signs += row['sign']
except:
  print(row)
  raise

with open('mapillary-feature-fetch.csv', 'w') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(['accuracy', 'direction', 'image_key', 'first_seen_at', 'last_seen_at', 'value', 'X', 'Y'])

slice = lambda A, n: [A[i:i+n] for i in range(0, len(A), n)]

# Germany
#bbox = [5.8663153, 47.2701114, 15.0419319, 55.099161]
# France
bbox = [-4.9658203125, 42.27730877423709, 8.28369140625, 51.11041991029264]
# IDF
#bbox = [1.4501953125, 48.1367666796927, 3.592529296875, 49.28214015975995]

sleep = 1
b = 0
for traffic_signs_ in slice(traffic_signs, 10):
  b = b +1
  print('Batch {0}/{1}: {2}'.format(b, round(len(traffic_signs) / 10 + 0.5), ','.join(traffic_signs_)))
  url = 'https://a.mapillary.com/v3/map_features?bbox={bbox}&client_id={client_id}&layers=trafficsigns&per_page=1000&start_time={start_time}&values={values}'.format(bbox=','.join(map(str, bbox)), client_id='MEpmMTFQclBTUWlacjV6RTUxWWMtZzo5OTc2NjY2MmRiMDUwYmMw', start_time='2016-06-01', values=','.join(traffic_signs_))
  with open('mapillary-feature-fetch.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)

    try:
      page = 0
      while(url):
        page = page + 1
        print("Page {0}".format(page))
        while True:
          r = requests.get(url=url)
          if r.status_code != 502 and r.status_code != 504:
            sleep = int(sleep / 2 + 0.5)
            break
          else:
            print("Too fast: sleep {0}".format(sleep))
            time.sleep(sleep)
            sleep = sleep * 2
        url = r.links['next']['url'] if 'next' in r.links else None

        features = json.loads(r.text)['features']
        filtered = 0
        print('features: {}'.format(len(features)))
        for j in features:
          p = j['properties']
          image_key = p['detections'][0]['image_key']
          gc = j['geometry']['coordinates']
          row = [p['accuracy'], p['direction'] if 'direction' in p else None, image_key, p['first_seen_at'], p['last_seen_at'], p['value']] + gc
          if row[0] > 0.01:
            writer.writerow(row)
            filtered = filtered + 1
        print('filtered: {}'.format(filtered))
    except:
      print(url)
      print(r.status_code)
      print(r.text[0:200])
      raise
