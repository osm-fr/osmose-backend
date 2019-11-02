# Backend part of Osmose QA tool

This is the part of osmose [http://osmose.openstreetmap.fr] which analyses OSM
and send results to frontend. This works as following:

  - an .osm.pbf extract is downloaded
  - analyses are run directly on .osm.pbf file, or on the database
  - analyses resultat are uploaded to the frontend
  - by default, temporary extract files and database are purged

## Installation

The default way to setup Osmose Backend is through Docker. Look at the
[docker/README.md](docker/README.md).

You can also follow the old manual installation [INSTALL.md](INSTALL.md).

## Run

Look at the osmose_run.py help for options
```
osmose_run.py -h
```

## Contributing

Setup a Docker install and follow the
"[Develop on Osmose with docker](docker/README.md#develop-on-osmose-with-docker)"
guide.

Read the additional contribution [guildelines](CONTRIBUTING.md).
