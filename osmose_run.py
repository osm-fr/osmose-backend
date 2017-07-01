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
from modules.OsmState import OsmState
from cStringIO import StringIO
import sys, os, fcntl, urllib, urllib2, traceback
try:
    import poster.encode
    import poster.streaminghttp
    poster.streaminghttp.register_openers()
    has_poster_lib = True
except:
    has_poster_lib = False
import psycopg2
import modules.config
import osmose_config as config
import inspect
import fileinput
import shutil
import datetime
import dateutil.parser
import socket
import subprocess
import time

#proxy_support = urllib2.ProxyHandler()
#print proxy_support.proxies
#opener = urllib2.build_opener(proxy_support)
#urllib2.install_opener(opener)

###########################################################################
## fonctions utiles

def get_pstree(pid=os.getpid()):
    tree = []
    while os.path.isdir("/proc/%d"%pid):
        tree.append((pid, open("/proc/%d/cmdline"%pid).read().replace('\x00', ' ').strip()))
        pid = int(open("/proc/%d/stat"%pid).read().split(" ")[3])
    tree.reverse()
    return tree

class lockfile:
    def __init__(self, filename):
        #return
        self.fn = filename
        try:
            olddata = open(self.fn, "r").read()
        except:
            olddata = ""
        try:
            self.fd = open(self.fn, "w")
            for l in get_pstree():
                self.fd.write("%6d %s\n"%l)
            self.fd.flush()
            fcntl.flock(self.fd, fcntl.LOCK_NB|fcntl.LOCK_EX)
        except:
            #restore old data
            self.fd.close()
            open(self.fn, "w").write(olddata)
            raise
        self.ok = True
    def __del__(self):
        #return
        if "fd" in dir(self):
            try:
                fcntl.flock(self.fd, fcntl.LOCK_NB|fcntl.LOCK_UN)
                self.fd.close()
            except:
                pass
        if "fn" in dir(self) and "ok" in dir(self):
            try:
                os.remove(self.fn)
            except:
                pass


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

def set_pgsql_schema(conf, logger, reset=False):
    if reset:
        db_schema = '"$user"'
    elif conf.db_schema:
        db_schema = conf.db_schema
    else:
        db_schema = conf.country
    logger.log("set pgsql schema to %s" % db_schema)
    cmd  = ["psql"]
    cmd += conf.db_psql_args
    cmd += ["-c", "ALTER ROLE %s IN DATABASE %s SET search_path = %s,public;" % (conf.db_user, conf.db_base, db_schema)]
    logger.execute_out(cmd)

###########################################################################

def lock_osmosis_database(logger):
    osmosis_lock = False
    for trial in xrange(60):
        # acquire lock
        try:
            lfil = "/tmp/osmose-osmosis_import"
            osmosis_lock = lockfile(lfil)
            break
        except:
            logger.log(logger.log_av_r + "can't lock %s" % lfil + logger.log_ap)
            logger.log("waiting 2 minutes")
            time.sleep(2*60)

    if not osmosis_lock:
        logger.log(logger.log_av_r + "definitively can't lock" + logger.log_ap)
        raise
    return osmosis_lock


def check_database(conf, logger):

    if "osmosis" in conf.download:
        # check if database contains all necessary extensions
        logger.sub().log("check database")
        gisconn = psycopg2.connect(conf.db_string)
        giscurs = gisconn.cursor()
        for extension in ["hstore", "fuzzystrmatch", "unaccent"]:
            giscurs.execute("""SELECT installed_version FROM pg_available_extensions
                               WHERE name = %s""",
                            [extension])
            if giscurs.rowcount != 1 or giscurs.fetchone()[0] == None:
                logger.log(logger.log_av_r+u"missing extension: "+extension+logger.log_ap)
                return False

        for table in ["geometry_columns", "spatial_ref_sys"]:
            giscurs.execute("""SELECT tablename FROM pg_tables
                               WHERE tablename = %s""",
                            [table])
            if giscurs.rowcount != 1:
                # On PostGIS 2.0, geometry_columns has been moved to a view
                giscurs.execute("""SELECT viewname FROM pg_views
                                   WHERE viewname = %s""",
                                [table])
                if giscurs.rowcount != 1:
                    logger.log(logger.log_av_r+u"missing table: "+table+logger.log_ap)
                    return False
                else:
                    # No need to check permissions for views
                    continue
            for perm in ["select", "update", "delete"]:
                giscurs.execute("SELECT has_table_privilege(%s, %s)",
                                [table,  perm])
                if giscurs.fetchone()[0] == False:
                    logger.log(logger.log_av_r+u"missing permission %s on table: %s" % (perm, table)+logger.log_ap)
                    return False

        giscurs.close()
        gisconn.close()

    return True

