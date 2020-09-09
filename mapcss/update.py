#!/usr/bin/env python3

import requests
import sys
import traceback
import importlib
from pathlib import Path
from . import mapcss2osmose
from .item_map import item_map


def main(mapcsss):
    Path('/tmp/mapcss').mkdir(parents=True, exist_ok=True)
    for k, v in item_map.items():
        if not mapcsss or k in mapcsss:
            importlib.reload(mapcss2osmose)
            print(v['url'])
            r = requests.get(v['url'], allow_redirects=True)
            f = '/tmp/mapcss/' + k + '.mapcss'
            open(f, 'w').write(r.text)
            try:
                mapcss2osmose.mapcss2osmose(mapcss = f, output_path = 'plugins')
            except Exception as e:
                print(traceback.format_exc())
                print(e)


if __name__ == '__main__':
    main(sys.argv[1:])
