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
    dir_scripts    = config.dir_osmose
    dir_osm2pgsql  = dir_scripts + "/osm2pgsql"
    bin_osm2pgsql  = config.bin_osm2pgsql
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

    def init(self):
        if self.db_base:
            self.db_string = "dbname=%s user=%s password=%s"%(self.db_base, self.db_user, self.db_password)
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

europe = template_config("europe")
europe.db_base = None
europe.download = {"dst": "/data/work/osmbin/extracts/europe/europe/europe.osm.pbf"}
europe.analyser["admin_level"] = "xxx"

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

        template_config.__init__(self, country, polygon_id, analyser_options, download_repo)
        if not download_country:
            download_country = country
        self.download = {
            "url": self.download_repo + part + "/" + download_country + "-latest.osm.pbf",
            "osmosis": country
        }
        if download_repo == GEOFABRIK:
            self.download["diff"] = self.download_repo + part + "/" + download_country + "-updates/"
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
        self.analyser["osmosis_railway_crossing"] = "xxx"
        self.analyser["osmosis_building_shapes"] = "xxx"
        self.analyser["osmosis_deadend"] = "xxx"
        self.analyser["osmosis_boundary_relation"] = "xxx"
        self.analyser["osmosis_highway_crossing"] = "xxx"
        self.analyser["osmosis_relation_restriction"] = "xxx"
        self.analyser["osmosis_tunnel_bridge"] = "xxx"
        self.analyser["osmosis_waterway"] = "xxx"
        self.analyser["osmosis_duplicated_geotag"] = "xxx"

class default_country(default_country_simple):
    def __init__(self, part, country, polygon_id=None, analyser_options=None,
                 download_repo=GEOFABRIK, download_country=None):

        default_country_simple.__init__(self, part, country, polygon_id, analyser_options,
                                        download_repo, download_country)
        self.analyser["osmosis_highway_cul-de-sac_level"] = "xxx"
        self.analyser["osmosis_way_approximate"] = "xxx"

class default_country_fr(default_country):
    def __init__(self, part, country, polygon_id=None, proj=None, analyser_options=None,
                 download_repo=GEOFABRIK, download_country=None):

        if not analyser_options:
            analyser_options = {}
        analyser_options.update({"country": "FR", "language": "fr", "proj": proj})
        default_country.__init__(self, part, country, polygon_id, analyser_options,
                                        download_repo, download_country)

class france_region(default_country_fr):
    def __init__(self, part, region, polygon_id=None, proj=2154, analyser_options=None,
                 download_repo=GEOFABRIK, download_country=None):

        country = "france_" + region.replace("-", "_")
        default_country_fr.__init__(self, part, country, polygon_id, proj, analyser_options,
                                    download_repo, download_country)
        self.download["url"]  = self.download_repo + part + "/" + region + "-latest.osm.pbf"
        self.download["diff"] = self.download_repo + part + "/" + region + "-updates/"
        self.analyser["osmosis_geodesie"] = "xxx"
        self.analyser["osmosis_natural_swimming-pool"] = "xxx"

france_region("europe/france", "alsace", 8636)
france_region("europe/france", "aquitaine", 8637)
france_region("europe/france", "auvergne", 8638)
france_region("europe/france", "basse-normandie", 8646)
france_region("europe/france", "bourgogne", 27768)
france_region("europe/france", "bretagne", 102740)
france_region("europe/france", "centre", 8640)
france_region("europe/france", "champagne-ardenne", 8641)
france_region("europe/france", "corse", None) # 76910
france_region("europe/france", "franche-comte", 8642)
france_region("europe/france", "haute-normandie", 8656)
france_region("europe/france", "ile-de-france", 8649)
france_region("europe/france", "languedoc-roussillon", 8643)
france_region("europe/france", "limousin", 8644)
france_region("europe/france", "lorraine", 8645)
france_region("europe/france", "midi-pyrenees", 8647)
france_region("europe/france", "nord-pas-de-calais", 8648)
france_region("europe/france", "pays-de-la-loire", 8650)
france_region("europe/france", "picardie", 8651)
france_region("europe/france", "poitou-charentes", 8652)
france_region("europe/france", "provence-alpes-cote-d-azur", 8654)
france_region("europe/france", "rhone-alpes", 8655)
france_region("europe/france", "guadeloupe", None, 32620) # 1401835
france_region("europe/france", "guyane", 1260551, 2972)
france_region("europe/france", "martinique", None, 32620) # 1891495
france_region("europe/france", "mayotte", None, 32738) # 1259885
france_region("europe/france", "reunion", None, 2975) # 1785276

