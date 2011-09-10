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

hostname = open("/etc/hostname").read().strip()
available_results_urls = {"osm1": "http://osm1.crans.org/osmose/",
                          "osm3": "http://osm3.crans.org/osmose/",
                          "osm4": "http://osm4.crans.org/osmose/",
                          "osm5": "http://osm5.univ-nantes.fr/osmose/",
                          "osm6": "http://osm6.univ-nantes.fr/osmose/",
                         }
if hostname in available_results_urls:
    results_url = available_results_urls[hostname]
else:
    results_url = None

###########################################################################

class template_config:

    clean_at_end          = True

    common_updt_url       = "http://osmose.openstreetmap.fr/map/cgi-bin/update.py"
    common_results_url    = results_url
    common_dir_work       = "/data/work/osmose"
    common_dir_scripts    = "/data/project/osmose"
    common_dir_osm2pgsql  = common_dir_scripts + "/osm2pgsql"
    common_bin_osm2pgsql  = common_dir_scripts + "/osm2pgsql/osm2pgsql"+"-squeeze"
    common_osmosis_bin    = common_dir_scripts + "/osmosis/osmosis-0.38/bin/osmosis"
    common_osmosis_schema = common_dir_scripts + "/osmosis/osmosis-0.38/script/pgsql_simple_schema_0.6.sql"
    common_osmosis_schema_bbox = common_dir_scripts + "/osmosis/osmosis-0.38/script/pgsql_simple_schema_0.6_bbox.sql"
    common_osmosis_schema_linestring = common_dir_scripts + "/osmosis/osmosis-0.38/script/pgsql_simple_schema_0.6_linestring.sql"
    common_osmosis_create_polygon = common_dir_scripts + "/osmosis/WaysCreatePolygon.sql"
    common_dir_results      = os.path.join(common_dir_work,"results")
    common_dir_extracts     = os.path.join(common_dir_work,"extracts")

    common_dbn      = "osmose"
    common_dbu      = "osmose"
    common_dbx      = "-osmose-"
    common_dbs      = "dbname=%s user=%s"%(common_dbn, common_dbu)

config = {}

###########################################################################

country = "europe1"
config[country] = template_config()

config[country].country = "europe"
config[country].download = { "large": { "url": "http://download.geofabrik.de/osm/europe.osm.bz2",
                                        "dst": template_config.common_dir_extracts+"/"+country+".osm",
                                      }
                            }
config[country].analyser = { "admin_level": "xxx",
                           }


country = "europe2"
config[country] = template_config()

config[country].country = "europe"
config[country].download = { "large": { "url": "http://download.geofabrik.de/osm/europe.osm.bz2",
                                        "dst": template_config.common_dir_extracts+"/"+country+".osm",
                                        "osm2pgsql": country,
                                      }
                            }
config[country].analyser = { "gis_polygon": "xxx",
                             "gis_boundary_intersect": "xxx",
                           }

###########################################################################

country = "france"
config[country] = template_config()

config[country].country = country
config[country].download = { "large": { "url": "http://download.geofabrik.de/osm/europe/france.osm.gz",
                                        "dst": template_config.common_dir_extracts+"/"+country+".osm",
                                        "osm2pgsql": country,
                                        "osmosis": country,
                                      }
                            }
config[country].analyser = { "sax": "xxx",
                             "gis_roundabout": "xxx",
                             "roundabout_level": "xxx",
                             "sql_soundex": "xxx",
                             "osmosis_roundabout": "xxx",
                             "osmosis_boundary_hole": "xxx",
                             "geodesie": "xxx",
                             "gis_building_overlaps": "xxx",
                           }
config[country].analyser_options = { "sax": { "plugin_filter": ["fr", "FR"] },
                                   }

###########################################################################

