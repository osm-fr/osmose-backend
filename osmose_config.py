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
try:
     from collections import OrderedDict
except ImportError:
     from modules.OrderedDict import OrderedDict
import modules.config

hostname = open("/etc/hostname").read().strip()
available_results_urls = {"osm1": "http://osm1.crans.org/osmose/",
                          "osm3": "http://osm3.crans.org/osmose/",
                          "osm4": "http://osm4.crans.org/osmose/",
                          "osm5": "http://osm5.univ-nantes.fr/osmose/",
                          "osm6": "http://osm6.univ-nantes.fr/osmose/",
                          "osm7": "http://osm7.pole-aquinetic.fr/osmose/",
                          "osm8": "http://osm8.pole-aquinetic.fr/~osmose/results",
                          "osmoseit": "http://194.116.72.25/osmose/",
                          "ubuntu12": "http://46.249.37.15/osmose/",
                         }
if hostname in available_results_urls:
    results_url = available_results_urls[hostname]
elif re.match("osm[0-9]+$", hostname):
    results_url = "http://%s.openstreetmap.fr/osmose/" % hostname
else:
    results_url = None

###########################################################################

GEOFABRIK = "http://download.geofabrik.de/"
OSMFR = "http://download.openstreetmap.fr/extracts/"

class template_config:

    clean_at_end   = True

    updt_url       = modules.config.url_frontend_update
    results_url    = results_url
    dir_work       = modules.config.dir_work
    dir_tmp        = modules.config.dir_tmp
    dir_cache      = modules.config.dir_cache
    dir_scripts    = modules.config.dir_osmose
    bin_osmosis    = modules.config.bin_osmosis
    osmosis_pre_scripts = [
        dir_scripts + "/osmosis/pgsnapshot_schema_0.6.sql",
#       dir_scripts + "/osmosis/osmosis-0.44/script/pgsnapshot_schema_0.6_bbox.sql",
        dir_scripts + "/osmosis/osmosis-0.44/script/pgsnapshot_schema_0.6_linestring.sql",
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
        dir_scripts + "/osmosis/osmosis-0.44/script/pgsnapshot_schema_0.6_action.sql",
    ]
    osmosis_change_post_scripts = [  # Scripts to run each time the database is updated
        dir_scripts + "/osmosis/CreateTouched.sql",
    ]
    osmosis_resume_init_post_scripts = [  # Scripts to run on database initialisation
        dir_scripts + "/osmosis/osmosis-0.44/script/pgsnapshot_schema_0.6_action.sql",
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
    db_host     = None        # Use socket by default
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

class default_country_simple(default_simple):
    def __init__(self, part, country, polygon_id=None, analyser_options=None,
                 download_repo=GEOFABRIK, download_country=None):

        if not download_country:
            download_country = country
        country = country.replace("-", "_").replace("/", "_")
        analyser_options = dict({"project": "openstreetmap"}, **analyser_options)
        default_simple.__init__(self, country, polygon_id, analyser_options, download_repo=download_repo)
        self.download.update({
            "url": self.download_repo + part + "/" + download_country + "-latest.osm.pbf",
            "poly": self.download_repo + part + "/" + download_country + ".poly",
        })
        if download_repo == GEOFABRIK:
            self.download["diff"] = self.download_repo + part + "/" + download_country + "-updates/"
        if download_repo == OSMFR:
            self.download["poly"] = self.download["poly"].replace("/extracts/", "/polygons/")
            self.download["diff"] = self.download_repo + "../replication/" + part + "/" + download_country + "/minute/"

class default_country(default_country_simple):
    def __init__(self, part, country, polygon_id=None, analyser_options=None,
                 download_repo=GEOFABRIK, download_country=None):

        default_country_simple.__init__(self, part, country, polygon_id, analyser_options,
                                        download_repo, download_country)
        self.analyser["osmosis_highway_cul-de-sac_level"] = "xxx"
        self.analyser["osmosis_way_approximate"] = "xxx"
        self.analyser["osmosis_highway_area_access"] = "xxx"

class default_country_fr(default_country):
    def __init__(self, part, country, polygon_id=None, proj=None, analyser_options={},
                 download_repo=GEOFABRIK, download_country=None):

        analyser_options = dict({"country": "FR", "language": "fr", "proj": proj, "addr:city-admin_level": "8,9", "municipality_ref": "ref:INSEE"}, **analyser_options)
        default_country.__init__(self, part, country, polygon_id, analyser_options,
                                        download_repo, download_country)

class france_region(default_country_fr):
    def __init__(self, region, polygon_id=None, proj=2154, analyser_options={},
                 download_repo=GEOFABRIK, download_country=None):

        default_country_fr.__init__(self, "europe", "france/" + region, polygon_id, proj, dict({"phone_code": "33", "phone_size": 8}, **analyser_options),
                                    download_repo, download_country)
        self.analyser["osmosis_building_geodesie_FR"] = "xxx"
        self.analyser["osmosis_natural_swimming-pool"] = "xxx"
        self.analyser["osmosis_fantoir"] = "xxx"
        self.analyser["osmosis_highway_motorway"] = "xxx"
        self.analyser["merge_traffic_signs"] = "xxx"

france_region("alsace", 8636)
france_region("aquitaine", 8637)
france_region("auvergne", 8638)
france_region("basse-normandie", 8646)
france_region("bourgogne", 27768)
france_region("bretagne", 102740)
france_region("centre", 8640)
france_region("champagne-ardenne", 8641)
france_region("corse", 76910)
france_region("franche-comte", 8642)
france_region("haute-normandie", 8656)
france_region("ile-de-france", 8649)
france_region("languedoc-roussillon", 8643)
france_region("limousin", 8644)
france_region("lorraine", 8645)
france_region("midi-pyrenees", 8647)
france_region("nord-pas-de-calais", 8648)
france_region("pays-de-la-loire", 8650)
france_region("picardie", 8651)
france_region("poitou-charentes", 8652)
france_region("provence-alpes-cote-d-azur", 8654)
france_region("rhone-alpes", 8655)

class france_region_dom(france_region):
    def __init__(self, region, polygon_id=None, proj=2154, analyser_options={},
                 download_repo=GEOFABRIK, download_country=None):

        france_region.__init__(self, region, polygon_id, proj, analyser_options, download_repo, download_country)
        self.analyser["merge_heritage_FR_merimee"] = "xxx"
        self.analyser["merge_poste_FR"] = "xxx"
        self.analyser["merge_school_FR"] = "xxx"
        self.analyser["merge_wikipedia_FR"] = "xxx"
        self.analyser["merge_college_FR"] = "xxx"
        self.analyser["merge_service_public_FR"] = "xxx"
        self.analyser["merge_pitch_FR"] = "xxx"
        self.analyser["merge_police_FR"] = "xxx"
        self.analyser["merge_pharmacy_FR"] = "xxx"
        self.analyser["merge_postal_code_FR"] = "xxx"
        self.analyser["merge_post_box_FR"] = "xxx"

france_region_dom("guadeloupe", 1401835, 32620, analyser_options = {"phone_code": "590", "phone_size": 8})
france_region_dom("guyane", 1260551, 2972, analyser_options = {"phone_code": "594", "phone_size": 8})
france_region_dom("martinique", 1891495, 32620, analyser_options = {"phone_code": "596", "phone_size": 8})
france_region_dom("mayotte", 1259885, 32738, analyser_options = {"phone_code": "262", "phone_size": 8})
france_region_dom("reunion", 1785276, 2975, analyser_options = {"phone_code": "262", "phone_size": 8})

class france_com(default_country_fr):
    def __init__(self, part, country, polygon_id=None, proj=None, analyser_options={},
                 download_repo=GEOFABRIK, download_country=None):

        default_country_fr.__init__(self, part, country, polygon_id, proj, analyser_options, download_repo, download_country)
        self.analyser["merge_wikipedia_FR"] = "xxx"
        self.analyser["merge_college_FR"] = "xxx"
        self.analyser["merge_service_public_FR"] = "xxx"
        self.analyser["merge_pitch_FR"] = "xxx"
        self.analyser["merge_police_FR"] = "xxx"
        self.analyser["merge_postal_code_FR"] = "xxx"

france_com("central-america", "france_saintbarthelemy", 537967, analyser_options = {"phone_code": "590", "phone_size": 6},
                   proj=2969, download_repo=OSMFR, download_country="saint_barthelemy")
france_com("central-america", "france_saintmartin", 1891583, analyser_options = {"phone_code": "590", "phone_size": 6},
                   proj=2969, download_repo=OSMFR, download_country="saint_martin")
france_com("north-america", "france_saintpierreetmiquelon", 233377, analyser_options = {"phone_code": "508", "phone_size": 6},
                   proj=32621, download_repo=OSMFR, download_country="saint_pierre_et_miquelon")
france_com("south-america", "france_wallisetfutuna", 290162, analyser_options = {"phone_code": "681", "phone_size": 6},
                   proj=32701, download_repo=OSMFR, download_country="wallis_et_futuna")
france_com("south-america", "france_polynesie", 3412620, analyser_options = {"phone_code": "689", "phone_size": 8},
                   proj=32706, download_repo=OSMFR, download_country="polynesie")
france_com("australia-oceania", "france_nouvellecaledonie", 3407643, analyser_options = {"country": "NC", "phone_code": "687", "phone_size": 6},
                   proj=3163, download_repo=GEOFABRIK, download_country="new-caledonia")

default_country("merge", "france_taaf", 6063103,
                download_repo=OSMFR, analyser_options={"country": "TF", "language": "fr", "proj": 32738})

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
france_local_db.analyser["merge_public_transport_FR_ratp"] = "xxx"
france_local_db.analyser["merge_public_transport_FR_stif"] = "xxx"
france_local_db.analyser["merge_railway_level_crossing_FR"] = "xxx"
france_local_db.analyser["merge_railway_railstation_FR"] = "xxx"
france_local_db.analyser["merge_tmc_point_FR"] = "xxx"
france_local_db.analyser["merge_geodesie"] = "xxx"
france_local_db.analyser["merge_street_number"] = "xxx"
france_local_db.analyser["merge_wikipedia_FR"] = "xxx"
france_local_db.analyser["merge_wikipedia_insee_FR"] = "xxx"
france_local_db.analyser["merge_college_FR"] = "xxx"
france_local_db.analyser["merge_service_public_FR"] = "xxx"
france_local_db.analyser["merge_public_transport_FR_transgironde"] = "xxx"
france_local_db.analyser["merge_public_transport_FR_tbm"] = "xxx"
france_local_db.analyser["merge_public_transport_FR_cg71"] = "xxx"
france_local_db.analyser["merge_public_transport_FR_stan"] = "xxx"
france_local_db.analyser["merge_recycling_FR_bm"] = "xxx"
france_local_db.analyser["merge_recycling_FR_capp_glass"] = "xxx"
france_local_db.analyser["merge_recycling_FR_capp_clothes"] = "xxx"
france_local_db.analyser["merge_recycling_FR_nm_glass"] = "xxx"
france_local_db.analyser["merge_parking_FR_capp"] = "xxx"
france_local_db.analyser["merge_parking_FR_bm"] = "xxx"
france_local_db.analyser["merge_tourism_FR_aquitaine_camp_caravan"] = "xxx"
france_local_db.analyser["merge_tourism_FR_aquitaine_museum"] = "xxx"
france_local_db.analyser["merge_tourism_FR_aquitaine_information"] = "xxx"
france_local_db.analyser["merge_bicycle_parking_FR_bordeaux"] = "xxx"
france_local_db.analyser["merge_bicycle_parking_FR_capp"] = "xxx"
france_local_db.analyser["merge_bicycle_rental_FR_bm"] = "xxx"
france_local_db.analyser["merge_public_equipment_FR_angers_toilets"] = "xxx"
france_local_db.analyser["merge_public_equipment_FR_bordeaux_toilets"] = "xxx"
france_local_db.analyser["merge_public_equipment_FR_lehavre_toilets"] = "xxx"
france_local_db.analyser["merge_public_equipment_FR_lyon_toilets"] = "xxx"
#france_local_db.analyser["merge_public_equipment_FR_montpellier_toilets"] = "xxx"
france_local_db.analyser["merge_public_equipment_FR_nantes_toilets"] = "xxx"
france_local_db.analyser["merge_public_equipment_FR_rennes_toilets"] = "xxx"
france_local_db.analyser["merge_public_equipment_FR_toulouse_toilets"] = "xxx"
france_local_db.analyser["merge_sport_FR_aquitaine_equestrian"] = "xxx"
france_local_db.analyser["merge_pitch_FR"] = "xxx"
france_local_db.analyser["merge_car_rental_FR_paris"] = "xxx"
france_local_db.analyser["merge_police_FR"] = "xxx"
france_local_db.analyser["merge_fuel_FR"] = "xxx"
france_local_db.analyser["merge_pharmacy_FR"] = "xxx"
france_local_db.analyser["merge_postal_code_FR"] = "xxx"
france_local_db.analyser["merge_library_FR_aquitaine"] = "xxx"
france_local_db.analyser["merge_winery_FR_aquitaine"] = "xxx"
france_local_db.analyser["merge_tourism_FR_aquitiane_museum"] = "xxx"
france_local_db.analyser["merge_restaurant_FR_aquitaine"] = "xxx"
france_local_db.analyser["merge_restaurant_FR_cg71"] = "xxx"
france_local_db.analyser["merge_geodesie_support_FR"] = "xxx"
france_local_db.analyser["merge_post_box_FR"] = "xxx"
france_local_db.analyser["merge_public_transport_FR_star"] = "xxx"
france_local_db.analyser["merge_power_generator_FR"] = "xxx"
france_local_db.analyser["merge_power_substation_FR"] = "xxx"
france_local_db.analyser["merge_power_tower_FR"] = "xxx"
france_local_db.analyser["merge_shop_FR"] = "xxx"
france_local_db.analyser["merge_restriction_motorway_FR"] = "xxx"
france_local_db.analyser["merge_restriction_FR_92"] = "xxx"
france_local_db.analyser["merge_power_substation_minor_FR"] = "xxx"

#########################################################################

default_country("europe", "albania", 53292, {"country": "AL", "language": "sq", "proj": 32634})
default_country("europe", "andorra", 9407, {"country": "AD", "language": "ca", "proj": 2154})
default_country("europe", "azores",  1629146, {"country": "PT", "language": "pt", "proj": 32627}, download_repo=GEOFABRIK)
default_country("europe", "belarus", 59065, {"country": "BY", "language": ["be", "ru"], "proj": 32635}, download_repo=GEOFABRIK)
#default_country("europe", "belgium", 52411, {"country": "BE", "language": "fr", "proj": 32631})
brussels_capital_region = default_country("europe", "belgium/brussels_capital_region", 54094, {"country": "BE", "language": ["fr", "nl"], "proj": 32631, "multilingual-style": "be", "municipality_ref": "ref:INS"}, download_repo=OSMFR)
default_country("europe", "belgium/flanders", 53134, {"country": "BE", "language": "nl", "proj": 32631, "municipality_ref": "ref:INS"}, download_repo=OSMFR)
default_country("europe", "belgium/wallonia_french_community", 2620920, {"country": "BE", "language": "fr", "proj": 32631, "municipality_ref": "ref:INS"}, download_repo=OSMFR)
default_country("europe", "belgium/wallonia_german_community", 2425209, {"country": "BE", "language": "de", "proj": 32631, "municipality_ref": "ref:INS"}, download_repo=OSMFR)
default_country("europe", "bosnia-herzegovina", 2528142, {"country": "BA", "proj": 32633}, download_repo=GEOFABRIK)
default_country("europe", "bulgaria", 186382, {"country": "BG", "language": "bg", "proj": 32635}, download_repo=GEOFABRIK)
default_country("europe", "croatia", 214885, {"country": "HR", "language": "hr", "proj": 32633}, download_repo=GEOFABRIK)
default_country("europe", "estonia", 79510, {"country": "EE", "language": "et", "proj": 32634}, download_repo=GEOFABRIK)
default_country("europe", "cyprus", 307787, {"country": "CY", "driving_side": "left", "proj": 32636})
default_country("europe", "faroe-islands", 52939, {"country": "FO", "language": "fo", "proj": 2169})
default_country("europe", "greece",  192307, {"country": "GR", "language": "el","proj": 32635}, download_repo=GEOFABRIK)
default_country("europe", "guernesey", 270009, {"country": "GG", "language": "en", "driving_side": "left", "proj": 32630}, download_repo=OSMFR)
default_country("europe", "hungary", 21335, {"country": "HU", "language": "hu", "proj": 32633}, download_repo=GEOFABRIK)
default_country("europe", "ireland", 62273, {"country": "IE", "driving_side": "left", "language": ["en", "ga"], "proj": 32629}, download_repo=OSMFR)
default_country("europe", "isle-of-man", 62269, {"country": "IM", "language": "en", "driving_side": "left", "proj": 32630})
default_country("europe", "jersey", 367988, {"country": "JE", "language": "en", "driving_side": "left", "proj": 32630}, download_repo=OSMFR)
default_country("europe", "kosovo", 2088990, {"country": "XK", "proj": 32634})
default_country("europe", "liechtenstein", 1155955, {"country": "LI", "language": "de", "proj": 32632})
lithuania = default_country("europe", "lithuania", 72596, {"country": "LT", "language": "lt", "proj": 32635, "osmosis_way_approximate": {"highway": ("motorway", "trunk", "primary", "secondary", "tertiary")}}, download_repo=GEOFABRIK)
del(lithuania.analyser["osmosis_highway_cul-de-sac_level"]) # follow official highway classification
del(lithuania.analyser["osmosis_highway_broken_level_continuity"]) # follow official highway classification
default_country("europe", "latvia", 72594, {"country": "LV","language": "lv", "proj": 32634}, download_repo=GEOFABRIK)
default_country("europe", "luxembourg", 2171347, {"country": "LU", "language": "fr", "proj": 2169, "boundary_detail_level": 6})
default_country("europe", "malta", 365307, {"country": "MT", "language": "en", "driving_side": "left", "proj": 32633})
default_country("europe", "macedonia", 53293, {"country": "MK", "language": "sq", "proj": 32634})
default_country("europe", "moldova", 58974, {"country": "MD", "language": "ro", "proj": 32635}, download_repo=GEOFABRIK)
default_country("europe", "monaco", 1124039, {"country": "MC", "language": "fr", "proj": 2154}, download_repo=OSMFR)
default_country("europe", "montenegro", 53296, {"country": "ME", "proj": 32634})
default_country("europe", "norway", 2978650, {"country": "NO", "language": "no", "proj": 32632})
default_country("europe", "portugal",  295480, {"country": "PT", "language": "pt", "proj": 32629}, download_repo=GEOFABRIK)
default_country("europe", "romania", 90689, {"country": "RO", "language": "ro", "proj": 31700})
default_country("europe", "serbia", 1741311, {"country": "RS", "language": "sr", "proj": 32634}, download_repo=GEOFABRIK)
default_country("europe", "slovenia", 218657, {"country": "SI", "proj": 32633}, download_repo=GEOFABRIK)
default_country("europe", "sweden", 52822, {"country": "SE", "language": "sv", "proj": 32633})
default_country("europe", "switzerland", 51701, {"country": "CH", "proj": 2056, "municipality_ref": "swisstopo:SHN"})
default_country("europe", "turkey", 174737, {"country": "TR", "language": "tr", "proj": 32636}, download_repo=GEOFABRIK)
default_country("europe", "ukraine", 60199, {"country": "UA", "language": "uk", "proj": 32636}, download_repo=GEOFABRIK)
default_country("europe", "united_kingdom_akrotiri_and_dhekelia", 3263728, {"country": "GB", "driving_side": "left", "proj": 32636},
                download_country="cyprus")  # British Sovereign Base in Cyprus
default_country("europe", "united_kingdom_gibraltar", 1278736, {"country": "GI", "language": "en", "proj": 32630},
                download_repo=OSMFR, download_country="gibraltar")
default_country("europe", "united_kingdom_northern_ireland", 156393, {"country": "IE", "driving_side": "left", "language": "en", "proj": 32629},
                download_repo=OSMFR, download_country="united_kingdom/northern_ireland")
default_country("europe", "united_kingdom_wales", 58437, {"country": "GB", "driving_side": "left", "proj": 32630},
                download_repo=GEOFABRIK, download_country="great-britain/wales")
default_country("europe", "united_kingdom_scotland", 58446, {"country": "GB", "driving_side": "left", "proj": 32630},
                download_repo=GEOFABRIK, download_country="great-britain/scotland")

iceland = default_country("europe","iceland", 299133, {"country": "IS", "language": "is", "proj": 32627}) # 299133
iceland.download["url"] = ""

default_country("europe", "finland", 54224, {"country": "FI", "language": ["fi", "sv"],  "proj": 32635},download_repo=GEOFABRIK)
default_country("europe", "denmark",  50046, {"country": "DK", "language": "da","proj": 32632}, download_repo=GEOFABRIK)

#########################################################################

default_country_simple("", "antarctica",  None, {"proj": 3031}, download_repo=GEOFABRIK)

#########################################################################

default_country("north-america", "greenland", 2184073, {"country": "GL", "language": "kl", "proj": 3184})
mexico = default_country("north-america", "mexico", 114686, {"country": "MX", "language": "es", "proj": 32614}, download_repo=GEOFABRIK)
del(mexico.analyser["osmosis_highway_name_close"]) # Complicated Street Numbering
default_country("north-america", "united_kingdom_bermuda", 1993208, {"country": "BM", "language": "en", "driving_side": "left", "proj": 32620}, download_repo=OSMFR, download_country="bermuda")


# United States of America
class us_state(default_country):
    def __init__(self, state, polygon_id=None, proj=None, analyser_options={},
                 download_repo=GEOFABRIK, download_country=None):

        analyser_options = dict({"country": "US", "language": "en", "proj": proj}, **analyser_options)
        default_country.__init__(self, "north-america", "usa_" + state, polygon_id, analyser_options,
                                    download_repo, download_country or ("us/" + state))

us_state("alabama", 161950, 26916)
us_state("alaska", 1116270, 26905)
us_state("arizona", 162018, 26912)
us_state("arkansas", 161646, 26715)
us_state("california", 165475, 26910)
us_state("colorado", 161961, 26713)
us_state("connecticut", 165794, 3507)
us_state("delaware", 162110, 3509)
us_state("district-of-columbia", 162069, 3559)
us_state("florida", 162050, 3513)
us_state("georgia", 161957, 26917)
us_state("hawaii", 166563, 2783) # note: projection for hawaii is the one used for center islands, not for the whole
us_state("idaho", 162116, 3741)
us_state("illinois", 122586, 3746)
us_state("indiana", 161816, 3745)
us_state("iowa", 161650, 3745)
us_state("kansas", 161644, 3744)
us_state("kentucky", 161655, 3088)
us_louisiana = us_state("louisiana", 224922, 3745)
del(us_louisiana.analyser["osmosis_waterway"]) # Too many swamp, not suitable
us_state("maine", 63512, 3749)
us_state("maryland", 162112, 26985)
us_state("massachusetts", 61315, 2805)
us_state("michigan", 165789, 3746)
us_state("minnesota", 165471, 26992)
us_state("mississippi", 161943, 3816)
us_state("missouri", 161638, 3601)
us_state("montana", 162115, 3604)
us_state("nebraska", 161648, 3606)
us_state("nevada", 165473, 3607)
us_state("new-hampshire", 67213, 3613)
us_state("new-jersey", 224951, 3615)
us_state("new-mexico", 162014, 3617)
us_state("new-york", 61320, 3623)
us_state("north-carolina", 224045, 3631)
us_state("north-dakota", 161653, 3633)
us_state("ohio", 162061, 26917)
us_state("oklahoma", 161645, 3639)
us_state("oregon", 165476, 3643)
us_state("pennsylvania", 162109, 3651)
us_state("rhode-island", 392915, 3653)
us_state("south-carolina", 224040, 3655)
us_state("south-dakota", 161652, 3659)
us_state("tennessee", 161838, 3661)
us_state("texas", 114690, 3082)
us_state("utah", 161993, 3675)
us_state("vermont", 60759, 3684)
us_state("virginia", 224042, 3968)
us_state("washington", 165479, 3725)
us_state("west-virginia",162068, 3747)
us_state("wisconsin", 165466, 3695)
us_state("wyoming", 161991, 26913)

default_country("oceania", "usa_guam", 306001, {"country": "GU", "language": "en", "proj": 32654}, download_repo=OSMFR, download_country="guam")
default_country("oceania", "usa_northern_mariana_islands", 306004, {"country": "MP", "language": "en", "proj": 32654}, download_repo=OSMFR, download_country="northern_mariana_islands")
default_country("south-america", "usa_american_samoa", 2177187, {"country": "AS", "language": "en", "proj": 32601}, download_repo=OSMFR, download_country="american_samoa")

# Canada
class canada_province(default_country):
    def __init__(self, province, polygon_id=None, proj=None, analyser_options={},
                 download_repo=GEOFABRIK, download_country=None):

        analyser_options = dict({"country": "CA", "language": "en", "proj": proj}, **analyser_options)
        default_country.__init__(self, "north-america", "canada_" + province, polygon_id, analyser_options,
                                    download_repo, download_country or ("canada/" + province))
        del(self.analyser["osmosis_waterway"]) # Too many crappy imports, not suitable

quebec = default_country("north-america", "canada/quebec", 61549, {"country": "CA","language": "fr", "proj": 2138}, download_repo=OSMFR)
quebec.download["diff"] = "http://download.openstreetmap.fr/replication/north-america/canada/quebec/minute/"
quebec.db_base = "osmose_canada_quebec"

canada_province("alberta", 391186, 32610)
canada_province("british-columbia", 390867, 32609)
canada_province("manitoba", 390841, 32615)
canada_province("new-brunswick", 68942, 32619)
canada_province("newfoundland-and-labrador", 391196, 32621)
canada_province("northwest-territories", 391220, 32612)
canada_province("nova-scotia", 390558, 32620)
canada_province("nunavut", 390840, 32616)
canada_province("ontario", 68841, 32616)
canada_province("prince-edward-island", 391115, 32620)
canada_province("saskatchewan", 391178, 32613)
canada_province("yukon", 391455, 32608)

#########################################################################

default_country("africa", "algeria", 192756,  {"country": "DZ", "language": ["ar", "fr"], "proj": 32631}, download_repo=OSMFR)
default_country_simple("africa", "angola", 195267, {"country": "AO", "language": "pt", "proj": 32733}, download_repo=OSMFR)
default_country("africa", "benin", 192784,    {"country": "BJ", "language": "fr", "proj": 32631}, download_repo=OSMFR)
default_country("africa", "botswana", 1889339, {"country": "BW", "language": "en", "driving_side": "left", "proj": 32734})
default_country("africa", "burkina_faso", 192783, {"country": "BF", "language": "fr", "proj": 32630}, download_repo=OSMFR)
default_country("africa", "burundi", 195269,  {"country": "BI", "proj": 32735}, download_repo=OSMFR)
default_country_simple("africa", "cameroon", 192830, {"country": "CM", "proj": 32632}, download_repo=OSMFR)
default_country_simple("africa", "cape_verde", 535774, {"country": "CV", "language": "pt", "proj": 32626}, download_repo=OSMFR)
default_country("africa", "central_african_republic", 192790, {"country": "CF", "proj": 32634}, download_repo=OSMFR)
default_country_simple("africa", "chad", 2361304,    {"country": "TD", "proj": 32634}, download_repo=OSMFR)
default_country_simple("africa", "comoros", 535790, {"country": "KM", "proj": 32738}, download_repo=OSMFR)
default_country("africa", "congo_brazzaville", 192794, {"country": "CG", "proj": 32733}, download_repo=OSMFR)
default_country("africa", "congo_kinshasa", 192795, {"country": "CD", "proj": 32734}, download_repo=OSMFR)
default_country_simple("africa", "djibouti", 192801, {"country": "DJ", "language": ["fr", "ar"], "proj": 32638, "multilingual-style": "ma"}, download_repo=OSMFR)
default_country("africa", "egypt", 1473947,   {"country": "EG", "language": "ar", "proj": 32635})
default_country_simple("africa", "equatorial_guinea", 192791, {"country": "GQ", "language": "es", "proj": 32732}, download_repo=OSMFR)
default_country_simple("africa", "eritrea", 296961, {"country": "ER", "proj": 32637}, download_repo=OSMFR)
default_country("africa", "ethiopia", 192800, {"country": "ET", "language": "en", "proj": 32638})
default_country_simple("africa", "gabon", 192793,    {"country": "GA", "language": "fr", "proj": 32732}, download_repo=OSMFR)
default_country("africa", "gambia", 192774, {"country": "GM", "language": "en", "proj": 32628}, download_repo=OSMFR)
default_country("africa", "ghana", 192781,    {"country": "GH", "language": "en", "proj": 32630}, download_repo=OSMFR)
default_country("africa", "guinea", 192778,   {"country": "GN", "language": "fr", "proj": 32628}, download_repo=OSMFR)
default_country("africa", "guinea-bissau", 192776, {"country": "GW", "language": "pt", "proj": 32628})
default_country("africa", "ivory_coast", 192779, {"country": "CI", "language": "fr", "proj": 32630}, download_repo=OSMFR)
default_country_simple("africa", "kenya", 192798,    {"country": "KE", "driving_side": "left", "proj": 32737}, download_repo=OSMFR)
default_country_simple("africa", "lesotho", 2093234, {"country": "LS", "driving_side": "left", "proj": 32735}, download_repo=OSMFR)
default_country_simple("africa", "liberia", 192780,  {"country": "LR", "language": "en", "proj": 32629})
default_country("africa", "libya", 192758,    {"country": "LY", "language": "ar", "proj": 32633})
default_country_simple("africa", "madagascar", 447325, {"country": "MG", "language": ["fr", "mg"], "proj": 32738}, download_repo=GEOFABRIK)
default_country_simple("africa", "malawi", 195290, {"country": "MW", "driving_side": "left", "proj": 32736}, download_repo=OSMFR)
default_country_simple("africa", "mali", 192785,     {"country": "ML", "language": "fr", "proj": 32630}, download_repo=OSMFR)
default_country("africa", "mauritania", 192763, {"country": "MR", "proj": 32628}, download_repo=OSMFR)
default_country_simple("africa", "mauritius", 535828, {"country": "MU", "driving_side": "left", "proj": 32740}, download_repo=OSMFR)
default_country("africa", "morocco", 3630439,  {"country": "MA", "language": ["ar", "fr", "zgh", "ber"], "proj": 32629, "multilingual-style": "ma"})
default_country_simple("africa", "mozambique", 195273, {"country": "MZ", "language": "pt", "driving_side": "left", "proj": 32736}, download_repo=OSMFR)
default_country_simple("africa", "namibia", 195266, {"country": "NA", "language": "en", "driving_side": "left", "proj": 32733}, download_repo=OSMFR)
default_country("africa", "niger", 192786,    {"country": "NE", "language": "fr", "proj": 32632}, download_repo=OSMFR)
default_country("africa", "nigeria", 192787,  {"country": "NG", "language": "en", "proj": 32633})
default_country("africa", "norway_bouvet_island", 2425963, {"country": "BV", "language": "no", "proj": 32729}, download_repo=OSMFR, download_country="bouvet_island")
default_country_simple("africa", "rwanda", 171496, {"country": "RW", "proj": 32735}, download_repo=OSMFR)
default_country_simple("africa", "sao_tome_and_principe", 535880, {"country": "ST", "proj": 32632}, download_repo=OSMFR)
default_country_simple("africa", "senegal", 192775,  {"country": "SN", "proj": 32628}, download_repo=OSMFR)
default_country_simple("africa", "seychelles", 536765, {"country": "SC", "driving_side": "left", "proj": 32739}, download_repo=OSMFR)
default_country("africa", "sierra-leone", 192777, {"country": "SL", "language": "en", "proj": 32629})
default_country("africa", "somalia", 192799,  {"country": "SO", "language": "so", "proj": 32638})
default_country_simple("africa", "south_africa", 87565, {"country": "ZA", "driving_side": "left", "proj": 32735}, download_repo=OSMFR)
default_country_simple("africa", "south_sudan", 1656678, {"country": "SS", "language": "en", "proj": 32635}, download_repo=OSMFR)
default_country_simple("africa", "sudan", 192789, {"country": "SD", "proj": 32636}, download_repo=OSMFR)
default_country_simple("africa", "swaziland", 88210, {"country": "SZ", "driving_side": "left", "proj": 32736}, download_repo=OSMFR)
default_country("africa", "tanzania", 195270, {"country": "TZ", "driving_side": "left", "proj": 32736})
default_country_simple("africa", "togo", 192782,     {"country": "TG", "language": "fr", "proj": 32631}, download_repo=OSMFR)
default_country("africa", "tunisia", 192757,  {"country": "TN", "language": ["ar", "fr"], "proj": 32632}, download_repo=OSMFR)
default_country_simple("africa", "uganda", 192796, {"country": "UG", "driving_side": "left", "proj": 32636}, download_repo=OSMFR)
default_country("africa", "united_kingdom_saint_helena_ascension_tristan_da_cunha", 1964272, {"country": "SH", "language": "en", "driving_side": "left", "proj": 32729}, download_repo=OSMFR, download_country="saint_helena_ascension_tristan_da_cunha")
default_country("africa", "western_sahara", 2559126, {"proj": 32629}, download_repo=OSMFR)
default_country_simple("africa", "zambia", 195271, {"country": "ZM", "language": "en", "driving_side": "left", "proj": 32736}, download_repo=OSMFR)
default_country_simple("africa", "zimbabwe", 195272, {"country": "ZW", "driving_side": "left", "proj": 32736}, download_repo=OSMFR)

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

default_country_simple("asia", "afghanistan", 303427, {"country": "AF", "proj": 32641}, download_repo=OSMFR)
default_country_simple("asia", "armenia", 364066, {"country": "AM", "language": "hy", "proj": 32641}, download_repo=OSMFR)
default_country_simple("asia", "azerbaijan", 364110, {"country": "AZ", "language": "az", "proj": 32638})
default_country_simple("asia", "bangladesh", 184640, {"country": "BD", "language": "bn", "driving_side": "left", "proj": 32646})
default_country_simple("asia", "bahrain", 378734, {"country": "BH", "language": "ar","proj": 32639}, download_repo=OSMFR)
default_country_simple("asia", "bhutan", 184629, {"country": "BT", "proj": 32646}, download_repo=OSMFR)
default_country_simple("asia", "brunei", 2103120, {"country": "BN", "driving_side": "left", "language": "ms", "proj": 32650}, download_repo=OSMFR)
default_country_simple("asia", "cambodia", 49898 , {"country": "KHM", "language": "km", "proj": 32648}, download_repo=OSMFR)
default_country_simple("asia", "east_timor", 305142, {"country": "TL", "proj": 32651}, download_repo=OSMFR)
default_country_simple("asia", "georgia", 28699, {"country": "GE", "language": "ka", "proj": 32637}, download_repo=OSMFR)
default_country_simple("asia", "israel", 1473946, {"country": "IL", "language": ["he", "ar"], "proj": 32636}, download_repo=OSMFR)
default_country_simple("asia", "iran", 304938, {"country": "IR", "language": "fa","proj": 32640}, download_repo=GEOFABRIK)
default_country_simple("asia", "iraq", 304934, {"country": "IQ", "language": "ar", "proj": 32638})
default_country_simple("asia", "jordan", 184818, {"country": "JO", "language": "ar", "proj": 32637})
default_country_simple("asia", "kazakhstan", 214665, {"country": "KZ", "proj": 32640}, download_repo=GEOFABRIK)
default_country_simple("asia", "kuwait", 305099, {"country": "KW", "language": "ar","proj": 32639}, download_repo=OSMFR)
default_country_simple("asia", "kyrgyzstan", 178009, {"country": "KG", "proj": 32643})
default_country_simple("asia", "laos", 49903, {"country": "LA", "proj": 32648}, download_repo=OSMFR)
default_country_simple("asia", "lebanon", 184843, {"country": "LB", "language": "ar", "proj": 32636})
default_country_simple("asia", "malaysia", 2108121 , {"country": "MY", "language": "ms", "driving_side": "left", "proj": 32649}, download_repo=OSMFR)
default_country_simple("asia", "maldives", 536773, {"country": "MV", "language": "dv", "proj": 32643}, download_repo=OSMFR)
default_country_simple("asia", "mongolia", 161033, {"country": "MN", "language": "mn", "proj": 32648})
default_country_simple("asia", "myanmar", 50371, {"country": "MM", "language": "my", "proj": 32646}, download_repo=OSMFR)
default_country_simple("asia", "north_korea", 192734, {"country": "KP", "language": "ko", "proj": 32652}, download_country="north-korea")
default_country_simple("asia", "nepal", 184633, {"country": "NP", "language": "ne", "driving_side": "left", "proj": 32645})
default_country_simple("asia", "oman", 305138, {"country": "OM", "language": "ar","proj": 32640}, download_repo=OSMFR)
default_country_simple("asia", "pakistan", 307573, {"country": "PK", "driving_side": "left", "proj": 32642})
default_country_simple("asia", "palestine", 1703814, {"country": "PS", "language": "ar", "proj": 32636}, download_repo=OSMFR)
default_country_simple("asia", "philippines", 2850940, {"country": "PH", "language": "en", "proj": 32651}, download_repo=GEOFABRIK)
default_country_simple("asia", "qatar", 305095, {"country": "QA", "language": "ar","proj": 32639}, download_repo=OSMFR)
default_country_simple("asia", "saudi_arabia", 307584, {"country": "SA", "language": "ar","proj": 32637}, download_repo=OSMFR)
default_country_simple("asia", "singapore", 536780 , {"country": "SG", "driving_side": "left", "proj": 32648}, download_repo=OSMFR)
default_country_simple("asia", "sri-lanka", 536807, {"country": "LK", "driving_side": "left", "proj": 32644})
default_country_simple("asia", "south_korea", 307756, {"country": "KR", "language": "ko", "proj": 32652}, download_country="south-korea")
default_country_simple("asia", "syria", 184840, {"country": "SY", "language": "ar", "proj": 32637})
default_country_simple("asia", "tajikistan", 214626, {"country": "TJ", "language": "tg", "proj": 32642})
default_country_simple("asia", "taiwan", 3777248, {"country": "TW", "language": ["zh_TW", "en"], "proj": 32651}, download_repo=GEOFABRIK)
default_country_simple("asia", "thailand", 2067731, {"country": "TH", "language": "th", "proj": 32647, "driving_side": "left"})
default_country_simple("asia", "turkmenistan", 223026, {"country": "TM", "language": "tk", "proj": 32640})
united_arab_emirates = default_country_simple("asia", "united_arab_emirates", 307763, {"country": "AE", "language": "ar","proj": 32640}, download_repo=OSMFR)
del(united_arab_emirates.analyser["osmosis_highway_name_close"]) # Complicated Street Numbering
default_country("asia", "united_kingdom_british_indian_ocean_territory", 1993867, {"country": "IO", "language": "en", "driving_side": "left", "proj": 32742}, download_repo=OSMFR, download_country="british_indian_ocean_territory")
default_country_simple("asia", "uzbekistan", 196240, {"country": "UZ", "proj": 32640}, download_repo=GEOFABRIK)
default_country_simple("asia", "vietnam", 49915, {"country": "VN", "language": "vi", "proj": 32648}, download_repo=GEOFABRIK)
default_country_simple("asia", "yemen", 305092, {"country": "YE", "language": "ar","proj": 32638}, download_repo=GEOFABRIK)

#########################################################################

class id_province(default_country_simple):
    def __init__(self, state, polygon_id=None, proj=23837, analyser_options={},
                 download_repo=OSMFR, download_country=None):

        analyser_options = dict({"country": "ID", "language": "id", "proj": proj, download_repo: download_repo}, **analyser_options)
        default_country_simple.__init__(self, "asia", "indonesia_" + state, polygon_id, analyser_options,
                                    download_repo, download_country or ("indonesia/" + state))

id_province("aceh", 2390836)
id_province("bali", 1615621)
id_province("bangka_belitung_islands", 3797243)
id_province("banten", 2388356)
id_province("bengkulu", 2390837)
id_province("central_java", 2388357)
id_province("central_kalimantan", 2388613)
id_province("central_sulawesi", 2388664)
id_province("east_java", 3438227)
id_province("east_kalimantan", 5449459)
id_province("east_nusa_tenggara", 2396778)
id_province("gorontalo", 2388665)
id_province("jakarta", 6362934)
id_province("jambi", 2390838)
id_province("lampung", 2390839)
id_province("maluku", 2396795)
id_province("north_kalimantan", 5449460)
id_province("north_maluku", 2396796)
id_province("north_sulawesi", 2388666)
id_province("north_sumatra", 2390843)
id_province("papua", 4521144)
id_province("riau", 2390840)
id_province("riau_islands", 3797244)
id_province("southeast_sulawesi", 2388668)
id_province("south_kalimantan", 2388615)
id_province("south_sulawesi", 2388667)
id_province("south_sumatra", 2390842)
id_province("west_java", 2388361)
id_province("west_kalimantan", 2388616)
id_province("west_nusa_tenggara", 1615622)
id_province("west_papua", 4521145)
id_province("west_sulawesi", 2388669)
id_province("west_sumatra", 2390841)
id_province("yogyakarta", 5616105)

#########################################################################

# central america

default_country("central-america", "belize", 287827, {"country": "BZ", "language": "en", "proj": 32616})
default_country("central-america", "costa_rica", 287667, {"country": "CR", "language": "es", "proj": 32617}, download_repo=OSMFR)
default_country("central-america", "el_salvador", 1520612, {"country": "SV", "language": "es", "proj": 32616}, download_repo=OSMFR)
default_country("central-america", "guatemala", 1521463, {"country": "GT", "language": "es", "proj": 32616})
default_country("central-america", "honduras", 287670, {"country": "HN", "language": "es", "proj": 32616}, download_repo=OSMFR)
default_country_simple("central-america", "panama", 287668, {"country": "PA", "language": "es", "proj": 32617}, download_repo=OSMFR)


# caribbean

default_country_simple("central-america", "haiti", 307829, {"country": "HT", "language": "fr", "proj": 32618},
                       download_repo=GEOFABRIK, download_country="haiti-and-domrep")

config["haiti"].analyser["osmosis_way_approximate"] = "xxx"

default_country("central-america", "antigua_and_barbuda", 536900, {"country": "BB", "language": "en", "driving_side": "left", "proj": 32620}, download_repo=OSMFR)
default_country("central-america", "barbados", 547511, {"country": "BB", "language": "en", "driving_side": "left", "proj": 32621}, download_repo=OSMFR)
default_country("central-america", "bahamas", 547469, {"country": "BS", "language": "en", "driving_side": "left", "proj": 32620}, download_repo=OSMFR)
default_country("central-america", "cuba", 307833, {"country": "CU", "language": "es", "proj": 32617})
default_country("central-america", "dominica", 307823, {"country": "DM", "driving_side": "left", "proj": 32620}, download_repo=OSMFR)
default_country("central-america", "dominican_republic", 307828, {"country": "DO", "language": "en", "proj": 32619},
                       download_repo=GEOFABRIK, download_country="haiti-and-domrep")
default_country("central-america", "grenada", 550727, {"country": "GD", "language": "en", "driving_side": "left", "proj": 32620}, download_repo=OSMFR)
default_country("central-america", "jamaica", 555017, {"country": "JM", "language": "en", "driving_side": "left", "proj": 32620}, download_repo=OSMFR)
default_country("central-america", "nicaragua", 287666, {"country": "NI", "language": "es", "proj": 32616}, download_repo=OSMFR)
default_country("central-america", "saint_lucia", 550728, {"country": "LC", "driving_side": "left", "proj": 32620}, download_repo=OSMFR)
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
default_country("oceania", "micronesia", 571802, {"country": "FM", "language": "en", "proj": 32656}, download_repo=OSMFR)
default_country("oceania", "papua_new_guinea", 307866, {"country": "PG", "language": "en","proj": 32755}, download_repo=OSMFR)
default_country("oceania", "solomon_islands", 1857436, {"country": "SB", "language": "en", "driving_side": "left", "proj": 32657}, download_repo=OSMFR)
default_country("oceania", "tuvalu", 2177266, {"country": "TV", "language": "en", "driving_side": "left", "proj": 32660}, download_repo=OSMFR)
default_country("oceania", "vanuatu", 2177246, {"country": "VU", "proj": 32658}, download_repo=OSMFR)

#########################################################################

default_country("merge", "fiji", 571747, {"country": "FJ", "language": "en", "driving_side": "left", "proj": 32660}, download_repo=OSMFR)
default_country("merge", "kiribati", 571178 , {"country": "KL", "language": "en", "driving_side": "left", "proj": 32660}, download_repo=OSMFR)

#########################################################################

class au_state(default_country):
    def __init__(self, state, polygon_id=None, proj=32755, analyser_options={},
                 download_repo=OSMFR, download_country=None):

        analyser_options = dict({"country": "AU", "language": "en", "driving_side": "left", "proj": proj}, **analyser_options)
        default_country.__init__(self, "oceania", "australia/" + state, polygon_id, analyser_options,
                                    download_repo, download_country)

au_state("australian_capital_territory", 2354197, 32755, download_repo=OSMFR)
au_state("new_south_wales", 2316593, 32755, download_repo=OSMFR)
au_state("northern_territory", 2316594, 32753, download_repo=OSMFR)
au_state("western_australia", 2316598, 32750, download_repo=OSMFR)
au_state("south_australia", 2316596, 32753, download_repo=OSMFR)
au_state("victoria", 2316741, 32755, download_repo=OSMFR)
au_state("queensland", 2316595, 32755, download_repo=OSMFR)
au_state("tasmania", 2369652, 32755, download_repo=OSMFR)

au_state("christmas_island", 2177207, 32648, analyser_options={"country": "CX"})
au_state("cocos_islands", 82636, 32646, analyser_options={"country": "CC"})
au_state("coral_sea_islands", 3225677, 32655)
au_state("norfolk_island", 2574988, 32658, analyser_options={"country": "NF"})


#########################################################################

default_country("south-america", "argentina", 286393, {"country": "AR", "language": "es", "proj": 32720})
default_country("south-america", "bolivia", 252645, {"country": "BO", "language": "es", "proj": 32720})
brazil = default_country("south-america", "brazil", 59470, {"country": "BR", "language": "pt", "proj": 32722})
del(brazil.analyser["osmosis_highway_name_close"]) # Complicated Street Numbering
default_country("south-america", "chile", 167454, {"country": "CL", "language": "es", "proj": 32718})
default_country("south-america", "cook_islands", 2184233, {"country": "CK", "language": "en", "driving_side": "left", "proj": 32603}, download_repo=OSMFR)
colombia = default_country("south-america", "colombia", 120027, {"country": "CO", "language": "es", "proj": 32618})
del(colombia.analyser["osmosis_highway_name_close"]) # Complicated Street Numbering
default_country("south-america", "ecuador", 108089, {"country": "EC", "language": "es", "proj": 32727})
default_country_simple("south-america", "guyana", 287083, {"country": "GY", "language": "en", "driving_side": "left", "proj": 32621}, download_repo=OSMFR)
default_country("south-america", "new_zealand_tokelau", 2186600, {"country": "TK", "language": "en", "driving_side": "left", "proj": 32602}, download_repo=OSMFR, download_country="tokelau")
default_country("south-america", "niue", 1558556, {"country": "NU", "language": "en", "driving_side": "left", "proj": 32602}, download_repo=OSMFR)
default_country("south-america", "paraguay", 287077, {"country": "PY", "language": "es", "proj": 32721}, download_repo=OSMFR)
default_country("south-america", "peru", 288247, {"country": "PE", "language": "es", "proj": 32718})
default_country("south-america", "samoa", 1872673, {"country": "WS", "language": "en", "driving_side": "left", "proj": 32602}, download_repo=OSMFR)
default_country("south-america", "tonga", 2186665 , {"country": "TO", "language": "en", "driving_side": "left", "proj": 32601}, download_repo=OSMFR)
default_country("south-america", "trinidad_and_tobago", 555717, {"country": "TT", "language": "en", "driving_side": "left","proj": 32620}, download_repo=OSMFR)
default_country_simple("south-america", "suriname", 287082, {"country": "SR", "language": "nl", "driving_side": "left", "proj": 32621}, download_repo=OSMFR)
default_country("south-america", "united_kingdom_falkland", 2185374, {"country": "FK", "language": "en", "driving_side": "left", "proj": 32721}, download_repo=OSMFR, download_country="falkland")
default_country("south-america", "united_kingdom_pitcairn", 2185375, {"country": "PN", "language": "en", "driving_side": "left", "proj": 32709}, download_repo=OSMFR, download_country="pitcairn")
default_country("south-america", "united_kingdom_south_georgia_and_south_sandwich", 1983628, {"country": "GS", "language": "en", "driving_side": "left", "proj": 32725}, download_repo=OSMFR, download_country="south_georgia_and_south_sandwich")
default_country("south-america", "uruguay", 287072, {"country": "UY", "language": "es", "proj": 32721})
default_country("south-america", "venezuela", 272644, {"country": "VE", "language": "es", "proj": 32620}, download_repo=OSMFR)

#########################################################################

class it_region(default_country):
    def __init__(self, region, polygon_id=None, part="europe/italy", proj=23032, analyser_options={},
                 download_repo=OSMFR, download_country=None):

        download_country = region.replace("-", "_")
        country = "italy_" + region
        analyser_options = dict({"country": "IT", "language": "it", "proj": proj, "municipality_ref": "ref:ISTAT"}, **analyser_options)
        default_country.__init__(self, part, country, polygon_id, analyser_options,
                                    download_repo, download_country)

it_region("abruzzo", 53937)
it_region("basilicata", 40137)
it_region("calabria", 1783980)
it_region("campania", 40218)
it_region("emilia-romagna", 42611)
it_region("friuli-venezia-giulia", 179296)
it_region("lazio", 40784)
it_region("liguria", 301482)
it_region("lombardia", 44879)
it_region("marche", 53060)
it_region("molise", 41256)
it_region("piemonte", 44874)
it_region("puglia", 40095)
it_region("sardegna", 279816)
it_region("sicilia", 39152)
it_region("toscana", 41977)
it_region("trentino-alto-adige", 45757, analyser_options={"language": ["it","de"]})
it_region("umbria", 42004)
it_region("valle-aosta", 2905554)
it_region("veneto", 43648)

#########################################################################

class nl_province(default_country):
    def __init__(self, province, polygon_id=None, part="europe/netherlands", proj=23032, analyser_options={},
                 download_repo=OSMFR, download_country=None):

        download_country = province.replace("-", "_")
        country = "netherlands_" + province
        analyser_options = dict({"country": "NL", "language": "nl", "proj": proj}, **analyser_options)
        default_country.__init__(self, part, country, polygon_id, analyser_options,
                                    download_repo, download_country)

nl_province("zuid-holland", 47772)
nl_province("zeeland", 47806)
nl_province("noord-brabant", 47696)
nl_province("limburg", 47793)
nl_province("gelderland", 47554)
nl_province("overijssel", 47608)
nl_province("drenthe", 47540)
nl_province("friesland", 47381, analyser_options={"language": ["nl", "fy"]})
nl_province("groningen", 47826)
nl_province("flevoland", 47407)
nl_province("utrecht", 47667)
nl_province("noord-holland", 47654)

nl_province("aruba",        1231749, part="central-america", proj=32620)
nl_province("curacao",      1216719, part="central-america", proj=32620)
nl_province("sint-maarten", 1231790, part="central-america", proj=32620)
nl_province("caribbean",    1216720, part="central-america", proj=32620)

#########################################################################

class cz_kraj(default_country):
    def __init__(self, kraj, polygon_id=None, proj=32633, analyser_options={},
                 download_repo=OSMFR, download_country=None):

        analyser_options = dict({"country": "CZ", "language": "cs", "proj": proj}, **analyser_options)
        default_country.__init__(self, "europe", "czech_republic/" + kraj, polygon_id, analyser_options,
                                    download_repo, download_country)

cz_kraj("praha", 435514)
cz_kraj("stredocesky", 442397)
cz_kraj("jihocesky", 442321)
cz_kraj("plzensky", 442466)
cz_kraj("karlovarsky", 442314)
cz_kraj("ustecky", 442452)
cz_kraj("liberecky", 442455)
cz_kraj("kralovehradecky", 442463)
cz_kraj("pardubicky", 442460)
cz_kraj("vysocina", 442453)
cz_kraj("jihomoravsky", 442311)
cz_kraj("olomoucky", 442459)
cz_kraj("moravskoslezsky", 442461)
cz_kraj("zlinsky", 442449)

#########################################################################

class pl_province(default_country):
    def __init__(self, province, polygon_id=None, proj=32634, analyser_options={},
                 download_repo=OSMFR, download_country=None):

        analyser_options = dict({"country": "PL", "language": "pl", "proj": proj}, **analyser_options)
        default_country.__init__(self, "europe", "poland/" + province, polygon_id, analyser_options,
                                    download_repo, download_country)

pl_province("dolnoslaskie", 224457)
pl_province("kujawsko_pomorskie", 223407)
pl_province("lubelskie", 130919)
pl_province("lubuskie", 130969)
pl_province("lodzkie", 224458)
pl_province("malopolskie", 224459)
pl_province("mazowieckie", 130935)
pl_province("opolskie", 224460)
pl_province("podkarpackie", 130957)
pl_province("podlaskie", 224461)
pl_province("pomorskie", 130975)
pl_province("slaskie", 224462)
pl_province("swietokrzyskie", 130914)
pl_province("warminsko_mazurskie", 223408)
pl_province("wielkopolskie", 130971)
pl_province("zachodniopomorskie", 104401)

#########################################################################

class de_state(default_country):
    def __init__(self, province, polygon_id=None, proj=32632, analyser_options={},
                 download_repo=GEOFABRIK, download_country=None):

        analyser_options = dict({"country": "DE", "language": "de", "proj": proj, "municipality_ref": "de:regionalschluessel"}, **analyser_options)
        default_country.__init__(self, "europe", "germany/" + province, polygon_id, analyser_options,
                                    download_repo, download_country)

de_state("baden-wuerttemberg", 62611)
#de_state("bayern", 2145268)
for (name, rel_id) in [("mittelfranken", 17614),
                       ("niederbayern", 17593),
                       ("oberbayern", 2145274),
                       ("oberfranken", 17592),
                       ("oberpfalz", 17596),
                       ("schwaben", 17657),
                       ("unterfranken", 17585)]:
    de_state("bayern/" + name, rel_id, download_repo=GEOFABRIK)

de_state("berlin", 62422)
de_state("brandenburg", 62504)
de_state("bremen", 62718)
de_state("hamburg", 62782)
de_state("hessen", 62650)
de_state("mecklenburg-vorpommern", 28322)
de_state("niedersachsen", 454192)
#de_state("nordrhein-westfalen", 62761)
for (name, rel_id) in [("arnsberg", 73340),
                       ("detmold", 73347),
                       ("dusseldorf", 63306),
                       ("koln", 72022),
                       ("munster", 63594)]:
    de_state("nordrhein_westfalen/" + name, rel_id, download_repo=OSMFR)

de_state("rheinland-pfalz", 62341)
de_state("saarland", 62372)
de_state("sachsen-anhalt", 62607)
de_state("sachsen", 62467)
de_state("schleswig-holstein", 51529)
de_state("thueringen", 62366)

#########################################################################

class at_state(default_country):
    def __init__(self, province, polygon_id=None, proj=32633, analyser_options={},
                 download_repo=OSMFR, download_country=None):

        analyser_options = dict({"country": "AT", "language": "de", "proj": proj}, **analyser_options)
        default_country.__init__(self, "europe", "austria/" + province, polygon_id, analyser_options,
                                    download_repo, download_country)

at_state("niederosterreich", 77189)
at_state("burgenland", 76909)
at_state("karnten", 52345)
at_state("oberosterreich", 102303)
at_state("salzburg", 86539)
at_state("steiermark", 35183)
at_state("tirol", 52343)
at_state("wien", 109166)
at_state("vorarlberg", 74942)

#########################################################################

class es_comm(default_country):
    def __init__(self, province, polygon_id=None, proj=32629, part="europe", analyser_options={},
                 download_repo=OSMFR, download_country=None):

        analyser_options = dict({"country": "ES", "language": "es", "proj": proj, "municipality_ref": "ine:municipio"}, **analyser_options)
        default_country.__init__(self, part, "spain/" + province, polygon_id, analyser_options,
                                    download_repo, download_country)

es_comm("andalucia", 349044, proj=32629)
es_comm("aragon", 349045, proj=32630)
es_comm("asturias", 349033, proj=32629)
es_comm("illes_balears", 348981, proj=32630, analyser_options={"language": "ca"})
es_comm("cantabria", 349013, proj=32630)
es_comm("castilla_la_mancha", 349052, proj=32630)
es_comm("castilla_y_leon", 349041, proj=32629)
es_comm("catalunya", 349053, proj=32630, analyser_options={"language": "ca"})
es_comm("comunitat_valenciana", 349043, proj=32630, analyser_options={"language": ["es", "ca"]})
es_comm("extremadura", 349050, proj=32629)
es_comm("galicia", 349036, proj=32629, analyser_options={"language": ["es", "gl"]})
es_comm("la_rioja", 348991, proj=32630)
es_comm("comunidad_de_madrid", 349055, proj=32630)
es_comm("comunidad_foral_de_navarra", 349027, proj=32630)
es_comm("euskadi", 349042, proj=32630, analyser_options={"language": ["es", "eu"]})
es_comm("region_de_murcia", 349047, proj=32630)

es_comm("canarias", 349048, proj=32628, part="africa")
es_comm("ceuta", 1154756, proj=32630, part="africa")
es_comm("melilla", 1154757, proj=32628, part="africa")

#########################################################################

class en_region(default_country):
    def __init__(self, province, polygon_id=None, proj=32630, part="europe", analyser_options={},
                 download_repo=OSMFR, download_country=None):

        analyser_options = dict({"country": "GB", "language": "en", "driving_side": "left", "proj": proj}, **analyser_options)
        default_country.__init__(self, "europe", "united_kingdom/england/" + province, polygon_id, analyser_options,
                                    download_repo, download_country)

en_region("east_midlands", 151279)
en_region("east", 151336)
en_region("greater_london", 175342)
en_region("north_east", 151164)
en_region("north_west", 151261)
en_region("south_east", 151304)
en_region("south_west", 151339, analyser_options={"language": ["en", "kw"]})
en_region("west_midlands", 151283)
en_region("yorkshire_and_the_humber", 151012)

#########################################################################

class sk_kraj(default_country):
    def __init__(self, province, polygon_id=None, proj=32634, part="europe", analyser_options={},
                 download_repo=OSMFR, download_country=None):

        analyser_options = dict({"country": "SK", "language": "sk", "proj": proj}, **analyser_options)
        default_country.__init__(self, "europe", "slovakia/" + province, polygon_id, analyser_options,
                                    download_repo, download_country)

sk_kraj("trnavsky", 388266)
sk_kraj("trenciansky", 388267)
sk_kraj("presovsky", 388271)
sk_kraj("nitriansky", 388268)
sk_kraj("kosicky", 388272)
sk_kraj("zilinsky", 388269)
sk_kraj("banskobystricky", 388270)
sk_kraj("bratislavsky", 388265)

#########################################################################

class india_state(default_country_simple):
    def __init__(self, state, polygon_id=None, proj=32644, analyser_options={},
                 download_repo=OSMFR, download_country=None):

        analyser_options = dict({"country": "IN",
                                 "language": ["hi", "en"],
                                 "driving_side": "left",
                                 "proj": proj,
                                }, **analyser_options)
        default_country_simple.__init__(self, "asia", "india/" + state, polygon_id, analyser_options,
                                    download_repo, download_country)

india_state("andhra_pradesh", 2022095, proj=32644)
india_state("arunachal_pradesh",2027346, proj=32646)
india_state("assam", 2025886, proj=32646)
india_state("bihar", 1958982, proj=32645)
india_state("chhattisgarh", 1972004, proj=32644)
india_state("goa", 1997192, proj=32643)
india_state("gujarat", 1949080, proj=32643)
india_state("haryana", 1942601, proj=32643)
india_state("himachal_pradesh", 364186, proj=32643)
india_state("jammu_and_kashmir", 1943188, proj=32643)
india_state("jharkhand", 1960191, proj=32645)
india_state("karnataka", 2019939, proj=32643)
india_state("kerala", 2018151, proj=32643)
india_state("madhya_pradesh", 1950071, proj=32643)
india_state("maharashtra", 1950884, proj=32643)
india_state("manipur", 2027869, proj=32646)
india_state("meghalaya", 2027521, proj=32646)
india_state("mizoram", 2029046, proj=32646)
india_state("nagaland", 2027973, proj=32646)
india_state("odisha", 1984022, proj=32645)
india_state("punjab", 1942686, proj=32643)
india_state("rajasthan", 1942920, proj=32643)
india_state("sikkim", 1791324, proj=32645)
india_state("tamil_nadu", 96905, proj=32644)
india_state("telangana", 3250963, proj=32646)
india_state("tripura", 2026458, proj=32644)
india_state("uttar_pradesh", 1942587, proj=32644)
india_state("uttarakhand", 374810, proj=32644)
india_state("west_bengal", 1960177, proj=32645)

india_state("andaman_and_nicobar_islands", 2025855, proj=32646)
india_state("chandigarh", 1942809, proj=32643)
india_state("dadra_and_nagar_haveli", 1952530, proj=32643)
india_state("daman_and_diu", 1953041, proj=32642)
india_state("lakshadweep", 2027460, proj=32643)
india_state("national_capital_territory_of_delhi", 1942586, proj=32643)
india_state("puducherry", 107001, proj=32643)

#########################################################################

class russia_region(default_country_simple):
    def __init__(self, iso_3166_2,  region, polygon_id=None, proj=None, analyser_options={},
                 download_repo="http://be.gis-lab.info/data/osm_dump/dump/latest/",
                 download_country=None):

        region = region.replace(" ", "_")
        region = region.replace("-", "_")

        analyser_options = dict({"country": "RU",
                                 "language": "ru",
                                 "proj": proj,
                                }, **analyser_options)
        default_country_simple.__init__(self, "", "russia_" + region, polygon_id, analyser_options,
                                    download_repo, download_country)

        self.download["url"] = "http://be.gis-lab.info/data/osm_dump/dump/latest/%s.osm.pbf" % iso_3166_2
        self.download["poly"] = "http://be.gis-lab.info/data/osm_dump/poly/%s.poly" % iso_3166_2

russia_region("RU-BEL", "belgorod oblast", 83184, proj=32637)
russia_region("RU-BRY", "bryansk oblast", 81997, proj=32636)
russia_region("RU-KGD", "kaliningrad oblast", 103906, proj=32634)
russia_region("RU-KLU", "kaluga oblast", 81995, proj=32636)
russia_region("RU-KRS", "kursk oblast", 72223, proj=32637)
russia_region("RU-LEN", "leningrad oblast", 176095, proj=32636)
russia_region("RU-NGR", "novgorod oblast", 89331, proj=32636)
russia_region("RU-ORL", "oryol oblast", 72224, proj=32637)
russia_region("RU-PSK", "pskov oblast", 155262, proj=32636)
russia_region("RU-SMO", "smolensk oblast", 81996, proj=32636)
russia_region("RU-TUL", "tula oblast", 81993, proj=32637)
russia_region("RU-TVE", "tver oblast", 2095259, proj=32637)
russia_region("RU-MOS", "moscow oblast", 51490, proj=32637)
russia_region("RU-RYA", "ryazan oblast", 71950, proj=32637)
russia_region("RU-LIP", "lipetsk oblast", 72169, proj=32637)
russia_region("RU-TAM", "tambov oblast", 72180, proj=32637)
russia_region("RU-VOR", "voronezh oblast", 72181, proj=32637)
russia_region("RU-PNZ", "penza oblast", 72182, proj=32638)
russia_region("RU-ULY", "ulyanovsk oblast", 72192, proj=32639)
russia_region("RU-SAR", "saratov oblast", 72193, proj=32638)
russia_region("RU-SAM", "samara oblast", 72194, proj=32639)
russia_region("RU-NIZ", "nizhny novgorod oblast", 72195, proj=32638)
russia_region("RU-VLA", "vladimir oblast", 72197, proj=32637)
russia_region("RU-VGG", "volgograd oblast", 77665, proj=32638)
russia_region("RU-ORE", "orenburg oblast", 77669, proj=32640)
russia_region("RU-CHE", "chelyabinsk oblast", 77687, proj=32641)
russia_region("RU-SVE", "sverdlovsk oblast", 79379, proj=32641)
russia_region("RU-YAR", "yaroslavl oblast", 81994, proj=32637)
russia_region("RU-ROS", "rostov oblast", 85606, proj=32637)
russia_region("RU-IVA", "ivanovo oblast", 85617, proj=32637)
russia_region("RU-KOS", "kostroma oblast", 85963, proj=32637)
russia_region("RU-AST", "astrakhan oblast", 112819, proj=32638)
russia_region("RU-KIR", "kirov oblast", 115100, proj=32639)
russia_region("RU-VLG", "vologda oblast", 115106, proj=32637)
russia_region("RU-KGN", "kurgan oblast", 140290, proj=32641)
russia_region("RU-TYU", "tyumen oblast", 140291, proj=32642)
russia_region("RU-OMS", "omsk oblast", 140292, proj=32643)
russia_region("RU-NVS", "novosibirsk oblast", 140294, proj=32644)
russia_region("RU-TOM", "tomsk oblast", 140295, proj=32644)
russia_region("RU-ARK", "arkhangelsk oblast", 140337, proj=32638)
russia_region("RU-KEM", "kemerovo oblast", 144763, proj=32645)
russia_region("RU-IRK", "irkutsk oblast", 145454, proj=32648)
russia_region("RU-AMU", "amur oblast", 147166, proj=32652)
russia_region("RU-MAG", "magadan oblast", 151228, proj=32656)
russia_region("RU-SAK", "sakhalin oblast", 394235, proj=32654)
russia_region("RU-MUR", "murmansk oblast", 2099216, proj=32636)
russia_region("RU-STA", "stavropol krai", 108081, proj=32638)
russia_region("RU-KDA", "krasnodar krai", 108082, proj=32637)
russia_region("RU-PER", "perm krai", 115135, proj=32640)
russia_region("RU-ALT", "altai krai", 144764, proj=32644)
russia_region("RU-ZAB", "zabaykalsky krai", 145730, proj=32650)
russia_region("RU-KHA", "khabarovsk krai", 151223, proj=32653)
russia_region("RU-PRI", "primorsky krai", 151225, proj=32653)
russia_region("RU-KAM", "kamchatka krai", 151233, proj=32658)
russia_region("RU-KYA", "krasnoyarsk krai", 190090, proj=32646)
russia_region("RU-MOW", "moscow", 102269, proj=32637)
russia_region("RU-SPE", "saint petersburg", 337422, proj=32636)
russia_region("RU-KHM", "khanty-mansi autonomous okrug", 140296, proj=32642)
russia_region("RU-CHU", "chukotka autonomous okrug", 151231, proj=32659)
russia_region("RU-YAN", "yamalo-nenets autonomous okrug", 191706, proj=32643)
russia_region("RU-NEN", "nenets autonomous okrug", 274048, proj=32639)
russia_region("RU-YEV", "jewish autonomous oblast", 147167, proj=32653)
russia_region("RU-KR", "karelia republic", 393980, proj=32636)
russia_region("RU-MO", "mordovia republic", 72196, proj=32638)
russia_region("RU-BA", "bashkortostan republic", 77677, proj=32640)
russia_region("RU-TA", "tatarstan republic", 79374, proj=32639)
russia_region("RU-CU", "chuvash republic", 80513, proj=32639)
russia_region("RU-KL", "kalmykia republic", 108083, proj=32638)
russia_region("RU-DA", "dagestan republic", 109876, proj=32638)
russia_region("RU-CE", "chechen republic", 109877, proj=32638)
russia_region("RU-KC", "karachay-cherkess republic", 109878, proj=32638)
russia_region("RU-KB", "kabardino-balkar republic", 109879, proj=32638)
russia_region("RU-SE", "north ossetia-alania republic", 110032, proj=32638)
russia_region("RU-ME", "mari el republic", 115114, proj=32639)
russia_region("RU-UD", "udmurt republic", 115134, proj=32639)
russia_region("RU-KO", "komi republic", 115136, proj=32640)
russia_region("RU-AL", "altai republic", 145194, proj=32645)
russia_region("RU-TY", "tuva republic", 145195, proj=32646)
russia_region("RU-BU", "buryatia republic", 145729, proj=32647)
russia_region("RU-SA", "sakha republic", 151234, proj=32652)
russia_region("RU-KK", "khakassia republic", 190911, proj=32646)
russia_region("RU-IN", "ingushetia republic", 253252, proj=32638)
russia_region("RU-AD", "adygea republic", 253256, proj=32637)

#########################################################################

class japan_region(default_country_simple):
    def __init__(self, region, polygon_id=None, proj=32654, analyser_options={},
                 download_repo=OSMFR, download_country=None):

        analyser_options = dict({"country": "JP",
                                 "language": "ja",
                                 "driving_side": "left",
                                 "proj": proj,
                                }, **analyser_options)
        default_country_simple.__init__(self, "asia", "japan/" + region, polygon_id, analyser_options,
                                    download_repo, download_country)

japan_region("hokkaido", 3795658, proj=32654)
japan_region("tohoku", 1835900, proj=32654)
japan_region("kanto", 1803923, proj=32654)
japan_region("chubu", 532759, proj=32654)
japan_region("kansai", 357113, proj=32653)
japan_region("chugoku", 1842114, proj=32653)
japan_region("shikoku", 1847663, proj=32653)
japan_region("kyushu", 1842245, proj=32652)

#########################################################################

class china_province(default_country_simple):
    def __init__(self, region, polygon_id=None, proj=32654, analyser_options={},
                 download_repo=OSMFR, download_country=None):

        analyser_options = dict({"country": "CN",
                                 "language": "zh",
                                 "proj": proj,
                                }, **analyser_options)
        default_country_simple.__init__(self, "asia", "china/" + region, polygon_id, analyser_options,
                                    download_repo, download_country)


china_province("anhui", 913011, proj=32650)
china_province("fujian", 553303, proj=32650)
china_province("gansu", 153314, proj=32648)
china_province("guangdong", 911844, proj=32649)
china_province("guizhou", 286937, proj=32648)
china_province("hainan", 2128285, proj=32649)
china_province("hebei", 912998, proj=32650)
china_province("heilongjiang", 199073, proj=32652)
china_province("henan", 407492, proj=32650)
china_province("hubei", 913106, proj=32649)
china_province("hunan", 913073, proj=32649)
china_province("jiangsu", 913012, proj=32650)
china_province("jiangxi", 913109, proj=32650)
china_province("jilin", 198590, proj=32652)
china_province("liaoning", 912942, proj=32651)
china_province("qinghai", 153269, proj=32647)
china_province("shaanxi", 913100, proj=32649)
china_province("shandong", 913006, proj=32650)
china_province("shanxi", 913105, proj=32650)
china_province("sichuan", 913068, proj=32648)
china_province("yunnan", 913094, proj=32648)
china_province("zhejiang", 553302, proj=32651)

china_province("tibet", 153292, proj=32645)
china_province("xinjiang", 153310, proj=32645)
china_province("guangxi", 286342, proj=32649)
china_province("inner_mongolia", 161349, proj=32650)
china_province("ningxia", 913101, proj=32648)

china_province("beijing", 912940, proj=32650)
china_province("tianjin", 912999, proj=32650)
china_province("shanghai", 913067, proj=32651)
china_province("chongqing", 913069, proj=32649)

china_province("hong_kong", 913110, proj=32650, analyser_options={"language": ["zh", "en"], "driving_side": "left"})
china_province("macau", 1867188, proj=32649, analyser_options={"language": ["zh", "pt"]})

#########################################################################

ogf = default_simple("ogf", None, {"project": "opengeofiction"},
        download_url="http://opengeofiction.net/backup/ogf_latest.osm.pbf")
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

  for (k,v) in config.iteritems():
    print(k)
    print(json.dumps(v.__dict__, indent=4))
