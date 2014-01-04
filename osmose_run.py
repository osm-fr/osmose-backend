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

from modules import OsmoseLog, download
from cStringIO import StringIO
import sys, time, os, fcntl, urllib, urllib2, traceback
import psycopg2
import osmose_config as config
import inspect
import fileinput
import shutil
import datetime
import dateutil.parser

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

###########################################################################

def check_database(conf):

    if "osmosis" in conf.download:
        # check if database contains all necessary extensions
        logger.sub().log("check database")
        gisconn = psycopg2.connect(conf.db_string)
        giscurs = gisconn.cursor()
        for extension in ["hstore", "fuzzystrmatch"]:
            giscurs.execute("""SELECT installed_version FROM pg_available_extensions
                               WHERE name = %s""",
                            [extension])
            if giscurs.rowcount != 1 or giscurs.fetchone()[0] == None:
                logger.log(log_av_r+u"missing extension: "+extension+log_ap)
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
                    logger.log(log_av_r+u"missing table: "+table+log_ap)
                    return False
                else:
                    # No need to check permissions for views
                    continue
            for perm in ["select", "update", "delete"]:
                giscurs.execute("SELECT has_table_privilege(%s, %s)",
                                [table,  perm])
                if giscurs.fetchone()[0] == False:
                    logger.log(log_av_r+u"missing permission %s on table: %s" % (perm, table)+log_ap)
                    return False

        giscurs.close()
        gisconn.close()

    return True

def init_database(conf):

    # import posgis
    if "osm2pgsql" in conf.download:
        logger.log(log_av_r+"import postgis : "+conf.download["osm2pgsql"]+log_ap)
        cmd = [conf.bin_osm2pgsql]
        cmd.append('--slim')
        cmd.append('--style=%s'%os.path.join(conf.dir_osm2pgsql,'default.style'))
        cmd.append('--merc')
        cmd.append('--database=%s'%conf.db_base)
        cmd.append('--username=%s'%conf.db_user)
        cmd.append('--prefix='+conf.download["osm2pgsql"])
        cmd.append(conf.download["dst"])
        logger.execute_err(cmd)

    # import osmosis
    if "osmosis" in conf.download:
        osmosis_lock = False
        for trial in xrange(60):
            # acquire lock
            try:
                lfil = "/tmp/osmose-osmosis_import"
                osmosis_lock = lockfile(lfil)
                break
            except:
                logger.log(log_av_r + "can't lock %s" % lfil + log_ap)
                logger.log("waiting 2 minutes")
                time.sleep(2*60)

        if not osmosis_lock:
            logger.log(log_av_r + "definitively can't lock" + log_ap)
            raise

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
        logger.log(log_av_r+"import osmosis schema"+log_ap)
        for script in conf.osmosis_pre_scripts:
            cmd  = ["psql"]
            cmd += ["-d", conf.db_base]
            cmd += ["-U", conf.db_user]
            cmd += ["-f", script]
            logger.execute_out(cmd)

        # data
        logger.log(log_av_r+"import osmosis data"+log_ap)
        cmd  = [conf.osmosis_bin]
        dst_ext = os.path.splitext(conf.download["dst"])[1]
        if dst_ext == ".pbf":
            cmd += ["--read-pbf", "file=%s" % conf.download["dst"]]
        else:
            cmd += ["--read-xml", "file=%s" % conf.download["dst"]]
        cmd += ["-quiet"]
        cmd += ["--write-pgsql", "database=%s"%conf.db_base, "user=%s"%conf.db_user, "password=%s"%conf.db_password]
        logger.execute_err(cmd)

        # post import scripts
        logger.log(log_av_r+"import osmosis post scripts"+log_ap)
        for script in conf.osmosis_post_scripts:
            cmd  = ["psql"]
            cmd += ["-d", conf.db_base]
            cmd += ["-U", conf.db_user]
            cmd += ["-f", script]
            logger.execute_out(cmd)

        # rename table
        logger.log(log_av_r+"rename osmosis tables"+log_ap)
        gisconn = psycopg2.connect(conf.db_string)
        giscurs = gisconn.cursor()
        giscurs.execute("DROP SCHEMA IF EXISTS %s CASCADE" % conf.download["osmosis"])
        giscurs.execute("CREATE SCHEMA %s" % conf.download["osmosis"])

        for t in ["nodes", "ways", "way_nodes", "relations", "relation_members", "users"]:
            sql = "ALTER TABLE %s SET SCHEMA %s;" % (t, conf.download["osmosis"])
            giscurs.execute(sql)

        gisconn.commit()
        giscurs.close()
        gisconn.close()

        # free lock
        del osmosis_lock

