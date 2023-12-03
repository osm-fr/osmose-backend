#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2021                                      ##
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
from .Analyser_Merge_Dynamic import Analyser_Merge_Dynamic, SubAnalyser_Merge_Dynamic
from .Analyser_Merge import SourceIGN, GPKG, LoadGeomCentroid, Conflate, Select, Mapping


class Analyser_Merge_POI_FR(Analyser_Merge_Dynamic):

    def __init__(self, config, logger = None):
        Analyser_Merge_Dynamic.__init__(self, config, logger)

        maping = [
        # 62967 Culte chrétien
        dict(
            #  31156 Eglise
            #  11728 Chapelle
            #    209 Abbaye
            #    168 Couvent
            #    157 Monastère
            #    134 Cathédrale
            #    108 Basilique
            #    106 Prieuré
            #     84 Abbatiale
            #      4 Collégiale
            item = 8100,
            id = 10001,
            level = 3,
            title = T_('Place of worship not integrated'),
            select = {'nature': 'Culte chrétien', 'nature_detaillee': ['Eglise', 'Chapelle', 'Abbaye', 'Couvent', 'Monastère', 'Cathédrale', 'Basilique', 'Prieuré', 'Abbatiale', 'Collégiale']},
            tags = {'amenity': 'place_of_worship'},
            generate_tags = {'amenity': 'place_of_worship', 'religion': 'christian', 'denomination': 'catholic'},
        ), dict(
            #  15289
            item = 8100,
            id = 10002,
            level = 3,
            title = T_('Place of worship not integrated'),
            select = {'nature': 'Culte chrétien', 'nature_detaillee': None},
            tags = {'amenity': 'place_of_worship'},
            generate_tags = {'amenity': 'place_of_worship', 'religion': 'christian'},
        ),
        dict(
            #   1417 Oratoire
            item = 8100,
            id = 10003,
            level = 3,
            title = T_('Place of worship not integrated'),
            select = {'nature': 'Culte chrétien', 'nature_detaillee': 'Oratoire'},
            tags = {'amenity': 'place_of_worship'},
            generate_tags = {'historic': 'wayside_shrine', 'amenity': 'place_of_worship', 'religion': 'christian', 'denomination': 'catholic'},
        ),
        dict(
            #   2255 Temple protestant
            item = 8100,
            id = 10004,
            level = 3,
            title = T_('Place of worship not integrated'),
            select = {'nature': 'Culte chrétien', 'nature_detaillee': 'Temple protestant'},
            tags = {'amenity': 'place_of_worship'},
            generate_tags = {'amenity': 'place_of_worship', 'religion': 'christian', 'denomination': 'protestant'},
        ),
        dict(
            #     64 Eglise orthodoxe
            item = 8100,
            id = 10005,
            level = 3,
            title = T_('Place of worship not integrated'),
            select = {'nature': 'Culte chrétien', 'nature_detaillee': 'Eglise orthodoxe'},
            tags = {'amenity': 'place_of_worship'},
            generate_tags = {'amenity': 'place_of_worship', 'religion': 'christian', 'denomination': 'orthodox'},
        ),
            #     46 Enclos paroissial
            #     42 Eglise simultanée
        # 54455 Enseignement primaire
        # 53718 Espace public
        # 38865 Mairie
        dict(
            item = 8110,
            id = 10100,
            level = 3,
            title = T_('Town hall not integrated'),
            select = {'nature': 'Mairie', 'nature_detaillee': [False, 'Mairie de commune associée ou déléguée', 'Mairie annexe', 'Hôtel de ville', 'Mairie d\'arrondissement']},
            tags = {'amenity': 'townhall'},
        ),
        # 27275 Monument
        dict(
            #  13600 Monument aux morts
            item = 8010,
            id = 10200,
            level = 3,
            title = T_('Memorial not integrated'),
            select = {'nature': 'Monument', 'nature_detaillee': 'Monument aux morts'},
            tags = {'historic': 'memorial'},
        ),
            #   7111
            #   5082 Stèle
            #   1304 Statue
            #    188 Mémorial

        # 23183 Station d'épuration
            # Other source
        # 19335 Station de pompage
        dict(
            item = 8500,
            id = 10400,
            level = 3,
            title = T_('Pumping station not integrated'),
            select = {'nature': 'Station de pompage'},
            tags = {'man_made': 'pumping_station'},
        ),
        # 14556 Poste
        # 13338 Zone industrielle
        # 13277 Autre équipement sportif
        # 12908 Aire de détente
        #  9952 Salle de spectacle ou conférence
        #  9025 Camping
        #  8283 Divers industriel
        #  8097 Maison de retraite
        #  7939 Complexe sportif couvert
        #  7889 Construction
        #  7383 Autre établissement d'enseignement
        #  7309 Collège
        #  7093 Point de vue
        dict(
            #   3971
            #    590 Belvédère
            item = 8450,
            id = 10500,
            level = 3,
            title = T_('Viewpoint not integrated'),
            select = {'nature': 'Point de vue', 'nature_detaillee': [False, 'Belvédère']},
            tags = {'tourism': 'viewpoint'},
        ),
        dict(
            #   2303 Table d'orientation
            item = 8450,
            id = 10501,
            level = 3,
            title = T_('Toposcope not integrated'),
            select = {'nature': 'Point de vue', 'nature_detaillee': 'Table d\'orientation'},
            tags = {'tourism': 'viewpoint', 'information': 'map', 'map_type': 'toposcope'},
        ),
            #    229 Observatoire ornithologique
        #  6683 Stade
        #  6590 Caserne de pompiers
        dict(
            item = 8520,
            id = 10600,
            level = 3,
            title = T_('Fire station not integrated'),
            select = {'nature': 'Caserne de pompiers'},
            tags = {'amenity': 'fire_station'},
        ),
        #  6474 Centre équestre
        #  6142 Tombeau
        #  5836 Usine
        #  5471 Déchèterie
        #  5051 Lycée
        #  4448 Carrière
        #  4385 Hébergement de loisirs
        #  4060 Mégalithe
        dict(
            #   1778 Menhir
            item = 8010,
            id = 10700,
            level = 3,
            title = T_('Menhir not integrated'),
            select = {'nature': 'Mégalithe', 'nature_detaillee': 'Menhir'},
            tags = {'historic': 'archaeological_site', 'archaeological_site': 'megalith', 'megalith_type': 'menhir'},
        ),
        dict(
            #   1601 Dolmen
            item = 8010,
            id = 10701,
            level = 3,
            title = T_('Dolmen not integrated'),
            select = {'nature': 'Mégalithe', 'nature_detaillee': 'Dolmen'},
            tags = {'historic': 'archaeological_site', 'archaeological_site': 'megalith', 'megalith_type': 'dolmen'},
        ),
        dict(
            #    377 Tumulus
            item = 8010,
            id = 10702,
            level = 3,
            title = T_('Tumulus not integrated'),
            select = {'nature': 'Mégalithe', 'nature_detaillee': 'Tumulus'},
            tags = {'historic': 'archaeological_site', 'archaeological_site': 'tumulus'},
        ),
        dict(
            #    188 Allée couverte
            item = 8010,
            id = 10703,
            level = 3,
            title = T_('Passage grave not integrated'),
            select = {'nature': 'Mégalithe', 'nature_detaillee': 'Allée couverte'},
            tags = {'historic': 'archaeological_site', 'archaeological_site': 'megalith', 'megalith_type': 'passage_grave'},
        ),
            #     61 Cairn
            #     55 Cromlech
        #  4037 Office de tourisme
        #  3945 Structure d'accueil pour personnes handicapées
        #  3708 Gendarmerie
        #  3682 Musée
        #  3554 Ouvrage militaire
        #  3409 Enseignement supérieur
        #  3327 Aquaculture
        #  3179 Divers commercial
        #  2924 Piscine
        #  2900 Divers public ou administratif
        #  2676 Hôpital
        #  2553 Borne frontière
        #  2446 Centre de documentation
        #  2432 Centrale électrique
        #  2304 Etablissement hospitalier
        #  2176 Habitation troglodytique
        #  2088 Site d'escalade
        #  2086 Siège d'EPCI
        #  1923 Vestige archéologique
        #  1868 Université
        #  1710 Autre service déconcentré de l'Etat
        #  1696 Parc de loisirs
        #  1679 Baignade surveillée
        #  1676 Maison forestière
        #  1598 Abri de montagne
        #  1486 Ecomusée
        #  1420 Elevage
        #  1255 Aire d'accueil des gens du voyage
        #  1239 Haras
        #  1218 Sports nautiques
        #  1162 Sports mécaniques
        #  1105 Marché
        #  1099 Mine
        #  1076 Site de vol libre
        #   841 Police
        #   828 Sports en eaux vives
        #   817 Palais de justice
        #   808 Enceinte militaire
        #   806 Refuge
        #   757 Culte musulman
        #   737 Golf
        #   721 Marais salant
        #   619 Usine de production d'eau potable
        #   575 Science
        #   541 Etablissement extraterritorial
        #   493 Stand de tir
        #   474 Départ de ski de fond
        #   447 Sentier de découverte
        #   440 Capitainerie
        #   401 Culte divers
        #   355 Caserne
        #   341 Divers agricole
        #   340 Salle de danse ou de jeux
        #   328 Parc zoologique
        #   298 Culte israélite
        #   256 Hippodrome
        #   256 Administration centrale de l'Etat
        #   245 Sous-préfecture
        #   244 Borne
        #   212 Etablissement pénitentiaire
        #   204 Parc des expositions
        #   198 Maison du parc
        #   174 Hôtel de département
        #   151 Préfecture
        #   149 Patinoire
        #   141 Etablissement thermal
        #    98 Champ de tir
        #    77 Surveillance maritime
        #    57 Camp militaire non clos
        #    31 Hôtel de région
        #    18 Préfecture de région
        ]

        for r in maping:
            self.classFactory(SubAnalyser_Merge_POI_FR, r['id'], r['item'], r['id'], r['level'], r['title'], r['select'], r['tags'], r.get('generate_tags', r['tags']), r.get('height', True))


