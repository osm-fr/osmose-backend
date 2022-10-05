Mapcss to Osmose analyser

Generate the parser
===================

```
java -jar antlr-4.10.1-complete.jar -o generated/ -Dlanguage=Python3 MapCSS.g4
```
ANTLR can be downloaded [here](https://github.com/antlr/antlr4/releases)

Convert one MapCSS
==================

```
python mapcss2osmose.py addresses.mapcss
```

Update all external MapCSS
==========================

From root directory
```
python -X utf8 -m mapcss.update
```