def clean_database(conf, no_clean):

    if set(("osm2pgsql", "osmosis")).isdisjoint(conf.download.keys()):
       return

    gisconn = psycopg2.connect(conf.db_string)
    giscurs = gisconn.cursor()

    if "osm2pgsql" in conf.download:
        if no_clean:
            pass
        else:
            for t in tables:
                if t in [conf.download["osm2pgsql"]+suffix for suffix in ["_line", "_nodes", "_point", "_polygon", "_rels", "_roads", "_ways"]]:
                    logger.sub().log("DROP TABLE %s"%t)
                    giscurs.execute("DROP TABLE %s;"%t)

    if "osmosis" in conf.download:
        if no_clean:
            # grant read-only access to everybody
            logger.sub().log("GRANT USAGE %s" % conf.download["osmosis"])
            sql = "GRANT USAGE ON SCHEMA %s TO public" % conf.download["osmosis"]
            logger.sub().log(sql)
            giscurs.execute(sql)
            for t in ("nodes", "relation_members", "relations", "users", "way_nodes", "ways"):
               sql = "GRANT SELECT ON %s.%s TO public" % (conf.download["osmosis"], t)
               logger.sub().log(sql)
               giscurs.execute(sql)

        else:
            # drop all tables
            logger.sub().log("DROP SCHEMA %s" % conf.download["osmosis"])
            sql = "DROP SCHEMA %s CASCADE;" % conf.download["osmosis"]
            logger.sub().log(sql)
            giscurs.execute(sql)

    gisconn.commit()
    giscurs.close()
    gisconn.close()

###########################################################################

def check_osmosis_diff(conf):

    logger.log("check osmosis replication")
    diff_path = conf.download["diff_path"]
    if not os.path.exists(diff_path):
        return False

    for f_name in ["configuration.txt", "download.lock", "state.txt"]:
        f = os.path.join(diff_path, f_name)
        if not os.path.exists(f):
            return False

    return True

def init_osmosis_diff(conf):

    logger.log(log_av_r+"init osmosis replication for diff"+log_ap)
    diff_path = conf.download["diff_path"]
    if os.path.exists(diff_path):
        for f_name in ["configuration.txt", "download.lock", "state.txt"]:
            f = os.path.join(diff_path, f_name)
            if os.path.exists(f):
                os.remove(f)
    else:
        os.makedirs(diff_path)
    cmd  = [conf.osmosis_bin]
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

    if conf.download["diff"].endswith("minute/"):
        from modules import OsmTs
        OsmTs.run(conf.download["dst"],
                  os.path.join(diff_path, "state.txt"),
                  "minute", logger)

    else:
        download.dl(conf.download["diff"] + "state.txt",
                    os.path.join(diff_path, "state.txt"),
                    logger.sub(),
                    min_file_size=10)

