# Contributing

When contributing to this repository, please first discuss the change you
wish to make via an issue on github if you want to change the core. Feel
free to make direct pull request for a new analyzer.

## Code Style

There is no written rules about this project or any specific code style.
But please try to make the code similar to code already existing.


## Fetching josm translations

JOSM translations are used by some MapCSS plugins, and can be retrieved by bzr:
```
apt install bzr
cd po/josm
bzr checkout --lightweight lp:~openstreetmap/josm/josm_trans
```

## Connection to the "official" frontend at http://osmose.openstreetmap.fr

When you have configured the backend for the country you want to add, please
send an email to osmose-contact@openstreetmap.fr. We will then send you the
password to use to connect to the frontend.