for region in "alsace aquitaine auvergne basse-normandie bourgogne bretagne centre champagne-ardenne corse franche-comte haute-normandie ile-de-france languedoc-roussillon limousin lorraine midi-pyrenees nord-pas-de-calais pays-de-la-loire picardie poitou-charentes provence-alpes-cote-d-azur rhone-alpes".split():
  country = "france_" + region.replace("-", "_")
  config[country] = template_config()

  config[country].country = country
  config[country].download = { "large": { "url": "http://download.geofabrik.de/osm/europe/france/%s.osm.bz2" % region,
                                          "dst": template_config.common_dir_extracts+"/"+country+".osm",
                                          "osmosis": country },
                             }

  config[country].analyser = { "sax": "xxx",
                               "osmosis_roundabout_reverse": "xxx",
                               "roundabout_level": "xxx",
                               "sql_soundex": "xxx",
                               "osmosis_roundabout": "xxx",
                               "osmosis_boundary_hole": "xxx",
                               "geodesie": "xxx",
                               "building_overlaps": "xxx",
                               "osmosis_natural_swimming-pool": "xxx",
                               "osmosis_missing_parent_tag": "xxx",
                               "stats": "xxx",
                             }

  config[country].analyser_options = { "sax": { "plugin_filter": ["fr", "FR"] },
                                     }

###########################################################################

for region in "guadeloupe guyane martinique mayotte nouvellecaledonie polynesie reunion saintbarthelemy saintmartin saintpierreetmiquelon wallisetfutuna".split():
  country = "france_" + region
  config[country] = template_config()

  config[country].country = country
  config[country].download = { "large": { "url": "http://download.geofabrik.de/osm/europe/france/%s.osm.pbf" % region,
                                          "dst": template_config.common_dir_extracts+"/"+country+".osm",
                                          "osmosis": country },
                             }

  config[country].analyser = { "sax": "xxx",
                               "osmosis_roundabout_reverse": "xxx",
                               "roundabout_level": "xxx",
                               "sql_soundex": "xxx",
                               "osmosis_roundabout": "xxx",
                               "osmosis_boundary_hole": "xxx",
                               "geodesie": "xxx",
                               "building_overlaps": "xxx",
                               "stats": "xxx",
                             }

  config[country].analyser_options = { "sax": { "plugin_filter": ["fr", "FR"] },
                                     }

country = "france_nouvellecaledonie"
config[country].download["large"]["url"] = "http://download.geofabrik.de/osm/australia-oceania/new-caledonia.osm.pbf"

###########################################################################

country = "belgique"
config[country] = template_config()

config[country].country = country
config[country].download = { "large": { "url": "http://download.geofabrik.de/osm/europe/belgium.osm.bz2",
                                        "dst": template_config.common_dir_extracts+"/"+country+".osm",
                                        "osmosis": country,
                                      }
                            }
config[country].analyser = { "sax": "xxx",
                             "osmosis_roundabout_reverse": "xxx",
                             "roundabout_level": "xxx",
                             "sql_soundex": "xxx",
                             "osmosis_roundabout": "xxx",
                             "osmosis_boundary_hole": "xxx",
                             "building_overlaps": "xxx",
                           }
config[country].analyser_options = { "sax": { "plugin_filter": ["fr", "FR"] },
                                   }

###########################################################################

country = "madagascar"
config[country] = template_config()

config[country].country = country
config[country].download = { "large": { "url": "http://download.geofabrik.de/osm/africa/madagascar.osm.bz2",
                                        "dst": template_config.common_dir_extracts+"/"+country+".osm",
                                        "osm2pgsql": country,
                                      }
                            }
config[country].analyser = { "sax": "xxx",
                             "gis_polygon": "xxx",
                             "gis_roundabout": "xxx",
                             "gis_building_overlaps": "xxx",
                           }
config[country].analyser_options = { "sax": { "plugin_filter": ["fr", "MG"] },
                                   }

###########################################################################
# Passwords are stored in separate file, not on git repository
import osmose_config_password

osmose_config_password.set_password(config)
