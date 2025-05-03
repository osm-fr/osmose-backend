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
python -m mapcss.mapcss2osmose plugins/Bicycle.validator.mapcss
```

Update all external MapCSS
==========================

From root directory
```
python -m mapcss.update
```
(Windows users should set the system variable `PYTHONUTF8` to `1` first)
