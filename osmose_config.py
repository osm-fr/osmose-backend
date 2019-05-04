#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
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

# langue : http://fr.wikipedia.org/wiki/Liste_des_codes_ISO_639-1
# PAYS   : http://fr.wikipedia.org/wiki/ISO_3166-1

import os
import re
from collections import OrderedDict
import modules.config

###########################################################################

GEOFABRIK = u"http://download.geofabrik.de/"
OSMFR = u"http://download.openstreetmap.fr/extracts/"

class template_config:

    clean_at_end   = True

    updt_url       = modules.config.url_frontend_update
    dir_work       = modules.config.dir_work
    dir_tmp        = modules.config.dir_tmp
    dir_cache      = modules.config.dir_cache
    dir_scripts    = modules.config.dir_osmose
    bin_osmosis    = modules.config.bin_osmosis
    osmosis_pre_scripts = [
        dir_scripts + "/osmosis/pgsnapshot_schema_0.6.sql",
#       dir_scripts + "/osmosis/osmosis-0.47/script/pgsnapshot_schema_0.6_bbox.sql",
        dir_scripts + "/osmosis/osmosis-0.47/script/pgsnapshot_schema_0.6_linestring.sql",
        dir_scripts + "/osmosis/CreateMetainfo.sql",
    ]
    osmosis_import_scripts = [
        dir_scripts + "/osmosis/ImportDatabase.sql",
    ]
    osmosis_post_scripts = [
        dir_scripts + "/osmosis/CreateTagsIndex.sql",
        dir_scripts + "/osmosis/CreateFunctions.sql",
    ]
    osmosis_change_init_post_scripts = [  # Scripts to run on database initialisation
        dir_scripts + "/osmosis/pgsimple_schema_0.6_action_drop.sql",
        dir_scripts + "/osmosis/osmosis-0.47/script/pgsnapshot_schema_0.6_action.sql",
    ]
    osmosis_change_post_scripts = [  # Scripts to run each time the database is updated
        dir_scripts + "/osmosis/CreateTouched.sql",
    ]
    osmosis_resume_init_post_scripts = [  # Scripts to run on database initialisation
        dir_scripts + "/osmosis/pgsimple_schema_0.6_action_drop.sql",
        dir_scripts + "/osmosis/osmosis-0.47/script/pgsnapshot_schema_0.6_action.sql",
    ]
    osmosis_resume_post_scripts = [  # Scripts to run each time the database is updated
        dir_scripts + "/osmosis/ActionFromTimestamp.sql",
        dir_scripts + "/osmosis/CreateTouched.sql",
    ]
    dir_results    = modules.config.dir_results
    dir_extracts   = modules.config.dir_extracts
    dir_diffs      = modules.config.dir_diffs

    db_base     = "osmose"
    db_user     = "osmose"
    db_password = "-osmose-"
    db_host     = os.environ.get('DB_HOST', None) # Use socket by default
    db_schema   = None
    db_schema_path = None
    db_persistent = False

    def __init__(self, country, polygon_id=None, analyser_options=None, download_repo=GEOFABRIK):
        config[country] = self
        self.country          = country
        self.polygon_id       = polygon_id # ID of a relation for the country boundary
        self.download         = {}
        self.download_repo    = download_repo
        self.analyser         = OrderedDict()
        if analyser_options:
            self.analyser_options = analyser_options
        else:
            self.analyser_options = {}

        self.sql_post_scripts = []  # Scripts to run everytime, just before launching analysers
        self.db_extension_check = []

    def init(self):
        if "diff" in self.download:
            self.download["diff_path"] = os.path.join(self.dir_diffs, self.country)

        if "url" in self.download and not "dst" in self.download:
            ext = os.path.splitext(self.download["url"])[1]
            for e in [".osm.pbf", ".osm.bz2", ".osm.gz"]:
                if self.download["url"].endswith(e):
                    ext = e
                    break

            self.download["dst"] = self.dir_extracts + "/" + self.country + ext

config = OrderedDict()

###########################################################################

world = template_config("world", analyser_options={"project": "openstreetmap"})
world.analyser["osmbin_open_relations"] = "xxx"
world.db_base = None

###########################################################################

class default_simple(template_config):
    def __init__(self, country, polygon_id=None, analyser_options=None, download_url=None, download_repo=None):

        template_config.__init__(self, country, polygon_id, analyser_options, download_repo)
        self.db_extension_check += ["fuzzystrmatch", "unaccent"]
        self.download = {
            "url": download_url
        }
        self.analyser["sax"] = "xxx"
        self.analyser["osmosis_roundabout_reverse"] = "xxx"
        self.analyser["osmosis_roundabout_level"] = "xxx"
        self.analyser["osmosis_soundex"] = "xxx"
        self.analyser["osmosis_roundabout"] = "xxx"
        self.analyser["osmosis_boundary_hole"] = "xxx"
        self.analyser["osmosis_building_overlaps"] = "xxx"
        self.analyser["osmosis_polygon"] = "xxx"
        self.analyser["osmosis_highway_vs_building"] = "xxx"
        self.analyser["osmosis_orphan_nodes_cluster"] = "xxx"
        self.analyser["osmosis_powerline"] = "xxx"
        self.analyser["osmosis_double_tagging"] = "xxx"
        self.analyser["osmosis_relation_associatedStreet"] = "xxx"
        self.analyser["osmosis_highway_link"] = "xxx"
        self.analyser["osmosis_highway_broken_level_continuity"] = "xxx"
        self.analyser["osmosis_relation_large"] = "xxx"
        self.analyser["osmosis_polygon_overlaps"] = "xxx"
        self.analyser["osmosis_useless"] = "xxx"
        self.analyser["osmosis_relation_multipolygon"] = "xxx"
        self.analyser["osmosis_boundary_intersect"] = "xxx"
        self.analyser["osmosis_node_like_way"] = "xxx"
        self.analyser["osmosis_boundary_administrative"] = "xxx"
        self.analyser["osmosis_tag_typo"] = "xxx"
        self.analyser["osmosis_cycleway_track"] = "xxx"
        self.analyser["osmosis_highway_features"] = "xxx"
        self.analyser["osmosis_building_shapes"] = "xxx"
        self.analyser["osmosis_highway_deadend"] = "xxx"
        self.analyser["osmosis_boundary_relation"] = "xxx"
        self.analyser["osmosis_highway_traffic_signals"] = "xxx"
        self.analyser["osmosis_relation_restriction"] = "xxx"
        self.analyser["osmosis_highway_tunnel_bridge"] = "xxx"
        self.analyser["osmosis_waterway"] = "xxx"
        self.analyser["osmosis_duplicated_geotag"] = "xxx"
        self.analyser["osmosis_highway_noexit"] = "xxx"
        self.analyser["osmosis_parking_highway"] = "xxx"
        self.analyser["osmosis_highway_bad_intersection"] = "xxx"
        self.analyser["osmosis_water"] = "xxx"
        self.analyser["osmosis_relation_public_transport"] = "xxx"
        self.analyser["osmosis_highway_turn_lanes"] = "xxx"
        self.analyser["osmosis_highway_almost_junction"] = "xxx"
        self.analyser["osmosis_highway_without_ref"] = "xxx"
        self.analyser["osmosis_building_3nodes"] = "xxx"
        self.analyser["osmosis_wikipedia"] = "xxx"
        self.analyser["osmosis_highway_name_close"] = "xxx"
        self.analyser["osmosis_relation_route_access"] = "xxx"
        self.analyser["osmosis_highway_floating_islands"] = "xxx"
        self.analyser["merge_traffic_signs"] = "xxx"
        self.analyser["merge_street_objects"] = "xxx"
        self.analyser["osmosis_relation_enforcement"] = "xxx"

class default_country_simple(default_simple):
    def __init__(self, part, country, polygon_id=None, analyser_options=None,
                 download_repo=GEOFABRIK, download_country=None):
        part = part + '/' if part != None else ''

        if not download_country:
            download_country = country
        country = country.replace("-", "_").replace("/", "_")
        analyser_options = dict({"project": "openstreetmap"}, **analyser_options)
        default_simple.__init__(self, country, polygon_id, analyser_options, download_repo=download_repo)
        self.download.update({
            "url": self.download_repo + part + download_country + "-latest.osm.pbf",
            "poly": self.download_repo + part + download_country + ".poly",
        })
        if download_repo == GEOFABRIK:
            self.download["diff"] = self.download_repo + part + download_country + "-updates/"
            self.download["state.txt"] = self.download["diff"] + "state.txt"
        if download_repo == OSMFR:
            self.download["poly"] = self.download["poly"].replace("/extracts/", "/polygons/")
            self.download["diff"] = self.download_repo + "../replication/" + part + download_country + "/minute/"
            self.download["state.txt"] = self.download_repo + part + download_country + ".state.txt"

class default_country(default_country_simple):
    def __init__(self, part, country, polygon_id=None, analyser_options=None,
                 download_repo=GEOFABRIK, download_country=None):

        default_country_simple.__init__(self, part, country, polygon_id, analyser_options,
                                        download_repo, download_country)
        self.analyser["osmosis_highway_cul-de-sac_level"] = "xxx"
        self.analyser["osmosis_way_approximate"] = "xxx"
        self.analyser["osmosis_highway_area_access"] = "xxx"

def gen_country(area, path_base=None,
        country_base=None, country_code=None, download_repo=GEOFABRIK, include=[], exclude=[], **analyser_options_default):
    area_default = area
    path_base_default = path_base
    country_base_default = country_base
    country_base_default = country_base_default or path_base
    country_code_default = country_code
    download_repo_default = download_repo
    include_default = include
    exclude_default = exclude

    def init(self, path, polygon_id=None, country_code=country_code_default,
            area=area_default, country=None, path_base=path_base_default, country_base=country_base_default, download_repo=download_repo_default, include=[], exclude=[], **analyser_options):
        ao = {'country': country_code}
        ao.update(analyser_options_default)
        ao.update(analyser_options)

        path = path if isinstance(path, list) else [path]
        country = (country or path[-1]).replace('-', '_')
        download_country = '/'.join(filter(lambda a: a != None, [path_base] + path))

        default_country.__init__(self, area, country_base + '_' + country, polygon_id, ao, download_repo, download_country)

        for analyser in exclude_default + exclude:
            del(self.analyser[analyser])

        for analyser in include_default + include:
            self.analyser[analyser] = 'xxx'

    class gen(default_country):
        __init__ = init

    return gen

france_departement = gen_country('europe', 'france', download_repo=OSMFR, language='fr', proj=2154, municipality_ref='ref:INSEE',
    phone_code='33', phone_len=9, phone_format=r'^([+]%s([- ./]*[0-9]){8}[0-9])|[0-9]{4}|[0-9]{6}$', phone_international='00', phone_local_prefix='0',
    include=[
    'osmosis_building_geodesie_FR',
    'osmosis_natural_swimming-pool',
    'osmosis_fantoir',
    'osmosis_highway_motorway',
    'osmosis_highway_zone',
], **{'addr:city-admin_level': '8,9'})

france_departement("alsace/bas_rhin", 7415, "FR-67")
france_departement("alsace/haut_rhin", 7403, "FR-68")

include_aquitaine = [
    # Aquitiane
    'merge_tourism_FR_aquitaine_camp_caravan',
    'merge_tourism_FR_aquitaine_museum',
    'merge_tourism_FR_aquitaine_information',
    'merge_sport_FR_aquitaine_equestrian',
    'merge_library_FR_aquitaine',
    'merge_winery_FR_aquitaine',
    'merge_restaurant_FR_aquitaine',
]
france_departement("aquitaine/dordogne", 7375, "FR-24", include=include_aquitaine)
france_departement("aquitaine/gironde", 7405, "FR-33", include=include_aquitaine + [
    # Bordeaux
    'merge_recycling_FR_bm',
    'merge_parking_FR_bm',
    'merge_bicycle_parking_FR_bordeaux',
    'merge_bicycle_rental_FR_bm',
    'merge_public_equipment_FR_bordeaux_toilets',
    'merge_public_transport_FR_tbm',
    'merge_street_number_bordeaux',
    # Gironde
    'merge_public_transport_FR_transgironde',
])
france_departement("aquitaine/landes", 7376, "FR-40", include=include_aquitaine)
france_departement("aquitaine/lot_et_garonne", 1284995, "FR-47", include=include_aquitaine)
france_departement("aquitaine/pyrenees_atlantiques", 7450, "FR-64", include=include_aquitaine + [
    # Pau
    'merge_recycling_FR_capp_glass',
    'merge_recycling_FR_capp_clothes',
    'merge_parking_FR_capp',
    'merge_bicycle_parking_FR_capp',
])

france_departement("auvergne/allier", 1450201, "FR-03")
france_departement("auvergne/cantal", 7381, "FR-15")
france_departement("auvergne/haute_loire", 7452, "FR-43")
france_departement("auvergne/puy_de_dome", 7406, "FR-63")

