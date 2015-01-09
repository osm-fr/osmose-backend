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
import modules.config as config

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
FMACH = "http://geodati.fmach.it/"

class template_config:

    clean_at_end   = True

    updt_url       = config.url_frontend_update
    results_url    = results_url
    dir_work       = config.dir_work
    dir_tmp        = config.dir_tmp
    dir_cache      = config.dir_cache
    dir_scripts    = config.dir_osmose
    osmosis_bin    = dir_scripts + "/osmosis/osmosis-0.41/bin/osmosis"
    osmosis_pre_scripts = [
        dir_scripts + "/osmosis/osmosis-0.41/script/pgsnapshot_schema_0.6.sql",
#       dir_scripts + "/osmosis/osmosis-0.41/script/pgsnapshot_schema_0.6_bbox.sql",
        dir_scripts + "/osmosis/osmosis-0.41/script/pgsnapshot_schema_0.6_linestring.sql",
    ]
    osmosis_post_scripts = [
        dir_scripts + "/osmosis/WaysCreatePolygon.sql",
        dir_scripts + "/osmosis/CreateFunctions.sql",
    ]
    osmosis_change_init_post_scripts = [  # Scripts to run on database initialisation
        dir_scripts + "/osmosis/osmosis-0.41/script/pgsnapshot_schema_0.6_action.sql",
        dir_scripts + "/osmosis/WaysCreateTriggerPolygon.sql",
    ]
    osmosis_change_post_scripts = [  # Scripts to run each time the database is updated
        dir_scripts + "/osmosis/CreateTouched.sql",
    ]
    dir_results    = config.dir_results
    dir_extracts   = config.dir_extracts
    dir_diffs      = config.dir_diffs

    db_base     = "osmose"
    db_user     = "osmose"
    db_password = "-osmose-"
    db_host     = None        # Use socket by default
    db_schema   = None

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
            self.analyser_options = None

        self.sql_post_scripts = []  # Scripts to run everytime, just before launching analysers

    def init(self):
        if self.db_base:
            self.db_string = ""
            if self.db_host:
                self.db_string += "host=%s " % self.db_host
            self.db_string += "dbname=%s " % self.db_base
            self.db_string += "user=%s " % self.db_user
            self.db_string += "password=%s "  % self.db_password

            self.db_psql_args = []
            if self.db_host:
                self.db_psql_args += ["-h", self.db_host]
            self.db_psql_args += ["-d", self.db_base]
            self.db_psql_args += ["-U", self.db_user]

            if self.db_schema is None:
                self.db_schema = "%s,\"$user\"" % self.country
        else:
            self.db_string = None

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

world = template_config("world")
world.analyser["osmbin_open_relations"] = "xxx"

###########################################################################

france = template_config("france", 1403916, {"country": "FR", "language": "fr"})
france.download = {
    "url": france.download_repo+"europe/france-latest.osm.gz",
    "osmosis": "france"
}
france.analyser["communes_manquantes"] = "xxx"

###########################################################################

