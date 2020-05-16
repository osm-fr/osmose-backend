#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2013                                      ##
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

from . import OsmSax
from .IssuesFile import IssuesFile


class IssuesFileOsmose(IssuesFile):

    def begin(self):
        output = super().begin()
        self.outxml = OsmSax.OsmSaxWriter(output, "UTF-8")
        self.outxml.startDocument()
        self.outxml.startElement("analysers", {})
        self.geom_type_renderer = {"node": self.outxml.NodeCreate, "way": self.outxml.WayCreate, "relation": self.outxml.RelationCreate, "position": self.position}

    def end(self):
        self.outxml.endElement("analysers")
        self.outxml.endDocument()
        del self.outxml
        super().end()

    def analyser(self, timestamp, analyser_version, change=False):
        self.mode = "analyserChange" if change else "analyser"
        attrs = {}
        attrs["timestamp"] = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
        attrs["analyser_version"] = str(analyser_version)
        if self.version is not None:
            attrs["version"] = self.version
        self.outxml.startElement(self.mode, attrs)

    def analyser_end(self):
        self.outxml.endElement(self.mode)

    def classs(self, id, item, level, tags, title, detail = None, fix = None, trap = None, example = None, source = None, resource = None):
        options = {
            'id': str(id),
            'item': str(item),
        }
        if source:
            options['source'] = str(source)
        if resource:
            options['resource'] = str(resource)
        if level:
            options['level'] = str(level)
        if tags:
            options['tag'] = ','.join(tags)
        self.outxml.startElement('class', options)
        for (key, value) in [
            ('classtext', title),
            ('detail', detail),
            ('fix', fix),
            ('trap', trap),
            ('example', example),
        ]:
            if value:
                for lang in sorted(value.keys()):
                    self.outxml.Element(key, {
                        'lang': lang,
                        'title': value[lang]
                    })
        self.outxml.endElement('class')

    def error(self, classs, subclass, text, ids, types, fix, geom, allow_override=False):
        if self.filter and not self.filter.apply(classs, subclass, geom):
            return

        if subclass is not None:
            self.outxml.startElement("error", {"class":str(classs), "subclass":str(subclass)})
        else:
            self.outxml.startElement("error", {"class":str(classs)})
        for type in geom:
            for g in geom[type]:
                self.geom_type_renderer[type](g)
        if text:
            for lang in text:
                self.outxml.Element("text", {"lang":lang, "value":text[lang]})
        if fix:
            fix = self.fixdiff(fix)
            if not allow_override:
                fix = self.filterfix(ids, types, fix, geom)
            self.dumpxmlfix(ids, types, fix)
        self.outxml.endElement("error")

    def position(self, args):
        self.outxml.Element("location", {"lat":str(args["lat"]), "lon":str(args["lon"])})

    def delete(self, t, id):
        self.outxml.Element("delete", {"type": t, "id": str(id)})

    def dumpxmlfix(self, ids, types, fixes):
        self.outxml.startElement("fixes", {})
        for fix in fixes:
            self.outxml.startElement("fix", {})
            i = 0
            for f in fix:
                if f is not None and i < len(types):
                    type = types[i]
                    if type:
                        self.outxml.startElement(type, {'id': str(ids[i])})
                        for opp, tags in f.items():
                            for k in tags:
                                if opp in '~+':
                                    self.outxml.Element('tag', {'action': self.FixTable[opp], 'k': k, 'v': tags[k]})
                                else:
                                    self.outxml.Element('tag', {'action': self.FixTable[opp], 'k': k})
                        self.outxml.endElement(type)
                i += 1
            self.outxml.endElement('fix')
        self.outxml.endElement('fixes')