france_departement("basse_normandie/calvados", 7453, "FR-14")
france_departement("basse_normandie/manche", 7404, "FR-50")
france_departement("basse_normandie/orne", 7419, "FR-61")

france_departement("bourgogne/cote_d_or", 7424, "FR-21")
france_departement("bourgogne/nievre", 7448, "FR-58")
france_departement("bourgogne/saone_et_loire", 7397, "FR-71", include=[
    # Saône-et-Loire
    'merge_restaurant_FR_cg71',
])
france_departement("bourgogne/yonne", 7392, "FR-89")

france_departement("bretagne/cotes_d_armor", 7398, "FR-22")
france_departement("bretagne/ille_et_vilaine", 7465, "FR-35", include=[
    # Rennes
    'merge_public_equipment_FR_rennes_toilets',
    'merge_public_transport_FR_star',
    'merge_street_number_rennes',
])
france_departement("bretagne/finistere", 102430, "FR-29")
france_departement("bretagne/morbihan", 7447, "FR-56")

france_departement("centre/cher", 7456, "FR-18")
france_departement("centre/eure_et_loir", 7374, "FR-28")
france_departement("centre/indre", 7417, "FR-36")
france_departement("centre/indre_et_loire", 7408, "FR-37")
france_departement("centre/loir_et_cher", 7399, "FR-41")
france_departement("centre/loiret", 7440, "FR-45")

france_departement("champagne_ardenne/ardennes", 7395, "FR-08")
france_departement("champagne_ardenne/aube", 7441, "FR-10")
france_departement("champagne_ardenne/marne", 7379, "FR-51")
france_departement("champagne_ardenne/haute_marne", 7396, "FR-52")

france_departement("corse/corse_du_sud", 76932, "FR-2A")
france_departement("corse/haute_corse", 76931, "FR-2B")

france_departement("franche_comte/doubs", 7462, "FR-25")
france_departement("franche_comte/jura", 7460, "FR-39")
france_departement("franche_comte/haute_saone", 7423, "FR-70")
france_departement("franche_comte/territoire_de_belfort", 7410, "FR-90")

france_departement("haute_normandie/eure", 7435, "FR-27")
france_departement("haute_normandie/seine_maritime", 7426, "FR-76", include=[
    # Le Havre
    'merge_public_equipment_FR_lehavre_toilets',
])

include_ile_de_france = [
    # Île-de-france
    'merge_public_transport_FR_ratp',
    'merge_public_transport_FR_stif',
    'merge_bicycle_rental_FR_IDF',
    'merge_parking_FR_IDF',
]
france_departement("ile_de_france/paris", 71525, "FR-75", include=include_ile_de_france + [
    # Paris
    'merge_bicycle_parking_FR_paris',
])
france_departement("ile_de_france/hauts_de_seine", 7449, "FR-92", include=include_ile_de_france + [
    # Hauts-de-Seine
    'merge_restriction_FR_92',
])
france_departement("ile_de_france/seine_saint_denis", 7389, "FR-93", include=include_ile_de_france)
france_departement("ile_de_france/val_de_marne", 7458, "FR-94", include=include_ile_de_france)
france_departement("ile_de_france/essonne", 7401, "FR-91", include=include_ile_de_france)
france_departement("ile_de_france/seine_et_marne", 7383, "FR-77", include=include_ile_de_france)
france_departement("ile_de_france/val_d_oise", 7433, "FR-95", include=include_ile_de_france)
france_departement("ile_de_france/yvelines", 7457, "FR-78", include=include_ile_de_france)

france_departement("languedoc_roussillon/aude", 7446, "FR-11")
france_departement("languedoc_roussillon/gard", 7461, "FR-30")
france_departement("languedoc_roussillon/herault", 7429, "FR-34", include=[
    # Montpellier
    #'merge_public_equipment_FR_montpellier_toilets',
    'merge_street_number_montpellier',
])
france_departement("languedoc_roussillon/lozere", 7421, "FR-48")
france_departement("languedoc_roussillon/pyrenees_orientales", 7466, "FR-66")

france_departement("limousin/correze", 7464, "FR-19")
france_departement("limousin/creuse", 7459, "FR-23")
france_departement("limousin/haute_vienne", 7418, "FR-87")

france_departement("lorraine/meurthe_et_moselle", 51856, "FR-54", include=[
    # Nancy
    'merge_public_transport_FR_stan',
])
france_departement("lorraine/meuse", 7382, "FR-55")
france_departement("lorraine/moselle", 51854, "FR-57")
france_departement("lorraine/vosges", 7384, "FR-88")

france_departement("midi_pyrenees/ariege", 7439, "FR-09")
france_departement("midi_pyrenees/aveyron", 7451, "FR-12")
france_departement("midi_pyrenees/haute_garonne", 7413, "FR-31", include=[
    # Toulouse
    'merge_public_equipment_FR_toulouse_toilets',
    'merge_street_number_toulouse',
])
france_departement("midi_pyrenees/gers", 7422, "FR-32")
france_departement("midi_pyrenees/lot", 7454, "FR-46")
france_departement("midi_pyrenees/hautes_pyrenees", 7467, "FR-65")
france_departement("midi_pyrenees/tarn", 7442, "FR-81")
france_departement("midi_pyrenees/tarn_et_garonne", 7388, "FR-82")

france_departement("nord_pas_de_calais/nord", 7400, "FR-59")
france_departement("nord_pas_de_calais/pas_de_calais", 7394, "FR-62")

france_departement("pays_de_la_loire/loire_atlantique", 7432, "FR-44", include=[
    # Nantes
    'merge_recycling_FR_nm_glass',
    'merge_public_equipment_FR_nantes_toilets',
    'merge_street_number_nantes',
])
france_departement("pays_de_la_loire/maine_et_loire", 7409, "FR-49", include=[
    # Angers
    'merge_public_equipment_FR_angers_toilets',
])
france_departement("pays_de_la_loire/mayenne", 7438, "FR-53")
france_departement("pays_de_la_loire/sarthe", 7443, "FR-72")
france_departement("pays_de_la_loire/vendee", 7402, "FR-85")

france_departement("picardie/aisne", 7411, "FR-02")
france_departement("picardie/oise", 7427, "FR-60")
france_departement("picardie/somme", 7463, "FR-80")

france_departement("poitou_charentes/charente", 7428, "FR-16")
france_departement("poitou_charentes/charente_maritime", 7431, "FR-17")
france_departement("poitou_charentes/deux_sevres", 7455, "FR-79")
france_departement("poitou_charentes/vienne", 7377, "FR-86")

france_departement("provence_alpes_cote_d_azur/alpes_de_haute_provence", 7380, "FR-04")
france_departement("provence_alpes_cote_d_azur/hautes_alpes", 7436, "FR-05")
france_departement("provence_alpes_cote_d_azur/alpes_maritimes", 7385, "FR-06")
france_departement("provence_alpes_cote_d_azur/bouches_du_rhone", 7393, "FR-13", include=[
    # Arles
    'merge_street_number_arles',
])
france_departement("provence_alpes_cote_d_azur/var", 7390, "FR-83")
france_departement("provence_alpes_cote_d_azur/vaucluse", 7445, "FR-84")

france_departement("rhone_alpes/ain", 7387, "FR-01")
france_departement("rhone_alpes/ardeche", 7430, "FR-07")
france_departement("rhone_alpes/drome", 7434, "FR-26")
france_departement("rhone_alpes/isere", 7437, "FR-38")
france_departement("rhone_alpes/loire", 7420, "FR-42")
france_departement("rhone_alpes/rhone", 7378, "FR-69", include=[
    # Lyon
    'merge_public_equipment_FR_lyon_toilets',
    'merge_street_number_lyon',
])
france_departement("rhone_alpes/savoie", 7425, "FR-73")
france_departement("rhone_alpes/haute_savoie", 7407, "FR-74")


france_departement_dom = gen_country('europe', 'france', language='fr', municipality_ref='ref:INSEE',
    phone_len=9, phone_format=r'^([+]%s([- ./]*[0-9]){8}[0-9])|[0-9]{4}|[0-9]{6}$', phone_international='00', phone_local_prefix='0',
    include=[
    'osmosis_building_geodesie_FR',
    'osmosis_natural_swimming-pool',
    'osmosis_fantoir',
    'osmosis_highway_motorway',
    'osmosis_highway_zone',

    'merge_heritage_FR_merimee',
    'merge_poste_FR',
    'merge_school_FR',
    'merge_college_FR',
    'merge_service_public_FR',
    'merge_pitch_FR',
    'merge_police_FR_gn',
    'merge_police_FR_pn',
    'merge_healthcare_FR_finess',
    'merge_postal_code_FR',
    'merge_post_box_FR',
], **{'addr:city-admin_level': '8,9'})

france_departement_dom("guadeloupe", 1401835, "FR-GP", proj=32620, phone_code="590")
france_departement_dom("guyane", 1260551, "FR-GF", proj=2972, phone_code="594")
france_departement_dom("martinique", 1891495, "FR-MQ", proj=32620, phone_code="596")
france_departement_dom("mayotte", 1259885, "FR-YT", proj=32738, phone_code="262")
france_departement_dom("reunion", 1785276, "FR-RE", proj=2975, phone_code="262")

france_com = gen_country(None, country_base='france', download_repo=OSMFR, language='fr', municipality_ref='ref:INSEE',
    phone_len=9, phone_format=r'^([+]%s([- ./]*[0-9]){8}[0-9])|[0-9]{4}|[0-9]{6}$', phone_international='00', phone_local_prefix='0',
    include=[
    'merge_college_FR',
    'merge_service_public_FR',
    'merge_pitch_FR',
    'merge_police_FR_gn',
    'merge_police_FR_pn',
    'merge_postal_code_FR',
], **{'addr:city-admin_level': '8,9'})

france_com(["central-america", "saint_barthelemy"], 537967, "FR-BL", proj=2969, phone_code="590", country="saintbarthelemy")
france_com(["central-america", "saint_martin"], 1891583, "FR-MF", proj=2969, phone_code="590", country="saintmartin")
france_com(["north-america", "saint_pierre_et_miquelon"], 233377, "FR-PM", proj=32621, phone_code="508", country="saintpierreetmiquelon")
france_com(["south-america", "wallis_et_futuna"], 290162, "FR-WF", proj=32701, phone_code="681", country="wallisetfutuna")
france_com(["south-america", "polynesie"], 3412620, "FR-PF", proj=32706, phone_code="689", phone_len=9)
france_com(["australia-oceania", "new-caledonia"], 3407643, "NC", download_repo=GEOFABRIK, proj=3163, country="nouvellecaledonie",
    phone_code="687", phone_len=6, phone_format=r"^[+]%s([- ./]*[0-9]){5}[0-9]$", phone_international='00')

default_country("merge", "france_taaf", 6063103, download_repo=OSMFR, analyser_options={"country": "TF", "language": "fr", "proj": 32738})

###########################################################################

france_local_db = template_config("france_local_db", 1403916, {"project": "openstreetmap", "country": "FR", "language": "fr", "proj": 2154})
france_local_db.db_persistent = True
france_local_db.db_base     = "osm"
france_local_db.db_user     = "osmose"
france_local_db.db_password = "clostAdtoi"
france_local_db.db_schema   = "osmosis"
france_local_db.db_schema_path = "\"$user\",osmosis,public"
france_local_db.sql_post_scripts += [
    france_local_db.dir_scripts + "/osmosis/CreateFunctions.sql",
    france_local_db.dir_scripts + "/osmosis/CreateMergeAnalyserCache.sql",
  ]

france_local_db.download["diff_path"] = "/data/work/osmosis/" # path to find state.txt

france_local_db.analyser["merge_heritage_FR_merimee"] = "xxx"
france_local_db.analyser["merge_poste_FR"] = "xxx"
france_local_db.analyser["merge_school_FR"] = "xxx"
france_local_db.analyser["merge_railway_level_crossing_FR"] = "xxx"
france_local_db.analyser["merge_railway_railstation_FR"] = "xxx"
france_local_db.analyser["merge_tmc_point_FR"] = "xxx"
france_local_db.analyser["merge_geodesie"] = "xxx"
france_local_db.analyser["merge_college_FR"] = "xxx"
france_local_db.analyser["merge_service_public_FR"] = "xxx"
france_local_db.analyser["merge_pitch_FR"] = "xxx"
france_local_db.analyser["merge_police_FR_gn"] = "xxx"
france_local_db.analyser["merge_police_FR_pn"] = "xxx"
france_local_db.analyser["merge_fuel_FR"] = "xxx"
france_local_db.analyser["merge_healthcare_FR_finess"] = "xxx"
france_local_db.analyser["merge_postal_code_FR"] = "xxx"
france_local_db.analyser["merge_geodesie_support_FR"] = "xxx"
france_local_db.analyser["merge_post_box_FR"] = "xxx"
#france_local_db.analyser["merge_power_generator_FR"] = "xxx" # Waiting for data source update, ETA 2019 1Q
france_local_db.analyser["merge_power_substation_FR"] = "xxx"
france_local_db.analyser["merge_power_tower_FR"] = "xxx"
france_local_db.analyser["merge_shop_FR"] = "xxx"
france_local_db.analyser["merge_restriction_motorway_FR"] = "xxx"
france_local_db.analyser["merge_power_substation_minor_FR"] = "xxx"