class default_country_simple(template_config):
    def __init__(self, part, country, polygon_id=None, analyser_options=None,
                 download_repo=GEOFABRIK, download_country=None):

        if not download_country:
            download_country = country
        country = country.replace("-", "_").replace("/", "_")
        template_config.__init__(self, country, polygon_id, analyser_options, download_repo)
        self.download = {
            "url": self.download_repo + part + "/" + download_country + "-latest.osm.pbf",
            "poly": self.download_repo + part + "/" + download_country + ".poly",
            "osmosis": country
        }
        if download_repo == GEOFABRIK:
            self.download["diff"] = self.download_repo + part + "/" + download_country + "-updates/"
        if download_repo == OSMFR:
            self.download["poly"] = self.download["poly"].replace("/extracts/", "/polygons/")
            self.download["diff"] = self.download_repo + "../replication/" + part + "/" + download_country + "/minute/"
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
        self.analyser["osmosis_broken_highway_level_continuity"] = "xxx"
        self.analyser["osmosis_relation_large"] = "xxx"
        self.analyser["osmosis_mini_farm"] = "xxx"
        self.analyser["osmosis_surface_overlaps"] = "xxx"
        self.analyser["osmosis_useless"] = "xxx"
        self.analyser["osmosis_relation_multipolygon"] = "xxx"
        self.analyser["osmosis_boundary_intersect"] = "xxx"
        self.analyser["osmosis_node_like_way"] = "xxx"
        self.analyser["osmosis_boundary_administrative"] = "xxx"
        self.analyser["osmosis_tag_typo"] = "xxx"
        self.analyser["osmosis_cycleway_track"] = "xxx"
        self.analyser["osmosis_feature_on_way"] = "xxx"
        self.analyser["osmosis_building_shapes"] = "xxx"
        self.analyser["osmosis_deadend"] = "xxx"
        self.analyser["osmosis_boundary_relation"] = "xxx"
        self.analyser["osmosis_highway_crossing"] = "xxx"
        self.analyser["osmosis_relation_restriction"] = "xxx"
        self.analyser["osmosis_tunnel_bridge"] = "xxx"
        self.analyser["osmosis_waterway"] = "xxx"
        self.analyser["osmosis_duplicated_geotag"] = "xxx"
        self.analyser["osmosis_noexit"] = "xxx"

class default_country(default_country_simple):
    def __init__(self, part, country, polygon_id=None, analyser_options=None,
                 download_repo=GEOFABRIK, download_country=None):

        default_country_simple.__init__(self, part, country, polygon_id, analyser_options,
                                        download_repo, download_country)
        self.analyser["osmosis_highway_cul-de-sac_level"] = "xxx"
        self.analyser["osmosis_way_approximate"] = "xxx"

class default_country_fr(default_country):
    def __init__(self, part, country, polygon_id=None, proj=None, analyser_options={},
                 download_repo=GEOFABRIK, download_country=None):

        analyser_options = dict({"country": "FR", "language": "fr", "proj": proj, "addr:city-admin_level": "8,9"}, **analyser_options)
        default_country.__init__(self, part, country, polygon_id, analyser_options,
                                        download_repo, download_country)

class france_region(default_country_fr):
    def __init__(self, region, polygon_id=None, proj=2154, analyser_options={},
                 download_repo=GEOFABRIK, download_country=None):

        default_country_fr.__init__(self, "europe", "france/" + region, polygon_id, proj, analyser_options,
                                    download_repo, download_country)
        self.analyser["osmosis_geodesie"] = "xxx"
        self.analyser["osmosis_natural_swimming-pool"] = "xxx"
        self.analyser["osmosis_fantoir"] = "xxx"

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
france_region("guadeloupe", 1401835, 32620)
france_region("guyane", 1260551, 2972)
france_region("martinique", 1891495, 32620)
france_region("mayotte", 1259885, 32738)
france_region("reunion", 1785276, 2975)

default_country_fr("central-america", "france_saintbarthelemy", 537967,
                   proj=2969, download_repo=OSMFR, download_country="saint_barthelemy")
default_country_fr("central-america", "france_saintmartin", 1891583,
                   proj=2969, download_repo=OSMFR, download_country="saint_martin")
default_country_fr("north-america", "france_saintpierreetmiquelon", 233377,
                   proj=32621, download_repo=OSMFR, download_country="saint_pierre_et_miquelon")
default_country_fr("oceania", "france_wallisetfutuna", 290162,
                   proj=32701, download_repo=OSMFR, download_country="wallis_et_futuna")
default_country_fr("oceania", "france_polynesie", 1363099,
                   proj=32706, download_repo=OSMFR, download_country="polynesie")
default_country("australia-oceania", "france_nouvellecaledonie", 3407643,
                   download_repo=GEOFABRIK, download_country="new-caledonia", analyser_options={"country": "NC", "language": "fr", "proj": 3163})

###########################################################################

france_local_db = template_config("france_local_db", 1403916, {"country": "FR", "language": "fr", "proj": 2154})
france_local_db.db_base     = "osm"
france_local_db.db_user     = "osmose"
france_local_db.db_password = "clostAdtoi"
france_local_db.db_schema   = "\"$user\",osmosis"
france_local_db.sql_post_scripts += [
    france_local_db.dir_scripts + "/osmosis/CreateFunctions.sql",
    france_local_db.dir_scripts + "/osmosis/CreateMergeAnalyserCache.sql",
  ]

