# Plugin based on MapCCS - The basics

The MapCSS is easier to understand and write than Python. The [definition of the MapCSS language](https://josm.openstreetmap.de/wiki/Help/Styles/MapCSSImplementation) is from JOSM. The MapCSS code can also be run and [shared with the JOSM validator](https://josm.openstreetmap.de/wiki/Rules).

## MapCSS Structure

### Overview

Example of a full MapCSS file for Osmose-QA with one validation rule:
```css
meta {
    title: "Osmose-QA – Object here";
    description: "Nice report.";
    author: "Bob";
    min-josm-version: 14481;
    -osmoseTags: list("tag");
}
meta[lang=en] { /* lang=en, unused, only to use tr() to catch string for translation */
    description: tr("Nice report.");
}
meta[lang=fr] {
    description: "Chouette rapport.";
}

*[amenity=fountain] {
    throwWarning: tr("Fountain here");
    -osmoseItemClassLevel: "4030/40301/2";
    -osmoseTags: list("fix:survey"); // The tags are added to the on of the global declaration
    
    assertMatch: "way amenity=fountain";
    assertMatch: "way amenity=fountain name='Eau Claire'";
    assertNoMatch: "node sport=boules";
}
```

### Meta

The `meta` header can be avoided but it is advisable. It contains information on the rules from this MapCSS file, like title, description, author... and can contains Osmose-QA properties to avoid repeating it on each rules.

```css
meta {
    title: "Parking lanes";   /* title shown in the JOSM menu */
    icon: "logo_16x16x8.png"; /* small icon shown in the JOSM menu next to the title */
    version: "1.2";           /* the version of the style */
    description: "...";       /* one or two sentences of describing the style */
    author: "...";            /* the author(s) of the style */
    link: "https://...";      /* URL to the web page of the rules */
    min-josm-version: 14481;  /* the minimum JOSM version where this style works */
}
```

The `min-josm-version` is required by JOSM to ignore Osmose-QA MapCSS extensions. But it is now an old JOSM version (14481) and can be safely ignored.

Additional Osmose-QA property `-osmoseTags` can be set to have common Osmose-QA tags applied to all the rules of this MapCSS file.

```css
meta {
    -osmoseTags: list("highway", "emergency");
}
```

JOSM have a limitation of using translation on `meta` part. So, we have to add extra `meta` sections, one for each translation. Note: translation on the following rules are supported in a more regular manner.

```css
meta[lang=en] { /* lang=en, unused, only to use tr() to catch string for translation */
    description: tr("Nice report.");
}

meta[lang=fr] {
    description: "Chouette rapport.";
}
```

### Rules

The rules are composed of one or multiple selectors, when an OSM object match one selector, the following block of properties is applied and produce an Osmose-QA issue.

### Selectors

A rule selector is composed by a type and the conditions. Eg: `way[highway][junction!=roundabout]`.

Multiple selectors can be used, separated by a comma `,`:
```css
node[highway],
way[highway][junction!=roundabout] {
    ...
}
```

#### Types

The rules selectors can apply on OSM objects filtered by type or not. The common object types are:
* `node`
* `way`
* `relation`

The wildcard selector is for all at once:
* `*`

Note: JOSM also have an `area` type. But it is not implemented in Osmose-QA, and such selector are ignored.

#### Condition on tags

Condition can be the presence or absence of an OSM key:
* `[highway]`
* `[!highway]`

Or condition on values:
* `[junction!=roundabout]`
* `[ref=~/A[0-9]+/]`: using regular expression
* `[population>=50000]`: comparing

See the full list of conditions on [JOSM documentation](https://josm.openstreetmap.de/wiki/Help/Styles/MapCSSImplementation).

Note: the conditions related to multiple objects are not implement on Osmose-QA. The current implementation is only for one object.

#### Functions

Functions may be used in selector (and properties, see below). Thank to these it is possible to rework string, number, regex... all the details are on the [JOSM documentation](https://josm.openstreetmap.de/wiki/Help/Styles/MapCSSImplementation#Evalexpressions). The full list of implemented function in Osmose-QA can be found in the [source code](https://github.com/osm-fr/osmose-backend/blob/master/mapcss/mapcss_lib.py).

One of the most present function is `tr()` for translation. Fist parameter of the `tr()` will be send to translator, and replaced by translation at runtime.

#### Conditions on Territories and Languages

A rule may apply to only a country a sub part of a country or is an area using a particular language. The condition can also be negated.

* `[inside("FR")]`: inside France,
* `[inside("US-FL")]`: inside state of Florida, USA,
* `[outside("IT,DE")]`: outside Italy and Germany,
* `[language("fa")]`: on area using Farsi language.

Note: the `language` is an extension of Osmose-QA, not supported by JOSM.

#### Pseudo Classes

Pseudo Classes allow to select objects by state, and can be negated.

```css
way:closed2 {
    ....
}

node!:tagged {
    ....
}
```

See the full [JOSM list](https://josm.openstreetmap.de/wiki/Help/Styles/MapCSSImplementation#PseudoClasses) of Pseudo Classes, but only the part not linked to JOSM edit functionality are supported in Osmose-QA.


### Properties

See full details in [MapCSS data validation definition](https://josm.openstreetmap.de/wiki/Help/Validator/MapCSSTagChecker) from JOSM. Here only an overview.

#### Groups

Rules can be grouped. It is not mandatory. Each rule of the group should use the same string definition.

```css
node[name] {
    group: tr("Bad name");
}

*[name_alt] {
    group: tr("Bad name");
}
```

The `group` value is assigned to the `title` field of the Osmose-QA issue class definition. It is better to have one.

#### Throws

The rule should throws one issue using:
* throwError
* throwWarning

##### Message
The `throw*` properties report a message with placeholders and can be adjusted to the current OSM object. This string value is assigned to the `text` (aka subtitle) field of Osmose-QA issues. When `group` is not defined it is also assigned to the `title` field, but without replacing the placeholder -so it is better to have a `group` defined.)

```css
*[barrier=wire_fence] {
  throwWarning: tr("{0} is deprecated", "{0.tag}"); /* "{0.tag}" evaluates to "barrier=wire_fence" */
}
```

The string will be translated, then placeholder `{0}` (`{1}`, `{2}`...) will be replaced by the parameters. The parameters could be string of using matched OSM objects, the number indicate the tag from the condition, in the same order. Then `[N].tag` will be `key=value` and `[N].key` or `[N].value` could be used.

##### Level
Each `throw*` define a level. Osmose-QA issue level and JOSM level are not based on the same concept. JOSM define Error, Warning and Info, like Osmose-QA use gravity from 1 up to 3 and only aim to report issues.

By default, `throwError` is mapped to Osmose-QA issue of level 2 and `throwWarning` is mapped to level 3. JOSM also define `throwOther`, but these are not reported by Osmose-QA.

Level can also be explicitly defined, and override the default mapping from `throw*`, using `-osmoseItemClassLevel` (see below).

#### Fix

A suggestion of correction can be made. Note the MapCSS allows less possibilities of suggesting fix than Osmose-QA Python implementation of plugins. Fix properties can be combined. But no alternative fix could be proposed.

* `fixAdd`: Add an OSM tag `fixAdd: "key=val";`
* `fixRemove`: Remove an OSM tag `fixRemove: "key";`
* `fixChangeKey`: Change a key, and keep the value `fixChangeKey: "old=>new";`
* `fixDeleteObject`: Delete the matched object `fixDeleteObject: this;` (partially implemented in Osmose-QA)

A free text on how to fix can also be present:
* `suggestAlternative: "any text (e.g., alternative key)";` (not implemented in Osmose-QA)

#### Osmose-QA Properties

Osmose-QA have two optional extensions, ignored by JOSM.

```css
    -osmoseTags: list("highway", "emergency");
```
These Osmose-QA tags extent the ones define in the `meta` section.

```css
    -osmoseItemClassLevel: "4030/40301/2";
```
Set the Osmose-QA class definition fields: `item`, `class` id, and `level`. When defined, override the default level of `throw`.

If required a sub class id can also be defined with `[class]:[subclass]`:
```css
    -osmoseItemClassLevel: "4030/40301:887554/2";
```

### Set, define MapCSS class

Parts of selectors can be factorized in a MapCSS class, and then reused.

```css
/* Define class */
way[highway] {
  set highway;
}

/* Use class */
way.highway[oneway=yes] {
    ...
}
```


## Compiling MapCSS to Osmose Python Plugin

The tools from `mapcss/mapcss2osmose.py` parse the MapCSS file and compile it into an Osmose-QA Python plugin.

Run it like this:
```
python -m mapcss.mapcss2osmose plugins/Fountain.validator.mapcss
```

For MapCSS from external sources (JOSM and JOSM contrib)), class id are generated and stored in `mapcss/item_map.py` to have stable value on next generation.

The generated python plugin can now be run as standard Osmose-QA plugin. See general documentation how to run it.


## Tests

The MapCSS rules can embed tests to check the selectors work as expected. This asserts are also compiled in the Osmose-QA Python plugin and can be run to ensure all is right. It is recommended to write asserts in the MapCSS file.

The available assert properties are:
* `assertMatch`
* `assertNoMatch`
* `-osmoseAssertMatchWithContext`
* `-osmoseAssertNoMatchWithContext`

They assert whether the following fake OSM objects match or not match any selector of the rule. The latter two are not supported by JOSM, and allow to set up a country or a language.

The fake OSM object is described by a type and a list of tags.

```css
* {
    assertMatch: "node power=transformer";
    assertNoMatch: "node power=transformer frequency=50";

    -osmoseAssertNoMatchWithContext: list('node place=hamlet name="Kerbrest"', "inside=FR");
}
```

The test code of generated plugins can be run with `pytest`:
```
pytest plugins/Bicycle.py
```

## Running on JOSM

Local MapCSS file can be added to the JOSM Validator.

In place of keeping it in Osmose-QA the MapCSS files can also be shared with the [contrib rules of JOSM](https://josm.openstreetmap.de/wiki/Rules). Osmose-QA already use part of this shared rule sets.

### Test on JOSM

The asserts in the MapCSS rules can also be checked by JSON. This is optional and must be enabled.