#########################################################################

default_country("europe", "albania", 53292, {"country": "AL", "language": "sq", "proj": 32634})
default_country("europe", "andorra", 9407, {"country": "AD", "language": "ca", "proj": 2154})
default_country("europe", "azores",  1629146, {"country": "PT", "language": "pt", "proj": 32627}, download_repo=GEOFABRIK)
default_country("europe", "belarus", 59065, {"country": "BY", "language": ["be", "ru"], "proj": 32635}, download_repo=GEOFABRIK)
default_country("europe", "bosnia-herzegovina", 2528142, {"country": "BA", "language": ["bs", "hr", "sr"], "proj": 32633}, download_repo=GEOFABRIK)
default_country("europe", "bulgaria", 186382, {"country": "BG", "language": "bg", "proj": 32635}, download_repo=GEOFABRIK)
default_country("europe", "croatia", 214885, {"country": "HR", "language": "hr", "proj": 32633}, download_repo=GEOFABRIK)
default_country("europe", "estonia", 79510, {"country": "EE", "language": "et", "proj": 32634}, download_repo=GEOFABRIK)
default_country("europe", "cyprus", 307787, {"country": "CY", "language": ["el", "tr", "en"], "driving_side": "left", "proj": 32636})
default_country("europe", "faroe-islands", 52939, {"country": "FO", "language": "fo", "proj": 2169})
default_country("europe", "greece",  192307, {"country": "GR", "language": "el","proj": 32635}, download_repo=GEOFABRIK)
default_country("europe", "guernesey", 270009, {"country": "GG", "language": "en", "driving_side": "left", "speed_limit_unit": "mph", "proj": 32630}, download_repo=OSMFR)
default_country("europe", "hungary", 21335, {"country": "HU", "language": "hu", "proj": 32633}, download_repo=GEOFABRIK)
default_country("europe", "ireland", 62273, {"country": "IE", "driving_side": "left", "language": ["en", "ga"], "proj": 32629}, download_repo=OSMFR)
default_country("europe", "isle-of-man", 62269, {"country": "IM", "language": "en", "driving_side": "left", "speed_limit_unit": "mph", "proj": 32630})
default_country("europe", "jersey", 367988, {"country": "JE", "language": "en", "driving_side": "left", "speed_limit_unit": "mph", "proj": 32630}, download_repo=OSMFR)
default_country("europe", "kosovo", 2088990, {"country": "XK", "language": ["sq", "sr-Latn"], "proj": 32634, "multilingual-style": "xk"})
default_country("europe", "liechtenstein", 1155955, {"country": "LI", "language": "de", "proj": 32632})
lithuania = default_country("europe", "lithuania", 72596, {"country": "LT", "language": "lt", "proj": 32635, "osmosis_way_approximate": {"highway": ("motorway", "trunk", "primary", "secondary", "tertiary")}}, download_repo=GEOFABRIK)
del(lithuania.analyser["osmosis_highway_cul-de-sac_level"]) # follow official highway classification
del(lithuania.analyser["osmosis_highway_broken_level_continuity"]) # follow official highway classification
default_country("europe", "latvia", 72594, {"country": "LV","language": "lv", "proj": 32634}, download_repo=GEOFABRIK)
default_country("europe", "luxembourg", 2171347, {"country": "LU", "language": "fr", "proj": 2169, "boundary_detail_level": 6})
default_country("europe", "malta", 365307, {"country": "MT", "language": "en", "driving_side": "left", "proj": 32633})
default_country("europe", "macedonia", 53293, {"country": "MK", "language": "sq", "proj": 32634})
default_country("europe", "moldova", 58974, {"country": "MD", "language": "ro", "proj": 32635}, download_repo=GEOFABRIK)
default_country("europe", "monaco", 1124039, {"country": "MC", "language": "fr", "proj": 2154, "phone_code": '377', "phone_len": 8, "phone_format": r'^[+]%s([- ./]*[469])([- ./]*[0-9]){6}[0-9]$', "phone_international": '00'}, download_repo=OSMFR)
default_country("europe", "montenegro", 53296, {"country": "ME", "proj": 32634})
default_country("europe", "portugal",  295480, {"country": "PT", "language": "pt", "proj": 32629}, download_repo=GEOFABRIK)
default_country("europe", "romania", 90689, {"country": "RO", "language": "ro", "proj": 31700})
default_country("europe", "serbia", 1741311, {"country": "RS", "language": "sr", "proj": 32634}, download_repo=GEOFABRIK)
default_country("europe", "slovenia", 218657, {"country": "SI", "language": ["sl", "hu", "it"], "proj": 32633}, download_repo=GEOFABRIK)
default_country("europe", "sweden", 52822, {"country": "SE", "language": "sv", "proj": 32633})
default_country("europe", "switzerland", 51701, {"country": "CH", "proj": 2056, "language": ["de", "fr", "it", "rm"], "municipality_ref": ["swisstopo:BFS_NUMMER", "swisstopo:BEZIRKSNUM"], 'phone_code': '41', 'phone_local_prefix': '0', 'phone_len': 9, 'phone_international': '00'})
default_country("europe", "turkey", 174737, {"country": "TR", "language": "tr", "proj": 32636}, download_repo=GEOFABRIK)
default_country("europe", "united_kingdom_akrotiri_and_dhekelia", 3263728, {"country": "GB", "language": ["en", "he"], "driving_side": "left", "proj": 32636}, download_country="cyprus")  # British Sovereign Base in Cyprus
default_country("europe", "united_kingdom_gibraltar", 1278736, {"country": "GI", "language": "en", "proj": 32630}, download_repo=OSMFR, download_country="gibraltar")
default_country("europe", "united_kingdom_northern_ireland", 156393, {"country": "GB-NIR", "language": "en", "driving_side": "left", "speed_limit_unit": "mph", "language": "en", "proj": 32629}, download_repo=OSMFR, download_country="united_kingdom/northern_ireland")
default_country("europe", "united_kingdom_wales", 58437, {"country": "GB-WLS", "language": ["en", "cy"], "driving_side": "left", "speed_limit_unit": "mph", "proj": 32630}, download_repo=GEOFABRIK, download_country="great-britain/wales")
default_country("europe", "united_kingdom_scotland", 58446, {"country": "GB-SCT", "language": "en", "driving_side": "left", "speed_limit_unit": "mph", "proj": 32630}, download_repo=GEOFABRIK, download_country="great-britain/scotland")

iceland = default_country("europe","iceland", 299133, {"country": "IS", "language": "is", "proj": 32627}) # 299133
iceland.download["url"] = ""

default_country("europe", "finland", 54224, {"country": "FI", "language": ["fi", "sv"],  "proj": 32635},download_repo=GEOFABRIK)
default_country("europe", "denmark",  50046, {"country": "DK", "language": "da","proj": 32632, "phone_code": '45', "phone_len": 8, "phone_international": '00'}, download_repo=GEOFABRIK)

#########################################################################

be_part = gen_country('europe', 'belgium', download_repo=OSMFR, proj=32631, municipality_ref='ref:INS',
    phone_code='32', phone_len=[8, 9], phone_len_short=4, phone_international='00', phone_local_prefix='0')

be_part('brussels_capital_region', 54094, 'BE-BRU', language=['fr', 'nl'], **{'multilingual-style': 'be'})
be_part('flanders', 53134, 'BE-VLG', language='nl')
be_part('wallonia_french_community', 2620920, 'BE-WAL', language='fr')
be_part('wallonia_german_community', 2425209, 'BE-WAL', language='de')

#########################################################################

ua_oblasts = gen_country('europe', 'ukraine', download_repo=OSMFR, language='uk', proj=32636)

ua_oblasts('cherkasy_oblast', 91278, 'UA-71')
ua_oblasts('chernihiv_oblast', 71249, 'UA-74')
ua_oblasts('chernivtsi_oblast', 72526, 'UA-77')
ua_oblasts('dnipropetrovsk_oblast', 101746, 'UA-12')
ua_oblasts('donetsk_oblast', 71973, 'UA-14')
ua_oblasts('ivano-frankivsk_oblast', 72488, 'UA-26')
ua_oblasts('kharkiv_oblast', 71254, 'UA-63')
ua_oblasts('kherson_oblast', 71022, 'UA-65')
ua_oblasts('khmelnytskyi_oblast', 90742, 'UA-68')
ua_oblasts('kiev_oblast', 71248, 'UA-32')
ua_oblasts('kiev', 421866, 'UA-30')
ua_oblasts('kirovohrad_oblast', 101859, 'UA-35')
ua_oblasts('luhansk_oblast', 71971, 'UA-09')
ua_oblasts('lviv_oblast', 72380, 'UA-46')
ua_oblasts('mykolaiv_oblast', 72635, 'UA-48')
ua_oblasts('odessa_oblast', 72634, 'UA-51')
ua_oblasts('poltava_oblast', 91294, 'UA-53')
ua_oblasts('rivne_oblast', 71236, 'UA-56')
ua_oblasts('sumy_oblast', 71250, 'UA-59')
ua_oblasts('ternopil_oblast', 72525, 'UA-61')
ua_oblasts('vinnytsia_oblast', 90726, 'UA-05')
ua_oblasts('volyn_oblast', 71064, 'UA-07')
ua_oblasts('zakarpattia_oblast', 72489, 'UA-21')
ua_oblasts('zaporizhia_oblast', 71980, 'UA-23')
ua_oblasts('zhytomyr_oblast', 71245, 'UA-18')


#########################################################################

no_county = gen_country('europe', 'norway', download_repo=OSMFR, language='no', proj=32632)

no_county('nordland', 408105, 'NO-18')
no_county('troms', 407717, 'NO-19')
no_county('finnmark', 406389, 'NO-20')
no_county('troendelag', 406567, 'NO-23')
no_county('moere_og_romsdal', 406868, 'NO-15')
no_county('sogn_og_fjordane', 407787, 'NO-14')
no_county('hordaland', 404144, 'NO-12')
no_county('rogaland', 405836, 'NO-11')
no_county('aust-agder', 406015, 'NO-09')
no_county('vest-agder', 405929, 'NO-10')
no_county('oslo', 406091, 'NO-03')
no_county('akershus', 406106, 'NO-02')
no_county('oestfold', 406060, 'NO-01')
no_county('vestfold', 404589, 'NO-07')
no_county('telemark', 405156, 'NO-08')
no_county('buskerud', 412297, 'NO-06')
no_county('oppland', 412377, 'NO-05')
no_county('hedmark', 412436, 'NO-04')

no_county('svalbard', 1337397, 'SJ')
no_county('jan_mayen', 1337126, 'SJ')

#########################################################################

default_country_simple("", "antarctica",  None, {"proj": 3031}, download_repo=GEOFABRIK)

#########################################################################

default_country("north-america", "greenland", 2184073, {"country": "GL", "language": "kl", "proj": 3184})
mexico = default_country("north-america", "mexico", 114686, {"country": "MX", "language": "es", "proj": 32614}, download_repo=GEOFABRIK)
del(mexico.analyser["osmosis_highway_name_close"]) # Complicated Street Numbering
default_country("north-america", "united_kingdom_bermuda", 1993208, {"country": "BM", "language": "en", "driving_side": "left", "proj": 32620}, download_repo=OSMFR, download_country="bermuda")

#########################################################################

us_state = gen_country('north-america/us', country_base='usa', language='en', speed_limit_unit='mph')

us_state("alabama", 161950, "US-AL", proj=26916)
us_state("alaska", 1116270, "US-AK", proj=26905)
us_state("arizona", 162018, "US-AZ", proj=26912)
us_state("arkansas", 161646, "US-AR", proj=26715)

us_ca_county = gen_country('north-america/us-west/california', country_base='usa_california', download_repo=OSMFR, language='en', proj=26910)

