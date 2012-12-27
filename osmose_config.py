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

class template_config:

    clean_at_end          = True

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

    db_base     = "osmose"
    db_user     = "osmose"
    db_password = "-osmose-"
    db_schema   = None

    def __init__(self):
        self.country          = None
        self.download         = {}
        self.analyser         = OrderedDict()
        self.analyser_options = {}

    def init(self):
        self.db_string = "dbname=%s user=%s password=%s"%(self.db_base, self.db_user, self.db_password)

analysers = [
             "sax",
             "osmosis_roundabout_reverse",
             "osmosis_roundabout_level",
             "osmosis_soundex",
             "osmosis_roundabout",
             "osmosis_boundary_hole",
             "osmosis_geodesie",
             "osmosis_building_overlaps",
             "osmosis_natural_swimming-pool",
             "osmosis_missing_parent_tag",
             "osmosis_polygon",
             "osmosis_highway_vs_building",
             "osmosis_orphan_nodes_cluster",
             "osmosis_powerline",
             "osmosis_highway_cul-de-sac_level",
             "osmosis_double_tagging",
             "osmosis_associatedStreet",
             "osmosis_highway_link",
             "osmosis_broken_highway_level_continuity",
             "osmosis_large_relation",
             "osmosis_mini_farm",
             "osmosis_surface_overlaps",
             "osmosis_useless",
             "osmosis_multipolygon",
             "osmosis_boundary_intersect",
             "osmosis_node_like_way",
             "osmosis_boundary_administrative",
             "osmosis_tag_typo",
             "osmosis_way_approximate",
             "osmosis_cycleway_track",
             "osmosis_crossing",
             "osmosis_building_shapes",
             "osmosis_riverbank",
            ]

config = OrderedDict()

###########################################################################

country = "world"
config[country] = template_config()

config[country].country = "world"
config[country].analyser["osmbin_open_relations"] = "xxx"

###########################################################################

country = "europe1"
config[country] = template_config()

config[country].country = "europe"
config[country].download = { "url": "http://download.geofabrik.de/openstreetmap/europe.osm.bz2",
                             "dst": template_config.dir_extracts+"/"+country+".osm",
                           }
config[country].analyser["admin_level"] = "xxx"


country = "europe2"
config[country] = template_config()

config[country].country = "europe"
config[country].download = { "url": "http://download.geofabrik.de/openstreetmap/europe.osm.bz2",
                                    "dst": template_config.dir_extracts+"/"+country+".osm",
                                    "osm2pgsql": country,
                           }
config[country].analyser["osmosis_polygon"] = "xxx"
config[country].analyser["osmosis_boundary_intersect"] = "xxx"

###########################################################################

country = "france"
config[country] = template_config()

config[country].country = country
config[country].download = { "url": "http://download.geofabrik.de/openstreetmap/europe/france.osm.gz",
                             "dst": template_config.dir_extracts+"/"+country+".osm",
                             "osm2pgsql": country,
                             "osmosis": country,
                           }
config[country].analyser["sax"] = "xxx"
config[country].analyser["osmosis_roundabout"] = "xxx"
config[country].analyser["osmosis_roundabout_level"] = "xxx"
config[country].analyser["osmosis_soundex"] = "xxx"
config[country].analyser["osmosis_roundabout"] = "xxx"
config[country].analyser["osmosis_boundary_hole"] = "xxx"
config[country].analyser["osmosis_geodesie"] = "xxx"
config[country].analyser["osmosis_building_overlaps"] = "xxx"

config[country].analyser_options = { "sax": { "plugin_filter": ["fr", "FR"] },
                                   }

###########################################################################

for region in "alsace aquitaine auvergne basse-normandie bourgogne bretagne centre champagne-ardenne corse franche-comte haute-normandie ile-de-france languedoc-roussillon limousin lorraine midi-pyrenees nord-pas-de-calais pays-de-la-loire picardie poitou-charentes provence-alpes-cote-d-azur rhone-alpes guadeloupe guyane martinique mayotte nouvellecaledonie polynesie reunion saintbarthelemy saintmartin saintpierreetmiquelon wallisetfutuna".split():
  country = "france_" + region.replace("-", "_")
  config[country] = template_config()

  config[country].country = country
  config[country].download = { "url": "http://download.geofabrik.de/openstreetmap/europe/france/%s.osm.pbf" % region,
                               "dst": template_config.dir_extracts+"/"+country+".osm.pbf",
                               "osmosis": country,
                             }

  for a in analysers:
    config[country].analyser[a] = "xxx"

  config[country].analyser_options = { "sax": { "plugin_filter": ["fr", "FR", "FR_%s" % region]
                                              },
                                     }

country = "france_nouvellecaledonie"
config[country].download["url"] = "http://download.geofabrik.de/openstreetmap/australia-oceania/new-caledonia.osm.pbf"