default_country_fr("central-america", "france_saintbarthelemy", None, # 537967
                   proj=2969, download_repo=OSMFR, download_country="saint_barthelemy")
default_country_fr("central-america", "france_saintmartin", None, # 1891583
                   proj=2969, download_repo=OSMFR, download_country="saint_martin")
default_country_fr("north-america", "france_saintpierreetmiquelon", None, # 233377
                   proj=32621, download_repo=OSMFR, download_country="saint_pierre_et_miquelon")
default_country_fr("oceania", "france_wallisetfutuna", None, # 290162
                   proj=32701, download_repo=OSMFR, download_country="wallis_et_futuna")
default_country_fr("oceania", "france_polynesie", None, # 1363099
                   proj=32706, download_repo=OSMFR, download_country="polynesie")
default_country("australia-oceania", "france_nouvellecaledonie", None, # 2177258
                   download_repo=GEOFABRIK, download_country="new-caledonia", analyser_options={"country": "NC", "language": "fr", "proj": 3163})

###########################################################################

france_local_db = template_config("france_local_db", 1403916, {"country": "FR", "language": "fr", "proj": 2154})
france_local_db.db_base     = "osm"
france_local_db.db_user     = "osmose"
france_local_db.db_password = "clostAdtoi"
france_local_db.db_schema   = "\"$user\",osmosis"
france_local_db.sql_post_scripts = [
    france_local_db.dir_scripts + "/osmosis/CreateFunctions.sql",
    france_local_db.dir_scripts + "/osmosis/CreateMergeAnalyserCache.sql",
  ]

france_local_db.analyser["merge_merimee"] = "xxx"
france_local_db.analyser["merge_poste_FR"] = "xxx"
france_local_db.analyser["merge_school_FR"] = "xxx"
france_local_db.analyser["merge_ratp"] = "xxx"
france_local_db.analyser["merge_level_crossing_FR"] = "xxx"
france_local_db.analyser["merge_railstation_FR"] = "xxx"
france_local_db.analyser["merge_tmc_point_FR"] = "xxx"
france_local_db.analyser["merge_geodesie"] = "xxx"
france_local_db.analyser["merge_street_number"] = "xxx"
france_local_db.analyser["merge_wikipedia_FR"] = "xxx"
france_local_db.analyser["merge_wikipedia_insee_FR"] = "xxx"
france_local_db.analyser["merge_college_FR"] = "xxx"
france_local_db.analyser["merge_service_public_FR"] = "xxx"

#########################################################################

default_country("europe", "andorra", 9407, {"country": "AD", "language": "ca", "proj": 2154})
#default_country("europe", "belgium", 52411, {"country": "BE", "language": "fr", "proj": 32631})
default_country("europe", "belgium_brussels_capital_region", 54094, {"country": "BE", "proj": 32631},
                download_repo=OSMFR, download_country="belgium/brussels_capital_region")
default_country("europe", "belgium_flanders", 53134, {"country": "BE", "language": "nl", "proj": 32631},
                download_repo=OSMFR, download_country="belgium/flanders")
default_country("europe", "belgium_wallonia_french_community", 2620920, {"country": "BE", "language": "fr", "proj": 32631},
                download_repo=OSMFR, download_country="belgium/wallonia_french_community")
default_country("europe", "belgium_wallonia_german_community", 2425209, {"country": "BE", "language": "de", "proj": 32631},
                download_repo=OSMFR, download_country="belgium/wallonia_german_community")
default_country("europe", "luxembourg", 2171347, {"country": "LU", "language": "fr", "proj": 2169, "osmosis_boundary_hole": {"admin_level": 6}})
default_country("europe", "monaco", 1124039, {"country": "MC", "language": "fr", "proj": 2154}, download_repo=OSMFR)
default_country("europe", "norway", 1059668, {"country": "NO", "language": "no", "proj": 32632})
default_country("europe", "sweden", 52822, {"country": "SE", "language": "sv", "proj": 32633})
default_country("europe", "switzerland", 51701, {"country": "CH", "proj": 2056})

iceland = default_country("europe","iceland", None, {"country": "IS", "language": "is", "proj": 32627}) # 299133
iceland.download["url"] = ""

#########################################################################