us_ca_county("alameda", 396499, "US-CA-ALA")
us_ca_county("alpine", 396497, "US-CA-ALP")
us_ca_county("amador", 396490, "US-CA-AMA")
us_ca_county("butte", 396508, "US-CA-BUT")
us_ca_county("calaveras", 396470, "US-CA-CAL")
us_ca_county("colusa", 396476, "US-CA-COL")
us_ca_county("contra_costa", 396462, "US-CA-CON")
us_ca_county("del_norte", 396503, "US-CA-DEL")
us_ca_county("el_dorado", 396481, "US-CA-ELD")
us_ca_county("fresno", 396492, "US-CA-FRE")
us_ca_county("glenn", 396493, "US-CA-GLE")
us_ca_county("humboldt", 396458, "US-CA-HUM")
us_ca_county("imperial", 396515, "US-CA-IMP")
us_ca_county("inyo", 396491, "US-CA-INY")
us_ca_county("kern", 396494, "US-CA-KER")
us_ca_county("kings", 396480, "US-CA-KIN")
us_ca_county("lake", 396502, "US-CA-LAK")
us_ca_county("lassen", 396469, "US-CA-LAS")
us_ca_county("los_angeles", 396479, "US-CA-LOS")
us_ca_county("madera", 396488, "US-CA-MAD")
us_ca_county("marin", 396461, "US-CA-MRN")
us_ca_county("mariposa", 396465, "US-CA-MP")
us_ca_county("mendocino", 396489, "US-CA-MEN")
us_ca_county("merced", 396504, "US-CA-MER")
us_ca_county("modoc", 396506, "US-CA-MOD")
us_ca_county("mono", 396472, "US-CA-MNO")
us_ca_county("monterey", 396485, "US-CA-MNT")
us_ca_county("napa", 396463, "US-CA-NAP")
us_ca_county("nevada", 396464, "US-CA-NEV")
us_ca_county("orange", 396466, "US-CA-ORA")
us_ca_county("placer", 396511, "US-CA-PLA")
us_ca_county("plumas", 396477, "US-CA-PLU")
us_ca_county("riverside", 396495, "US-CA-RIV")
us_ca_county("sacramento", 396460, "US-CA-SAC")
us_ca_county("san_benito", 396500, "US-CA-SBT")
us_ca_county("san_bernardino", 396509, "US-CA-SBD")
us_ca_county("san_diego", 396482, "US-CA-SDG")
us_ca_county("san_francisco", 396487, "US-CA-SFO")
us_ca_county("san_joaquin", 396467, "US-CA-SJQ")
us_ca_county("san_luis_obispo", 396496, "US-CA-SLO")
us_ca_county("san_mateo", 396498, "US-CA-SMT")
us_ca_county("santa_barbara", 396510, "US-CA-SBA")
us_ca_county("santa_clara", 396501, "US-CA-SCL")
us_ca_county("santa_cruz", 7870163, "US-CA-SCZ")
us_ca_county("shasta", 396512, "US-CA-SHA")
us_ca_county("sierra", 396474, "US-CA-SIE")
us_ca_county("siskiyou", 396483, "US-CA-SIS")
us_ca_county("solano", 396513, "US-CA-SOL")
us_ca_county("sonoma", 396468, "US-CA-SON")
us_ca_county("stanislaus", 396514, "US-CA-STA")
us_ca_county("sutter", 396478, "US-CA-SUT")
us_ca_county("tehama", 396486, "US-CA-TEH")
us_ca_county("trinity", 396484, "US-CA-TRI")
us_ca_county("tulare", 396459, "US-CA-TUL")
us_ca_county("tuolumne", 396471, "US-CA-TUO")
us_ca_county("ventura", 396505, "US-CA-VEN")
us_ca_county("yolo", 396507, "US-CA-YOL")
us_ca_county("yuba", 396475, "US-CA-YUB")

us_state("colorado", 161961, "US-CO", proj=26713)
us_state("connecticut", 165794, "US-CT", proj=3507)
us_state("delaware", 162110, "US-DE", proj=3509)
us_state("district-of-columbia", 162069, "US-DC", proj=3559)
us_state("florida", 162050, "US-FL", proj=3513)
us_state("georgia", 161957, "US-GA", proj=26917)
us_state("hawaii", 166563, "US-HI", proj=2783) # note: projection for hawaii is the one used for center islands, not for the whole
us_state("idaho", 162116, "US-ID", proj=3741)
us_state("illinois", 122586, "US-IL", proj=3746)
us_state("indiana", 161816, "US-IN", proj=3745)
us_state("iowa", 161650, "US-IA", proj=3745)
us_state("kansas", 161644, "US-KS", proj=3744)
us_state("kentucky", 161655, "US-KY", proj=3088)
us_state("louisiana", 224922, "US-LA", proj=3745, exclude=[
    'osmosis_waterway',  # Too many swamp, not suitable
])
us_state("maine", 63512, "US-ME", proj=3749)
us_state("maryland", 162112, "US-MD", proj=26985)
us_state("massachusetts", 61315, "US-MA", proj=2805)
us_state("michigan", 165789, "US-MI", proj=3746)
us_state("minnesota", 165471, "US-MN", proj=26992)
us_state("mississippi", 161943, "US-MS", proj=3816)
us_state("missouri", 161638, "US-MO", proj=3601)
us_state("montana", 162115, "US-MT", proj=3604)
us_state("nebraska", 161648, "US-NE", proj=3606)
us_state("nevada", 165473, "US-NV", proj=3607)
us_state("new-hampshire", 67213, "US-NH", proj=3613)
us_state("new-jersey", 224951, "US-NJ", proj=3615)
us_state("new-mexico", 162014, "US-NM", proj=3617)
us_state("new-york", 61320, "US-NY", proj=3623)
us_state("north-carolina", 224045, "US-NC", proj=3631)
us_state("north-dakota", 161653, "US-ND", proj=3633)
us_state("ohio", 162061, "US-OH", proj=26917)
us_state("oklahoma", 161645, "US-OK", proj=3639)
us_state("oregon", 165476, "US-OR", proj=3643)
us_state("pennsylvania", 162109, "US-PA", proj=3651)
us_state("rhode-island", 392915, "US-RI", proj=3653)
us_state("south-carolina", 224040, "US-SC", proj=3655)
us_state("south-dakota", 161652, "US-SD", proj=3659)
us_state("tennessee", 161838, "US-TN", proj=3661)
us_state("texas", 114690, "US-TX", proj=3082)
us_state("utah", 161993, "US-UT", proj=3675)
us_state("vermont", 60759, "US-VT", proj=3684)
us_state("virginia", 224042, "US-VA", proj=3968)
us_state("washington", 165479, "US-WA", proj=3725)
us_state("west-virginia",162068, "US-WV", proj=3747)
us_state("wisconsin", 165466, "US-WI", proj=3695)
us_state("wyoming", 161991, "US-WY", proj=26913)

default_country("oceania", "usa_guam", 306001, {"country": "GU", "language": "en", "proj": 32654}, download_repo=OSMFR, download_country="guam")
default_country("oceania", "usa_northern_mariana_islands", 306004, {"country": "MP", "language": "en", "proj": 32654}, download_repo=OSMFR, download_country="northern_mariana_islands")
default_country("south-america", "usa_american_samoa", 2177187, {"country": "AS", "language": "en", "proj": 32601}, download_repo=OSMFR, download_country="american_samoa")

#########################################################################

canada_province = gen_country('north-america', 'canada', language='en',
    phone_code="1", phone_len=10, phone_format=r"^[+]%s[- ][0-9]{3}[- ][0-9]{3}[- ][0-9]{4}$", suffix_separators="x",
    exclude=[
    'osmosis_waterway',
])

canada_province("alberta", 391186, "CA-AB", proj=32610)
canada_province("british-columbia", 390867, "CA-BC", proj=32609)
canada_province("manitoba", 390841, "CA-MB", proj=32615)
canada_province("new-brunswick", 68942, "CA-NB", proj=32619)
canada_province("newfoundland-and-labrador", 391196, "CA-NL", proj=32621)
canada_province("northwest-territories", 391220, "CA-NT", proj=32612)
canada_province("nova-scotia", 390558, "CA-NS", proj=32620)
canada_province("nunavut", 390840, "CA-NU", proj=32616)
canada_province("ontario", 68841, "CA-ON", proj=32616)
canada_province("prince-edward-island", 391115, "CA-PE", proj=32620)
canada_province("quebec", 61549, "CA-QC", proj=2138, language="fr")
canada_province("saskatchewan", 391178, "CA-SK", proj=32613)
canada_province("yukon", 391455, "CA-YT", proj=32608)

#########################################################################

default_country("africa", "algeria", 192756,  {"country": "DZ", "language": ["ar", "fr"], "proj": 32631}, download_repo=OSMFR)
default_country("africa", "angola", 195267, {"country": "AO", "language": "pt", "proj": 32733}, download_repo=OSMFR)
default_country("africa", "benin", 192784, {"country": "BJ", "language": "fr", "proj": 32631, 'phone_code': '229', 'phone_len': 8, 'phone_international': '00'}, download_repo=OSMFR)
default_country("africa", "botswana", 1889339, {"country": "BW", "language": "en", "driving_side": "left", "proj": 32734})
default_country("africa", "burkina_faso", 192783, {"country": "BF", "language": "fr", "proj": 32630}, download_repo=OSMFR)
default_country("africa", "burundi", 195269,  {"country": "BI", "language": "fr", "proj": 32735}, download_repo=OSMFR)
default_country("africa", "cameroon", 192830, {"country": "CM", "language": "fr", "proj": 32632}, download_repo=OSMFR)
default_country("africa", "cape_verde", 535774, {"country": "CV", "language": "pt", "proj": 32626}, download_repo=OSMFR)
default_country("africa", "central_african_republic", 192790, {"country": "CF", "language": "fr", "proj": 32634}, download_repo=OSMFR)
default_country("africa", "chad", 2361304,    {"country": "TD", "language": ["ar", "fr"], "proj": 32634}, download_repo=OSMFR)
default_country("africa", "comoros", 535790, {"country": "KM", "language": ["ar", "fr"], "proj": 32738}, download_repo=OSMFR)
default_country("africa", "congo_brazzaville", 192794, {"country": "CG", "language": "fr", "proj": 32733}, download_repo=OSMFR)
default_country("africa", "congo_kinshasa", 192795, {"country": "CD", "language": "fr", "proj": 32734}, download_repo=OSMFR)
default_country("africa", "djibouti", 192801, {"country": "DJ", "language": ["fr", "ar"], "proj": 32638, "multilingual-style": "dj"}, download_repo=OSMFR)
default_country("africa", "egypt", 1473947,   {"country": "EG", "language": "ar", "proj": 32635})
default_country("africa", "equatorial_guinea", 192791, {"country": "GQ", "language": "es", "proj": 32732}, download_repo=OSMFR)
default_country("africa", "eritrea", 296961, {"country": "ER", "proj": 32637}, download_repo=OSMFR)
default_country("africa", "ethiopia", 192800, {"country": "ET", "proj": 32638})
default_country("africa", "gabon", 192793,    {"country": "GA", "language": "fr", "proj": 32732}, download_repo=OSMFR)
default_country("africa", "gambia", 192774, {"country": "GM", "language": "en", "proj": 32628}, download_repo=OSMFR)
default_country("africa", "ghana", 192781,    {"country": "GH", "language": "en", "proj": 32630}, download_repo=OSMFR)
default_country("africa", "guinea", 192778,   {"country": "GN", "language": "fr", "proj": 32628}, download_repo=OSMFR)
default_country("africa", "guinea-bissau", 192776, {"country": "GW", "language": "pt", "proj": 32628})
default_country("africa", "ivory_coast", 192779, {"country": "CI", "language": "fr", "proj": 32630}, download_repo=OSMFR)
default_country("africa", "kenya", 192798,    {"country": "KE", "language": "en", "driving_side": "left", "proj": 32737}, download_repo=OSMFR)
default_country("africa", "lesotho", 2093234, {"country": "LS", "language": "en", "driving_side": "left", "proj": 32735}, download_repo=OSMFR)
default_country("africa", "liberia", 192780,  {"country": "LR", "language": "en", "speed_limit_unit": "mph", "proj": 32629})
default_country("africa", "libya", 192758,    {"country": "LY", "language": "ar", "proj": 32633})
default_country("africa", "madagascar", 447325, {"country": "MG", "language": ["fr", "mg"], "proj": 32738}, download_repo=GEOFABRIK)
default_country("africa", "malawi", 195290, {"country": "MW", "language": "en", "driving_side": "left", "proj": 32736}, download_repo=OSMFR)
default_country("africa", "mali", 192785,     {"country": "ML", "language": "fr", "proj": 32630}, download_repo=OSMFR)
default_country("africa", "mauritania", 192763, {"country": "MR", "language": "ar", "proj": 32628}, download_repo=OSMFR)
default_country("africa", "mauritius", 535828, {"country": "MU", "language": ["en", "fr"], "driving_side": "left", "proj": 32740}, download_repo=OSMFR)
default_country("africa", "morocco", 3630439,  {"country": "MA", "language": ["ar", "fr", "zgh", "ber"], "proj": 32629, "multilingual-style": "ma"})
default_country("africa", "mozambique", 195273, {"country": "MZ", "language": "pt", "driving_side": "left", "proj": 32736}, download_repo=OSMFR)
default_country("africa", "namibia", 195266, {"country": "NA", "language": "en", "driving_side": "left", "proj": 32733}, download_repo=OSMFR)
default_country("africa", "niger", 192786,    {"country": "NE", "language": "fr", "proj": 32632}, download_repo=OSMFR)
default_country("africa", "nigeria", 192787,  {"country": "NG", "language": "en", "proj": 32633})
default_country("africa", "norway_bouvet_island", 2425963, {"country": "BV", "language": "no", "proj": 32729}, download_repo=OSMFR, download_country="bouvet_island")
default_country("africa", "rwanda", 171496, {"country": "RW", "language": ["en", "fr"], "proj": 32735}, download_repo=OSMFR)
default_country("africa", "sao_tome_and_principe", 535880, {"country": "ST", "language": "pt", "proj": 32632}, download_repo=OSMFR)
default_country("africa", "senegal", 192775,  {"country": "SN", "language": "fr", "proj": 32628}, download_repo=OSMFR)
default_country("africa", "seychelles", 536765, {"country": "SC", "language": ["en", "fr"], "driving_side": "left", "proj": 32739}, download_repo=OSMFR)
default_country("africa", "sierra-leone", 192777, {"country": "SL", "language": "en", "proj": 32629})
default_country("africa", "somalia", 192799,  {"country": "SO", "language": "so", "proj": 32638})
default_country("africa", "south_africa", 87565, {"country": "ZA", "language": "en", "driving_side": "left", "proj": 32735}, download_repo=OSMFR)
default_country("africa", "south_sudan", 1656678, {"country": "SS", "language": "en", "proj": 32635}, download_repo=OSMFR)
default_country("africa", "sudan", 192789, {"country": "SD", "language": ["ar", "en"], "proj": 32636}, download_repo=OSMFR)
default_country("africa", "swaziland", 88210, {"country": "SZ", "language": "en", "driving_side": "left", "proj": 32736}, download_repo=OSMFR)
default_country("africa", "tanzania", 195270, {"country": "TZ", "language": "en", "driving_side": "left", "proj": 32736})
default_country("africa", "togo", 192782,     {"country": "TG", "language": "fr", "proj": 32631}, download_repo=OSMFR)
default_country("africa", "tunisia", 192757,  {"country": "TN", "language": ["ar", "fr"], "proj": 32632}, download_repo=OSMFR)
default_country("africa", "uganda", 192796, {"country": "UG", "language": "en", "driving_side": "left", "proj": 32636}, download_repo=OSMFR)
default_country("africa", "united_kingdom_saint_helena_ascension_tristan_da_cunha", 1964272, {"country": "SH", "language": "en", "driving_side": "left", "proj": 32729}, download_repo=OSMFR, download_country="saint_helena_ascension_tristan_da_cunha")
default_country("africa", "western_sahara", 2559126, {"country": "EH", "proj": 32629}, download_repo=OSMFR)
default_country("africa", "zambia", 195271, {"country": "ZM", "language": "en", "driving_side": "left", "proj": 32736}, download_repo=OSMFR)
default_country("africa", "zimbabwe", 195272, {"country": "ZW", "language": "en", "driving_side": "left", "proj": 32736}, download_repo=OSMFR)

