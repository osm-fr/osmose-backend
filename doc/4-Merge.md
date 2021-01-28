# OpenData Merge

This kind of analyzers are based on the basic SQL analyzer, but mastering the latter is not required. The merge framework aim to simplify this task.


## Generals concepts

The global idea is to:
* fetch an OpenData set,
* load it into database,
* convert OpenData attributes to OSM tags,
* compare with OSM by location distance and tags (aka conflate)
* report differences: missing objects in OSM, objects present in OSM but not in OpenData set, matching objects with different tags or values and more.


## General implementation

We aim here to have configuration over code. Nevertheless this configuration is written in Python and may contain Python code when necessary (but not on typical use case). The goal is to easy the process of creating and maintaining this kind of merger analyzers.

The configuration can be seen as a chain:
- Content is fetched from a `Source`: remote or local file or archive.
- File format reader: the `Parser` with implementation available for multiple formats like CSV, JSON, GeoJSON, GTFS, SHP... It imports the data into the database.
- The reader make data available to `Load`. Thos one pre-process and filters data to a convenient schema.
- The `Conflate` allows to compare and report from
  - the OSM data filtered by `Select`,
  - the OpenData converted to OSM tags with `Mapping`

The full merge framework code is in `Analyser_Merge.py`.

The support of the diff mode is not implemented.


## Classes of issues

Like other analyzer merge must define classes, picked from these available helpers:
- `def_class_missing_official`: OpenData set contains an object, but no matching one found in OSM. By convention the item number look like `8yy0` and class `id` is 1.
- `def_class_missing_osm`: OSM contains an object, but no matching one found in the OpenData set. By convention the item number look like `7xxx` and class `id` is 2.
- `def_class_possible_merge`: A probable matching object found. By convention the item number look like `8yy1` and class `id` is 3.
- `def_class_update_official`: An OSM object matchs the OpenData one, close location and same reference value. But new tags or values from OpenData are available. By convention the item number look like `8yy2` and class `id` is 4.
- `def_class_moved_official`: The matching OSM found, but not at the same location as OpenData. Not for main use case.

All classes of issues are optional, but the main used one is `def_class_missing_official`.

By convention the `level` value for this kind of issues is `3`, but other could be used.

For other attributes, see common documentations.

```python
from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge

class Analyser_Merge_Charging_station_FR(Analyser_Merge):
    def __init__(self, config, logger=None):
        self.def_class_missing_official(item = 8410, id = 1, level = 3, tags = ['merge'],
            title = T_('Car charging station not integrated'))
        self.def_class_missing_osm(item = 7051, id = 2, level = 3, tags = ['merge', 'post'],
            title = T_('Car charging without tag "ref" or invalid'))
        self.def_class_possible_merge(item = 8411, id = 3, level = 3, tags = ['merge'],
            title = T_('Car charging station, integration suggestion'))
        self.def_class_update_official(item = 8412, id = 4, level = 3, tags = ['merge'],
            title = T_('Car charging station update'))
```

## OpenData set Source

The OpenData set is available online and can be fetched online. On edge case, the data can be included directly on the Osmose-QA backed repository, but we try to avoid this case.

There are multiple OpenData classes to facilitate retrieving data, depending on the source.

