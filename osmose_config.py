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
from modules.OrderedDict import OrderedDict
import modules.config as config

hostname = open("/etc/hostname").read().strip()
available_results_urls = {"osm1": "http://osm1.crans.org/osmose/",
                          "osm3": "http://osm3.crans.org/osmose/",
                          "osm4": "http://osm4.crans.org/osmose/",
                          "osm5": "http://osm5.univ-nantes.fr/osmose/",
                          "osm6": "http://osm6.univ-nantes.fr/osmose/",
                          "osm7": "http://osm7.pole-aquinetic.fr/~osmose/results",
                          "osm8": "http://osm8.pole-aquinetic.fr/~osmose/results",
                         }
if hostname in available_results_urls:
    results_url = available_results_urls[hostname]
else:
    results_url = None

###########################################################################

GEOFABRIK = "http://download.geofabrik.de/"
OSMFR = "http://download.openstreetmap.fr/extracts/"

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
    "dst": template_config.dir_extracts+"/france.osm",
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
            "dst": template_config.dir_extracts + "/" + country + ".osm.pbf",
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
        self.analyser["osmosis_missing_parent_tag"] = "xxx"
        self.analyser["osmosis_polygon"] = "xxx"
        self.analyser["osmosis_highway_vs_building"] = "xxx"
        self.analyser["osmosis_orphan_nodes_cluster"] = "xxx"
        self.analyser["osmosis_powerline"] = "xxx"
        self.analyser["osmosis_double_tagging"] = "xxx"
        self.analyser["osmosis_associatedStreet"] = "xxx"
        self.analyser["osmosis_highway_link"] = "xxx"
        self.analyser["osmosis_broken_highway_level_continuity"] = "xxx"
        self.analyser["osmosis_large_relation"] = "xxx"
        self.analyser["osmosis_mini_farm"] = "xxx"
        self.analyser["osmosis_surface_overlaps"] = "xxx"
        self.analyser["osmosis_useless"] = "xxx"
        self.analyser["osmosis_multipolygon"] = "xxx"
        self.analyser["osmosis_boundary_intersect"] = "xxx"
        self.analyser["osmosis_node_like_way"] = "xxx"
        self.analyser["osmosis_boundary_administrative"] = "xxx"
        self.analyser["osmosis_tag_typo"] = "xxx"
        self.analyser["osmosis_cycleway_track"] = "xxx"
        self.analyser["osmosis_crossing"] = "xxx"
        self.analyser["osmosis_building_shapes"] = "xxx"
        self.analyser["osmosis_deadend"] = "xxx"
        self.analyser["osmosis_boundary_relation"] = "xxx"
        self.analyser["osmosis_highway_crossing"] = "xxx"
        self.analyser["osmosis_relation_restriction"] = "xxx"
        self.analyser["osmosis_tunnel_bridge"] = "xxx"

class default_country(default_country_simple):
    def __init__(self, part, country, polygon_id=None, analyser_options=None,
                 download_repo=GEOFABRIK, download_country=None):

        default_country_simple.__init__(self, part, country, polygon_id, analyser_options,
                                        download_repo, download_country)
        self.analyser["osmosis_highway_cul-de-sac_level"] = "xxx"
        self.analyser["osmosis_way_approximate"] = "xxx"
        self.analyser["osmosis_riverbank"] = "xxx"

class default_country_fr(default_country):
    def __init__(self, part, country, polygon_id=None, analyser_options=None,
                 download_repo=GEOFABRIK, download_country=None):

        if not analyser_options:
            analyser_options = {}
        analyser_options.update({"country": "FR", "language": "fr"})
        default_country.__init__(self, part, country, polygon_id, analyser_options,
                                        download_repo, download_country)

class france_region(default_country_fr):
    def __init__(self, part, region, polygon_id=None, analyser_options=None,
                 download_repo=GEOFABRIK, download_country=None):

        country = "france_" + region.replace("-", "_")
        default_country_fr.__init__(self, part, country, polygon_id, analyser_options,
                                    download_repo, download_country)
        self.download["url"] = self.download_repo+part+"/"+region+"-latest.osm.pbf"
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
france_region("europe/france", "guadeloupe", None) # 1401835
france_region("europe/france", "guyane", 1260551)
france_region("europe/france", "martinique", None) # 1891495
france_region("europe/france", "mayotte", None) # 1259885
france_region("europe/france", "reunion", None) # 1785276

default_country_fr("central-america", "france_saintbarthelemy", None, # 537967
                   download_repo=OSMFR, download_country="saint_barthelemy")
default_country_fr("central-america", "france_saintmartin", None, # 1891583
                   download_repo=OSMFR, download_country="saint_martin")
default_country_fr("north-america", "france_saintpierreetmiquelon", None, # 233377
                   download_repo=OSMFR, download_country="saint_pierre_et_miquelon")
default_country_fr("oceania", "france_wallisetfutuna", None, # 290162
                   download_repo=OSMFR, download_country="wallis_et_futuna")
default_country_fr("oceania", "france_polynesie", None, # 1363099
                   download_repo=OSMFR, download_country="polynesie")
default_country_fr("australia-oceania", "france_nouvellecaledonie", None, # 2177258
                   download_repo=GEOFABRIK, download_country="new-caledonia")