def init_database(conf, logger):

    # import osmosis
    if "osmosis" in conf.download:
        osmosis_lock = lock_osmosis_database(logger)
        set_pgsql_schema(conf, logger, reset=True)

        # drop schema if present - might be remaining from a previous failing import
        logger.sub().log("DROP SCHEMA %s" % conf.download["osmosis"])
        gisconn = psycopg2.connect(conf.db_string)
        giscurs = gisconn.cursor()
        sql = "DROP SCHEMA IF EXISTS %s CASCADE;" % conf.download["osmosis"]
        giscurs.execute(sql)
        gisconn.commit()
        giscurs.close()
        gisconn.close()

        # schema
        logger.log(logger.log_av_r+"import osmosis schema"+logger.log_ap)
        for script in conf.osmosis_pre_scripts:
            cmd  = ["psql"]
            cmd += conf.db_psql_args
            cmd += ["-f", script]
            logger.execute_out(cmd)

        # data
        logger.log(logger.log_av_r+"import osmosis data"+logger.log_ap)
        cmd  = [conf.bin_osmosis]
        dst_ext = os.path.splitext(conf.download["dst"])[1]
        dir_country_tmp = os.path.join(conf.dir_tmp, conf.download["osmosis"])
        shutil.rmtree(dir_country_tmp, ignore_errors=True)
        os.makedirs(dir_country_tmp)
        if dst_ext == ".pbf":
            cmd += ["--read-pbf", "file=%s" % conf.download["dst"]]
        else:
            cmd += ["--read-xml", "file=%s" % conf.download["dst"]]
        cmd += ["-quiet"]
        cmd += ["--write-pgsql-dump", "directory=%s"%dir_country_tmp, "enableLinestringBuilder=yes"]
        logger.execute_err(cmd)

        for script in conf.osmosis_import_scripts:
            cmd  = ["psql"]
            cmd += conf.db_psql_args
            cmd += ["-f", script]
            logger.execute_out(cmd, cwd=dir_country_tmp)

        shutil.rmtree(dir_country_tmp, ignore_errors=True)

        # post import scripts
        logger.log(logger.log_av_r+"import osmosis post scripts"+logger.log_ap)
        for script in conf.osmosis_post_scripts:
            cmd  = ["psql"]
            cmd += conf.db_psql_args
            cmd += ["-f", script]
            logger.execute_out(cmd)

        # rename table
        logger.log(logger.log_av_r+"rename osmosis tables"+logger.log_ap)
        gisconn = psycopg2.connect(conf.db_string)
        giscurs = gisconn.cursor()
        giscurs.execute("DROP SCHEMA IF EXISTS %s CASCADE" % conf.download["osmosis"])
        giscurs.execute("CREATE SCHEMA %s" % conf.download["osmosis"])

        for t in ["nodes", "ways", "way_nodes", "relations", "relation_members", "users", "schema_info", "metainfo"]:
            sql = "ALTER TABLE %s SET SCHEMA %s;" % (t, conf.download["osmosis"])
            giscurs.execute(sql)

        gisconn.commit()
        giscurs.close()
        gisconn.close()

        # free lock
        del osmosis_lock


def update_metainfo(conf, logger):

    if "osmosis" in conf.download:

        # Fill metainfo table
        gisconn = psycopg2.connect(conf.db_string)
        giscurs = gisconn.cursor()

        try:
            diff_path = conf.download["diff_path"]
            osm_state = OsmState(os.path.join(diff_path, "state.txt")).timestamp()
        except:
            from modules.OsmPbf import OsmPbfReader
            osm_state = OsmPbfReader(conf.download["dst"], None).timestamp()

        sql = "UPDATE %s.metainfo " % conf.download["osmosis"]
        giscurs.execute(sql + "SET tstamp = %s", [ osm_state])

        gisconn.commit()
        giscurs.close()
        gisconn.close()