france_local_db.analyser["merge_heritage_FR_merimee"] = "xxx"
france_local_db.analyser["merge_poste_FR"] = "xxx"
france_local_db.analyser["merge_school_FR"] = "xxx"
france_local_db.analyser["merge_public_transport_FR_ratp"] = "xxx"
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
france_local_db.analyser["merge_public_transport_FR_tbc"] = "xxx"
france_local_db.analyser["merge_public_transport_FR_cg71"] = "xxx"
france_local_db.analyser["merge_recycling_FR_cub"] = "xxx"
france_local_db.analyser["merge_recycling_FR_capp_glass"] = "xxx"
france_local_db.analyser["merge_recycling_FR_capp_clothes"] = "xxx"
france_local_db.analyser["merge_parking_FR_capp"] = "xxx"
france_local_db.analyser["merge_parking_FR_cub"] = "xxx"
france_local_db.analyser["merge_tourism_FR_gironde_camp_caravan"] = "xxx"
france_local_db.analyser["merge_tourism_FR_gironde_museum"] = "xxx"
france_local_db.analyser["merge_tourism_FR_gironde_information"] = "xxx"
france_local_db.analyser["merge_bicycle_parking_FR_bordeaux"] = "xxx"
france_local_db.analyser["merge_bicycle_parking_FR_capp"] = "xxx"
france_local_db.analyser["merge_bicycle_rental_FR_cub"] = "xxx"
france_local_db.analyser["merge_bicycle_rental_FR_capp"] = "xxx"
france_local_db.analyser["merge_public_equipment_FR_bordeaux_toilets"] = "xxx"
france_local_db.analyser["merge_sport_FR_gironde_equestrian"] = "xxx"
france_local_db.analyser["merge_pitch_FR"] = "xxx"
france_local_db.analyser["merge_car_rental_FR_paris"] = "xxx"
france_local_db.analyser["merge_police_FR"] = "xxx"
france_local_db.analyser["merge_fuel_FR"] = "xxx"
france_local_db.analyser["merge_pharmacy_FR"] = "xxx"
france_local_db.analyser["merge_postal_code_FR"] = "xxx"
france_local_db.analyser["merge_library_FR_aquitaine"] = "xxx"
france_local_db.analyser["merge_winery_FR_aquitaine"] = "xxx"
france_local_db.analyser["merge_restaurant_FR_aquitaine"] = "xxx"
france_local_db.analyser["merge_restaurant_FR_cg71"] = "xxx"

#########################################################################