default_country("north-america", "greenland", None, {"country": "GL", "language": "kl", "proj": 3184})  # 2184073

# United States of Ameria
default_country("north-america", "usa_delaware", 162110, {"country": "US", "language": "en", "proj": 3509},
                download_country="us/delaware")
default_country("north-america", "usa_district_of_columbia", 162069, {"country": "US", "language": "en", "proj": 3559},
                download_country="us/district-of-columbia")
# note: projection for hawaii is the one used for center islands, not for the whole
default_country("north-america", "usa_hawaii", None, {"country": "US", "language": "en", "proj": 2783},
                download_country="us/hawaii")

quebec = default_country("north-america", "canada_quebec", 61549, {"country": "QC","language": "fr", "proj": 2138},
                          download_repo=OSMFR, download_country="canada/quebec")
quebec.download["diff"] = "http://download.openstreetmap.fr/replication/north-america/canada/quebec/minute/"
quebec.db_base = "osmose_canada_quebec"

#########################################################################

default_country_simple("africa", "benin", 192784,    {"country": "BJ", "language": "fr", "proj": 32631}, download_repo=OSMFR)
default_country_simple("africa", "botswana", 1889339, {"country": "BW", "language": "en", "driving_side": "left", "proj": 32734})
default_country_simple("africa", "burkina_faso", 192783, {"country": "BF", "language": "fr", "proj": 32630}, download_repo=OSMFR)
default_country_simple("africa", "burundi", 195269,  {"country": "BI", "proj": 32735}, download_repo=OSMFR)
default_country_simple("africa", "cameroon", 192830, {"country": "CM", "proj": 32632}, download_repo=OSMFR)
default_country_simple("africa", "central_african_republic", 192790, {"country": "CF", "proj": 32634}, download_repo=OSMFR)
default_country_simple("africa", "congo_brazzaville", 192794, {"country": "CG", "proj": 32733}, download_repo=OSMFR)
default_country_simple("africa", "congo_kinshasa", 192795, {"country": "CD", "proj": 32734}, download_repo=OSMFR)
default_country_simple("africa", "chad", 2361304,    {"country": "TD", "proj": 32634}, download_repo=OSMFR)
default_country_simple("africa", "djibouti", 192801, {"country": "DJ", "language": "fr", "proj": 32638}, download_repo=OSMFR)
default_country_simple("africa", "egypt", 1473947,   {"country": "EG", "language": "ar", "proj": 32635})
default_country_simple("africa", "ethiopia", 192800, {"country": "ET", "language": "am", "proj": 32638})
default_country_simple("africa", "gabon", 192793,    {"country": "GA", "language": "fr", "proj": 32732}, download_repo=OSMFR)
default_country_simple("africa", "guinea", 192778,   {"country": "GN", "language": "fr", "proj": 32628}, download_repo=OSMFR)
default_country_simple("africa", "ivory_coast", 192779, {"country": "CI", "language": "fr", "proj": 32630}, download_repo=OSMFR)
default_country_simple("africa", "kenya", 192798,    {"country": "KE", "driving_side": "left", "proj": 32737}, download_repo=OSMFR)
default_country_simple("africa", "liberia", 192780,  {"country": "LR", "language": "en", "proj": 32629})
default_country_simple("africa", "libya", 192758,    {"country": "LY", "language": "ar", "proj": 32635})
default_country_simple("africa", "madagascar", None, {"country": "MG", "language": "fr", "proj": 32738}, download_repo=GEOFABRIK)
default_country_simple("africa", "morocco", 192691,  {"country": "MA", "language": "ar", "proj": 32629})
default_country_simple("africa", "mali", 192785,     {"country": "ML", "language": "fr", "proj": 32630}, download_repo=OSMFR)
default_country_simple("africa", "mauritania", 192763, {"country": "MR", "proj": 32628}, download_repo=OSMFR)
default_country_simple("africa", "niger", 192786,    {"country": "NE", "language": "fr", "proj": 32632}, download_repo=OSMFR)
default_country_simple("africa", "nigeria", 192787,  {"country": "NG", "language": "en", "proj": 32633})
default_country_simple("africa", "senegal", 192775,  {"country": "SN", "proj": 32628}, download_repo=OSMFR)
default_country_simple("africa", "sierra_leone", 192777, {"country": "SL", "language": "en", "proj": 32629})
default_country_simple("africa", "somalia", 192799,  {"country": "SO", "language": "so", "proj": 32638})
default_country_simple("africa", "tanzania", 195270, {"country": "TZ", "driving_side": "left", "proj": 32736})
default_country_simple("africa", "togo", 192782,     {"country": "TG", "language": "fr", "proj": 32631}, download_repo=OSMFR)

