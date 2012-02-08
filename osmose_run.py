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
import osmose_config as config
import inspect

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

def run(conf, logger, skip_download, no_clean, change):

    country = conf.country

    ##########################################################################
    ## téléchargement
    
    for n, d in conf.download.iteritems():
        logger.log(log_av_r+u"téléchargement : "+n+log_ap)
        if skip_download:
            logger.sub().log("skip download")
            newer = True
        else:
            newer = download.dl(d["url"], d["dst"], logger.sub())

        if not newer:
            return

        # import posgis
        if "osm2pgsql" in d:
            logger.log(log_av_r+"import postgis : "+d["osm2pgsql"]+log_ap)
            cmd = [conf.common_bin_osm2pgsql]
            cmd.append('--slim')
            cmd.append('--style=%s'%os.path.join(conf.common_dir_osm2pgsql,'default.style'))
            cmd.append('--merc')
            cmd.append('--database=%s'%conf.db_base)
            cmd.append('--username=%s'%conf.db_user)
            cmd.append('--prefix='+d["osm2pgsql"])
            cmd.append(d["dst"])
            logger.execute_err(cmd)


        # import osmosis
        if "osmosis" in d:
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

            # schema
            logger.log(log_av_r+"import osmosis schema"+log_ap)
            cmd  = ["psql"]
            cmd += ["-d", conf.db_base]
            cmd += ["-U", conf.db_user]
            cmd += ["-f", conf.common_osmosis_schema]
            logger.execute_out(cmd)
            cmd  = ["psql"]
            cmd += ["-d", conf.db_base]
            cmd += ["-U", conf.db_user]
            cmd += ["-f", conf.common_osmosis_schema_bbox]
            logger.execute_out(cmd)
            cmd  = ["psql"]
            cmd += ["-d", conf.db_base]
            cmd += ["-U", conf.db_user]
            cmd += ["-f", conf.common_osmosis_schema_linestring]
            logger.execute_out(cmd)

            # data
            logger.log(log_av_r+"import osmosis data"+log_ap)
            os.environ["JAVACMD_OPTIONS"] = "-Xms2048M -Xmx2048M -XX:MaxPermSize=2048M -Djava.io.tmpdir=/data/work/osmose/tmp/"
            cmd  = [conf.common_osmosis_bin]
            cmd += ["--read-xml", "file=%s" % d["dst"]]
