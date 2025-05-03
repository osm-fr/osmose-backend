# Osmose-QA Backend

This documentation is for understanding how Osmose-QA Backend works. With the main goal to modify or add new validations rules.

This documentation is written in Markdown and in Jupyter Notebook. The Jupyter Notebook are interactive shell for learn and test code.
Nevertheless, and like the Markdown part, it could be accessed as static view [online at Github](https://github.com/osm-fr/osmose-backend/tree/master/doc).
If you want to run the Jupyter Notebook in interactive mode follow the [installation with Docker](../docker/README.md).

0. [Index](0-Index.md): General consideration and concept, good point to start.
1. [Python Plugin](https://github.com/osm-fr/osmose-backend/blob/master/doc/1-Plugin.ipynb): Interactive introduction to how to make simple validation rule using Python.
2. [MapCSS Plugin](2-PluginMapCSS.md): Consideration and concept about making validation rule using the [MapCSS](https://josm.openstreetmap.de/wiki/Help/Styles/MapCSSImplementation) language.
  * [Minimal MapCSS Plugin](https://github.com/osm-fr/osmose-backend/blob/master/doc/2_0-PluginMapCSS-minimal.ipynb): Interactive introduction to how to make simple validation rule using MapCSS language.
3. [SQL Analyzer](3-SQL-basics.md): Consideration and concept about making validation rule using the Osmose-QA Osmosis Framework.
  * [Minimal SQL Analyzer](https://github.com/osm-fr/osmose-backend/blob/master/doc/3_0-SQL-minimal.ipynb): Interactive introduction to how to make a complex validation rule using SQL.
4. [OpenData Merge Analyzer](4-Merge.md): Consideration and concept about making merge analyzer using the Osmose-QA conflation Framework.
