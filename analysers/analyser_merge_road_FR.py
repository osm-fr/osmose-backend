#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2022                                      ##
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

from modules.OsmoseTranslation import T_
from .Analyser_Merge import SourceIGN, GPKG, Load, Select, Mapping
from .Analyser_Merge_Network import Analyser_Merge_Network, ConflateNetwork


class Analyser_Merge_Road_FR(Analyser_Merge_Network):
    def __init__(self, config, logger = None):
        Analyser_Merge_Network.__init__(self, config, logger)
        self.def_class_missing_official(item = 7170, id = 13, level = 2, tags = ['merge', 'highway', 'fix:survey', 'fix:imagery'],
            title = T_('Road not integrated'))

        dep_code = config.options.get('dep_code') or config.options.get('country').split('-')[1]
        if len(str(dep_code)) == 2:
            dep_code = f"0{dep_code}"
        self.init(
            "https://ign.fr",
            "IGN-troncon_de_route",
            GPKG(SourceIGN(dep_code = config.options.get('dep_code') or config.options.get('country').split('-')[1]),
                layer = "troncon_de_route",
                fields = ['importance', 'fictif', 'etat_de_l_objet', 'nature', 'nom_collaboratif_gauche', 'nom_collaboratif_droite', 'alias_gauche', 'alias_droit']),
            Load('geom',
                table_name = 'road_fr_' + config.options['country'].replace("-", "_"),
                # Ignore : 'Chemin', 'Bac ou liaison maritime', 'Sentier'
                select = [{
                    # Even without name
                    'importance': ['1', '2', '3', '4', '5'],
                    'fictif': 'false',
                    'etat_de_l_objet': 'En service',
                    # 'Escalier', 'Route empierrée'
                    'nature': ['Bretelle', 'Rond-point', 'Route à 1 chaussée', 'Route à 2 chaussées', 'Type autoroutier', 'Piste cyclable'],
                }, {
                    # Only with name
                    'importance': ['1', '2', '3', '4', '5'],
                    'fictif': 'false',
                    'etat_de_l_objet': 'En service',
                    'nom_collaboratif_gauche': {'like': '_%'},
                    # 'Bretelle', 'Rond-point', 'Route à 1 chaussée', 'Route à 2 chaussées', 'Type autoroutier', 'Piste cyclable'
                    'nature': ['Escalier', 'Route empierrée'] }] ),
            ConflateNetwork(
                select = Select(
                    types = ['ways'],
                    tags = {'highway': None}),
                conflationDistance = 15,
                minLength = 50,
                mapping = Mapping(
                    static1 = {'highway': 'road'},
                    static2 = {'source': self.source},
                    text = lambda tags, fields: {'en': ', '.join(filter(lambda x: x and x != 'None', set([fields['nature'], fields['nom_collaboratif_gauche'], fields['nom_collaboratif_droite'], fields['alias_gauche'], fields['alias_droit']]) ))} )))