config["chad"].analyser["osmosis_way_approximate"] = "xxx"
config["djibouti"].analyser["osmosis_way_approximate"] = "xxx"
config["kenya"].analyser["osmosis_way_approximate"] = "xxx"
config["madagascar"].analyser["osmosis_way_approximate"] = "xxx"
config["mali"].analyser["osmosis_way_approximate"] = "xxx"
config["senegal"].analyser["osmosis_way_approximate"] = "xxx"
config["togo"].analyser["osmosis_way_approximate"] = "xxx"

for country, c in config.items():
    if c.download and "url" in c.download and "/africa/" in c.download["url"]:
        del(c.analyser["osmosis_building_shapes"])

#########################################################################

default_country("asia", "afghanistan", 303427, {"country": "AF", "proj": 32641}, download_repo=OSMFR)
default_country("asia", "armenia", 364066, {"country": "AM", "language": "hy", "proj": 32641}, download_repo=OSMFR)
default_country("asia", "azerbaijan", 364110, {"country": "AZ", "language": "az", "proj": 32638})
default_country("asia", "bangladesh", 184640, {"country": "BD", "language": "bn", "driving_side": "left", "proj": 32646})
default_country("asia", "bahrain", 378734, {"country": "BH", "language": "ar","proj": 32639}, download_repo=OSMFR)
default_country("asia", "bhutan", 184629, {"country": "BT", "language": ["dz", "en"], "proj": 32646}, download_repo=OSMFR)
default_country("asia", "brunei", 2103120, {"country": "BN", "driving_side": "left", "language": "ms", "proj": 32650}, download_repo=OSMFR)
default_country("asia", "cambodia", 49898 , {"country": "KHM", "language": "km", "proj": 32648}, download_repo=OSMFR)
default_country("asia", "east_timor", 305142, {"country": "TL", "language": "pt", "proj": 32651}, download_repo=OSMFR)
default_country("asia", "georgia", 28699, {"country": "GE", "language": "ka", "proj": 32637}, download_repo=OSMFR)
default_country("asia", "israel", 1473946, {"country": "IL", "language": ["he", "ar"], "proj": 32636}, download_repo=OSMFR)
default_country("asia", "iran", 304938, {"country": "IR", "language": "fa","proj": 32640}, download_repo=GEOFABRIK)
default_country("asia", "iraq", 304934, {"country": "IQ", "language": "ar", "proj": 32638})
default_country("asia", "jordan", 184818, {"country": "JO", "language": "ar", "proj": 32637})
default_country("asia", "kazakhstan", 214665, {"country": "KZ", "proj": 32640}, download_repo=GEOFABRIK)
default_country("asia", "kuwait", 305099, {"country": "KW", "language": "ar","proj": 32639}, download_repo=OSMFR)
default_country("asia", "kyrgyzstan", 178009, {"country": "KG", "language": ["ky", "ru"], "proj": 32643})
default_country("asia", "laos", 49903, {"country": "LA", "language": ["lo", "en"], "proj": 32648}, download_repo=OSMFR)
default_country("asia", "lebanon", 184843, {"country": "LB", "language": "ar", "proj": 32636})
default_country("asia", "malaysia", 2108121 , {"country": "MY", "language": "ms", "driving_side": "left", "proj": 32649}, download_repo=OSMFR)
default_country("asia", "maldives", 536773, {"country": "MV", "language": "dv", "proj": 32643}, download_repo=OSMFR)
default_country("asia", "mongolia", 161033, {"country": "MN", "language": "mn", "proj": 32648})
default_country("asia", "myanmar", 50371, {"country": "MM", "language": "my", "proj": 32646}, download_repo=OSMFR)
default_country("asia", "north_korea", 192734, {"country": "KP", "language": "ko", "proj": 32652}, download_country="north-korea")
default_country("asia", "nepal", 184633, {"country": "NP", "language": "ne", "driving_side": "left", "proj": 32645})
default_country("asia", "oman", 305138, {"country": "OM", "language": "ar","proj": 32640}, download_repo=OSMFR)
default_country("asia", "pakistan", 307573, {"country": "PK", "language": ["en", "ur"], "driving_side": "left", "proj": 32642})
default_country("asia", "palestine", 1703814, {"country": "PS", "language": "ar", "proj": 32636}, download_repo=OSMFR)
default_country("asia", "philippines", 2850940, {"country": "PH", "language": "en", "proj": 32651, 'phone_code': '63', 'phone_len': [7, 8], 'phone_international': '00'}, download_repo=GEOFABRIK)
default_country("asia", "qatar", 305095, {"country": "QA", "language": "ar","proj": 32639}, download_repo=OSMFR)
default_country("asia", "saudi_arabia", 307584, {"country": "SA", "language": "ar","proj": 32637}, download_repo=OSMFR)
default_country("asia", "singapore", 536780 , {"country": "SG", "language": "en", "driving_side": "left", "proj": 32648}, download_repo=OSMFR)
default_country("asia", "sri-lanka", 536807, {"country": "LK", "language": ["en", "si", "ta"], "driving_side": "left", "proj": 32644})
default_country("asia", "south_korea", 307756, {"country": "KR", "language": "ko", "proj": 32652}, download_country="south-korea")
default_country("asia", "syria", 184840, {"country": "SY", "language": "ar", "proj": 32637})
default_country("asia", "tajikistan", 214626, {"country": "TJ", "language": "tg", "proj": 32642})
default_country("asia", "taiwan", 3777248, {"country": "TW", "language": ["zh_TW", "en"], "proj": 32651}, download_repo=GEOFABRIK)
default_country("asia", "thailand", 2067731, {"country": "TH", "language": "th", "proj": 32647, "driving_side": "left"})
default_country("asia", "turkmenistan", 223026, {"country": "TM", "language": "tk", "proj": 32640})
united_arab_emirates = default_country("asia", "united_arab_emirates", 307763, {"country": "AE", "language": "ar","proj": 32640}, download_repo=OSMFR)
del(united_arab_emirates.analyser["osmosis_highway_name_close"]) # Complicated Street Numbering
default_country("asia", "united_kingdom_british_indian_ocean_territory", 1993867, {"country": "IO", "language": "en", "driving_side": "left", "proj": 32742}, download_repo=OSMFR, download_country="british_indian_ocean_territory")
default_country("asia", "uzbekistan", 196240, {"country": "UZ", "proj": 32640}, download_repo=GEOFABRIK)
default_country("asia", "vietnam", 49915, {"country": "VN", "language": "vi", "proj": 32648}, download_repo=GEOFABRIK)
default_country("asia", "yemen", 305092, {"country": "YE", "language": "ar","proj": 32638}, download_repo=GEOFABRIK)

#########################################################################

id_province = gen_country('asia', 'indonesia', download_repo=OSMFR, language='id', proj=23837)

id_province("aceh", 2390836, "ID-AC")
id_province("bali", 1615621, "ID-BA")
id_province("bangka_belitung_islands", 3797243, "ID-BB")
id_province("banten", 2388356, "ID-BT")
id_province("bengkulu", 2390837, "ID-BE")
id_province("central_java", 2388357, "ID-JT")
id_province("central_kalimantan", 2388613, "ID-KT")
id_province("central_sulawesi", 2388664, "ID-ST")
id_province("east_java", 3438227, "ID-JI")
id_province("east_kalimantan", 5449459, "ID-KI")
id_province("east_nusa_tenggara", 2396778, "ID-NT")
id_province("gorontalo", 2388665, "ID-GO")
id_province("jakarta", 6362934, "ID-JK")
id_province("jambi", 2390838, "ID-JA")
id_province("lampung", 2390839, "ID-LA")
id_province("maluku", 2396795, "ID-MA")
id_province("north_kalimantan", 5449460, "ID-KU")
id_province("north_maluku", 2396796, "ID-MU")
id_province("north_sulawesi", 2388666, "ID-SA")
id_province("north_sumatra", 2390843, "ID-SU")
id_province("papua", 4521144, "ID-PA")
id_province("riau", 2390840, "ID-RI")
id_province("riau_islands", 3797244, "ID-KR")
id_province("southeast_sulawesi", 2388668, "ID-SG")
id_province("south_kalimantan", 2388615, "ID-KS")
id_province("south_sulawesi", 2388667, "ID-SN")
id_province("south_sumatra", 2390842, "ID-SS")
id_province("west_java", 2388361, "ID-JB")
id_province("west_kalimantan", 2388616, "ID-KB")
id_province("west_nusa_tenggara", 1615622, "ID-NB")
id_province("west_papua", 4521145, "ID-PB")
id_province("west_sulawesi", 2388669, "ID-SR")
id_province("west_sumatra", 2390841, "ID-SB")
id_province("yogyakarta", 5616105, "ID-YO")

#########################################################################

# central america

default_country("central-america", "belize", 287827, {"country": "BZ", "language": "en", "speed_limit_unit": "mph", "proj": 32616})
default_country("central-america", "costa_rica", 287667, {"country": "CR", "language": "es", "proj": 32617}, download_repo=OSMFR)
default_country("central-america", "el_salvador", 1520612, {"country": "SV", "language": "es", "proj": 32616}, download_repo=OSMFR)
default_country("central-america", "guatemala", 1521463, {"country": "GT", "language": "es", "proj": 32616})
default_country("central-america", "honduras", 287670, {"country": "HN", "language": "es", "proj": 32616}, download_repo=OSMFR)
default_country("central-america", "panama", 287668, {"country": "PA", "language": "es", "proj": 32617}, download_repo=OSMFR)


# caribbean

default_country("central-america", "haiti", 307829, {"country": "HT", "language": "fr", "proj": 32618},
                       download_repo=GEOFABRIK, download_country="haiti-and-domrep")

config["haiti"].analyser["osmosis_way_approximate"] = "xxx"

