#!/usr/bin/env python3
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

from modules import OsmoseLog, download
from modules.lockfile import lockfile
from modules import downloader
from modules import IssuesFileOsmose
from modules import IssuesFileCsv
from modules import IssuesFileGeoJson
import sys
import os
import traceback
import modules.OsmOsisManager
import modules.config
import osmose_config as config

import importlib
import inspect
import subprocess
import time
import dateutil.parser
import requests

try:
    import sentry_sdk
except:
    pass

###########################################################################

def get_version():
    version = os.getenv('OSMOSE_VERSION')
    if not version:
        try:
            version = subprocess.check_output("git describe --long --dirty".split()).decode('utf-8').strip()
        except:
            version = "(unknown)"
    return version

###########################################################################

def check(conf, logger, options):
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

    ## check available free space, for extract and database storage
    if options.minimum_free_space:
        for i in dirs:
            s = os.statvfs(conf.dir_tmp)
            free_space = s.f_bavail * s.f_bsize  # in bytes
            needed_space = options.minimum_free_space*1024*1024*1024

            if free_space < needed_space:
                err_msg = u"directory '%s' has %.2f GB free instead of %.2f GB " % (i, free_space / (1024.*1024*1024), options.minimum_free_space)
                logger.err(err_msg)
                logger.send_alert_email(options.alert_emails, err_msg)
                return 0x20

    return 0

##########################################################################

class analyser_config:
    def __init__(self, conf, options, osmosis_manager, xml_change = None):
        self.dst_dir = conf.dir_results

        self.osmosis_manager = osmosis_manager
        self.db_user = conf.db_user
        if conf.db_schema:
            self.db_schema = conf.db_schema
        else:
            self.db_schema = conf.country
        self.db_schema_path = conf.db_schema_path

        self.options = conf.analyser_options
        self.polygon_id = conf.polygon_id

        self.source_url = conf.source_url

        self.plugins = options.plugin

        self.verbose = options.verbose

        if options.change and xml_change:
            self.src = xml_change
        elif "dst" in conf.download:
            self.src = conf.download["dst"]
            if "diff_path" in conf.download:
                self.src_state = os.path.join(conf.download["diff_path"], "state.txt")


def issues_file_from_fromat(dst, format, bz2 = False, version = None, polygon_id = None):
    if format == 'csv':
        if isinstance(dst, str):
            dst += '.csv'
        c = IssuesFileCsv.IssuesFileCsv
    elif format == 'geojson':
        if isinstance(dst, str):
            dst += '.geojson'
        c = IssuesFileGeoJson.IssuesFileGeoJson
    else:
        if isinstance(dst, str):
            dst += '.xml'
        c = IssuesFileOsmose.IssuesFileOsmose
    if bz2 and isinstance(dst, str):
        dst += '.bz2'

    return c(dst, version, polygon_id)