default_country("europe", "albania", 53292, {"country": "AL", "language": "sq", "proj": 32634})
default_country("europe", "andorra", 9407, {"country": "AD", "language": "ca", "proj": 2154})
default_country("europe", "austria",  16239, {"country": "AT", "language": "de","proj": 32633}, download_repo=GEOFABRIK)
default_country("europe", "azores",  1629146, {"country": "PT", "language": "pt", "proj": 32627}, download_repo=GEOFABRIK)
#default_country("europe", "belgium", 52411, {"country": "BE", "language": "fr", "proj": 32631})
default_country("europe", "belgium/brussels_capital_region", 54094, {"country": "BE", "proj": 32631}, download_repo=OSMFR)
default_country("europe", "belgium/flanders", 53134, {"country": "BE", "language": "nl", "proj": 32631}, download_repo=OSMFR)
default_country("europe", "belgium/wallonia_french_community", 2620920, {"country": "BE", "language": "fr", "proj": 32631}, download_repo=OSMFR)
default_country("europe", "belgium/wallonia_german_community", 2425209, {"country": "BE", "language": "de", "proj": 32631}, download_repo=OSMFR)
default_country("europe", "bosnia-herzegovina", 2528142, {"country": "BA", "proj": 32633}, download_repo=GEOFABRIK)
default_country("europe", "bulgaria", 186382, {"country": "BG", "language": "bg", "proj": 32635}, download_repo=GEOFABRIK)
default_country("europe", "croatia", 214885, {"country": "HR", "language": "hr", "proj": 32633}, download_repo=GEOFABRIK)
default_country("europe", "estonia", 79510, {"country": "EE", "language": "et", "proj": 32634}, download_repo=GEOFABRIK)
default_country("europe", "cyprus", 307787, {"country": "CY", "driving_side": "left", "proj": 32636})
default_country("europe", "faroe-islands", 52939, {"country": "FO", "language": "fo", "proj": 2169})
default_country("europe", "greece",  192307, {"country": "GR", "language": "el","proj": 32635}, download_repo=GEOFABRIK)
default_country("europe", "hungary", 21335, {"country": "HU", "language": "hu", "proj": 32633}, download_repo=GEOFABRIK)
default_country("europe", "isle-of-man", 62269, {"country": "IM", "language": "en", "driving_side": "left", "proj": 32630})
default_country("europe", "kosovo", 2088990, {"country": "XK", "proj": 32634})
default_country("europe", "liechtenstein", 1155955, {"country": "LI", "language": "de", "proj": 32632})
default_country("europe", "lithuania", 72596, {"country": "LT", "language": "lt", "proj": 32635}, download_repo=GEOFABRIK)
default_country("europe", "latvia", 72594, {"country": "LV","language": "lv", "proj": 32634}, download_repo=GEOFABRIK)
default_country("europe", "luxembourg", 2171347, {"country": "LU", "language": "fr", "proj": 2169, "osmosis_boundary_hole": {"admin_level": 6}})
default_country("europe", "malta", 365307, {"country": "MT", "language": "en", "driving_side": "left", "proj": 32633})
default_country("europe", "macedonia", 53293, {"country": "MK", "language": "sq", "proj": 32634})
default_country("europe", "moldova", 58974, {"country": "MD", "language": "ro", "proj": 32635}, download_repo=GEOFABRIK)
default_country("europe", "monaco", 1124039, {"country": "MC", "language": "fr", "proj": 2154}, download_repo=OSMFR)
default_country("europe", "montenegro", 53296, {"country": "ME", "proj": 32634})
default_country("europe", "norway", 1059668, {"country": "NO", "language": "no", "proj": 32632})
default_country("europe", "portugal",  295480, {"country": "PT", "language": "pt", "proj": 32629}, download_repo=GEOFABRIK)
default_country("europe", "romania", 90689, {"country": "RO", "language": "ro", "proj": 31700})
default_country("europe", "serbia", 1741311, {"country": "RS", "language": "sr", "proj": 32634}, download_repo=GEOFABRIK)
default_country("europe", "slovakia",  14296, {"country": "SK", "language": "sk","proj": 32634}, download_repo=GEOFABRIK)
default_country("europe", "slovenia", 218657, {"country": "SI", "proj": 32633}, download_repo=GEOFABRIK)
default_country("europe", "sweden", 52822, {"country": "SE", "language": "sv", "proj": 32633})
default_country("europe", "switzerland", 51701, {"country": "CH", "proj": 2056})
default_country("europe", "united_kingdom_wales", 58437, {"country": "GB", "driving_side": "left", "proj": 32630},
                download_repo=GEOFABRIK, download_country="great-britain/wales")
default_country("europe", "united_kingdom_scotland", 58446, {"country": "GB", "driving_side": "left", "proj": 32630},
                download_repo=GEOFABRIK, download_country="great-britain/scotland")

config["belgium_wallonia_french_community"].analyser["merge_public_transport_BE_wallonia"] = "xxx"
config["belgium_wallonia_german_community"].analyser["merge_public_transport_BE_wallonia"] = "xxx"
config["belgium_wallonia_french_community"].sql_post_scripts += [
    config["belgium_wallonia_french_community"].dir_scripts + "/osmosis/CreateMergeAnalyserCache.sql",
]
config["belgium_wallonia_german_community"].sql_post_scripts += [
    config["belgium_wallonia_german_community"].dir_scripts + "/osmosis/CreateMergeAnalyserCache.sql",
]

iceland = default_country("europe","iceland", 299133, {"country": "IS", "language": "is", "proj": 32627}) # 299133
iceland.download["url"] = ""