default_country("central-america", "antigua_and_barbuda", 536900, {"country": "BB", "language": "en", "driving_side": "left", "proj": 32620}, download_repo=OSMFR)
default_country("central-america", "barbados", 547511, {"country": "BB", "language": "en", "driving_side": "left", "proj": 32621}, download_repo=OSMFR)
default_country("central-america", "bahamas", 547469, {"country": "BS", "language": "en", "driving_side": "left", "speed_limit_unit": "mph", "proj": 32620}, download_repo=OSMFR)
default_country("central-america", "cuba", 307833, {"country": "CU", "language": "es", "proj": 32617})
default_country("central-america", "dominica", 307823, {"country": "DM", "language": "en", "driving_side": "left", "proj": 32620}, download_repo=OSMFR)
default_country("central-america", "dominican_republic", 307828, {"country": "DO", "language": "es", "proj": 32619}, download_repo=GEOFABRIK, download_country="haiti-and-domrep")
default_country("central-america", "grenada", 550727, {"country": "GD", "language": "en", "driving_side": "left", "proj": 32620}, download_repo=OSMFR)
default_country("central-america", "jamaica", 555017, {"country": "JM", "language": "en", "driving_side": "left", "proj": 32620}, download_repo=OSMFR)
default_country("central-america", "nicaragua", 287666, {"country": "NI", "language": "es", "proj": 32616}, download_repo=OSMFR)
default_country("central-america", "saint_lucia", 550728, {"country": "LC", "language": "en", "driving_side": "left", "proj": 32620}, download_repo=OSMFR)
default_country("central-america", "saint_vincent_and_the_grenadines", 550725, {"country": "VC", "language": "en", "proj": 32620}, download_repo=OSMFR)
default_country("central-america", "saint_kitts_and_nevis", 536899, {"country": "KN", "language": "en", "driving_side": "left", "proj": 2005}, download_repo=OSMFR)
default_country("central-america", "united_kingdom_anguilla", 2177161, {"country": "AI", "language": "en", "driving_side": "left", "proj": 32620}, download_repo=OSMFR, download_country="anguilla")
default_country("central-america", "united_kingdom_cayman_islands", 2185366, {"country": "KY", "language": "en", "driving_side": "left", "proj": 32617}, download_repo=OSMFR, download_country="cayman_islands")
default_country("central-america", "united_kingdom_montserrat", 537257, {"country": "MS", "language": "en", "driving_side": "left", "proj": 2005}, download_repo=OSMFR, download_country="montserrat")
default_country("central-america", "united_kingdom_turks_and_caicos_islands", 547479, {"country": "TC", "language": "en", "driving_side": "left", "proj": 32619}, download_repo=OSMFR, download_country="turks_and_caicos_islands")
default_country("central-america", "united_kingdom_virgin_islands", 285454, {"country": "VG", "language": "en", "driving_side": "left", "proj": 32620}, download_repo=OSMFR, download_country="british_virgin_islands")
default_country("central-america", "usa_puerto_rico", 4422604, {"country": "PR", "language": ["es", "en"], "proj": 32619, "boundary_detail_level": 6}, download_repo=OSMFR, download_country="puerto_rico")
default_country("central-america", "usa_virgin_islands", 286898, {"country": "VI", "language": "en", "proj": 4437}, download_repo=OSMFR, download_country="usa_virgin_islands")


#########################################################################

default_country("australia-oceania", "new-zealand", 556706, {"country": "NZ", "language": "en", "proj": 32759, "driving_side": "left"})

default_country("oceania", "marshall_islands", 571771, {"country": "MH", "language": "en", "proj": 32660}, download_repo=OSMFR)
default_country("oceania", "nauru", 571804, {"country": "NR", "language": "en", "driving_side": "left", "proj": 32659}, download_repo=OSMFR)
default_country("oceania", "palau", 571805, {"country": "PW", "language": "en", "proj": 32653}, download_repo=OSMFR)
default_country("oceania", "micronesia", 571802, {"country": "FM", "language": "en", "speed_limit_unit": "mph", "proj": 32656}, download_repo=OSMFR)
default_country("oceania", "papua_new_guinea", 307866, {"country": "PG", "language": "en","proj": 32755}, download_repo=OSMFR)
default_country("oceania", "solomon_islands", 1857436, {"country": "SB", "language": "en", "driving_side": "left", "proj": 32657}, download_repo=OSMFR)
default_country("oceania", "tuvalu", 2177266, {"country": "TV", "language": "en", "driving_side": "left", "proj": 32660}, download_repo=OSMFR)
default_country("oceania", "vanuatu", 2177246, {"country": "VU", "language": ["en", "fr"], "proj": 32658}, download_repo=OSMFR)

#########################################################################

default_country("merge", "fiji", 571747, {"country": "FJ", "language": "en", "driving_side": "left", "proj": 32660}, download_repo=OSMFR)
default_country("merge", "kiribati", 571178 , {"country": "KL", "language": "en", "driving_side": "left", "proj": 32660}, download_repo=OSMFR)

#########################################################################

au_state = gen_country('oceania', 'australia', download_repo=OSMFR, language='en', driving_side='left')

au_state("australian_capital_territory", 2354197, "AU-ACT", proj=32755)
au_state("new_south_wales", 2316593, "AU-NSW", proj=32755)
au_state("northern_territory", 2316594, "AU-NT", proj=32753)
au_state("western_australia", 2316598, "AU-WA", proj=32750)
au_state("south_australia", 2316596, "AU-SA", proj=32753)
au_state("victoria", 2316741, "AU-VIC", proj=32755)
au_state("queensland", 2316595, "AU-QLD", proj=32755)
au_state("tasmania", 2369652, "AU-TAS", proj=32755)

au_state("christmas_island", 2177207, "CX", proj=32648)
au_state("cocos_islands", 82636, "CC", proj=32646)
au_state("coral_sea_islands", 3225677, "AU", proj=32655)
au_state("norfolk_island", 2574988, "NF", proj=32658)

#########################################################################

default_country("south-america", "bolivia", 252645, {"country": "BO", "language": "es", "proj": 32720})
default_country("south-america", "chile", 167454, {"country": "CL", "language": "es", "proj": 32718})
default_country("south-america", "cook_islands", 2184233, {"country": "CK", "language": "en", "driving_side": "left", "proj": 32603}, download_repo=OSMFR)
colombia = default_country("south-america", "colombia", 120027, {"country": "CO", "language": "es", "proj": 32618})
del(colombia.analyser["osmosis_highway_name_close"]) # Complicated Street Numbering
default_country("south-america", "ecuador", 108089, {"country": "EC", "language": "es", "proj": 32727})
default_country("south-america", "guyana", 287083, {"country": "GY", "language": "en", "driving_side": "left", "proj": 32621}, download_repo=OSMFR)
default_country("south-america", "new_zealand_tokelau", 2186600, {"country": "TK", "language": "en", "driving_side": "left", "proj": 32602}, download_repo=OSMFR, download_country="tokelau")
default_country("south-america", "niue", 1558556, {"country": "NU", "language": "en", "driving_side": "left", "proj": 32602}, download_repo=OSMFR)
default_country("south-america", "paraguay", 287077, {"country": "PY", "language": "es", "proj": 32721}, download_repo=OSMFR)
default_country("south-america", "peru", 288247, {"country": "PE", "language": "es", "proj": 32718})
default_country("south-america", "samoa", 1872673, {"country": "WS", "language": "en", "driving_side": "left", "speed_limit_unit": "mph", "proj": 32602}, download_repo=OSMFR)
default_country("south-america", "tonga", 2186665 , {"country": "TO", "language": "en", "driving_side": "left", "proj": 32601}, download_repo=OSMFR)
default_country("south-america", "trinidad_and_tobago", 555717, {"country": "TT", "language": "en", "driving_side": "left","proj": 32620}, download_repo=OSMFR)
default_country("south-america", "suriname", 287082, {"country": "SR", "language": "nl", "driving_side": "left", "proj": 32621}, download_repo=OSMFR)
default_country("south-america", "united_kingdom_falkland", 2185374, {"country": "FK", "language": "en", "driving_side": "left", "proj": 32721}, download_repo=OSMFR, download_country="falkland")
default_country("south-america", "united_kingdom_pitcairn", 2185375, {"country": "PN", "language": "en", "driving_side": "left", "proj": 32709}, download_repo=OSMFR, download_country="pitcairn")
default_country("south-america", "united_kingdom_south_georgia_and_south_sandwich", 1983628, {"country": "GS", "language": "en", "driving_side": "left", "proj": 32725}, download_repo=OSMFR, download_country="south_georgia_and_south_sandwich")
default_country("south-america", "uruguay", 287072, {"country": "UY", "language": "es", "proj": 32721})
default_country("south-america", "venezuela", 272644, {"country": "VE", "language": "es", "proj": 32620}, download_repo=OSMFR)

#########################################################################

ar_state = gen_country('south-america', 'argentina', download_repo=OSMFR, language='es', proj=32720,
    phone_code='54', phone_local_prefix='0', phone_len=10, phone_international=00, suffix_separators='INT')

ar_state('buenos_aires_city', 1224652, 'AR-C')
ar_state('buenos_aires', 1632167, 'AR-B')
ar_state('catamarca', 153545, 'AR-K')
ar_state('chaco', 153554, 'AR-H')
ar_state('chubut', 153548, 'AR-CU')
ar_state('cordoba', 3592494, 'AR-X')
ar_state('corrientes', 153552, 'AR-W')
ar_state('entre_rios', 153551, 'AR-E')
ar_state('formosa', 2849847, 'AR-P')
ar_state('jujuy', 153556, 'AR-Y')
ar_state('la_pampa', 153541, 'AR-L')
ar_state('la_rioja', 153536, 'AR-F')
ar_state('mendoza', 153540, 'AR-M')
ar_state('misiones', 153553, 'AR-N')
ar_state('neuquen', 1606727, 'AR-Q')
ar_state('rio_negro', 153547, 'AR-R')
ar_state('salta', 2405230, 'AR-A')
ar_state('san_juan', 153539, 'AR-J')
ar_state('san_luis', 153538, 'AR-D')
ar_state('santa_cruz', 153549, 'AR-Z')
ar_state('santa_fe', 153543, 'AR-S')
ar_state('santiago_del_estero', 153544, 'AR-G')
ar_state('tierra_del_fuego', 153550, 'AR-V')
ar_state('tucuman', 153558, 'AR-T')

#########################################################################

br_region = gen_country('south-america', 'brazil', download_repo=OSMFR, language='pt', proj=32722, exclude=[
    'osmosis_highway_name_close', # Complicated Street Numbering
])

br_region(["north", "acre"], 326266, "BR-AC")
br_region(["northeast", "alagoas"], 303781, "BR-AL")
br_region(["north", "amapa"], 331463, "BR-AP")
br_region(["north", "amazonas"], 332476, "BR-AM")
br_region(["northeast", "bahia"], 362413, "BR-BA")
br_region(["northeast", "ceara"], 302635, "BR-CE")
br_region(["central-west", "distrito-federal"], 421151, "BR-DF")
br_region(["southeast", "espirito-santo"], 54882, "BR-ES")
br_region(["central-west", "goias"], 334443, "BR-GO")
br_region(["northeast", "maranhao"], 332924, "BR-MA")
br_region(["central-west", "mato-grosso"], 333597, "BR-MT")
br_region(["central-west", "mato-grosso-do-sul"], 334051, "BR-MS")
br_region(["southeast", "minas-gerais"], 315173, "BR-MG")
br_region(["north", "para"], 185579, "BR-PA")
br_region(["northeast", "paraiba"], 301464, "BR-PB")
br_region(["south", "parana"], 297640, "BR-PR")
br_region(["northeast", "pernambuco"], 303702, "BR-PE")
br_region(["northeast", "piaui"], 302819, "BR-PI")
br_region(["southeast", "rio-de-janeiro"], 57963, "BR-RJ")
br_region(["northeast", "rio-grande-do-norte"], 301079, "BR-RN")
br_region(["south", "rio-grande-do-sul"], 242620, "BR-RS")
br_region(["north", "rondonia"], 325866, "BR-RO")
br_region(["north", "roraima"], 326287, "BR-RR")
br_region(["south", "santa-catarina"], 296584, "BR-SC")
br_region(["southeast", "sao-paulo"], 298204, "BR-SP")
br_region(["northeast", "sergipe"], 303940, "BR-SE")
br_region(["north", "tocantins"], 336819, "BR-TO")

#########################################################################

it_region = gen_country('europe', 'italy', download_repo=OSMFR, language='it', proj=23032, municipality_ref='ref:ISTAT')