config["france_saintmartin"].download["url"] = "http://download.openstreetmap.fr/extracts/central-america/saint_martin.osm.pbf"
config["france_saintbarthelemy"].download["url"] = "http://download.openstreetmap.fr/extracts/central-america/saint_barthelemy.osm.pbf"
config["france_polynesie"].download["url"] = "http://download.openstreetmap.fr/extracts/oceania/polynesie.osm.pbf"
config["france_wallisetfutuna"].download["url"] = "http://download.openstreetmap.fr/extracts/oceania/wallis_et_futuna.osm.pbf"
config["france_saintpierreetmiquelon"].download["url"] = "http://download.openstreetmap.fr/extracts/north-america/saint_pierre_et_miquelon.osm.pbf"

###########################################################################

country = "france_local_db"
config[country] = template_config()

config[country].db_base     = "osm"
config[country].db_user     = "osmose"
config[country].db_password = "clostAdtoi"
config[country].db_schema   = "osmose,osmosis"

config[country].country = country
config[country].analyser["merge_merimee"] = "xxx"
config[country].analyser["merge_poste_fr"] = "xxx"
config[country].analyser["merge_school_fr"] = "xxx"
config[country].analyser["merge_ratp"] = "xxx"
config[country].analyser["merge_level_crossing_fr"] = "xxx"
config[country].analyser["merge_railstation_fr"] = "xxx"
config[country].analyser["merge_tmc_point_fr"] = "xxx"
config[country].analyser["merge_geodesie"] = "xxx"
config[country].analyser["merge_street_number_toulouse"] = "xxx"
config[country].analyser["osmosis_deadend"] = "xxx"

#########################################################################

analysers.remove("osmosis_geodesie")

for country in "belgium luxembourg switzerland quebec".split():
  config[country] = template_config()

  config[country].country = country
  config[country].download = { "url": "http://download.geofabrik.de/openstreetmap/europe/%s.osm.pbf" % country,
                               "dst": template_config.dir_extracts+"/"+country+".osm.pbf",
                               "osmosis": country,
                             }

  for a in analysers:
    config[country].analyser[a] = "xxx"


country = "belgium"
config[country].download["url"] = "http://download.geofabrik.de/openstreetmap/europe/belgium.osm.pbf"
config[country].analyser_options = { "sax": { "plugin_filter": ["fr", "BE"] },
                                   }

country = "luxembourg"
config[country].analyser_options = { "sax": { "plugin_filter": ["fr", "LU"] },
                                     "osmosis_boundary_hole": { "admin_level": 6 },
                                   }

country = "switzerland"
config[country].download["url"] = "http://download.geofabrik.de/openstreetmap/europe/switzerland.osm.pbf"
config[country].analyser_options = { "sax": { "plugin_filter": ["CH"] },
                                   }

country = "quebec"
config[country].download["url"] = "http://osm8.openstreetmap.fr/extracts/quebec.osm.pbf"
config[country].analyser_options = { "sax": { "plugin_filter": ["fr", "QC"] },
                                   }

#########################################################################

analysers_simp = list(analysers)
analysers_simp.remove("osmosis_highway_cul-de-sac_level")
analysers_simp.remove("osmosis_riverbank")

for country in "madagascar".split():
  config[country] = template_config()

  config[country].country = country
  config[country].download = { "url": "http://download.openstreetmap.fr/extracts/africa/%s.osm.pbf" % country,
                               "dst": template_config.dir_extracts+"/"+country+".osm.pbf",
                               "osmosis": country,
                             }

  for a in analysers_simp:
    config[country].analyser[a] = "xxx"

country = "madagascar"
config[country].download["url"] = "http://download.geofabrik.de/openstreetmap/africa/madagascar.osm.pbf"
config[country].analyser_options = { "sax": { "plugin_filter": ["fr", "MG"] },
                                   }

#########################################################################

analysers_simp = list(analysers)
analysers_simp.remove("osmosis_highway_cul-de-sac_level")
analysers_simp.remove("osmosis_way_approximate")
analysers_simp.remove("osmosis_riverbank")

for country in "burundi cameroon central_african_republic chad haiti kenya senegal".split():
  config[country] = template_config()

  config[country].country = country
  config[country].download = { "url": "http://download.openstreetmap.fr/extracts/africa/%s.osm.pbf" % country,
                               "dst": template_config.dir_extracts+"/"+country+".osm.pbf",
                               "osmosis": country,
                             }

  for a in analysers_simp:
    config[country].analyser[a] = "xxx"


config["burundi"].analyser_options = { "sax": { "plugin_filter": ["BI"] },
                                     }
config["cameroon"].analyser_options = { "sax": { "plugin_filter": ["CM"] },
                                      }
config["central_african_republic"].analyser_options = { "sax": { "plugin_filter": ["CF"] },
                                                      }
config["chad"].analyser_options = { "sax": { "plugin_filter": ["TD"] },
                                  }

country = "haiti"
config[country].download["url"] = "http://download.geofabrik.de/openstreetmap/central-america/haiti-and-domrep.osm.pbf"
config[country].analyser_options = { "sax": { "plugin_filter": ["HT"] },
                                   }

config["kenya"].analyser_options = { "sax": { "plugin_filter": ["KE"] },
                                   }

config["senegal"].analyser_options = { "sax": { "plugin_filter": ["SN"] },
                                     }

###########################################################################
# Passwords are stored in separate file, not on git repository
import osmose_config_password

osmose_config_password.set_password(config)
