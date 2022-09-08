# Contributing

When contributing to this repository, please first discuss the change you
wish to make via an issue on github if you want to change the core. Feel
free to make direct pull request for adding a new analyzer.

## Coding Style

There are no written rules about this project or any specific coding style.
However, please try to make the code similar to the already existing code.

## Tests

We try to have tests on analyzers, but there are not present on all. When
adding new code try to add or improve the corresponding code tests.

It is recommended to run tests using [Docker](docker/README.md).

Code tests can be run on one source code file using pytest, from root
directory:
```
pytest plugins/TagFix_Housenumber.py
```

Full test can be run with the help of the script `tools/pytest.sh`:
```
./tools/pytest.sh sax # Run all plugins tests
./tools/pytest.sh merge # Run all test on merge from analysers directory
./tools/pytest.sh other # Run all other analysers and non analyser tests
```

Beside code test, we have static code analysis and linting:
```
./tools/pytest.sh lint
./tools/pytest.sh mypy
```
Only a subset of standard Python linting is active.

For code pull request, `sax`, `lint` and `mypy` are required to pass.

## Fetching josm translations

JOSM translations are used by some MapCSS plugins, and can be retrieved by bzr:
```
apt install bzr
cd po/josm
bzr checkout --lightweight lp:~openstreetmap/josm/josm_trans
```

## Connection to the "official" frontend at https://osmose.openstreetmap.fr

When you have configured the backend for the country you want to add, please
send an email to osmose-contact@openstreetmap.fr. We will then send you the
password that you should use to connect to the frontend.