default_country("europe", "finland", 54224, {"country": "FI", "language": ["fi", "sv"],  "proj": 32635},download_repo=GEOFABRIK)
default_country("europe", "denmark",  50046, {"country": "DK", "language": "da","proj": 32632}, download_repo=GEOFABRIK)

#########################################################################

default_country_simple("", "antarctica",  None, {"proj": 3031}, download_repo=GEOFABRIK)

#########################################################################

default_country("north-america", "greenland", 2184073, {"country": "GL", "language": "kl", "proj": 3184})

# United States of Ameria
default_country("north-america", "usa_delaware", 162110, {"country": "US", "language": "en", "proj": 3509},
                download_country="us/delaware")
default_country("north-america", "usa_district_of_columbia", 162069, {"country": "US", "language": "en", "proj": 3559},
                download_country="us/district-of-columbia")
# note: projection for hawaii is the one used for center islands, not for the whole
default_country("north-america", "usa_hawaii", None, {"country": "US", "language": "en", "proj": 2783},
                download_country="us/hawaii")

quebec = default_country("north-america", "canada/quebec", 61549, {"country": "QC","language": "fr", "proj": 2138}, download_repo=OSMFR)
quebec.download["diff"] = "http://download.openstreetmap.fr/replication/north-america/canada/quebec/minute/"
quebec.db_base = "osmose_canada_quebec"

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
default_country_simple("africa", "djibouti", 192801, {"country": "DJ", "language": "fr", "proj": 32638}, download_repo=OSMFR)
default_country("africa", "egypt", 1473947,   {"country": "EG", "language": "ar", "proj": 32635})
default_country_simple("africa", "equatorial_guinea", 192791, {"country": "GQ", "language": "es", "proj": 32732}, download_repo=OSMFR)
default_country_simple("africa", "eritrea", 296961, {"country": "ER", "proj": 32637}, download_repo=OSMFR)
default_country("africa", "ethiopia", 192800, {"country": "ET", "language": "en", "proj": 32638})
default_country_simple("africa", "gabon", 192793,    {"country": "GA", "language": "fr", "proj": 32732}, download_repo=OSMFR)
default_country("africa", "ghana", 192781,    {"country": "GH", "language": "en", "proj": 32630}, download_repo=OSMFR)
default_country("africa", "guinea", 192778,   {"country": "GN", "language": "fr", "proj": 32628}, download_repo=OSMFR)
default_country("africa", "guinea-bissau", 192776, {"country": "GW", "language": "pt", "proj": 32628})
default_country("africa", "ivory_coast", 192779, {"country": "CI", "language": "fr", "proj": 32630}, download_repo=OSMFR)
default_country_simple("africa", "kenya", 192798,    {"country": "KE", "driving_side": "left", "proj": 32737}, download_repo=OSMFR)
default_country_simple("africa", "lesotho", 2093234, {"country": "LS", "driving_side": "left", "proj": 32735}, download_repo=OSMFR)
default_country_simple("africa", "liberia", 192780,  {"country": "LR", "language": "en", "proj": 32629})
default_country("africa", "libya", 192758,    {"country": "LY", "language": "ar", "proj": 32633})
default_country_simple("africa", "madagascar", 447325, {"country": "MG", "language": "fr", "proj": 32738}, download_repo=GEOFABRIK)
default_country_simple("africa", "malawi", 195290, {"country": "MW", "driving_side": "left", "proj": 32736}, download_repo=OSMFR)
default_country_simple("africa", "mali", 192785,     {"country": "ML", "language": "fr", "proj": 32630}, download_repo=OSMFR)
default_country("africa", "mauritania", 192763, {"country": "MR", "proj": 32628}, download_repo=OSMFR)
default_country_simple("africa", "mauritius", 535828, {"country": "MU", "driving_side": "left", "proj": 32740}, download_repo=OSMFR)
default_country("africa", "morocco", 3630439,  {"country": "MA", "language": ["ar", "fr"], "proj": 32629})
default_country_simple("africa", "mozambique", 195273, {"country": "MZ", "language": "pt", "driving_side": "left", "proj": 32736}, download_repo=OSMFR)
default_country_simple("africa", "namibia", 195266, {"country": "NA", "language": "en", "driving_side": "left", "proj": 32733}, download_repo=OSMFR)
default_country("africa", "niger", 192786,    {"country": "NE", "language": "fr", "proj": 32632}, download_repo=OSMFR)
default_country("africa", "nigeria", 192787,  {"country": "NG", "language": "en", "proj": 32633})
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