def clean_database(conf, logger, no_clean):

    if "osmosis" in conf.download:
        gisconn = psycopg2.connect(conf.db_string)
        giscurs = gisconn.cursor()

        if conf.db_persistent:
            pass

        elif no_clean:
            # grant read-only access to everybody
            logger.sub().log("GRANT USAGE %s" % conf.download["osmosis"])
            sql = "GRANT USAGE ON SCHEMA %s TO public" % conf.download["osmosis"]
            logger.sub().log(sql)
            giscurs.execute(sql)
            for t in ["nodes", "ways", "way_nodes", "relations", "relation_members", "users", "schema_info", "metainfo"]:
               sql = "GRANT SELECT ON %s.%s TO public" % (conf.download["osmosis"], t)
               logger.sub().log(sql)
               giscurs.execute(sql)

        else:
            # drop all tables
            logger.sub().log("DROP SCHEMA %s" % conf.download["osmosis"])
            sql = "DROP SCHEMA IF EXISTS %s CASCADE;" % conf.download["osmosis"]
            logger.sub().log(sql)
            giscurs.execute(sql)

        gisconn.commit()
        giscurs.close()
        gisconn.close()

###########################################################################

def check_osmosis_diff(conf, logger):

    logger.log("check osmosis replication")
    diff_path = conf.download["diff_path"]
    if not os.path.exists(diff_path):
        return False

    for f_name in ["configuration.txt", "download.lock", "state.txt"]:
        f = os.path.join(diff_path, f_name)
        if not os.path.exists(f):
            return False

    return True

def init_osmosis_diff(conf, logger):

    logger.log(logger.log_av_r+"init osmosis replication for diff"+logger.log_ap)
    diff_path = conf.download["diff_path"]

    for f_name in ["configuration.txt", "download.lock", "state.txt"]:
        f = os.path.join(diff_path, f_name)
        if os.path.exists(f):
            os.remove(f)

    cmd  = [conf.bin_osmosis]
    cmd += ["--read-replication-interval-init", "workingDirectory=%s" % diff_path]
    cmd += ["-quiet"]
    logger.execute_err(cmd)

    for line in fileinput.input(os.path.join(diff_path, "configuration.txt"), inplace=1):
        if line.startswith("baseUrl"):
            sys.stdout.write("baseUrl=" + conf.download["diff"])
        elif line.startswith("maxInterval"):
            if "geofabrik" in conf.download["diff"]:
                # on daily diffs provided by Geofabrik, we should apply only one diff at a time
                sys.stdout.write("maxInterval=" + str(60*60*24/2)) # 1/2 day at most
            else:
                sys.stdout.write("maxInterval=" + str(7*60*60*24)) # 7 day at most
        else:
            sys.stdout.write(line)
    fileinput.close()

    try:
        download.dl(conf.download["diff"] + "state.txt",
                    os.path.join(diff_path, "state.txt"),
                    logger.sub(),
                    min_file_size=10)

    except:
        if conf.download["diff"].endswith("minute/"):
            from modules import OsmTs
            OsmTs.run(conf.download["dst"],
                      os.path.join(diff_path, "state.txt"),
                      "minute", logger)
        else:
            raise


