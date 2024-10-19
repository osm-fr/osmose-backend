#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Osmose project 2024                                        ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################


# This module file contains functions to read MediaWiki markup tables, templates, lists, ...

import wikitextparser
from typing import Union, Optional

# Get a list of lists containing all cells of a table.
# Parameters:
#   wikitext - the text of a wikipedia page
#   tab_index - the index of the table (if there's multiple tables on the wiki)
#   keep_markup - if False, everything (except Templates) will be converted to plain text
#   skip_headers - if True, header rows are removed. Assumes all headers are on top
# Returns:
#   The cell contents, specified as a list in a list.
#   The outer list is the rows, the inner list are the cells in that row
# Throws:
#   If the table at the specified index isn't found
def read_wiki_table(wikitext: str, tab_index: int = 0, keep_markup: bool = False, skip_headers: bool = True) -> list[list[Optional[str]]]:
    # Drops all markup, such as italics, hyperlinks, ...
    if not keep_markup:
        wikitext = wikitextparser.remove_markup(wikitext, replace_tables=False, replace_templates=False)

    t = wikitextparser.parse(wikitext).tables[tab_index]

    # Remove header rows if desired
    removable_header_rows = 0
    if skip_headers:
        removable_header_rows = len(list(filter(lambda c: c.is_header, t.cells(column=0))))
    t = t.data()[removable_header_rows:]

    # Remove whitespace around the cells
    return list(map(lambda row: list(map(lambda c: c.strip() if isinstance(c, str) else c, row)), t))


# Get all instances of a certain wiki template within wikitext
# Parameters:
#   wikitext - the text of a wikipedia page
#   template_name - the name or names of the template to locate, e.g. 'Deprecated features/item'
#   keep_markup - if False, everything (except Templates) will be converted to plain text
# Returns:
#   A list containing lists of strings with values [template_string, template_name, argument1, argument2, argument3, ...]
#   Example: ["{{Tag | key | value}}", "Tag", "key", "value"]
#   (Note that the template_string is affected by the markup removal, so for string replace purposes, use keep_markup=True)
def read_wiki_templates(wikitext: str, template_name: Union[str, list[str]], keep_markup: bool = False) -> list[list[str]]:
    if isinstance(template_name, str):
        template_name = [template_name]
    template_name = list(map(str.lower, template_name))

    # Drops all markup, such as italics, hyperlinks, ...
    if not keep_markup:
        wikitext = wikitextparser.remove_markup(wikitext, replace_templates=False)

    # Get all templates that match the filter
    template_objects = list(filter(lambda t: t.name.strip().lower() in template_name, wikitextparser.parse(wikitext).templates))

    return list(map(lambda t: [t.string, t.name.strip()] + [str(a)[1:].strip() for a in t.arguments], template_objects))


# Get all entries in a list within wikitext
# Parameters:
#   wikitext - the text of a wikipedia page
#   list_index - the index of the list (if there's multiple lists on the wiki)
#   keep_markup - if False, everything (except Templates) will be converted to plain text
#   include_sublists - if true, include subitems. If false, only include the highest level items
#       When true, the list item symbol (*, **, #, ##, :, ...) will also be included in the output
# Returns:
#   A list with all list items
# Throws:
#   If the list at index list_index doesn't exist
def read_wiki_list(wikitext: str, list_index: int = 0, keep_markup: bool = False, include_sublists: bool = False) -> list[str]:
    if not keep_markup:
        wikitext = wikitextparser.remove_markup(wikitext, replace_templates=False)

    lst = wikitextparser.parse(wikitext).get_lists()[list_index]
    if include_sublists:
        # Note this contains the list identifier, e.g. *, **, #, ##
        return list(map(str.strip, lst.fullitems))
    return list(map(str.strip, lst.items))


# Get all list entries within wikitext
# See read_wiki_list for details (excluding list_index)
def read_all_wiki_lists(wikitext: str, keep_markup: bool = False, include_sublists: bool = False) -> list[str]:
    res = []
    if not keep_markup:
        wikitext = wikitextparser.remove_markup(wikitext, replace_templates=False)

    try:
        list_index = 0
        while True:
            res.extend(read_wiki_list(wikitext, list_index=list_index, keep_markup=True, include_sublists=include_sublists))
            list_index += 1
    except IndexError:
        return res


# Convert all instances of Tag-templates to textual tags, e.g. {{Tag|oneway|yes}} -> "oneway=yes"
# Parameters:
#   wikitext - the text of a wikipedia page
#   quote - whether the tag should be wrapped in ``
#   star_value - whether empty tag values should be represented by *
# Returns:
#   The wikitext with {{Tag|*}} replaced by the textual tag
def wikitag2text(wikitext: str, quote: bool = False, star_value: bool = True) -> str:
    tag_templates = read_wiki_templates(wikitext, ["Tag", "Key"], keep_markup = True)
    for t in tag_templates:
        k = t[2]
        # This part isn't perfect yet, there's special syntax for ;-separated, :-subkeys, :-subvalues, languages, ...
        v = "*" if star_value else ""
        if len(t) > 3:
            v = "".join(t[3:]) or v
        if v:
            v = "=" + v
        wikitext = wikitext.replace(t[0], "{2}{0}{1}{2}".format(k, v, "`" if quote else ""))
    return wikitext