###########################################################################

france_local_db = template_config("france_local_db", 1403916)
france_local_db.db_base     = "osm"
france_local_db.db_user     = "osmose"
france_local_db.db_password = "clostAdtoi"
france_local_db.db_schema   = "\"$user\",osmosis"

france_local_db.analyser["merge_merimee"] = "xxx"
france_local_db.analyser["merge_poste_fr"] = "xxx"
france_local_db.analyser["merge_school_fr"] = "xxx"
france_local_db.analyser["merge_ratp"] = "xxx"
france_local_db.analyser["merge_level_crossing_fr"] = "xxx"
france_local_db.analyser["merge_railstation_fr"] = "xxx"
france_local_db.analyser["merge_tmc_point_fr"] = "xxx"
france_local_db.analyser["merge_geodesie"] = "xxx"
france_local_db.analyser["merge_street_number_toulouse"] = "xxx"
france_local_db.analyser["merge_wikipedia_FR"] = "xxx"
france_local_db.analyser["merge_wikipedia_insee_FR"] = "xxx"

#########################################################################

default_country("europe", "belgium", 52411, {"country": "BE","language": "fr"})
default_country("europe", "luxembourg", 2171347, {"country": "LU", "language": "fr", "osmosis_boundary_hole": {"admin_level": 6}})
default_country("europe", "monaco", 1124039, {"country": "MC", "language": "fr"}, download_repo=OSMFR)
default_country("europe", "switzerland", 51701, {"country": "CH"})

iceland = default_country("europe","iceland", None, {"country": "IS", "language": "is"}) # 299133
iceland.download["url"] = ""

quebec = default_country("north-america", "canada_quebec", 61549, {"country": "QC","language": "fr"},
                          download_repo=OSMFR, download_country="canada/quebec")
quebec.db_base = "osmose_quebec"
quebec.db_password = "clostAdtoi"
quebec.download["diff"] = "http://download.openstreetmap.fr/replication/north-america/canada/quebec/minute/"

#########################################################################

default_country_simple("africa", "benin", 192784,    {"country": "BJ", "language": "fr"}, download_repo=OSMFR)
default_country_simple("africa", "burkina_faso", 192783, {"country": "BF", "language": "fr"}, download_repo=OSMFR)
default_country_simple("africa", "burundi", 195269,  {"country": "BI"}, download_repo=OSMFR)
default_country_simple("africa", "cameroon", 192830, {"country": "CM"}, download_repo=OSMFR)
default_country_simple("africa", "central_african_republic", 192790, {"country": "CF"}, download_repo=OSMFR)
default_country_simple("africa", "congo_brazzaville", 192794, {"country": "CG"}, download_repo=OSMFR)
default_country_simple("africa", "congo_kinshasa", 192795, {"country": "CD"}, download_repo=OSMFR)
default_country_simple("africa", "chad", 2361304,    {"country": "TD"}, download_repo=OSMFR)
default_country_simple("africa", "djibouti", 192801, {"country": "DJ", "language": "fr"}, download_repo=OSMFR)
default_country_simple("africa", "gabon", 192793,    {"country": "GA", "language": "fr"}, download_repo=OSMFR)
default_country_simple("africa", "guinea", 192778,   {"country": "GN", "language": "fr"}, download_repo=OSMFR)
default_country_simple("africa", "ivory_coast", 192779, {"country": "CI", "language": "fr"}, download_repo=OSMFR)
default_country_simple("africa", "kenya", 192798,    {"country": "KE", "driving_side": "left"}, download_repo=OSMFR)
default_country_simple("africa", "madagascar", None, {"country": "MG", "language": "fr"}, download_repo=GEOFABRIK)
default_country_simple("africa", "mali", 192785,     {"country": "ML", "language": "fr"}, download_repo=OSMFR)
default_country_simple("africa", "mauritania", 192763, {"country": "MR"}, download_repo=OSMFR)
default_country_simple("africa", "niger", 192786,    {"country": "NE", "language": "fr"}, download_repo=OSMFR)
default_country_simple("africa", "senegal", 192775,  {"country": "SN"}, download_repo=OSMFR)
default_country_simple("africa", "togo", 192782,     {"country": "TG", "language": "fr"}, download_repo=OSMFR)

config["chad"].analyser["osmosis_way_approximate"] = "xxx"
config["djibouti"].analyser["osmosis_way_approximate"] = "xxx"
config["kenya"].analyser["osmosis_way_approximate"] = "xxx"
config["madagascar"].analyser["osmosis_way_approximate"] = "xxx"
config["mali"].analyser["osmosis_way_approximate"] = "xxx"
config["senegal"].analyser["osmosis_way_approximate"] = "xxx"
config["togo"].analyser["osmosis_way_approximate"] = "xxx"

#########################################################################

default_country_simple("central-america", "haiti", 307829, {"country": "HT"},
                       download_repo=GEOFABRIK, download_country="haiti-and-domrep")

config["haiti"].analyser["osmosis_way_approximate"] = "xxx"

#########################################################################
# Passwords are stored in separate file, not on git repository
import osmose_config_password

osmose_config_password.set_password(config)