it_region("abruzzo", 53937, "IT-65")
it_region("basilicata", 40137, "IT-77")
it_region("calabria", 1783980, "IT-78")
it_region("campania", 40218, "IT-72")
it_region("emilia_romagna", 42611, "IT-45")
it_region("friuli_venezia_giulia", 179296, "IT-36")
it_region("lazio", 40784, "IT-62")
it_region("liguria", 301482, "IT-42")
it_region("lombardia", 44879, "IT-25")
it_region("marche", 53060, "IT-57")
it_region("molise", 41256, "IT-67")
it_region("piemonte", 44874, "IT-21")
it_region("puglia", 40095, "IT-75")
it_region("sardegna", 279816, "IT-88")
it_region("sicilia", 39152, "IT-82")
it_region("toscana", 41977, "IT-52")
it_region("trentino_alto_adige", 45757, "IT-32", language=["it","de"])
it_region("umbria", 42004, "IT-55")
it_region("valle_aosta", 2905554, "IT-23")
it_region("veneto", 43648, "IT-34")

#########################################################################

nl_province = gen_country('europe', 'netherlands', download_repo=OSMFR, language='nl', proj=23032)

nl_province("zuid_holland", 47772, "NL-ZH")
nl_province("zeeland", 47806, "NL-ZE")
nl_province("noord_brabant", 47696, "NL-NB")
nl_province("limburg", 47793, "NL-LI")
nl_province("gelderland", 47554, "NL-GE")
nl_province("overijssel", 47608, "NL-OV")
nl_province("drenthe", 47540, "NL-DR")
nl_province("friesland", 47381, "NL-FR", language=["nl", "fy"])
nl_province("groningen", 47826, "NL-GR")
nl_province("flevoland", 47407, "NL-FL")
nl_province("utrecht", 47667, "NL-UT")
nl_province("noord_holland", 47654, "NL-NH")

nl_province("aruba",        1231749, "AW", area="central-america", path_base=None, proj=32620)
nl_province("curacao",      1216719, "CW", area="central-america", path_base=None, proj=32620)
nl_province("sint_maarten", 1231790, "SX", area="central-america", path_base=None, proj=32620)
nl_province("caribbean",    1216720, "NL", area="central-america", path_base=None, proj=32620)

#########################################################################

cz_kraj = gen_country('europe', 'czech_republic', download_repo=OSMFR, language='cs', proj=32633)

cz_kraj("praha", 435514, "CZ-PR")
cz_kraj("stredocesky", 442397, "CZ-ST")
cz_kraj("jihocesky", 442321, "CZ-JC")
cz_kraj("plzensky", 442466, "CZ-PL")
cz_kraj("karlovarsky", 442314, "CZ-KA")
cz_kraj("ustecky", 442452, "CZ-US")
cz_kraj("liberecky", 442455, "CZ-LI")
cz_kraj("kralovehradecky", 442463, "CZ-KR")
cz_kraj("pardubicky", 442460, "CZ-PA")
cz_kraj("vysocina", 442453, "CZ-VY")
cz_kraj("jihomoravsky", 442311, "CZ-JM")
cz_kraj("olomoucky", 442459, "CZ-OL")
cz_kraj("moravskoslezsky", 442461, "CZ-MO")
cz_kraj("zlinsky", 442449, "CZ-ZL")

#########################################################################

pl_province = gen_country('europe', 'poland', download_repo=OSMFR, language='pl', proj=32634)

pl_province("dolnoslaskie", 224457, "PL-DS")
pl_province("kujawsko_pomorskie", 223407, "PL-KP")
pl_province("lubelskie", 130919, "PL-LU")
pl_province("lubuskie", 130969, "PL-LB")
pl_province("lodzkie", 224458, "PL-LD")
pl_province("malopolskie", 224459, "PL-MA")
pl_province("mazowieckie", 130935, "PL-MZ")
pl_province("opolskie", 224460, "PL-OP")
pl_province("podkarpackie", 130957, "PL-PK")
pl_province("podlaskie", 224461, "PL-PD")
pl_province("pomorskie", 130975, "PL-PM")
pl_province("slaskie", 224462, "PL-SL")
pl_province("swietokrzyskie", 130914, "PL-SK")
pl_province("warminsko_mazurskie", 223408, "PL-WN")
pl_province("wielkopolskie", 130971, "PL-WP")
pl_province("zachodniopomorskie", 104401, "PL-ZP")

#########################################################################

de_state = gen_country('europe', 'germany', language='de', proj=32632, municipality_ref='de:regionalschluessel',
    phone_code='49', phone_international='00', phone_local_prefix='0', phone_values_separators=[','],
    include=[
        'osmosis_highway_zone'
    ]
)

#de_state("baden-wuerttemberg", 62611, "DE-BW")
for (name, rel_id) in [("freiburg-regbez", 2106112),
                       ("karlsruhe-regbez", 22027),
                       ("stuttgart-regbez", 22041),
                       ("tuebingen-regbez", 2811874)]:
    de_state("baden-wuerttemberg/" + name, rel_id, "DE-BW", download_repo=GEOFABRIK)

#de_state("bayern", 2145268, "DE-BY")
for (name, rel_id) in [("mittelfranken", 17614),
                       ("niederbayern", 17593),
                       ("oberbayern", 2145274),
                       ("oberfranken", 17592),
                       ("oberpfalz", 17596),
                       ("schwaben", 17657),
                       ("unterfranken", 17585)]:
    de_state("bayern/" + name, rel_id, "DE-BY", download_repo=GEOFABRIK)

de_state("berlin", 62422, "DE-BE")
de_state("brandenburg", 62504, "DE-BB")
de_state("bremen", 62718, "DE-HB")
de_state("hamburg", 62782, "DE-HH")
de_state("hessen", 62650, "DE-HE")
de_state("mecklenburg-vorpommern", 28322, "DE-MV")
de_state("niedersachsen", 454192, "DE-NI")

#de_state("nordrhein-westfalen", 62761, "DE-NW")
for (name, rel_id) in [("arnsberg", 73340),
                       ("detmold", 73347),
                       ("dusseldorf", 63306),
                       ("koln", 72022),
                       ("munster", 63594)]:
    de_state("nordrhein_westfalen/" + name, rel_id, "DE-NW", download_repo=OSMFR)

de_state("rheinland-pfalz", 62341, "DE-RP")
de_state("saarland", 62372, "DE-SL")
de_state("sachsen-anhalt", 62607, "DE-ST")
de_state("sachsen", 62467, "DE-SN")
de_state("schleswig-holstein", 51529, "DE-SH")
de_state("thueringen", 62366, "DE-TH")

#########################################################################

at_state = gen_country('europe', 'austria', download_repo=OSMFR, language='de', proj=32633)

at_state("niederosterreich", 77189, "AT-3")
at_state("burgenland", 76909, "AT-1")
at_state("karnten", 52345, "AT-2")
at_state("oberosterreich", 102303, "AT-4")
at_state("salzburg", 86539, "AT-5")
at_state("steiermark", 35183, "AT-6")
at_state("tirol", 52343, "AT-7")
at_state("wien", 109166, "AT-9")
at_state("vorarlberg", 74942, "AT-8")

#########################################################################

es_comm = gen_country('europe', 'spain', download_repo=OSMFR, language='es', proj=32629, municipality_ref='ine:municipio')

es_comm("andalucia", 349044, "ES-AN", proj=32629)
es_comm("aragon", 349045, "ES-AR", proj=32630)
es_comm("asturias", 349033, "ES-AS", proj=32629)
es_comm("illes_balears", 348981, "ES-IB", proj=32630, language="ca")
es_comm("cantabria", 349013, "ES-CB", proj=32630)
es_comm("castilla_la_mancha", 349052, "ES-CM", proj=32630)
es_comm("castilla_y_leon", 349041, "ES-CL", proj=32629)
es_comm("catalunya", 349053, "ES-CT", proj=32630, language="ca")
es_comm("comunitat_valenciana", 349043, "ES-VC", proj=32630, language=["es", "ca"])
es_comm("extremadura", 349050, "ES-EX", proj=32629)
es_comm("galicia", 349036, "ES-GA", proj=32629, language=["es", "gl"])
es_comm("la_rioja", 348991, "ES-RI", proj=32630)
es_comm("comunidad_de_madrid", 349055, "ES-MD", proj=32630)
es_comm("comunidad_foral_de_navarra", 349027, "ES-NC", proj=32630)
es_comm("euskadi", 349042, "ES-PV", proj=32630, language=["es", "eu"])
es_comm("region_de_murcia", 349047, "ES-MC", proj=32630)

es_comm("canarias", 349048, "ES-CN", proj=32628, area="africa")
es_comm("ceuta", 1154756, "ES-CE", proj=32630, area="africa")
es_comm("melilla", 1154757, "ES-ML", proj=32628, area="africa")

#########################################################################

en_region = gen_country('europe', 'united_kingdom/england', download_repo=OSMFR, country_code='GB-ENG', language='en', proj=32630, driving_side='left', speed_limit_unit='mph')

en_region("east_midlands", 151279)
en_region("east", 151336)
en_region("greater_london", 175342)
en_region("north_east", 151164)
en_region("north_west", 151261)
en_region("south_east", 151304)
en_region("south_west", 151339, language=["en", "kw"])
en_region("west_midlands", 151283)
en_region("yorkshire_and_the_humber", 151012)

#########################################################################

sk_kraj = gen_country('europe', 'slovakia', download_repo=OSMFR, language='sk', proj=32634)

sk_kraj("trnavsky", 388266, "SK-TA")
sk_kraj("trenciansky", 388267, "SK-TC")
sk_kraj("presovsky", 388271, "SK-PV")
sk_kraj("nitriansky", 388268, "SK-NI")
sk_kraj("kosicky", 388272, "SK-KI")
sk_kraj("zilinsky", 388269, "SK-ZI")
sk_kraj("banskobystricky", 388270, "SK-BC")
sk_kraj("bratislavsky", 388265, "SK-BL")

#########################################################################

india_state = gen_country('asia', 'india', download_repo=OSMFR, language=['hi', 'en'], proj=32644, driving_side='left')

india_state("andhra_pradesh", 2022095, "IN-AP", proj=32644)
india_state("arunachal_pradesh",2027346, "IN-AR", proj=32646)
india_state("assam", 2025886, "IN-AS", proj=32646)
india_state("bihar", 1958982, "IN-BR", proj=32645)
india_state("chhattisgarh", 1972004, "IN-CT", proj=32644)
india_state("goa", 1997192, "IN-GA", proj=32643)
india_state("gujarat", 1949080, "IN-GJ", proj=32643)
india_state("haryana", 1942601, "IN-HR", proj=32643)
india_state("himachal_pradesh", 364186, "IN-HP", proj=32643)
india_state("jammu_and_kashmir", 1943188, "IN-JK", proj=32643)
india_state("jharkhand", 1960191, "IN-JH", proj=32645)
india_state("karnataka", 2019939, "IN-KA", proj=32643)
india_state("kerala", 2018151, "IN-KL", proj=32643)
india_state("madhya_pradesh", 1950071, "IN-MP", proj=32643)
india_state("maharashtra", 1950884, "IN-MH", proj=32643)
india_state("manipur", 2027869, "IN-MN", proj=32646)
india_state("meghalaya", 2027521, "IN-ML", proj=32646)
india_state("mizoram", 2029046, "IN-MZ", proj=32646)
india_state("nagaland", 2027973, "IN-NL", proj=32646)
india_state("odisha", 1984022, "IN-OR", proj=32645)
india_state("punjab", 1942686, "IN-PB", proj=32643)
india_state("rajasthan", 1942920, "IN-RJ", proj=32643)
india_state("sikkim", 1791324, "IN-SK", proj=32645)
india_state("tamil_nadu", 96905, "IN-TN", proj=32644)
india_state("telangana", 3250963, "IN-TG", proj=32646)
india_state("tripura", 2026458, "IN-TR", proj=32644)
india_state("uttar_pradesh", 1942587, "IN-UP", proj=32644)
india_state("uttarakhand", 374810, "IN-UT", proj=32644)
india_state("west_bengal", 1960177, "IN-WB", proj=32645)

india_state("andaman_and_nicobar_islands", 2025855, "IN-AN", proj=32646)
india_state("chandigarh", 1942809, "IN-CH", proj=32643)
india_state("dadra_and_nagar_haveli", 1952530, "IN-DN", proj=32643)
india_state("daman_and_diu", 1953041, "IN-DD", proj=32642)
india_state("lakshadweep", 2027460, "IN-LD", proj=32643)
india_state("national_capital_territory_of_delhi", 1942586, "IN-DL", proj=32643)
india_state("puducherry", 107001, "IN-PY", proj=32643)

#########################################################################

russia_region = gen_country(None, 'russia', download_repo=OSMFR, language='ru')