#########################################################################

default_country_simple("asia", "azerbaijan", 364110, {"country": "AZ", "language": "az", "proj": 32638})
default_country_simple("asia", "bangladesh", 184640, {"country": "BD", "language": "bn", "driving_side": "left", "proj": 32646})
default_country_simple("asia", "brunei", 2103120, {"country": "BN", "driving_side": "left", "language": "ms", "proj": 32650}, download_repo=OSMFR)
default_country_simple("asia", "cambodia", 49898 , {"country": "KHM", "language": "km", "proj": 32648}, download_repo=OSMFR)
default_country_simple("asia", "iraq", 304934, {"country": "IQ", "language": "ar", "proj": 32638})
default_country_simple("asia", "jordan", 184818, {"country": "JO", "language": "ar", "proj": 32637})
default_country_simple("asia", "kyrgyzstan", 178009, {"country": "KG", "proj": 32643})
default_country_simple("asia", "laos", 49903, {"country": "LA", "proj": 32648}, download_repo=OSMFR)
default_country_simple("asia", "lebanon", 184843, {"country": "LB", "language": "ar", "proj": 32636})
default_country_simple("asia", "malaysia", 2108121 , {"country": "MY", "language": "ms", "driving_side": "left", "proj": 32649}, download_repo=OSMFR)
default_country_simple("asia", "mongolia", 161033, {"country": "MN", "language": "mn", "proj": 32648})
default_country_simple("asia", "myanmar", 50371, {"country": "MM", "language": "my", "proj": 32646}, download_repo=OSMFR)
default_country_simple("asia", "pakistan", 307573, {"country": "PK", "driving_side": "left", "proj": 32642})
default_country_simple("asia", "philippines", 2850940, {"country": "PH", "language": "en", "proj": 32651}, download_repo=GEOFABRIK)
default_country_simple("asia", "singapore", 536780 , {"country": "SG", "driving_side": "left", "proj": 32648}, download_repo=OSMFR)
default_country_simple("asia", "sri-lanka", 536807, {"country": "LK", "driving_side": "left", "proj": 32644})
default_country_simple("asia", "syria", 184840, {"country": "SY", "language": "ar", "proj": 32637})
default_country_simple("asia", "tajikistan", 214626, {"country": "TJ", "language": "tg", "proj": 32642})
default_country_simple("asia", "thailand", 2067731, {"country": "TH", "language": "th", "proj": 32647, "driving_side": "left"})
default_country_simple("asia", "turkmenistan", 223026, {"country": "TM", "language": "tk", "proj": 32640})
default_country_simple("asia", "vietnam", 49915, {"country": "VN", "language": "vi", "proj": 32648}, download_repo=GEOFABRIK)

#########################################################################

default_country_simple("central-america", "haiti", 307829, {"country": "HT", "language": "fr", "proj": 32618},
                       download_repo=GEOFABRIK, download_country="haiti-and-domrep")

config["haiti"].analyser["osmosis_way_approximate"] = "xxx"

default_country("central-america", "antigua_and_barbuda", 536900, {"country": "BB", "language": "en", "driving_side": "left", "proj": 32620}, download_repo=OSMFR)
default_country("central-america", "bahamas", 547469, {"country": "BS", "language": "en", "driving_side": "left", "proj": 32620}, download_repo=OSMFR)
default_country("central-america", "belize", 287827, {"country": "BZ", "language": "en", "proj": 32616})
default_country("central-america", "cuba", 307833, {"country": "CU", "language": "es", "proj": 32617})
default_country("central-america", "dominican_republic", 307828, {"country": "DO", "language": "en", "proj": 32619},
                       download_repo=GEOFABRIK, download_country="haiti-and-domrep")