### SourceOpenDataSoft
A lot of OpenData providers use [OpenDataSoft](https://www.opendatasoft.com/). It can usually be identified by the presence of `/explore/dataset/` in the URL.

It uses the following attributes:
- `url`: The URL of the dataset
- `format`: Requested format of the file. Usually `csv` (default), `json` or `shp`

Example:

```python
from .Analyser_Merge import SourceOpenDataSoft

    SourceOpenDataSoft(
        attribution='La Poste',
        url='https://datanova.legroupe.laposte.fr/explore/dataset/laposte_boiterue',
    )
```

### SourceDataGouv
Data shared on [data.gouv.fr](https://data.gouv.fr/) can be retrieved with this class.

It uses the following attributes:
- `dataset`: Dataset identifier. It can be seen by clicking on Details on the dataset page.
- `resource`: The resource (file) identifier. It can be seen by clicking on the resource in the dataset page. It's the end of the "stable URL"

Example:

```python
from .Analyser_Merge import SourceDataGouv

    SourceDataGouv(
        attribution='data.gouv.fr:Etalab',
        dataset='5c70a7f206e3e755537bb849',
        resource='01f2a133-4929-4001-906c-412f682d0d59',
    )
```

### SourceHttpLastModified
Retrieve the `millesime` from the `Last-modified` HTTP header. Otherwise it is identical to `Source`.

### Source
Base class that can be used data sources not covered by specific classes.

It uses the following attributes:
- Either:
  - `fileUrl`: remote content file URL.
  - `file`: local content file from the `merge_data` directory, avoid this case.
- `millesime`: optional, date of the last release, for the OSM `source` tag. Note: since it is hard coded, it is not automatically updated when the remote data is updated. May be required with the attribution in some jurisdiction.

```python
from .Analyser_Merge import Source

    Source(
        attribution='data.gouv.fr:Etalab',
        fileUrl='https://www.data.gouv.fr/fr/datasets/r/01f2a133-4929-4001-906c-412f682d0d59',
        millesime='01/2020',
    )
```

### Common attributes

All above OpenData sets accept these attributes:
- `attribution`: Author of the data, for the OSM `source` tag.

Remote files are fetched and saved in the Osmose-QA Backend cache, the delay can be adjusted:
- `fileUrlCache`: cache delay in days, default to 30 days.

The remote file could be compressed or an archive:
- `bz2` (boolean): the content is compressed in BZip2 format.
- `gzip` (boolean): the content is compressed in GZip format.
- `zip`: the remote URL is a ZIP archive and the data is at this path inside the archive.
- `extract`: same as `zip`, but for all archive formats.

Assuming the resource is a text file:
- `encoding`: define the encoding of the text content, in order to be re-encoded into the default UTF-8 encoding.
- `filter`: a lambda expression applied on text content before loading (text in one big blob). Only to hijack bad formatted content and make it usable. See `Load` option for proper data filters.

Alongside that and outside of the source attributes, can be found:
- **URL** of a comprehensive web description of the data set: for human, link found on Osmose-QA frontend help for OSM contributors.
- **Title** of the remote OpenData set.


## File format Parser

Once the content is fetched a file format parser read it and import raw data, record by record, into a table in PostgreSQL database. Each file format parser may have dedicated options (more detail in `Analyser_Merge.py`).

Available parser are:
- CSV
- GTFS, read the stops.txt file from a GTFS ZIP archive.
- JSON, GeoJSON
- SHP, inside ZIP archive
- GDAL: all formats supported by GDAL [`ogr2ogr`](https://gdal.org/drivers/vector/index.html).

```python
from .Analyser_Merge import CSV

    CSV(
        Source(...),
        separator = ';',
    )
```


## Load

The load step reads the raw data records from the database and convert these to OSM tags and geographical location.

### Location
First, the load process must fetch or build a geographical location. From geographical file data format, the raw record is already loaded with a geographical fields. An helper keep the point geometry or get the object centroid:
```python
from .Analyser_Merge import LoadGeomCentroid

    LoadGeomCentroid(...)
```

In other case, the `x` (longitude) and the `y` (latitude) field name must be given:
```python
from .Analyser_Merge import Load

    Load('lon', 'lat', ...)
```

Note: sometime the both coordinates are in the same field, then the field must be given twice.

A lambda function may be applied to `x` and `y` field to extract or convert to proper number:
```python
    Load('coords', 'coords',
        xFunction = lambda x: ...,
        yFunction = lambda y: ...,
    )
```

A common usage is to split a unique coordinate field:
```python
        xFunction = lambda x: x.split(',')[0]
```

`Load` take care of removing extra spaces and converting to float number.

Helpers function are also available:
- `Load.float_comma`: Convert decimal comma to dot separated.
- `Load.degree`: Convert coordinate in degree, minute, second to decimal degrees.

If the raw data coordinates are not in longitude / latitude (SIRD 4362), the SIRD must be set in order to reproject the data:
- `srid`: SIRD code of the data coordinates.

### Data Table
The names of the attributes are generally given with the data. If it is not the case an SQL table definition can be given with parameter `create`.

### Data Records

The loaded records can be filtered and edited:
- `select`: query structure reformatted as SQL to filter records, prefer this to the `where` parameter. See Annex `Select` for syntax.
- `where`: lambda expression taking a records as dict and returning boolean to determine whether or not inserting the row into the table.
- `map`: lambda returning a dict from a dict to replace the record.
- `unique`: keep only one distinct record by list of column.


## Mapping

Once the data is loaded, filtered and adjusted, attributes can be converted to OSM tags using the `Mapping` definition.

The desired OSM tags for the produced objects can be `static` (same value for all objects) or extracted from the records attributes (`mapping`).

The `static` tags are just a dictionary of tags, like in OSM:
```python
    static1 = {
        'heritage:operator': 'mhs',
        'source:heritage': 'Ministère de la Culture',
    }
```

The `mapping` can be just the value of an record attribute or a computed one from one or multiple attributes.
```python
    mapping1 = {
        # Use as OSM tag `ref:mhs` the value of the attribute `Ref`.
        'ref:mhs': 'Ref',
        # Compute the value
        'name': lambda res: res['Name'] if res['Name'] not in BLACK_LIST else None,
        # Use an external function to compute the value
        'mhs:inscription_date': lambda res: parseDate(res['Date']),
    }
```

There is two sets of static tags (`static1`, `static2`) and two of mapping tags (`mapping1`, `mapping2`). First level tags (`static1` and `mapping1`) are used in a different way later in configuration than second level tags (`static2` and `mapping2`).

When a tag value is `None` the key is excluded from the tag set.

A special value `Mapping.delete_tag` means the key will be proposed to suppression to the contributor when this record will raise an issue.

```python
from .Analyser_Merge import Conflate, Mapping

    Conflate(
        mapping = Mapping(
            static1 = {'heritage:operator': 'mhs'},
            static2 = {'source:heritage': 'Ministère de la Culture'},
            mapping1 = {
                # Use for the OSM tag `ref:mhs` the value of the attribute `Ref`.
                'ref:mhs': 'Ref',
                # Compute the value from attribute `Name`.
                'name': lambda res: res['Name'] if res['Name'] not in BLACK_LIST else None,
                # Use an external function to compute the value.
                'mhs:inscription_date': lambda res: parseDate(res['Date']),
            },
        )
    )
```

### Cache
Once the data is converted to OSM tags format is stored in a cache for future reuse. This cache is update on data source fetch update or in analyzer source code update.


## Conflation

The conflation is done geographically by looking at similar close objects, between OSM and the OpenData set, and using a common reference if available.

### OSM Objects
The set of OSM objects to be compared with is defined by a query on object types and tags, the `Select`:
- `types`: object types, array of one or more: `relations`, `ways` and `nodes`.
- `tags`: query structure reformatted as SQL to filter on tags. See Annex `Select` for syntax.

```python
    Conflate(
        select = Select(
            # OSM nodes
            types = ['nodes'],
            # With `emergency=defibrillator` tag.
            tags = {'emergency': 'defibrillator'}),
    )
```

```python
    Conflate(
        select = Select(
            # All OSM object types
            types = ['nodes', 'ways', 'relations'],
            tags = {
                # With `heritage` tag value 1, 2 or 3.
                'heritage': ['1', '2', '3']
                # Without `heritage:operator` tag.
                'heritage:operator': None,
                # With custom `ref:mhs` tag.
                'ref:mhs': lambda t: "{0} NOT LIKE 'PM%' AND {0} NOT LIKE 'IA%'".format(t)}),
    )
```

### Conflation parameters
A match between an OpenData set record and an OSM object is done when:
- `conflationDistance`: max distance in meters,
- `osmRef`: the OSM key for join data on common reference,
- `extraJoin`: an additional OSM key to join.

`osmRef` and `extraJoin` must refer a mapped tags from OpenData set.

At least one of those conditions is required. But having `conflationDistance` is highly advised.

```python
    Conflate(
        osmRef = 'ref:mhs',
        conflationDistance = 1000,
    )
```

`missing_official` method is always available. The other methods `missing_osm`, `possible_merge`, `update_official` and `moved_official` require an `osmRef`.

### Output
Missing and updatable objects are raised as issues.

Updatable is considered regarding first level tags from `static1` and `mapping1`. When these tags are different between OpenData and OSM, an update issue is raised. The second level tags are not used for that (but still included in the results). Typical use case is for `source` tags value or `name` from "official" OpenData not always corresponding to the one from the ground and so not considered as an update.

Alongside that tags, the field issue `text` (aka subtitle) is produced. It helps the contributor to understand the issue and can contain any attributes or tags, including unmapped attributes.

```python
    Conflate(
        mapping = Mapping(
            text = lambda tags, fields: T_('Power substation of {0}', fields['Name'])
        )
    )
```

When no translatable text is required, just provide a default "English" string:
```python
            text = lambda tags, fields: {'en': '{0} - {1}', fields['Name'], fields['Ref'])

```

By default the merge framework understand tags with multiple OSM values separated by `;` and can match on one of this values. On output, produced tags contain only one value by default, but can be combined with already existing ones, using the `tag_keep_multiple_values` to `True` on `Conflate`.

In addition to the Osmose-QA issues, the backend outputs CSV files containing the merge of the OpenData and the OSM content. The OpenData set is mapped on OSM tags. It is the union of objects from both sources and union of all available tags from both sources.


## Annexes

### Select

The `Select` syntax works as well on attributes of OpenData set or on OSM tags. It allows to filter a subset of records or OSM objects.

The syntax is based on a dictionary where keys are attribute names or OSM keys, and values are literals or with special meanings. All dictionary keys and values must be found at once in the record or the OSM object in order to be selected (it means `AND`).

- `True` or `None`: there is a value or the tag exists `{'a': None}`.
- `False`: there is no value for attribute or the tags does not exists: `{'a': False}`.
- literal value: there a key with this exact value `{'a': 'foobar'}`. Note: on OSM tags with multiple  values (`;` separated) it means the literal value is one of the multiple values.
- list: the value is one of the list `{'a': [1, 2]}`. `None` may be in the list.
- SQL `LIKE`: the check of the value is done with SQL `LIKE` (string with placeholders) `{'a': {'like': 'a%'}}`.
- Regex: the check of the value is done with a regex: `{'a': {'regex': 'ab.*z'}}`

```python
{
    # With `emergency=defibrillator` tag.
    'emergency': 'defibrillator',
    # With `heritage` tag value 1, 2 or 3.
    'heritage': ['1', '2', '3']
    # Without `heritage:operator` tag.
    'heritage:operator': None,
    # With custom `ref:mhs` tag.
    'ref:mhs': lambda t: "{0} NOT LIKE 'PM%' AND {0} NOT LIKE 'IA%'".format(t)}),
}
```

`AND` clauses can be combined with alternative queries by using a list `[{'a': 'foo'}, {'b': 'bar'}]`. The meaning of the list is `OR`.

```python
# `man_made=cross` OR `historic=wayside_cross`
[
    {'man_made': 'cross'},
    {'historic': 'wayside_cross'}
]
```