def execc(conf, logger, analysers, options, osmosis_manager):
    err_code = 0

    ## download and create database

    xml_change = None
    if not options.skip_init:
        if options.change and osmosis_manager.check_change(conf) and not options.change_init:
            xml_change = osmosis_manager.run_change(conf)

        elif "url" in conf.download:
            newer = False
            xml_change = None

            if not newer and options.skip_download:
                logger.sub().log("skip download")
                newer = True

            if not newer and options.diff and os.path.exists(conf.download["dst"]):
                status = False
                if options.pbf_update_tool == 'osmosis':
                    if osmosis_manager.check_osmosis_diff(conf):
                        (status, xml_change) = osmosis_manager.run_osmosis_diff(conf)
                else:
                    if osmosis_manager.check_osmium_diff(conf):
                        (status, xml_change) = osmosis_manager.run_osmium_diff(conf)
                if status:
                    newer = True

            if not newer:
                logger.log(logger.log_av_r+u"downloading"+logger.log_ap)
                newer = download.dl(conf.download["url"], conf.download["dst"], logger.sub(),
                                    min_file_size=8*1024)

                if newer and options.diff:
                    if options.pbf_update_tool == 'osmosis':
                        osmosis_manager.init_osmosis_diff(conf)
                    if "/minute/" in conf.download["diff"] or "/hour/" in conf.download["diff"]:
                        # update extract with any more recent available diff
                        if options.pbf_update_tool == 'osmosis':
                            osmosis_manager.run_osmosis_diff(conf)
                        else:
                            osmosis_manager.run_osmium_diff(conf)

            if not newer:
                return 0x11

            if osmosis_manager:
                osmosis_manager.init_database(conf, options)

            if options.change:
                osmosis_manager.init_change(conf)

        if hasattr(conf, "sql_post_scripts"):
            logger.log(logger.log_av_r+"import post scripts"+logger.log_ap)
            for script in conf.sql_post_scripts:
                osmosis_manager.psql_f(script)

        if osmosis_manager:
            osmosis_manager.update_metainfo(conf)

        if options.resume:
            osmosis_manager.run_resume(conf)

    ##########################################################################
    ## analyses

    version = get_version()

    lunched_analyser = []
    lunched_analyser_change = []
    lunched_analyser_resume = []

    for analyser in analysers:
        if os.getenv('SENTRY_DSN'):
            sentry_sdk.set_tag('analyser', analyser)

        if not options.analyser and analyser not in conf.analyser:
            continue

        logger.log(logger.log_av_r + conf.country + " : " + analyser + logger.log_ap)

        password = conf.analyser.get(analyser)

        if not options.skip_upload and (not password or password == "xxx"):
            logger.sub().err("No password to upload result to %s" % conf.updt_url)

        try:
            analyser_conf = analyser_config(conf, options, osmosis_manager, xml_change)

            for name, obj in inspect.getmembers(analysers[analyser]):
                if (inspect.isclass(obj) and obj.__module__ == "analysers.analyser_" + analyser and
                    (name.startswith("Analyser") or name.startswith("analyser"))):
                    analyser_name = name[len("Analyser_"):]
                    resume = options.resume or (options.resume_analyser and analyser in options.resume_analyser)

                    dst = os.path.join(conf.dir_results, name + "-" + conf.country)
                    analyser_conf.error_file = issues_file_from_fromat(dst, options.result_format, bz2 = True, version = version, polygon_id = analyser_conf.polygon_id)

                    # analyse
                    if not options.skip_analyser:
                        with obj(analyser_conf, logger.sub()) as analyser_obj:
                            remote_timestamp = None
                            if not options.skip_frontend_check:
                                url = modules.config.url_frontend_update + "/../../control/status/%s/%s?%s" % (conf.country, analyser_name, 'objects=true' if resume else '')
                                resp = downloader.request_get(url)
                                if not resp.ok:
                                    logger.sub().err("Fails to get status from frontend: {0}".format(resp.status_code))
                                else:
                                    try:
                                        status = resp.json()
                                        remote_timestamp = dateutil.parser.parse(status['timestamp']) if status else None
                                        remote_analyser_version = int(status['analyser_version'])
                                    except Exception as e:
                                        logger.sub().err(e)

                            if analyser_obj.timestamp() and remote_timestamp and analyser_obj.timestamp() <= remote_timestamp and analyser_obj.analyser_version() == remote_analyser_version:
                                logger.sub().warn("Skip, frontend is already up to date")
                                continue

                            if resume and remote_timestamp and analyser_obj.analyser_version() == remote_analyser_version:
                                already_issued_objects = {'N': status['nodes'] or [], 'W': status['ways'] or [], 'R': status['relations'] or []}
                                analyser_obj.analyser_resume(remote_timestamp, already_issued_objects)
                                lunched_analyser_resume.append([obj, analyser_conf])
                            else:
                                if resume:
                                    if not remote_timestamp:
                                        logger.sub().err("No remote timestamp to resume from, start a full run")
                                    elif analyser_obj.analyser_version() == remote_analyser_version:
                                        logger.sub().err("Analyser version changed, start a full run")

                                if not options.change or not xml_change:
                                    analyser_obj.analyser()
                                    lunched_analyser.append([obj, analyser_conf])
                                else:
                                    analyser_obj.analyser_change()
                                    lunched_analyser_change.append([obj, analyser_conf])

                    # update
                    if not options.skip_upload and password != "xxx":
                        logger.sub().log("update")

                        if analyser in conf.analyser_updt_url:
                            list_urls = conf.analyser_updt_url[analyser]
                        else:
                            list_urls = [conf.updt_url]

                        for url in list_urls:
                            update_finished = False
                            nb_iter = 0
                            was_on_timeout = False
                            while not update_finished and nb_iter < 3:
                                time.sleep(nb_iter * 15)
                                nb_iter += 1
                                logger.sub().sub().log("iteration=%d" % nb_iter)
                                try:
                                    u = url + '?analyser=' + analyser_name + '&country=' + conf.country
                                    r = requests.post(u, timeout=1800, data={
                                        'analyser': analyser_name,
                                        'country': conf.country,
                                        'code': password
                                    }, files={
                                        'content': open(analyser_conf.error_file.dst, 'rb')
                                    })
                                    r.raise_for_status()
                                    logger.sub().sub().log(r.text.strip())
                                    update_finished = True
                                except requests.exceptions.HTTPError as e:
                                    if e.response.status_code == 504:
                                        was_on_timeout = True
                                        logger.sub().sub().sub().err('got an HTTP timeout status')
                                    else:
                                        dt = r.text.strip()
                                        logger.sub().sub().sub().err(u"UPDATE ERROR %s/%s : %s\n" % (conf.country, analyser_name, dt))
                                        if dt == "FAIL: Already up to date":
                                            update_finished = True
                                        if nb_iter >= 3 and not was_on_timeout:
                                            err_code |= 4
                                except Exception as e:
                                    if isinstance(e, requests.exceptions.ConnectTimeout):
                                        was_on_timeout = True
                                        logger.sub().sub().sub().err('got a connection timeout')
                                    else:
                                        tb = traceback.format_exc()
                                        logger.sub().err('error on update...')
                                        for l in tb.splitlines():
                                            logger.sub().sub().log(l)

                        if not update_finished:
                            err_code |= 1

        except Exception as e:
            tb = traceback.format_exc()
            logger.sub().err("error on analyse {0}...".format(analyser))
            for l in tb.splitlines():
                logger.sub().sub().log(l)
            err_code |= 2
            if os.getenv('SENTRY_DSN'):
                sentry_sdk.capture_exception(e)
            continue

    if os.getenv('SENTRY_DSN'):
        sentry_sdk.set_tag('analyser', None)

    if not options.no_clean:
        for (obj, analyser_conf) in lunched_analyser:
            analyser_conf.error_file = None
            with obj(analyser_conf, logger.sub()) as analyser_obj:
                analyser_obj.analyser_deferred_clean()
        for (obj, analyser_conf) in lunched_analyser_change:
            analyser_conf.error_file = None
            with obj(analyser_conf, logger.sub()) as analyser_obj:
                analyser_obj.analyser_deferred_clean()
        for (obj, analyser_conf) in lunched_analyser_resume:
            analyser_conf.error_file = None
            with obj(analyser_conf, logger.sub()) as analyser_obj:
                analyser_obj.analyser_deferred_clean()

    return err_code


