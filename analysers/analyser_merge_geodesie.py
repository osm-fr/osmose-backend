#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
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

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate

doc = dict(
    detail = T_(
'''[WikiProject_France/Repères_Géodésiques](https://wiki.openstreetmap.org/wiki/WikiProject_France/Rep%C3%A8res_G%C3%A9od%C3%A9siques)
French survey point imported in OSM but not found.'''),
    fix = T_(
'''Restore node or relation.'''),
    trap = T_(
'''Offered fix reimport the missing sites as point, but if was a
relation. Must be converted manually, keep the tags and put survey points
in relation.'''))

class Analyser_Merge_Geodesie(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8070, id = 1, level = 3, tags = ['merge'],
            title = T_('Missing survey point'),
            **doc)
        self.def_class_moved_official(item = 8070, id = 3, level = 3, tags = ['merge'],
            title = T_('Moved survey point'),
            **doc)

        self.init(
            u"http://geodesie.ign.fr",
            u"Fiches géodésiques",
            CSV(Source(attribution = u"©IGN %s dans le cadre de la cartographie réglementaire", millesime = "2010",
                    file = "geodesie.csv.bz2"),
                header = False),
            Load("lon", "lat",
                where = lambda res: not(u'Point constaté détruit' in res[u'description'] or u'Point non retrouvé' in res[u'description']), # No more uniq ref
                create = """
                    id VARCHAR(254) PRIMARY KEY,
                    lat VARCHAR(254),
                    lon VARCHAR(254),
                    description VARCHAR(4096),
                    ele VARCHAR(254),
                    ref VARCHAR(254)"""),
            Mapping(
                select = Select(
                    types = ["nodes"],
                    tags = {"man_made": "survey_point"}),
                osmRef = "ref",
                extraJoin = "description",
                generate = Generate(
                    static1 = {
                        "man_made": "survey_point"},
                    static2 = {
                        "note": u"Ne pas déplacer ce point, cf. - Do not move this node, see - http://wiki.openstreetmap.org/wiki/WikiProject_France/Repères_Géodésiques#Permanence_des_rep.C3.A8res",
                        "source": self.source},
                    mapping1 = {
                        "ref": "ref",
                        "ele": "ele"},
                    mapping2 = {
                        "description": "description"},
                    text = lambda tags, fields: {"en": u"Survey point %s" % tags["ref"], "fr": u"Repères géodésiques %s" % tags["ref"], "es": u"Señales geodésicas %s" % tags["ref"]} )))


class Analyser_Merge_Geodesie_Site(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8070, id = 2, level = 3, tags = ['merge'],
            title = T_('Missing survey site'),
            **doc)

        self.init(
            u"http://geodesie.ign.fr",
            u"Fiches géodésiques-site",
            CSV(Source(attribution = u"©IGN %s dans le cadre de la cartographie réglementaire", millesime = "2010",
                    file = "geodesie_site.csv.bz2"),
                header = False),
            Load("lon", "lat",
                create = """
                    id VARCHAR(254) PRIMARY KEY,
                    ref VARCHAR(254),
                    name VARCHAR(254),
                    note VARCHAR(254),
                    network VARCHAR(254),
                    source VARCHAR(254),
                    lat VARCHAR(254),
                    lon VARCHAR(254)"""),
            Mapping(
                select = Select(
                    types = ["relations"],
                    tags = {
                        "type": "site",
                        "site": "geodesic"}),
                osmRef = "ref",
                generate = Generate(
                    static1 = {
                        "type": "site",
                        "site": "geodesic"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref": "ref",
                        "name": "name",
                        "network": "network"},
                    mapping2 = {"note": "note"},
                    text = lambda tags, fields: {"en": u"Survey site %s - %s" % (fields["ref"], fields["name"]), "fr": u"Site géodésique %s - %s" % (fields["ref"], fields["name"]), "es": u"Sitio geodésico %s - %s" % (fields["ref"], fields["name"])} )))