def run_osmosis_diff(conf, logger):

    logger.log(logger.log_av_r+"run osmosis replication"+logger.log_ap)
    diff_path = conf.download["diff_path"]
    xml_change = os.path.join(diff_path, "change.osc.gz")
    tmp_pbf_file = conf.download["dst"] + ".tmp"

    shutil.copyfile(os.path.join(diff_path, "state.txt"),
                    os.path.join(diff_path, "state.txt.old"))

    try:
        prev_state_ts = None
        is_uptodate = False
        nb_iter = 0

        osm_state = OsmState(os.path.join(diff_path, "state.txt"))
        cur_ts = datetime.datetime.today()
        print("state: ", osm_state.timestamp(), end=' ')
        if osm_state.timestamp() < (cur_ts - datetime.timedelta(days=10)):
            # Skip updates, and directly download .pbf file if extract is too old
            logger.log(logger.log_av_r + "stop updates, to download full extract" + logger.log_ap)
            return (False, None)


        while not is_uptodate and nb_iter < 30:
            nb_iter += 1
            logger.log("iteration=%d" % nb_iter)

            try:
                cmd  = [conf.bin_osmosis]
                cmd += ["--read-replication-interval", "workingDirectory=%s" % diff_path]
                cmd += ["--simplify-change", "--write-xml-change", "file=%s" % xml_change]
                cmd += ["-quiet"]
                logger.execute_err(cmd)
            except:
                logger.log("waiting 2 minutes")
                time.sleep(2*60)
                continue

            cmd  = [conf.bin_osmosis]
            cmd += ["--read-xml-change", "file=%s" % xml_change]
            cmd += ["--read-pbf", "file=%s" % conf.download["dst"] ]
            cmd += ["--apply-change", "--buffer"]
            cmd += ["--write-pbf", "file=%s" % tmp_pbf_file]
            cmd += ["-quiet"]
            logger.execute_err(cmd)

            shutil.move(tmp_pbf_file, conf.download["dst"])

            # find if state.txt is more recent than one day
            osm_state = OsmState(os.path.join(diff_path, "state.txt"))
            cur_ts = datetime.datetime.today()
            print("state: ", nb_iter, " - ", osm_state.timestamp(), end=' ')
            if prev_state_ts != None:
                print("   ", prev_state_ts - osm_state.timestamp())
            if osm_state.timestamp() > (cur_ts - datetime.timedelta(days=1)):
                is_uptodate = True
            elif prev_state_ts == osm_state.timestamp():
                is_uptodate = True
            else:
                prev_state_ts = osm_state.timestamp()

        if not is_uptodate:
            # we didn't get the latest version of the pbf file
            logger.log(logger.log_av_r + "didn't get latest version of osm file" + logger.log_ap)
            return (False, None)
        elif nb_iter == 1:
            return (True, xml_change)
        else:
            # TODO: we should return a merge of all xml change files
            return (True, None)

    except:
        logger.log(logger.log_av_r+"got error, aborting"+logger.log_ap)
        shutil.copyfile(os.path.join(diff_path, "state.txt.old"),
                        os.path.join(diff_path, "state.txt"))

        raise

###########################################################################

def check_osmosis_change(conf, logger):

    if not check_osmosis_diff(conf, logger):
        return False

    logger.log("check osmosis replication for database")

    return True


def init_osmosis_change(conf, logger):

    init_osmosis_diff(conf, logger)

    logger.log(logger.log_av_r+"import osmosis change post scripts"+logger.log_ap)
    set_pgsql_schema(conf, logger)
    for script in conf.osmosis_change_init_post_scripts:
        cmd  = ["psql"]
        cmd += conf.db_psql_args
        cmd += ["-f", script]
        logger.execute_out(cmd)
    set_pgsql_schema(conf, logger, reset=True)

def run_osmosis_change(conf, logger):

    logger.log(logger.log_av_r+"run osmosis replication"+logger.log_ap)
    diff_path = conf.download["diff_path"]
    xml_change = os.path.join(diff_path, "change.osc.gz")

    shutil.copyfile(os.path.join(diff_path, "state.txt"),
                    os.path.join(diff_path, "state.txt.old"))

    try:
        osmosis_lock = lock_osmosis_database(logger)
        set_pgsql_schema(conf, logger)
        cmd  = [conf.bin_osmosis]
        cmd += ["--read-replication-interval", "workingDirectory=%s" % diff_path]
        cmd += ["--simplify-change", "--write-xml-change", "file=%s" % xml_change]
        cmd += ["-quiet"]
        logger.execute_err(cmd)

        cmd  = ["psql"]
        cmd += conf.db_psql_args
        cmd += ["-c", "TRUNCATE TABLE actions"]
        logger.execute_out(cmd)

        cmd  = [conf.bin_osmosis]
        cmd += ["--read-xml-change", xml_change]
        cmd += ["--write-pgsql-change", "database=%s"%conf.db_base, "user=%s"%conf.db_user, "password=%s"%conf.db_password]
        cmd += ["-quiet"]
        logger.execute_err(cmd)

        logger.log(logger.log_av_r+"import osmosis change post scripts"+logger.log_ap)
        for script in conf.osmosis_change_post_scripts:
            logger.log(script)
            cmd  = ["psql"]
            cmd += conf.db_psql_args
            cmd += ["-f", script]
            logger.execute_out(cmd)
        set_pgsql_schema(conf, logger, reset=True)
        del osmosis_lock

        # Fill metainfo table
        gisconn = psycopg2.connect(conf.db_string)
        giscurs = gisconn.cursor()

        osm_state = OsmState(os.path.join(diff_path, "state.txt"))
        giscurs.execute("UPDATE metainfo SET tstamp = %s", [osm_state.timestamp()])

        gisconn.commit()
        giscurs.close()
        gisconn.close()

        return xml_change

    except:
        logger.log(logger.log_av_r+"got error, aborting"+logger.log_ap)
        shutil.copyfile(os.path.join(diff_path, "state.txt.old"),
                        os.path.join(diff_path, "state.txt"))

        raise


