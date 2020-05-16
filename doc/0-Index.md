# Osmose-QA Analyzers Backend Developer Guide


## General architecture

Osmose-QA is composed of two parts:
* Backends, data processor that report list of issues to the Frontend.
* Frontend, web site to display issues to contributors and offer API to other applications.

Backends can be this project or any other application able to produce issues lists in the Osmose-QA XML format and able to upload it to the Frontend.

This Backend project is composed by an engine and lot of the rules of validation written in analyzers. An analyzer can implemented multiple checks, and so report many class of issues.

There are several type of analyzers, they implement a particular way to access the data.


## Analyzers organization

The abstract root classes:
* `Aanalyser` (Analyser.py): the main root class
  * `Analyser_Osmosis` (Analyser_Osmosis.py): the root class for all SQL analyzers using the PostgreSQL/PostGIS database imported by the Osmosis tool.
    * `Analyser_Merge` (Analyser_Merge.py): the root class for merging OpenData source with OSM data.
      * `SubAnalyser_Merge_Dynamic` (Analyser_Merge_Dynamic.py): the same, but form multiple type of OSM Objects.

This abstract classes are implemented by few kind of classes:
* `Analyser_Osmosis_*`: directly implementing `Analyser_Osmosis` to run SQL queries on the database.
* `Analyser_Merge_*`: implementing `Analyser_Merge` to report results of conflation with an OpenData source.
* `Analyser_Sax`: directly implementing `Analyser` and run a set of simple analyzers so called "Plugins", it parse the OSM PBF extract and call rules on each OSM objects.


## Analyzer types

### Plugins
Plugins from `plugins` directory are dedicated to check one OSM object at the time. Mainly to validate tags. No validation on geometry or relation of objects between them.

