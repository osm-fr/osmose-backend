# Contributing

When contributing to this repository, please first discuss the change you
wish to make via an issue on github if you want to change the core. Feel
free to make direct pull request for adding a new analyzer.

## Coding Style

There are no written rules about this project or any specific coding style.
However, please try to make the code similar to the already existing code.

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
password that you should use to connect to the frontend.