def clean(conf, logger, options, osmosis_manager):
    logger.log(logger.log_av_r + u"cleaning : " + logger.log_ap)

    if options.change:
        pass
    else:
        if osmosis_manager:
            osmosis_manager.clean_database(conf, options.no_clean or not conf.clean_at_end)

    if options.diff:
        # don't erase any file
        return

    # remove files
    if "url" in conf.download and "dst" in conf.download and not options.no_clean:
        f = ".osm".join(conf.download["dst"].split(".osm")[:-1])
        for ext in ["osm", "osm.bz2", "osm.pbf"]:
            try:
                os.remove("%s.%s" % (f, ext))
                logger.sub().log("DROP FILE %s.%s" % (f, ext))
            except:
                pass

###########################################################################

def run(conf, logger, analysers, options):
    err = check(conf, logger, options)
    if err != 0:
        return err

    try:
        osmosis_manager = None
        if hasattr(conf, "db_base") and conf.db_base:
            try:
                osmosis_manager = modules.OsmOsisManager.OsmOsisManager(conf, conf.db_host, conf.db_user, conf.db_password, conf.db_base, conf.db_schema or conf.country, conf.db_persistent, logger)
            except:
                traceback.print_exc()
                logger.err(u"error in database initialisation")
                return 0x10

        return execc(conf, logger, analysers, options, osmosis_manager)
    except:
        # Log error in case finally also fails
        traceback.print_exc()
        raise
    finally:
        clean(conf, logger, options, osmosis_manager)

###########################################################################