They can be written in [MapCSS](https://josm.openstreetmap.de/wiki/Help/Styles/MapCSSImplementation) or in Python.

The MapCSS code is compiled into Python using `mapcss2osmose.py` from the `mapcss` directory.

### Osmose Analyzers
This kind of analyzer concern more complex checks. It can deal with geometries using [PostGIS](https://postgis.net/docs/reference.html) functions. It can also validate tags, topological or semantics relation between objects.

The main part of the rules are written in SQL.

### Merge Analyzers
These analyzers use the OSM Osmosis database to compare it to an external OpenData data source also importer in the database.

There are able to report:
* Missing Objects in the OSM Data.
* Suspect Objects in OSM data not found on OpenData.
* Improvement and Update could be done on OSM data brought by OpenData.


## Concepts of Osmose-QA Issue

The Osmose-QA Issues are probable errors that a contributor should review. In some case it points to possible improvement, but it is not the main target of Osmose-QA.

The issues are defined and produced by analyzers (and plugins).

### Classes of issues
A class of issue is a definition of the issues the analyzer will yield. The classes of issues are defined by the following fields.

* `id`: each class of issue should have an unique `id` in the scope of the analyzer. Note: all plugins are in the same scope of the `Analyser_Sax`.

Documentation:
* `title`: short string which describes the issue (answers "what is the issue?"). Ideally titles should not contain any OSM tagging. Only the first word of the title should be capitalized (and any proper nouns or acronyms) and there should be no end period.
* `detail` (markdown):  longer string which explains the issue (answers "why is this an issue?"). Is constructed with valid sentences and ends with a period.
* `fix` (optional, markdown): general guide on how to fix the issue. Constructed with valid sentences and ends with a period.
* `trap` (optional, markdown): common mistakes and complications you may make while fixing the issue. Constructed with valid sentences and ends with a period.
* `example` (optional, markdown): an example of the issue. Constructed with valid sentences and ends with a period. Images are commonly found here (`![](imgURL)` in markdown).
* `source`: URL to the source code of this analyzer. The abstract root class automatically fill this fields.
* `resource` (optional): URL to any data used to produce this issue. The abstract root class `Analyser_Merge` automatically fill this fields.

Classification:
* `item`: where to put the result of this class of issues in the Frontend menu of categories.
* `level`: the impact of the Osmose-QA issues on the OSM data, `1`: hight, `2`: normal, `3`: low.
* `tags`: Osmose-QA tags (not OSM tags), allow thematic classification on the Frontend, see already existing tags at [/api/0.3/tags](http://osmose.openstreetmap.fr/api/0.3/tags).

### Instances of issues
Each issue yield by the analyzer should refer to a class definition by using the same class `id`:
* `class`: the class `id` from the definition.
* `subclass` (optional): an extra identifier to make the issue instance unique. Used in case of a same OSM object trigger multiple time the same issue (eg misspelling). It can also be used to distinguee multiple behaviors of the a validation rule to easy debug.
* `text` (optional): field also know as "subtitle". It explains the issue for this specific object, eg by quoting the tag value raising this issue.
* `res` (optional): ????????????????????????????????????????????????????????
* `fixType` (optional): ??????????????????????????????????????????????
* `fix` (optional): a structured field of suggested changes to fix the OSM objects. See details below.
* `geom`: the point location of the issue. Preferably on the object boundary, the objects intersection or the exact location of the geometrical issue.

### Fix Suggestion

The fixes are possible corrections of the OSM objects involved in the issues. Multiple OSM Objects can be involved in a issue. But also multiple different Fixes can be possible for an issue.

The full structure of fixes is:
* Array of alternative ways to fix:
  * Array of fixes for objects part of issue:
    * Dictionary for change actions:
      * Dictionary of array for OSM tags.

This tree can be shortened.

The Change Actions are `+` for add tags, `-` to delete tags and `~` to alter values of tags.

Examples of  shortened fixes:
* `{'+': {'foo': 'bar'}}`: to add a tag `foo=bar` as unique suggestion to the unique object involved in the issue.
* `{'~': {'foo': 'bar2'}}`: to alter the existing value of the tag `foo`.
* `{'-': ['foo']}}`: to delete the tag `foo`.

The actions can be combined: `{'-': ['oof'], '+': {'foo': 'bar'}}`, delete for `foo` and add `foo=bar` on the same object.

To fix multiples objects: `[{'-': ['foo']}, {'+': {'foo': 'bar'}]]` remove the `foo` tag from the first object and add `foo=bar` to the second.

To make different suggestions on one object: `[[{'+': {'foo': 'bar'}], [{'+': {'foofoo': 'barbar'}]]`, alternatively suggested to add `foo=bar` or `foofoo=barbar`.


## Execution

The main steps of running Osmose-QA are:
* Download OSM extract
* Importing the data into the database
* Complementary data process into the database (eg. add index)
* For each analyzer:
  * Call the Frontend API to see it the analyzer need to be update
  * Lunching the analyzers
  * Uploading the result to the Frontend
* Destroy the database

All the process is ruled by the command `osmose_run.py`. Some complementary utilities can found in the `tools` directory.

For help run:
```
osmose_run.py --help
```

### Database management
Osmose-QA use a database schema per country. By default it loads the OSM extract into the database and erase it at the end. Use `--no-clean` to keep the database at the end of the process and `--skip-init` to not reimport once you already have it.

### Run modes

TODO diff, change mode, resume mode.

## Development Environment

### Environment
There are multiple way to run Osmose-QA Backend and test your code. The easier to setup is by using with Docker. Docker avoid you to deals with install process and dependencies.

[Jupyter](https://en.wikipedia.org/wiki/Project_Jupyter) can be used from Docker to have web shell on Osmose-QA and make this doc interactive (the *.ipynb part). A static view of the Jupyter notebook can also be view online at [Github repository](https://github.com/osm-fr/osmose-backend/tree/master/doc).

Lastly, if you don’t support Docker and love the old school way, you can directly use Python Virtualenv. You will also have to install ans setup PostgreSQL yourself.

### Translation
Translation are make in Osmose-QA but without language destination. The translation are make in all languages at the same time. For that we use `T_()` and `T_f()`, the last if the `string.format()` variant. These functions return a dictionary of all available translations. When no translation is requited, just use `{'en': 'foobar'}`.