default_country("central-america", "guatemala", 1521463, {"country": "GT", "language": "es", "proj": 32616})
default_country("central-america", "grenada", 550727, {"country": "GD", "language": "en", "driving_side": "left", "proj": 32620}, download_repo=OSMFR)
default_country("central-america", "jamaica", 555017, {"country": "JM", "language": "en", "driving_side": "left", "proj": 32620}, download_repo=OSMFR)
default_country("central-america", "nicaragua", 287666, {"country": "NI", "language": "es", "proj": 32616}, download_repo=OSMFR)
default_country("central-america", "saint_lucia", 550728, {"country": "LC", "driving_side": "left", "proj": 32620}, download_repo=OSMFR)


#########################################################################

default_country("australia-oceania", "new-zealand", 556706, {"country": "NZ", "language": "en", "proj": 32759, "driving_side": "left"})

#########################################################################

default_country("south-america", "argentina", 286393, {"country": "AR", "language": "es", "proj": 32720})
default_country("south-america", "bolivia", 252645, {"country": "BO", "language": "es", "proj": 32720})
default_country("south-america", "brazil", 59470, {"country": "BR", "language": "pt", "proj": 32722})
default_country("south-america", "chile", 167454, {"country": "CL", "language": "es", "proj": 32718})
default_country("south-america", "colombia", 120027, {"country": "CO", "language": "es", "proj": 32618})
default_country("south-america", "ecuador", 108089, {"country": "EC", "language": "es", "proj": 32727})
default_country_simple("south-america", "guyana", 287083, {"country": "GY", "language": "en", "driving_side": "left", "proj": 32621}, download_repo=OSMFR)
default_country("south-america", "paraguay", 287077, {"country": "PY", "language": "es", "proj": 32721}, download_repo=OSMFR)
default_country("south-america", "peru", 288247, {"country": "PE", "language": "es", "proj": 32718})
default_country("south-america", "trinidad_and_tobago", 555717, {"country": "TT", "language": "en", "driving_side": "left","proj": 32620}, download_repo=OSMFR)
default_country_simple("south-america", "suriname", 287082, {"country": "SR", "language": "nl", "proj": 32621}, download_repo=OSMFR)
default_country("south-america", "uruguay", 287072, {"country": "UY", "language": "es", "proj": 32721})
default_country("south-america", "venezuela", 272644, {"country": "VE", "language": "es", "proj": 32620}, download_repo=OSMFR)

#########################################################################

class it_region(default_country):
    def __init__(self, region, polygon_id=None, proj=23032, analyser_options={},
                 download_repo=FMACH, download_country=None):

        part = "gfoss_geodata/osm/output_osm_regioni/"
        analyser_options = dict({"country": "IT", "language": "it", "proj": proj}, **analyser_options)
        default_country.__init__(self, part, "italy/" + region, polygon_id, analyser_options,
                                    download_repo, download_country)

        self.download["url"] = self.download_repo + part + "/" + region + ".pbf"
        self.download["poly"] = self.download_repo + part + "/" + region + ".poly"

# FMACH
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
        del(self.analyser["osmosis_mini_farm"]) # Landuse are really too detailed in Netherlands to use this analyser

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

        analyser_options = dict({"country": "DE", "language": "de", "proj": proj}, **analyser_options)
        default_country.__init__(self, "europe", "germany/" + province, polygon_id, analyser_options,
                                    download_repo, download_country)

#de_state("baden-wuerttemberg", 62611)
#de_state("bayern", 2145268)
de_state("berlin", 62422)
de_state("brandenburg", 62504)
de_state("bremen", 62718)
de_state("hamburg", 62782)
de_state("hessen", 62650)
de_state("mecklenburg-vorpommern", 28322)
#de_state("niedersachsen", 454192)
#de_state("nordrhein-westfalen", 62761)
de_state("rheinland-pfalz", 62341)
de_state("saarland", 62372)
de_state("sachsen-anhalt", 62607)
de_state("sachsen", 62467)
de_state("schleswig-holstein", 51529)
de_state("thueringen", 62366)

#########################################################################
# Passwords are stored in separate file, not on git repository
import osmose_config_password

osmose_config_password.set_password(config)