config["chad"].analyser["osmosis_way_approximate"] = "xxx"
config["djibouti"].analyser["osmosis_way_approximate"] = "xxx"
config["kenya"].analyser["osmosis_way_approximate"] = "xxx"
config["madagascar"].analyser["osmosis_way_approximate"] = "xxx"
config["mali"].analyser["osmosis_way_approximate"] = "xxx"
config["senegal"].analyser["osmosis_way_approximate"] = "xxx"
config["togo"].analyser["osmosis_way_approximate"] = "xxx"

#########################################################################

default_country_simple("asia", "philippines", None, {"country": "PH", "language": "en", "proj": 32651}, download_repo=GEOFABRIK)

#########################################################################

default_country_simple("central-america", "haiti", 307829, {"country": "HT", "proj": 32618},
                       download_repo=GEOFABRIK, download_country="haiti-and-domrep")

config["haiti"].analyser["osmosis_way_approximate"] = "xxx"

default_country("central-america", "nicaragua", 287666, {"country": "NI", "language": "es", "proj": 32616},
                download_repo=OSMFR)

#########################################################################

default_country("australia-oceania", "new_zealand", None,
                {"country": "NZ", "language": "en", "proj": 32759, "driving_side": "left"},
                download_country="new-zealand")

#########################################################################

class default_country_it(default_country):
    def __init__(self, part, country, polygon_id=None, proj=None, analyser_options=None,
                 download_repo=FMACH, download_country=None):

        if not analyser_options:
            analyser_options = {}
        analyser_options.update({"country": "IT", "language": "it", "proj": proj})
        default_country.__init__(self, part, country, polygon_id, analyser_options,
                                        download_repo, download_country)


class italy_region(default_country_it):
    def __init__(self, part, region, polygon_id=None, proj=23032, analyser_options=None,
                 download_repo=FMACH, download_country=None):

        country = "italy_" + region.replace("-", "_")
        default_country_it.__init__(self, part, country, polygon_id, proj, analyser_options,
                                    download_repo, download_country)

        self.download["url"] = self.download_repo + part + "/" + region + ".pbf"

# FMACH
italy_region("gfoss_geodata/osm/output_osm_regioni/", "abruzzo", 53937)
italy_region("gfoss_geodata/osm/output_osm_regioni/", "basilicata", 40137)
italy_region("gfoss_geodata/osm/output_osm_regioni/", "calabria", 1783980)
italy_region("gfoss_geodata/osm/output_osm_regioni/", "campania", 40218)
italy_region("gfoss_geodata/osm/output_osm_regioni/", "emilia-romagna", 42611)
italy_region("gfoss_geodata/osm/output_osm_regioni/", "friuli-venezia-giulia", 179296)
italy_region("gfoss_geodata/osm/output_osm_regioni/", "lazio", 40784)
italy_region("gfoss_geodata/osm/output_osm_regioni/", "liguria", 301482)
italy_region("gfoss_geodata/osm/output_osm_regioni/", "lombardia", 44879)
italy_region("gfoss_geodata/osm/output_osm_regioni/", "marche", 53060)
italy_region("gfoss_geodata/osm/output_osm_regioni/", "molise", 41256)
italy_region("gfoss_geodata/osm/output_osm_regioni/", "piemonte", 44874)
italy_region("gfoss_geodata/osm/output_osm_regioni/", "puglia", 40095)
italy_region("gfoss_geodata/osm/output_osm_regioni/", "sardegna", 279816)
italy_region("gfoss_geodata/osm/output_osm_regioni/", "sicilia", 39152)
italy_region("gfoss_geodata/osm/output_osm_regioni/", "toscana", 41977)
italy_region("gfoss_geodata/osm/output_osm_regioni/", "trentino-alto-adige", 45757)
italy_region("gfoss_geodata/osm/output_osm_regioni/", "umbria", 42004)
italy_region("gfoss_geodata/osm/output_osm_regioni/", "valle-aosta", 2905554)
italy_region("gfoss_geodata/osm/output_osm_regioni/", "veneto", 43648)

#########################################################################
# Passwords are stored in separate file, not on git repository
import osmose_config_password

osmose_config_password.set_password(config)