def run_osmosis_diff(conf):

    logger.log(log_av_r+"run osmosis replication"+log_ap)
    diff_path = conf.download["diff_path"]
    xml_change = os.path.join(diff_path, "change.osc.gz")
    tmp_pbf_file = conf.download["dst"] + ".tmp"

    shutil.copyfile(os.path.join(diff_path, "state.txt"),
                    os.path.join(diff_path, "state.txt.old"))

    try:
        prev_state_ts = None
        is_uptodate = False
        nb_iter = 0

        with open(os.path.join(diff_path, "state.txt"), 'r') as f:
           state_lines = f.readlines()
        for line in state_lines:
           print "state: ", line,

        while not is_uptodate and nb_iter < 30:
            nb_iter += 1
            logger.log("iteration=%d" % nb_iter)

            try:
                cmd  = [conf.osmosis_bin]
                cmd += ["--read-replication-interval", "workingDirectory=%s" % diff_path]
                cmd += ["--simplify-change", "--write-xml-change", "file=%s" % xml_change]
                cmd += ["-quiet"]
                logger.execute_err(cmd)
            except:
                logger.log("waiting 2 minutes")
                time.sleep(2*60)
                continue

            cmd  = [conf.osmosis_bin]
            cmd += ["--read-xml-change", "file=%s" % xml_change]
            cmd += ["--read-pbf", "file=%s" % conf.download["dst"] ]
            cmd += ["--apply-change", "--buffer"]
            cmd += ["--write-pbf", "file=%s" % tmp_pbf_file]
            cmd += ["-quiet"]
            logger.execute_err(cmd)

            shutil.move(tmp_pbf_file, conf.download["dst"])

            # find if state.txt is more recent than one day
            with open(os.path.join(diff_path, "state.txt"), 'r') as f:
               state_lines = f.readlines()
            for line in state_lines:
               print "state: ", nb_iter, " - ", line,
               if line.startswith("timestamp="):
                   s = line.translate(None, "\\")
                   state_ts = dateutil.parser.parse(s[len("timestamp="):]).replace(tzinfo=None)
                   cur_ts = datetime.datetime.today()
                   print prev_state_ts, state_ts
                   if prev_state_ts != None:
                      print "   ", prev_state_ts - state_ts
                   if state_ts > (cur_ts - datetime.timedelta(1)):
                       is_uptodate = True
                   elif prev_state_ts == state_ts:
                       is_uptodate = True
                   else:
                       prev_state_ts = state_ts

        if nb_iter == 1:
            return xml_change
        else:
            # TODO: we should return a merge of all xml change files
            return None

    except:
        logger.log(log_av_r+"got error, aborting"+log_ap)
        shutil.copyfile(os.path.join(diff_path, "state.txt.old"),
                        os.path.join(diff_path, "state.txt"))

        raise

###########################################################################

def check_osmosis_change(conf):

    if not check_osmosis_diff(conf):
        return False

    logger.log("check osmosis replication for database")

    return True


def init_osmosis_change(conf):

    init_osmosis_diff(conf)

    logger.log(log_av_r+"init osmosis replication for database"+log_ap)
    if conf.db_schema:
        db_schema = conf.db_schema
    else:
        db_schema = conf.country
    cmd  = ["psql"]
    cmd += ["-d", conf.db_base]
    cmd += ["-U", conf.db_user]
    cmd += ["-c", "ALTER ROLE %s IN DATABASE %s SET search_path = %s,public;" % (conf.db_user, conf.db_base, db_schema)]
    logger.execute_out(cmd)

    logger.log(log_av_r+"import osmosis change post scripts"+log_ap)
    for script in conf.osmosis_change_init_post_scripts:
        cmd  = ["psql"]
        cmd += ["-d", conf.db_base]
        cmd += ["-U", conf.db_user]
        cmd += ["-f", script]
        logger.execute_out(cmd)

def run_osmosis_change(conf):

    logger.log(log_av_r+"run osmosis replication"+log_ap)
    diff_path = conf.download["diff_path"]
    xml_change = os.path.join(diff_path, "change.osc.gz")

    shutil.copyfile(os.path.join(diff_path, "state.txt"),
                    os.path.join(diff_path, "state.txt.old"))

    try:
        cmd  = [conf.osmosis_bin]
        cmd += ["--read-replication-interval", "workingDirectory=%s" % diff_path]
        cmd += ["--simplify-change", "--write-xml-change", "file=%s" % xml_change]
        cmd += ["-quiet"]
        logger.execute_err(cmd)

        cmd  = ["psql"]
        cmd += ["-d", conf.db_base]
        cmd += ["-U", conf.db_user]
        cmd += ["-c", "TRUNCATE TABLE actions"]
        logger.execute_out(cmd)

        cmd  = [conf.osmosis_bin]
        cmd += ["--read-xml-change", xml_change]
        cmd += ["--write-pgsql-change", "database=%s"%conf.db_base, "user=%s"%conf.db_user, "password=%s"%conf.db_password]
        cmd += ["-quiet"]
        logger.execute_err(cmd)

        logger.log(log_av_r+"import osmosis change post scripts"+log_ap)
        for script in conf.osmosis_change_post_scripts:
            logger.log(script)
            cmd  = ["psql"]
            cmd += ["-d", conf.db_base]
            cmd += ["-U", conf.db_user]
            cmd += ["-f", script]
            logger.execute_out(cmd)

        return xml_change

    except:
        logger.log(log_av_r+"got error, aborting"+log_ap)
        shutil.copyfile(os.path.join(diff_path, "state.txt.old"),
                        os.path.join(diff_path, "state.txt"))

        raise