class SubAnalyser_Merge_POI_FR(SubAnalyser_Merge_Dynamic):
    def __init__(self, config, error_file, logger, item, id, level, title, select, tags, generate_tags, height = True):
        SubAnalyser_Merge_Dynamic.__init__(self, config, error_file, logger)
        self.def_class_missing_official(item = item, id = id, level = level, tags = ['merge', 'fix:survey', 'fix:picture'], title = title)

        select.update({'etat_de_l_objet': 'En service'})
        self.init(
            "https://ign.fr",
            "IGN-Zone d'activité ou d'intérêt",
            GPKG(SourceIGN(attribution = "IGN", gzip = True,
                    fileUrl = "http://files.opendatarchives.fr/professionnels.ign.fr/bdtopo/latest/geopackage/zone_d_activite_ou_d_interet.gpkg.gz")),
            LoadGeomCentroid(
                select = select),
            Conflate(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = tags),
                conflationDistance = 100,
                mapping = Mapping(
                    static1 = generate_tags,
                    static2 = {"source": self.source},
                    mapping2 = {
                        "name": lambda fields: fields["toponyme"] if fields["statut_du_toponyme"] == "Validé" else None},
                    text = lambda tags, fields: {'en': ', '.join(filter(lambda f: f not in (None, 'None'), [fields["nature"], fields["nature_detaillee"], fields["toponyme"]]))} )))
