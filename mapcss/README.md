Mapcss to Osmose analyser

Generate the parser
===================

```
java -jar antlr-4.8-complete.jar -o generated/ -Dlanguage=Python3 MapCSS.g4
```

Convert one MapCSS
==================

```
python mapcss2osmose.py addresses.mapcss
```

Update all external MapCSS
==========================

From root directory
```
python -m mapcss.update
```
