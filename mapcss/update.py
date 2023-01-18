#!/usr/bin/env python3
#-*- coding: utf-8 -*-

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
            r.encoding = 'utf-8' # Force bad encoding
            f = '/tmp/mapcss/' + k + '.mapcss'
            open(f, 'w').write(r.text)
            try:
                mapcss2osmose.mapcss2osmose(mapcss = f, output_path = 'plugins')
            except Exception as e:
                print(traceback.format_exc())
                print(e)

    # Regenerate all local files too
    files = list(Path('plugins').rglob('*.mapcss'))
    for file in files:
        importlib.reload(mapcss2osmose)
        print(file)
        mapcss2osmose.mapcss2osmose(mapcss = file, output_path = str(file.parent))

if __name__ == '__main__':
    main(sys.argv[1:])
