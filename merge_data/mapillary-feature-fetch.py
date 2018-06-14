import requests
import json
import csv

traffic_signs = []
with open('mapillary-traffic-signs.mapping.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  try:
    for row in reader:
      if len(row) > 0 and row[0][0] != '#':
        traffic_signs += row[5].split('|')
  except:
    print(row)
    raise

with open('mapillary-feature-fetch.csv', 'w') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(['accuracy', 'direction', 'image_key', 'first_seen_at', 'last_seen_at', 'value', 'X', 'Y'])

slice = lambda A, n: [A[i:i+n] for i in range(0, len(A), n)]

# IDF
bbox = [1.4501953125, 48.1367666796927, 3.592529296875, 49.28214015975995]
# Bordeaux
#bbox = [0.63720703125,49.33228198473771,0.758056640625,0.758056640625]
# Villenave
#bbox = [-0.5863094329833984, 44.746977076311985, -0.5397891998291016, 44.77495043385323]

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
        r = requests.get(url=url)
        url = r.links['next']['url'] if 'next' in r.links else None

        for j in json.loads(r.text)['features']:
          p = j['properties']
          image_key = p['detections'][0]['image_key']
          gc = j['geometry']['coordinates']
          row = [p['accuracy'], p['direction'] if 'direction' in p else None, image_key, p['first_seen_at'], p['last_seen_at'], p['value']] + gc
          if row[0] > 0.8:
            writer.writerow(row)
    except:
      print(url)
      print(r.text[0:200])
      raise
