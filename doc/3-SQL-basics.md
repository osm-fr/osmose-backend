# Analyzer based on SQL query - The basics

The database is a PostgreSQL with PostGIS spatial extension and hstore. It is know as [Osmosis](https://wiki.openstreetmap.org/wiki/Osmosis) schema and loaded by the tool of the same name.


## Database schema

There is 3 main tables `nodes`, `ways` and `relations`.

All table have in common:
* `id`: bigint
* `version`: integer
* `user_id`: integer, the value may not be available
* `tstamp`: timestamp without time zone
* `changeset_id`: bigint
* `tags`: hstore

The **nodes** have the location in the `geom` field:
* `geom`: geometry(Point,4326)

The **ways** have the location on `linestring` field:
* `nodes`: bigint[], node ids of the way,
* `is_polygon`: boolean, is the `linestring` a loop and valid geometry?
* `linestring`: geometry(Geometry,4326)

The **relations** have no geometry and specific field.

In addition to the basics there are join tables to make the links.

The **way_nodes** allow to pass from nodes to ways and vice versa. But note the `ways` table also have the `nodes` fields for better performance when passing from ways to nodes.
* `way_id`: bigint
* `node_id`: bigint
* `sequence_id`: integer

The **relation_members**, for the content of the relations:
* `relation_id`: bigint
* `member_id`: bigint
* `member_type`: character(1), `N`, `W` or `R`
* `member_role`: text
* `sequence_id`: integer


## Tags and hstore

hstore is key-value storage for the OpenStreetMap tags. See general usage at [PostgreSQL hstore reference](https://www.postgresql.org/docs/current/hstore.html).

But for short we use:
* `tags?'key'` to check if there is an OSM key `key`.
* `tags->'key'` to get the value of the osm key `key`, while `key` may not exists.
* `tags->'key' = 'value'` to test the `value` of a `key`, and so on.

**Note 1**: where using the tags, always add the clause `tags != ''::hstore`. It checks whether or not there is tags on the object before using your own clauses. The tags are indexed on object only having tags. It helps on better performance, especially on node objects where most of the objects does not have tags.

**Note 2**: for same performance goal, always check a main tags exists before access the values. It helps with indexes: `tags?'highway' AND tags->'highway' = 'primary'`. Then, you can access directly secondary tag value `ways.tags->'junction'`.


## Geometry and PostGIS

PostGIS allows to make spatial queries, aka geometrical. See available function at [PostGIS reference](https://postgis.net/docs/reference.html).

The geometries coordinate are in EPSG:4326, aka WGS 84, aka longitude and latitude. The coordinates unit are in degree, witch is unsuitable for computing ground distances and areas.

Spatial index must be used to largely improve performance on spatial crossing queries: `ways1.linestring && ways2.linestring`, it allows to use the spatial index on bbox of the objects.


## Analyzer architecture


### Definition

The analyzer inherit from class `Analyser_Osmosis`. It have to implement `__init__()` for defining Osmose issues classes using method `def_class` (see general documentation about this).

The analyzer also have to implement a non diff mode:
* `analyser_osmosis_common()`: run check not supporting diff mode.
Or a diff mode, with this two methods:
* `analyser_osmosis_full()`: run check supporting diff mode. but for full data check.
* `analyser_osmosis_diff()`: run check supporting diff mode. Checks only on data changed from last run.

The Osmose issues classes not supporting diff go into `self.classs` while the other in `self.classs_change`.

```python
self.classs[7] = self.def_class(item = 7040, level = 3, tags = ['power', 'fix:chair'],
    title = T_('Unmatched voltage of line on substation'))
```


### SQL run

The SQL queries are just strings. Placeholder can be used to add parameters or support diff mode. Use as many SQL queries as you want. You can create temporary table.

The query are run using `self.run(sql, callback)`. The callback is optional.

#### Callback
The callback is a function (a lambda function) responsible of mapping row results from SQL query to Osmose issues. The callback receives the row as parameter. It should return a dictionary with the keys:
* `class`: referring one class id defined in `__init__()`
* `subclass`, optional
* `text`, optional
* `fix`, optional
* `data`: an array of interpretation of ordered fields from the SQL row.

With the exception of `data`, all the other keys are generic fields of osmose issues. See general documentation about this fields.

#### Data mapping
The available value for the `data`, mapping OSM object id are:
* `node`
* `node_full`
* `way`
* `way_full`
* `relation`
* `relation_full`
From array of (type: N/W/R, ids):
* `array_full`

Without `_full` variant, only the id is keep in the Osmose issue, not the tags and other attributes.

When we want to create a new node object we can use:
* `node_new`

The location can be provided by
* `positionAsText` from location point as text,
* `node_position` from a node id: so the query does not have to join on nodes to get the location.

In fact this are functions, fetching from SQL returned fields the OSM object details (geometry, tags...) for filling the Osmose issues.

#### Location extraction

The location should a point in text format, eg.:
```sql
ST_AsText(nodes.geom)
ST_AsText(ST_Centroid(ways.linestring))
```

SQL Helpers are available to compute a location from OSM objects:
* `way_locate(linestring)`: extract position from central point on the linestring, avoid joining on `nodes`.
* `relation_locate(id)`: loop over relation members to extract a location.
* `any_locate(type N/W/R, id)`: get location of variable object types.
* `array_locate(array[type N/W/R, id])`: get location of array of variable object types.

Eg. with helper:
```sql
ST_AsText(way_locate(ways.linestring))
```


### SQL queries

SQL query strings can be parametrized with placeholder `sql = "SELECT {0}"` and the using `sql.format(33)`.

#### Parameters
Parameters from country settings can be accessed using `self.config.options.get("paramter_name")`, especially to use the local projection (`proj` setting).

#### Projection
Since data are stored in longitude and latitude, the unit is degree, and distance like areas cannot be computed. Each country come with an adapted local projection setting to have units in meters. The data should be re-projected in the query to do so.

```sql
SELECT
    id,
    ST_Transform(linestring, {0}) AS linestring_proj
FROM
    ways
```

#### Common Factorized tables
May analyzers work on same topic. To avoid recomputing intermediate tables many time, and not always on the ways in interpreting OSM tags, some generic tables are available. There are computed only on request, but reused once it is done.

The available common tables are (see full definition in Analyser_Osmosis.py):
* highways: with tags normalization, levels classification and re projected in local country _projection_.
* highway_ends: the start and ends of all highways ways.
* buildings: from ways (and not from multipolygon relations), with tags normalization and re-projected in local country _projection_ as _polygons_.

The dependencie on this common tables should be declared in the analyzer class:
```python
class Analyser_Osmosis_Highway_CulDeSac_Level(Analyser_Osmosis):

    requires_tables_common = ['highway_ends']
```


### Diff analyze support

Osmose can be run in diff modes and analyzer must check only changed data.

`analyser_osmosis_full()` is call when diff mode is supported but a initial (full) analysis is requested. Then on update by diff `analyser_osmosis_diff()` is called.

The diff support is not required or always possible and analysis can be done anyway in full mode using `analyser_osmosis_common()`. Diff mode lower the SQL query run time.