###########################################################################


def run_osmosis_resume(conf, logger, tstamp):
    logger.log(logger.log_av_r+"import osmosis resume post scripts"+logger.log_ap)
    set_pgsql_schema(conf, logger)
    for script in conf.osmosis_resume_init_post_scripts:
        cmd  = ["psql"]
        cmd += conf.db_psql_args
        cmd += ["-f", script]
        logger.execute_out(cmd)


###########################################################################

def run(conf, logger, options):

    err_code = 0
    country = conf.country
    try:
      version = get_version()
    except:
      version = None

    if not check_database(conf, logger):
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

    # variable used by osmosis
    if not "JAVACMD_OPTIONS" in os.environ:
        os.environ["JAVACMD_OPTIONS"] = ""
    os.environ["JAVACMD_OPTIONS"] += " -Djava.io.tmpdir="+conf.dir_tmp
    os.environ["JAVACMD_OPTIONS"] += " -Duser.timezone=GMT"

    ##########################################################################
    ## download and create database

    if options.skip_init:
        pass

    elif options.change and check_osmosis_change(conf, logger) and not options.change_init:
        xml_change = run_osmosis_change(conf, logger)

    elif "url" in conf.download:
        newer = False
        xml_change = None
        updated = False  # set if extract was updated instead of fully downloaded

        if options.diff and check_osmosis_diff(conf, logger) and os.path.exists(conf.download["dst"]):
            (status, xml_change) = run_osmosis_diff(conf, logger)
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

        init_database(conf, logger)

        if options.change:
            init_osmosis_change(conf, logger)
        elif options.diff and not updated:
            init_osmosis_diff(conf, logger)

    if hasattr(conf, "sql_post_scripts"):
        logger.log(logger.log_av_r+"import post scripts"+logger.log_ap)
        for script in conf.sql_post_scripts:
            cmd  = ["psql"]
            cmd += conf.db_psql_args
            cmd += ["-f", script]
            logger.execute_out(cmd)

    if not options.skip_init and "osmosis" in conf.download:
        update_metainfo(conf, logger)

    if options.resume:
        run_osmosis_resume(conf, logger)

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

            analyser_conf.db_string = conf.db_string
            analyser_conf.db_user = conf.db_user
            if conf.db_schema:
                analyser_conf.db_schema = conf.db_schema
            else:
                analyser_conf.db_schema = country

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
                                        tmp_req = urllib2.Request(url, tmp_dat, tmp_headers)
                                        fd = urllib2.urlopen(tmp_req, timeout=1800)

                                    else:
                                        tmp_req = urllib2.Request(url)
                                        tmp_url = os.path.join(conf.results_url, analyser_conf.dst_file)
                                        tmp_dat = urllib.urlencode([('url', tmp_url),
                                                                    ('source', tmp_src),
                                                                    ('code', password)])
                                        fd = urllib2.urlopen(tmp_req, tmp_dat, timeout=1800)

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
                    with obj as o:
                        o.analyser_resume_clean()

    ##########################################################################
    ## final cleaning

    logger.log(logger.log_av_r + u"cleaning : " + country + logger.log_ap)

    if options.change:
        pass
    else:
        clean_database(conf, logger, options.no_clean or not conf.clean_at_end)

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