russia_region(["central_federal_district", "belgorod_oblast"], 83184, "RU-BEL", proj=32637)
russia_region(["central_federal_district", "bryansk_oblast"], 81997, "RU-BRY", proj=32636)
russia_region(["central_federal_district", "ivanovo_oblast"], 85617, "RU-IVA", proj=32637)
russia_region(["central_federal_district", "kaluga_oblast"], 81995, "RU-KLU", proj=32636)
russia_region(["central_federal_district", "kostroma_oblast"], 85963, "RU-KOS", proj=32637)
russia_region(["central_federal_district", "kursk_oblast"], 72223, "RU-KRS", proj=32637)
russia_region(["central_federal_district", "lipetsk_oblast"], 72169, "RU-LIP", proj=32637)
russia_region(["central_federal_district", "moscow_oblast"], 51490, "RU-MOS", proj=32637)
russia_region(["central_federal_district", "moscow"], 102269, "RU-MOW", proj=32637)
russia_region(["central_federal_district", "oryol_oblast"], 72224, "RU-ORL", proj=32637)
russia_region(["central_federal_district", "ryazan_oblast"], 71950, "RU-RYA", proj=32637)
russia_region(["central_federal_district", "smolensk_oblast"], 81996, "RU-SMO", proj=32636)
russia_region(["central_federal_district", "tambov_oblast"], 72180, "RU-TAM", proj=32637)
russia_region(["central_federal_district", "tula_oblast"], 81993, "RU-TUL", proj=32637)
russia_region(["central_federal_district", "tver_oblast"], 2095259, "RU-TVE", proj=32637)
russia_region(["central_federal_district", "vladimir_oblast"], 72197, "RU-VLA", proj=32637)
russia_region(["central_federal_district", "voronezh_oblast"], 72181, "RU-VOR", proj=32637)
russia_region(["central_federal_district", "yaroslavl_oblast"], 81994, "RU-YAR", proj=32637)
russia_region(["far_eastern_federal_district", "amur_oblast"], 147166, "RU-AMU", proj=32652)
russia_region(["far_eastern_federal_district", "chukotka_autonomous_okrug"], 151231, "RU-CHU", proj=32659)
russia_region(["far_eastern_federal_district", "jewish_autonomous_oblast"], 147167, "RU-YEV", proj=32653)
russia_region(["far_eastern_federal_district", "kamchatka_krai"], 151233, "RU-KAM", proj=32658)
russia_region(["far_eastern_federal_district", "khabarovsk_krai"], 151223, "RU-KHA", proj=32653)
russia_region(["far_eastern_federal_district", "magadan_oblast"], 151228, "RU-MAG", proj=32656)
russia_region(["far_eastern_federal_district", "primorsky_krai"], 151225, "RU-PRI", proj=32653)
russia_region(["far_eastern_federal_district", "sakha_republic"], 151234, "RU-SA", proj=32652)
russia_region(["far_eastern_federal_district", "sakhalin_oblast"], 394235, "RU-SAK", proj=32654)
russia_region(["north_caucasian_federal_district", "chechen_republic"], 109877, "RU-CE", proj=32638)
russia_region(["north_caucasian_federal_district", "dagestan_republic"], 109876, "RU-DA", proj=32638)
russia_region(["north_caucasian_federal_district", "ingushetia_republic"], 253252, "RU-IN", proj=32638)
russia_region(["north_caucasian_federal_district", "kabardino_balkar_republic"], 109879, "RU-KB", proj=32638)
russia_region(["north_caucasian_federal_district", "karachay_cherkess_republic"], 109878, "RU-KC", proj=32638)
russia_region(["north_caucasian_federal_district", "north_ossetia_alania_republic"], 110032, "RU-SE", proj=32638)
russia_region(["north_caucasian_federal_district", "stavropol_krai"], 108081, "RU-STA", proj=32638)
russia_region(["northwestern_federal_district", "arkhangelsk_oblast"], 140337, "RU-ARK", proj=32638)
russia_region(["northwestern_federal_district", "kaliningrad_oblast"], 103906, "RU-KGD", proj=32634)
russia_region(["northwestern_federal_district", "karelia_republic"], 393980, "RU-KR", proj=32636)
russia_region(["northwestern_federal_district", "komi_republic"], 115136, "RU-KO", proj=32640)
russia_region(["northwestern_federal_district", "leningrad_oblast"], 176095, "RU-LEN", proj=32636)
russia_region(["northwestern_federal_district", "murmansk_oblast"], 2099216, "RU-MUR", proj=32636)
russia_region(["northwestern_federal_district", "nenets_autonomous_okrug"], 274048, "RU-NEN", proj=32639)
russia_region(["northwestern_federal_district", "novgorod_oblast"], 89331, "RU-NGR", proj=32636)
russia_region(["northwestern_federal_district", "pskov_oblast"], 155262, "RU-PSK", proj=32636)
russia_region(["northwestern_federal_district", "saint_petersburg"], 337422, "RU-SPE", proj=32636)
russia_region(["northwestern_federal_district", "vologda_oblast"], 115106, "RU-VLG", proj=32637)
russia_region(["siberian_federal_district", "altai_krai"], 144764, "RU-ALT", proj=32644)
russia_region(["siberian_federal_district", "altai_republic"], 145194, "RU-AL", proj=32645)
russia_region(["siberian_federal_district", "buryatia_republic"], 145729, "RU-BU", proj=32647)
russia_region(["siberian_federal_district", "irkutsk_oblast"], 145454, "RU-IRK", proj=32648)
russia_region(["siberian_federal_district", "kemerovo_oblast"], 144763, "RU-KEM", proj=32645)
russia_region(["siberian_federal_district", "khakassia_republic"], 190911, "RU-KK", proj=32646)
russia_region(["siberian_federal_district", "krasnoyarsk_krai"], 190090, "RU-KYA", proj=32646)
russia_region(["siberian_federal_district", "novosibirsk_oblast"], 140294, "RU-NVS", proj=32644)
russia_region(["siberian_federal_district", "omsk_oblast"], 140292, "RU-OMS", proj=32643)
russia_region(["siberian_federal_district", "tomsk_oblast"], 140295, "RU-TOM", proj=32644)
russia_region(["siberian_federal_district", "tuva_republic"], 145195, "RU-TY", proj=32646)
russia_region(["siberian_federal_district", "zabaykalsky_krai"], 145730, "RU-ZAB", proj=32650)
russia_region(["southern_federal_district", "crimea_republic"], 3795586, "RU-CR", proj=32636)
russia_region(["southern_federal_district", "adygea_republic"], 253256, "RU-AD", proj=32637)
russia_region(["southern_federal_district", "astrakhan_oblast"], 112819, "RU-AST", proj=32638)
russia_region(["southern_federal_district", "kalmykia_republic"], 108083, "RU-KL", proj=32638)
russia_region(["southern_federal_district", "krasnodar_krai"], 108082, "RU-KDA", proj=32637)
russia_region(["southern_federal_district", "rostov_oblast"], 85606, "RU-ROS", proj=32637)
russia_region(["southern_federal_district", "sevastopol"], 1574364, "RU", proj=32636)
russia_region(["southern_federal_district", "volgograd_oblast"], 77665, "RU-VGG", proj=32638)
russia_region(["ural_federal_district", "chelyabinsk_oblast"], 77687, "RU-CHE", proj=32641)
russia_region(["ural_federal_district", "khanty_mansi_autonomous_okrug"], 140296, "RU-KHM", proj=32642)
russia_region(["ural_federal_district", "kurgan_oblast"], 140290, "RU-KGN", proj=32641)
russia_region(["ural_federal_district", "sverdlovsk_oblast"], 79379, "RU-SVE", proj=32641)
russia_region(["ural_federal_district", "tyumen_oblast"], 140291, "RU-TYU", proj=32642)
russia_region(["ural_federal_district", "yamalo_nenets_autonomous_okrug"], 191706, "RU-YAN", proj=32643)
russia_region(["volga_federal_district", "bashkortostan_republic"], 77677, "RU-BA", proj=32640)
russia_region(["volga_federal_district", "chuvash_republic"], 80513, "RU-CU", proj=32639)
russia_region(["volga_federal_district", "kirov_oblast"], 115100, "RU-KIR", proj=32639)
russia_region(["volga_federal_district", "mari_el_republic"], 115114, "RU-ME", proj=32639)
russia_region(["volga_federal_district", "mordovia_republic"], 72196, "RU-MO", proj=32638)
russia_region(["volga_federal_district", "nizhny_novgorod_oblast"], 72195, "RU-NIZ", proj=32638)
russia_region(["volga_federal_district", "orenburg_oblast"], 77669, "RU-ORE", proj=32640)
russia_region(["volga_federal_district", "penza_oblast"], 72182, "RU-PNZ", proj=32638)
russia_region(["volga_federal_district", "perm_krai"], 115135, "RU-PER", proj=32640)
russia_region(["volga_federal_district", "samara_oblast"], 72194, "RU-SAM", proj=32639)
russia_region(["volga_federal_district", "saratov_oblast"], 72193, "RU-SAR", proj=32638)
russia_region(["volga_federal_district", "tatarstan_republic"], 79374, "RU-TA", proj=32639)
russia_region(["volga_federal_district", "udmurt_republic"], 115134, "RU-UD", proj=32639)
russia_region(["volga_federal_district", "ulyanovsk_oblast"], 72192, "RU-ULY", proj=32639)

#########################################################################

japan_region = gen_country('asia', 'japan', download_repo=OSMFR, country_code='JP', language='ja', proj=32654, driving_side='left')

japan_region("hokkaido", 3795658, proj=32654)
japan_region("tohoku", 1835900, proj=32654)
japan_region("kanto", 1803923, proj=32654)
japan_region("chubu", 532759, proj=32654)
japan_region("kansai", 357113, proj=32653)
japan_region("chugoku", 1842114, proj=32653)
japan_region("shikoku", 1847663, proj=32653)
japan_region("kyushu", 1842245, proj=32652)

#########################################################################

china_province = gen_country('asia', 'china', download_repo=OSMFR, language='zh')

china_province("anhui", 913011, "CN-34", proj=32650)
china_province("fujian", 553303, "CN-35", proj=32650)
china_province("gansu", 153314, "CN-62", proj=32648)
china_province("guangdong", 911844, "CN-44", proj=32649)
china_province("guizhou", 286937, "CN-52", proj=32648)
china_province("hainan", 2128285, "CN-46", proj=32649)
china_province("hebei", 912998, "CN-13", proj=32650)
china_province("heilongjiang", 199073, "CN-23", proj=32652)
china_province("henan", 407492, "CN-41", proj=32650)
china_province("hubei", 913106, "CN-42", proj=32649)
china_province("hunan", 913073, "CN-43", proj=32649)
china_province("jiangsu", 913012, "CN-32", proj=32650)
china_province("jiangxi", 913109, "CN-36", proj=32650)
china_province("jilin", 198590, "CN-22", proj=32652)
china_province("liaoning", 912942, "CN-21", proj=32651)
china_province("qinghai", 153269, "CN-63", proj=32647)
china_province("shaanxi", 913100, "CN-61", proj=32649)
china_province("shandong", 913006, "CN-37", proj=32650)
china_province("shanxi", 913105, "CN-14", proj=32650)
china_province("sichuan", 913068, "CN-51", proj=32648)
china_province("yunnan", 913094, "CN-53", proj=32648)
china_province("zhejiang", 553302, "CN-33", proj=32651)

china_province("tibet", 153292, "CN-54", proj=32645)
china_province("xinjiang", 153310, "CN-65", proj=32645)
china_province("guangxi", 286342, "CN-45", proj=32649)
china_province("inner_mongolia", 161349, "CN-15", proj=32650)
china_province("ningxia", 913101, "CN-64", proj=32648)

china_province("beijing", 912940, "CN-11", proj=32650)
china_province("tianjin", 912999, "CN-12", proj=32650)
china_province("shanghai", 913067, "CN-31", proj=32651)
china_province("chongqing", 913069, "CN-50", proj=32649)

china_province("hong_kong", 913110, "CN-91", proj=32650, language=["zh", "en"], driving_side="left")
china_province("macau", 1867188, "CN-92", proj=32649, language=["zh", "pt"])

#########################################################################

ogf = default_simple("ogf", None, {"project": "opengeofiction"},
        download_url=u"http://opengeofiction.net/backup/ogf_latest.osm.pbf")
del(ogf.analyser["osmosis_soundex"])

###########################################################################
# Merge analysers are uploaded to a different frontend server
for country in config.keys():
  config[country].analyser_updt_url = {}
  for k in config[country].analyser.keys():
    if k.startswith("merge_"):
      config[country].analyser_updt_url[k] = [modules.config.url_frontend_update, modules.config.url_frontend_opendata_update]

#########################################################################
# Passwords are stored in separate file, not on git repository
import osmose_config_password

osmose_config_password.set_password(config)

###########################################################################

if __name__ == "__main__":

  import json

  j = []
  for (k,v) in config.items():
    j.append(dict(v.__dict__, **{"country": k}))
  print(json.dumps(j, indent=4))
