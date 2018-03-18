#!/usr/bin/env python
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

from __future__ import print_function

from modules import OsmoseLog, download
from modules.lockfile import lockfile
import sys, os, traceback
try:
    import poster.encode
    import poster.streaminghttp
    poster.streaminghttp.register_openers()
    has_poster_lib = True
except:
    has_poster_lib = False
import modules.OsmOsisManager
import modules.config
import osmose_config as config
import inspect
import socket
import subprocess
import time

try:
    # For Python 3.0 and later
    from io import StringIO
except ImportError:
    # Fall back to Python 2
    from cStringIO import StringIO

try:
    # For Python 3.0 and later
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request
    from urllib2 import HTTPError
    from urllib import urlencode

#proxy_support = urllib2.ProxyHandler()
#print proxy_support.proxies
#opener = urllib2.build_opener(proxy_support)
#urllib2.install_opener(opener)

###########################################################################
## fonctions utiles

class analyser_config:
  pass

def get_version():
    cmd  = ["git", "describe"]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        version = proc.stdout.readlines()[0].strip()
    except:
        version = "(unknown)"
    return version

###########################################################################


def run(conf, logger, options):

    err_code = 0
    country = conf.country
    try:
      version = get_version()
    except:
      version = None

    osmosis_manager = None
    if hasattr(conf, "db_base") and conf.db_base:
        try:
            osmosis_manager = modules.OsmOsisManager.OsmOsisManager(conf, conf.db_host, conf.db_user, conf.db_password, conf.db_base, conf.db_schema or conf.country, conf.db_persistent, logger)
        except:
            traceback.print_exc()
            logger.log(logger.log_av_r+u"error in database initialisation"+logger.log_ap)
            return 0x10


    ##########################################################################
    ## check for working dirs and creates when needed

    dirs = [conf.dir_tmp, conf.dir_cache, conf.dir_results, conf.dir_extracts, conf.dir_diffs]
    if "diff_path" in conf.download:
        dirs.append(conf.download["diff_path"])

    for i in dirs:
        if not os.path.exists(i):
            try:
                os.makedirs(i)
            except OSError as e:
                sys.exit("%s\nCheck 'dir_work' in modules/config.py and its permissions" % str(e))

    ##########################################################################
    ## download and create database

    if options.skip_init:
        pass

    elif options.change and osmosis_manager.check_change(conf) and not options.change_init:
        xml_change = osmosis_manager.run_change(conf)

    elif "url" in conf.download:
        newer = False
        xml_change = None
        updated = False  # set if extract was updated instead of fully downloaded

        if options.diff and osmosis_manager.check_diff(conf) and os.path.exists(conf.download["dst"]):
            (status, xml_change) = osmosis_manager.run_diff(conf)
            if status:
                newer = True
                updated = True

        if not newer and options.skip_download:
            logger.sub().log("skip download")
            newer = True

        if not newer:
            logger.log(logger.log_av_r+u"downloading"+logger.log_ap)
            newer = download.dl(conf.download["url"], conf.download["dst"], logger.sub(),
                                min_file_size=8*1024)

            updated = False

        if not newer:
            return 0

        if osmosis_manager:
            osmosis_manager.init_database(conf)

        if options.change:
            osmosis_manager.init_change(conf)
        elif options.diff and not updated:
            osmosis_manager.init_diff(conf)

    if hasattr(conf, "sql_post_scripts"):
        logger.log(logger.log_av_r+"import post scripts"+logger.log_ap)
        for script in conf.sql_post_scripts:
            osmosis_manager.psql_f(script)

    if not options.skip_init and osmosis_manager:
        osmosis_manager.update_metainfo(conf)

    if options.resume:
        osmosis_manager.run_resume(conf)

    ##########################################################################
    ## analyses

    for analyser, password in conf.analyser.iteritems():
        logger.log(logger.log_av_r + country + " : " + analyser + logger.log_ap)

        if not "analyser_" + analyser in analysers:
            logger.sub().log("skipped")
            continue

        if password == "xxx":
            logger.sub().log("code is not correct - won't upload to %s" % conf.updt_url)
        elif not conf.results_url and not has_poster_lib:
            logger.sub().log("results_url is not correct - won't upload to %s" % conf.updt_url)

        try:
            analyser_conf = analyser_config()
            analyser_conf.dst_dir = conf.dir_results

            analyser_conf.osmosis_manager = osmosis_manager
            analyser_conf.db_user = conf.db_user
            if conf.db_schema:
                analyser_conf.db_schema = conf.db_schema
            else:
                analyser_conf.db_schema = country
            analyser_conf.db_schema_path = conf.db_schema_path

            analyser_conf.dir_scripts = conf.dir_scripts
            analyser_conf.options = conf.analyser_options
            analyser_conf.polygon_id = conf.polygon_id

            if options.change and xml_change:
                analyser_conf.src = xml_change
            elif "dst" in conf.download:
                analyser_conf.src = conf.download["dst"]
                if "diff_path" in conf.download:
                    analyser_conf.src_state = os.path.join(conf.download["diff_path"], "state.txt")

            lunched_analyser = []
            lunched_analyser_change = []
            lunched_analyser_resume = []

            for name, obj in inspect.getmembers(analysers["analyser_" + analyser]):
                if (inspect.isclass(obj) and obj.__module__ == "analyser_" + analyser and
                    (name.startswith("Analyser") or name.startswith("analyser"))):
                    # analyse
                    analyser_conf.dst_file = name + "-" + country + ".xml"
                    analyser_conf.dst_file += ".bz2"
                    analyser_conf.dst = os.path.join(conf.dir_results, analyser_conf.dst_file)
                    analyser_conf.version = version
                    analyser_conf.verbose = options.verbose
                    with obj(analyser_conf, logger.sub()) as analyser_obj:
                        if options.resume:
                            try:
                                body = urllib2.urlopen(modules.config.url_frontend_update + "/../../control/status/%s/%s" % (country, analyser)).read().split("\n")
                                if body[0] == 'NOTHING':
                                    raise Exception("Nothing to resume")
                                resume_from_timestamp, resume_from_version, nodes, ways, relations = body[0:5]
                                already_issued_objects = {'N': nodes and map(int, nodes.split(',')) or [], 'W': ways and map(int, ways.split(',')) or [], 'R': relations and map(int, relations.split(',') or [])}
                                analyser_obj.analyser_resume(resume_from_timestamp, already_issued_objects)
                                lunched_analyser_resume.append(analyser_obj)
                                continue
                            except BaseException as e:
                                logger.sub().log("resume fail")
                                traceback.print_exc()
                                pass

                        if not options.change or not xml_change:
                            analyser_obj.analyser()
                            lunched_analyser.append(analyser_obj)
                        else:
                            analyser_obj.analyser_change()
                            lunched_analyser_change.append(analyser_obj)

                    # update
                    if (conf.results_url or has_poster_lib) and password != "xxx":
                        logger.sub().log("update")

                        if analyser in conf.analyser_updt_url:
                            list_urls = conf.analyser_updt_url[analyser]
                        else:
                            list_urls = [conf.updt_url]

                        for url in list_urls:
                            update_finished = False
                            nb_iter = 0
                            while not update_finished and nb_iter < 3:
                                time.sleep(nb_iter * 15)
                                nb_iter += 1
                                logger.sub().sub().log("iteration=%d" % nb_iter)
                                try:
                                    tmp_src = "%s-%s" % (analyser, country)
                                    if has_poster_lib:
                                        (tmp_dat, tmp_headers) = poster.encode.multipart_encode(
                                                                    {"content": open(analyser_conf.dst, "rb"),
                                                                     "source": tmp_src,
                                                                     "code": password})
                                        tmp_req = Request(url, tmp_dat, tmp_headers)
                                        fd = urlopen(tmp_req, timeout=1800)

                                    else:
                                        tmp_req = Request(url)
                                        tmp_url = os.path.join(conf.results_url, analyser_conf.dst_file)
                                        tmp_dat = urlencode([('url', tmp_url),
                                                             ('source', tmp_src),
                                                             ('code', password)])
                                        fd = urlopen(tmp_req, tmp_dat, timeout=1800)

                                    dt = fd.read().decode("utf8").strip()
                                    if dt[-2:] != "OK":
                                        sys.stderr.write((u"UPDATE ERROR %s/%s : %s\n"%(country, analyser, dt)).encode("utf8"))
                                        err_code |= 4
                                    else:
                                        logger.sub().sub().log(dt)
                                    update_finished = True
                                except socket.timeout:
                                    logger.sub().sub().sub().log("got a timeout")
                                    pass
                                except:
                                    s = StringIO()
                                    traceback.print_exc(file=s)
                                    logger.sub().log("error on update...")
                                    for l in s.getvalue().decode("utf8").split("\n"):
                                        logger.sub().sub().log(l)

                        if not update_finished:
                            err_code |= 1

        except:
            s = StringIO()
            traceback.print_exc(file=s)
            logger.sub().log("error on analyse...")
            for l in s.getvalue().decode("utf8").split("\n"):
                logger.sub().sub().log(l)
            err_code |= 2
            continue
        finally:
            if not options.no_clean:
                for obj in lunched_analyser:
                    obj.config.dst = None
                    with obj as o:
                        o.analyser_clean()
                for obj in lunched_analyser_change:
                    obj.config.dst = None
                    with obj as o:
                        o.analyser_change_clean()
                for obj in lunched_analyser_resume:
                    obj.config.dst = None
                    with obj as o:
                        o.analyser_resume_clean()

    ##########################################################################
    ## final cleaning

    logger.log(logger.log_av_r + u"cleaning : " + country + logger.log_ap)

    if options.change:
        pass
    else:
        if osmosis_manager:
            osmosis_manager.clean_database(conf, options.no_clean or not conf.clean_at_end)

    if options.diff:
        # don't erase any file
        return err_code

    # remove files
    if "url" in conf.download and "dst" in conf.download and not options.no_clean:
        f = ".osm".join(conf.download["dst"].split(".osm")[:-1])
        for ext in ["osm", "osm.bz2", "osm.pbf"]:
            try:
                os.remove("%s.%s"%(f, ext))
                logger.sub().log("DROP FILE %s.%s"%(f, ext))
            except:
                pass

    return err_code