#            cmd += ["-quiet"]
            cmd += ["--write-pgsql", "database=%s"%conf.db_base, "user=%s"%conf.db_user, "password=%s"%conf.db_password]
            logger.execute_err(cmd)

            # polygon
            logger.log(log_av_r+"create polygon column"+log_ap)
            cmd  = ["psql"]
            cmd += ["-d", conf.db_base]
            cmd += ["-U", conf.db_user]
            cmd += ["-f", conf.common_osmosis_create_polygon]
            logger.execute_out(cmd)


            # rename table
            logger.log(log_av_r+"rename osmosis tables"+log_ap)
            import psycopg2
            gisconn = psycopg2.connect(conf.db_string)
            giscurs = gisconn.cursor()
            giscurs.execute("DROP SCHEMA IF EXISTS %s CASCADE" % d["osmosis"])
            giscurs.execute("CREATE SCHEMA %s" % d["osmosis"])

            for t in ["nodes", "ways", "way_nodes", "relations", "relation_members", "users"]:
                sql = "ALTER TABLE %s SET SCHEMA %s;" % (t, d["osmosis"])
                giscurs.execute(sql)

            gisconn.commit()
            giscurs.close()
            gisconn.close()

            # free lock
            del osmosis_lock



    ##########################################################################
    ## analyses
    
    for analyser, password in conf.analyser.iteritems():
        logger.log(log_av_r + country + " : " + analyser + log_ap)

        if not "analyser_" + analyser in analysers:
            logger.sub().log("skipped")
            continue

        if password == "xxx":
            logger.sub().log("code is not correct - won't upload to %s" % conf.common_updt_url)

        # analyse
        try:
            analyser_conf = analyser_config()
            analyser_conf.dst_file = "analyser_" + analyser + "-" + country + ".xml"
            if analyser == "sax":
                analyser_conf.dst_file += ".bz2"
            analyser_conf.dst = os.path.join(conf.common_dir_results, analyser_conf.dst_file)

            analyser_conf.db_string = conf.db_string
            analyser_conf.db_user = conf.db_user
            if conf.db_schema:
                analyser_conf.db_schema = conf.db_schema
            else:
                analyser_conf.db_schema = country

            analyser_conf.dir_scripts = conf.common_dir_scripts
            if analyser in conf.analyser_options:
                analyser_conf.options = conf.analyser_options[analyser]
            else:
                analyser_conf.options = None

            if "small" in conf.download:
                analyser_conf.src_small = conf.download["small"]["dst"]
            elif "large" in conf.download:
                analyser_conf.src_small = conf.download["large"]["dst"]

            for name, obj in inspect.getmembers(analysers["analyser_" + analyser]):
                if inspect.isclass(obj) and obj.__module__ == "analyser_" + analyser:
                    analyser_obj = obj(analyser_conf, logger.sub())
                    if not change:
                        analyser_obj.analyser()
                    else:
                        analyser_obj.analyser_change()
        except:
            s = StringIO()
            traceback.print_exc(file=s)
            logger.sub().log("error on analyse...")
            for l in s.getvalue().decode("utf8").split("\n"):
                logger.sub().sub().log(l)
            continue
            
        # update
        if conf.common_results_url and password != "xxx":
            logger.sub().log("update")
            tmp_req = urllib2.Request(conf.common_updt_url)
            tmp_url = os.path.join(conf.common_results_url, analyser_conf.dst_file)
            tmp_dat = urllib.urlencode([('url', tmp_url), ('code', password)])
            fd = urllib2.urlopen(tmp_req, tmp_dat)
            dt = fd.read().decode("utf8").strip()
            if dt[-2:] <> "OK":
                sys.stderr.write((u"UPDATE ERROR %s/%s : %s\n"%(country, analyser, dt)).encode("utf8"))
            else:
                logger.sub().sub().log(dt)
            
    ##########################################################################
    ## vidange
    
    if no_clean:
        return
    if not conf.clean_at_end:
        return
    
    logger.log(log_av_r + u"nettoyage : " + country + log_ap)
    
    import psycopg2
    gisconn = psycopg2.connect(conf.db_string)
    giscurs = gisconn.cursor()
    
    # liste des tables
    tables = []
    sql = "SELECT c.relname FROM pg_catalog.pg_class c LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace WHERE c.relkind='r' AND n.nspname <> 'pg_catalog' AND n.nspname !~ '^pg_toast' AND pg_catalog.pg_table_is_visible(c.oid);"
    giscurs.execute(sql)
    for res in giscurs.fetchall():
        tables.append(res[0])

    # drop des tables
    for n, d in conf.download.iteritems():
        if "osm2pgsql" in d:
            for t in tables:
                if t in [d["osm2pgsql"]+sufix for sufix in ["_line", "_nodes", "_point", "_polygon", "_rels", "_roads", "_ways"]]:
                    logger.sub().log("DROP TABLE %s"%t)
                    giscurs.execute("DROP TABLE %s;"%t)

        if "osmosis" in d:
            # drop des tables osmosis
            logger.sub().log("DROP SCHEMA %s" % d["osmosis"])
            sql = "DROP SCHEMA %s CASCADE;" % d["osmosis"]
            logger.sub().log(sql)
            giscurs.execute(sql)

        gisconn.commit()
        giscurs.close()
        gisconn.close()

        # drop des fichiers
        f = ".osm".join(d["dst"].split(".osm")[:-1])
#       for ext in ["osm", "osm.bz2", "ts", "osm.ts"]:
        for ext in ["osm", "osm.bz2"]:
            try:
                os.remove("%s.%s"%(f, ext))
                logger.sub().log("DROP FILE %s.%s"%(f, ext))
            except:
                pass
    
###########################################################################

if __name__ == "__main__":
    log_av_r = u'\033[0;31m'
    log_av_b = u'\033[0;34m'
    log_av_v = u'\033[0;32m'
    log_ap   = u'\033[0m'
    
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
                      help="Run analyser on change mode when avialable")

    parser.add_option("--skip-download", dest="skip_download", action="store_true",
                      help="Don't download extract")
    parser.add_option("--no-clean", dest="no_clean", action="store_true",
                      help="Don't remove extract and database after analyses")

    parser.add_option("--cron", dest="cron", action="store_true",
                      help="Record output in a specific log")

    (options, args) = parser.parse_args()
    
    if options.list_analyser:
        for fn in sorted(os.listdir(os.path.dirname(__file__))):
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
        
    #=====================================
    # chargement des analysers
    
    analysers = {}
    for fn in os.listdir(os.path.dirname(__file__)):
        if fn.startswith("analyser_") and fn.endswith(".py"):
            if options.analyser and fn[:-3] not in options.analyser:
                continue
            logger.log(log_av_v+"load "+fn[:-3]+log_ap)
            analysers[fn[:-3]] = __import__(fn[:-3])
    if options.analyser:
        for k in options.analyser:
            if k not in analysers:
                logger.log(log_av_b+"not found "+fn[:-3]+log_ap)
            
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
        
        # analyse
        run(country_conf, logger, options.skip_download, options.no_clean, options.change)
        
        # free lock
        del lock
            
    logger.log(log_av_v+u"fin des analyses"+log_ap)