###########################################################################

def run(conf, logger, options):

    err_code = 0
    country = conf.country

    if not check_database(conf):
        logger.log(log_av_r+u"error in database initialisation"+log_ap)
        return 0x10

    # variable used by osmosis
    os.environ["JAVACMD_OPTIONS"] = "-Xms2048M -Xmx2048M -XX:MaxPermSize=2048M -Djava.io.tmpdir="+conf.dir_tmp
    if "http_proxy" in os.environ:
        (_tmp, host, port) = os.environ["http_proxy"].split(":")
        host = host.split("/")[2]
        os.environ["JAVACMD_OPTIONS"] += " -Dhttp.proxyHost=%s -Dhttp.proxyPort=%s" % (host, port)
        os.environ["JAVACMD_OPTIONS"] += " -Djava.net.preferIPv6Addresses=false"

    ##########################################################################
    ## download and create database

    if options.skip_init:
        pass
   
    elif options.change and check_osmosis_change(conf) and not options.change_init:
        xml_change = run_osmosis_change(conf)

    elif "url" in conf.download:
        xml_change = None
        if options.diff and check_osmosis_diff(conf) and os.path.exists(conf.download["dst"]):
            xml_change = run_osmosis_diff(conf)
            newer = True  # TODO

        elif options.skip_download:
            logger.sub().log("skip download")
            newer = True

        else:
            logger.log(log_av_r+u"downloading"+log_ap)
            newer = download.dl(conf.download["url"], conf.download["dst"], logger.sub())

        if not newer:
            return 0

        init_database(conf)

        if options.change:
            init_osmosis_change(conf)
        elif options.diff and not xml_change:
            init_osmosis_diff(conf)

    if hasattr(conf, "sql_post_scripts"):
        logger.log(log_av_r+"import post scripts"+log_ap)
        for script in conf.sql_post_scripts:
            cmd  = ["psql"]
            cmd += ["-d", conf.db_base]
            cmd += ["-U", conf.db_user]
            cmd += ["-f", script]
            logger.execute_out(cmd)

    ##########################################################################
    ## analyses
    
    for analyser, password in conf.analyser.iteritems():
        logger.log(log_av_r + country + " : " + analyser + log_ap)

        if not "analyser_" + analyser in analysers:
            logger.sub().log("skipped")
            continue

        if password == "xxx":
            logger.sub().log("code is not correct - won't upload to %s" % conf.updt_url)
        elif not conf.results_url:
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

            for name, obj in inspect.getmembers(analysers["analyser_" + analyser]):
                if (inspect.isclass(obj) and obj.__module__ == "analyser_" + analyser and
                    (name.startswith("Analyser") or name.startswith("analyser"))):
                    # analyse
                    analyser_conf.dst_file = name + "-" + country + ".xml"
                    analyser_conf.dst_file += ".bz2"
                    analyser_conf.dst = os.path.join(conf.dir_results, analyser_conf.dst_file)
                    with obj(analyser_conf, logger.sub()) as analyser_obj:
                        if not options.change or not xml_change:
                            analyser_obj.analyser()
                        else:
                            analyser_obj.analyser_change()

                    # update
                    if conf.results_url and password != "xxx":
                        logger.sub().log("update")
                        try:
                            tmp_req = urllib2.Request(conf.updt_url)
                            tmp_url = os.path.join(conf.results_url, analyser_conf.dst_file)
                            tmp_src = "%s-%s" % (analyser, country)
                            tmp_dat = urllib.urlencode([('url', tmp_url),
                                                        ('source', tmp_src),
                                                        ('code', password)])
                            fd = urllib2.urlopen(tmp_req, tmp_dat, timeout=1800)
                            dt = fd.read().decode("utf8").strip()
                            if dt[-2:] <> "OK":
                                sys.stderr.write((u"UPDATE ERROR %s/%s : %s\n"%(country, analyser, dt)).encode("utf8"))
                            else:
                                logger.sub().sub().log(dt)
                        except:
                            s = StringIO()
                            traceback.print_exc(file=s)
                            logger.sub().log("error on update...")
                            for l in s.getvalue().decode("utf8").split("\n"):
                                logger.sub().sub().log(l)
                            err_code |= 1
                            continue

        except:
            s = StringIO()
            traceback.print_exc(file=s)
            logger.sub().log("error on analyse...")
            for l in s.getvalue().decode("utf8").split("\n"):
                logger.sub().sub().log(l)
            err_code |= 2
            continue

    ##########################################################################
    ## vidange
    
    logger.log(log_av_r + u"cleaning : " + country + log_ap)
    
    if options.change:
        pass
    else:
        clean_database(conf, options.no_clean or not conf.clean_at_end)

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
    log_av_r = u'\033[0;31m'
    log_av_b = u'\033[0;34m'
    log_av_v = u'\033[0;32m'
    log_ap   = u'\033[0m'

    err_code = 0

    #=====================================
    # analyse des arguments

    from optparse import OptionParser

    parser = OptionParser()
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

    parser.add_option("--skip-download", dest="skip_download", action="store_true",
                      help="Don't download extract")
    parser.add_option("--skip-init", dest="skip_init", action="store_true",
                      help="Don't initialize database")
    parser.add_option("--no-clean", dest="no_clean", action="store_true",
                      help="Don't remove extract and database after analyses")

    parser.add_option("--cron", dest="cron", action="store_true",
                      help="Record output in a specific log")

    (options, args) = parser.parse_args()
   
    analysers_path = os.path.join(os.path.dirname(__file__), "analysers")
 
    if options.list_analyser:
        for fn in sorted(os.listdir(analysers_path)):
            if fn.startswith("analyser_") and fn.endswith(".py"):
                print fn[9:-3]
        sys.exit(0)
    
    if options.list_country:
        for k in sorted(config.config.keys()):
           print k
        sys.exit(0)
        
    if options.cron:
        output = sys.stdout
        logger = OsmoseLog.logger(output, False)
    else:
        output = sys.stdout
        logger = OsmoseLog.logger(output, True)

    if options.change_init and not options.change:
        logger.log(log_av_b+"--change must be specified "+fn[:-3]+log_ap)
        sys.exit(1)
        
    #=====================================
    # chargement des analysers
    
    old_path = list(sys.path)
    sys.path.insert(0, analysers_path)

    analysers = {}
    for fn in os.listdir(analysers_path):
        if fn.startswith("analyser_") and fn.endswith(".py"):
            if options.analyser and fn[:-3] not in options.analyser:
                continue
            logger.log(log_av_v+"load "+fn[:-3]+log_ap)
            analysers[fn[:-3]] = __import__(fn[:-3])
    if options.analyser:
        for k in options.analyser:
            if k not in analysers:
                logger.log(log_av_b+"not found "+fn[:-3]+log_ap)
            
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
            logger.log(log_av_r+"can't lock %s"%country+log_ap)
            if options.cron:
                sys.stderr.write("can't lock %s\n"%country)
            for l in open(lfil).read().rstrip().split("\n"):
                logger.log("  "+l)
                if options.cron:
                    sys.stderr.write("  "+l+"\n")
            if options.cron:
                sys.stderr.flush()
            continue

        country_conf.init()
        options.diff = not options.change and "diff" in country_conf.download

        # analyse
        err_code |= run(country_conf, logger, options)
        
        # free lock
        del lock
            
    logger.log(log_av_v+u"end of analyses"+log_ap)
    sys.exit(err_code)