###########################################################################

if __name__ == "__main__":

    err_code = 0

    #=====================================
    # analyse des arguments

    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("--verbose", dest="verbose", action="store_true",
                      help="Verbose mode")

    parser.add_option("--list-analyser", dest="list_analyser", action="store_true",
                      help="List all available analysers")
    parser.add_option("--list-country", dest="list_country", action="store_true",
                      help="List all available countries")
    parser.add_option("--country", dest="country", action="append",
                      help="Country to analyse (can be repeated)")
    parser.add_option("--analyser", dest="analyser", action="append",
                      help="Analyser to run (can be repeated)")

    parser.add_option("--change", dest="change", action="store_true",
                      help="Run analyser on change mode when available")
    parser.add_option("--change_init", dest="change_init", action="store_true",
                      help="Initialize database for change mode")

    parser.add_option("--resume", dest="resume", action="store_true",
                      help="Run analyser on change mode by continuing from last run when available")

    parser.add_option("--skip-download", dest="skip_download", action="store_true",
                      help="Don't download extract")
    parser.add_option("--skip-init", dest="skip_init", action="store_true",
                      help="Don't initialize database")
    parser.add_option("--no-clean", dest="no_clean", action="store_true",
                      help="Don't remove extract and database after analyses")

    parser.add_option("--cron", dest="cron", action="store_true",
                      help="Record output in a specific log")

    parser.add_option("--version", dest="version", action="store_true",
                      help="Output version information and exit")

    (options, args) = parser.parse_args()

    analysers_path = os.path.join(os.path.dirname(__file__), "analysers")

    if options.list_analyser:
        for fn in sorted(os.listdir(analysers_path)):
            if fn.startswith("analyser_") and fn.endswith(".py"):
                print(fn[9:-3])
        sys.exit(0)

    if options.list_country:
        for k in sorted(config.config.keys()):
           print(k)
        sys.exit(0)

    if options.cron:
        output = sys.stdout
        logger = OsmoseLog.logger(output, False)
    else:
        output = sys.stdout
        logger = OsmoseLog.logger(output, True)

    if options.change_init and not options.change:
        logger.log(logger.log_av_b+"--change must be specified "+logger.log_ap)
        sys.exit(1)

    if options.version:
        print("osmose backend version: %s" % get_version())
        sys.exit(0)

    if not options.country:
        parser.print_help()
        sys.exit(1)

    #=====================================
    # chargement des analysers

    old_path = list(sys.path)
    sys.path.insert(0, analysers_path)

    logger.log(logger.log_av_v+"loading analyses "+logger.log_ap)
    analysers = {}
    for fn in os.listdir(analysers_path):
        if fn.startswith("analyser_") and fn.endswith(".py"):
            if options.analyser and fn[9:-3] not in options.analyser:
                continue
            logger.log("  load "+fn[9:-3])
            analysers[fn[:-3]] = __import__(fn[:-3])
    if options.analyser:
        count = 0
        for k in options.analyser:
            if ("analyser_%s" % k) not in analysers:
                logger.log(logger.log_av_b+"not found "+k+logger.log_ap)
                count += 1
        # user is passing only non-existent analysers
        if len(options.analyser) == count:
            sys.exit("No valid analysers specified")

    sys.path[:] = old_path # restore previous path

    #=====================================
    # analyse

    for country, country_conf in config.config.iteritems():

        # filter
        if options.country and country not in options.country:
            continue

        # acquire lock
        try:
            lfil = "/tmp/analyse-%s"%country
            lock = lockfile(lfil)
        except:
            logger.log(logger.log_av_r+"can't lock %s"%country+logger.log_ap)
            if options.cron:
                sys.stderr.write("can't lock %s\n"%country)
            for l in open(lfil).read().rstrip().split("\n"):
                logger.log("  "+l)
                if options.cron:
                    sys.stderr.write("  "+l+"\n")
            if options.cron:
                sys.stderr.flush()
            err_code |= 0x80
            continue

        country_conf.init()
        options.diff = not options.change and "diff" in country_conf.download

        # analyse
        err_code |= run(country_conf, logger, options)

        # free lock
        del lock

    logger.log(logger.log_av_v+u"end of analyses"+logger.log_ap)
    sys.exit(err_code)