def main(options):

    analysers_path = os.path.join(os.path.dirname(__file__), "analysers")

    if options.list_analyser:
        for fn in sorted(os.listdir(analysers_path)):
            if fn.startswith("analyser_") and fn.endswith(".py"):
                print(fn[9:-3])
        return 0

    if options.list_country:
        for k in sorted(config.config.keys()):
           print(k)
        return 0

    if options.cron:
        output = sys.stdout
        logger = OsmoseLog.logger(output, False)
    else:
        output = sys.stdout
        logger = OsmoseLog.logger(output, True)

    if options.change_init and not options.change:
        logger.err("--change must be specified")
        return 1

    #=====================================
    # Load of analysers
    err_code = 0

    logger.log("osmose backend version: %s" % get_version())

    if os.getenv('SENTRY_DSN'):
        sentry_sdk.init(dsn=os.getenv('SENTRY_DSN'), traces_sample_rate=1.0, release=get_version())

    old_path = list(sys.path)
    sys.path.insert(0, analysers_path)

    logger.log(logger.log_av_green+"loading analyses "+logger.log_ap)
    analysers = {}
    for fn in os.listdir(analysers_path):
        if fn.startswith("analyser_") and fn.endswith(".py"):
            if options.analyser and fn[9:-3] not in options.analyser:
                continue
            logger.log("  load "+fn[9:-3])
            try:
                analysers[fn[9:-3]] = importlib.import_module("analysers." + fn[:-3])
            except ImportError as e:
                logger.log(e)
                logger.err("Fails to load analysers {0}".format(fn[:-3]))
    if options.analyser:
        count = 0
        for k in options.analyser:
            if k not in analysers:
                logger.err("not found "+k)
                count += 1
        # user is passing only non-existent analysers
        if len(options.analyser) == count:
            logger.err("No valid analysers specified")
            return 1

    sys.path[:] = old_path # restore previous path

    #=====================================
    # analyser

    for country in options.country:
        if country in config.config:
            country_conf = config.config[country]
        else:
            logger.err("Failed to load country {0}".format(country))
            return 8

        if os.getenv('SENTRY_DSN'):
            sentry_sdk.set_tag('country', country)

        # acquire lock
        try:
            base = '|'.join(map(str, [country_conf.db_base, country_conf.db_host]))
            lfil = "/tmp/analyse-{0}-{1}".format(country, base)
            lock = lockfile(lfil)
        except:
            logger.err("can't lock {0} ({1})".format(country, lfil))
            if options.cron:
                sys.stderr.write("can't lock %s\n" % country)
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
        err_code |= run(country_conf, logger, analysers, options)

        # free lock
        del lock

    if os.getenv('SENTRY_DSN'):
        sentry_sdk.set_tag('country', None)

    logger.log(logger.log_av_green+u"end of analyses"+logger.log_ap)
    return err_code


if __name__ == "__main__":
    #=====================================
    # analyse of parameters

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
    parser.add_option("--plugin", dest="plugin", action="append",
                      help="Plugin to run (can be repeated). For analyser 'sax' only")

    parser.add_option("--change", dest="change", action="store_true",
                      help="Run analyser on change mode when available")
    parser.add_option("--change_init", dest="change_init", action="store_true",
                      help="Initialize database for change mode")

    parser.add_option("--resume", dest="resume", action="store_true",
                      help="Run analyser on change mode by continuing from last run when available")
    parser.add_option("--resume-analyser", dest="resume_analyser", action="append",
                      help="Subset of analysers to run in resume mode (can be repeated)")

    parser.add_option("--skip-download", dest="skip_download", action="store_true",
                      help="Don't download extract")
    parser.add_option("--skip-init", dest="skip_init", action="store_true",
                      help="Don't initialize database")
    parser.add_option("--skip-frontend-check", dest="skip_frontend_check", action="store_true",
                      help="Don't check the status of this analyser on the frontend")
    parser.add_option("--skip-analyser", dest="skip_analyser", action="store_true",
                      help="Don't run the analyse part")
    parser.add_option("--skip-upload", dest="skip_upload", action="store_true",
                      help="Don't upload the analyse result")
    parser.add_option("--no-clean", dest="no_clean", action="store_true",
                      help="Don't remove extract and database after analyses")

    parser.add_option("--result-format", dest="result_format", action="store", default="osmose",
                      type="choice", choices=["osmose", "csv", "geojson"],
                      help="Analyser result format. Default 'osmose' XML. For debug purpose can be 'csv' or 'geojson'")

    parser.add_option("--cron", dest="cron", action="store_true",
                      help="Record output in a specific log")
    parser.add_option("--send-alert-email", dest="alert_emails", action="append",
                      help="Send an email alert in case of error")
    parser.add_option("--minimum-free-space", dest="minimum_free_space", type=int,
                      help="Minimum free space required on filesystem before running (in GB)")

    parser.add_option("--extract-update-tool", dest="pbf_update_tool", action="store", default="osmosis",
                      help="Use \"osmosis\" (default) or \"osmium\" to update the OSM extract")

    parser.add_option("--import-tool", dest="import_tool", action="store", default="osmosis",
                      help="Use \"osmosis\" (default) or \"osmosis-parallel\" to import to postgresql database")

    parser.add_option("--version", dest="version", action="store_true",
                      help="Output version information and exit")

    (options, args) = parser.parse_args()

    if options.version:
        print("osmose backend version: %s" % get_version())
        sys.exit(0)

    if not options.country and not options.list_country and not options.list_analyser:
        parser.print_help()
        sys.exit(1)

    sys.exit(main(options))
