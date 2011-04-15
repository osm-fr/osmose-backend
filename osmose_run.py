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

def class2dict(cl):
    dc = {}
    for x in dir(cl):
        dc[x] = eval("cl."+x)
    return dc

def dict2class(dc):
    class cl:
        pass
    for x in dc:
        exec("cl."+x+"="+repr(dc[x]))
    return cl

def class2full(cl):
    dc = class2dict(cl)
    if ("download_small_dst" not in dc) and ("download_large_dst" in dc):
        dc["download_small_dst"] = dc["download_large_dst"]
    if ("download_large_dst" not in dc) and ("download_small_dst" in dc):
        dc["download_large_dst"] = dc["download_small_dst"]
    if "download_small_dst" in dc:
        dc["common_src_small"] = dc["download_small_dst"]
    if "download_large_dst" in dc:
        dc["common_src_large"] = dc["download_large_dst"]
    return dict2class(dc)

def class2config(cl, base):
    dc  = class2dict(cl)
    cfg = {}
    for x in dc:
        if x.startswith("common_"):
            cfg[x[len("common_"):]] = dc[x]
    for x in dc:
        if x.startswith(base):
            cfg[x[len(base)+1:]] = dc[x]
    cfg["dst"] = os.path.join(cl.common_dir_results, base + "-" + dc["common_country"] + ".xml")
    if base == "analyser_sax":
        cfg["dst"] += ".bz2"
    return dict2class(cfg)
    
def run(cl, logger, skip_dl):
    cl = class2full(cl)
    dc = class2dict(cl)

    ##########################################################################
    ## téléchargement
    
    for k in dc:
        if not(k.startswith("download_") and k.endswith("_url")):
            continue
        logger.log(log_av_r+u"téléchargement : "+dc[k]+log_ap)
        if skip_dl:
            logger.sub().log("skip download")
            newer = True
        else:
            newer = download.dl(dc[k], dc[k[:-3]+"dst"], logger.sub())

        # import posgis
        if newer and k[:-3]+"gis" in dc:
            logger.log(log_av_r+"import postgis : "+dc[k[:-3]+"gis"]+log_ap)
            cmd = [dc['common_bin_osm2pgsql']]
            cmd.append('--slim')
            cmd.append('--style=%s'%os.path.join(dc['common_dir_osm2pgsql'],'default.style'))
            cmd.append('--merc')
            cmd.append('--database=%s'%dc['common_dbn'])
            cmd.append('--username=%s'%dc['common_dbu'])
            cmd.append('--prefix='+dc[k[:-3]+"gis"])
            cmd.append(dc[k[:-3]+"dst"])
            logger.execute_err(cmd)


        # import osmosis
        if (newer and k[:-3]+"sis" in dc) and (dc[k[:-3]+"sis"]):
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
            cmd += ["-d", dc['common_dbn']]
            cmd += ["-U", dc['common_dbu']]
            cmd += ["-f", dc['common_osmosis_schema']]
            logger.execute_out(cmd)
            cmd  = ["psql"]
            cmd += ["-d", dc['common_dbn']]
            cmd += ["-U", dc['common_dbu']]
            cmd += ["-f", dc['common_osmosis_schema_bbox']]
            logger.execute_out(cmd)
            cmd  = ["psql"]
            cmd += ["-d", dc['common_dbn']]
            cmd += ["-U", dc['common_dbu']]
            cmd += ["-f", dc['common_osmosis_schema_linestring']]
            logger.execute_out(cmd)

            # data
            logger.log(log_av_r+"import osmosis data"+log_ap)
            os.environ["JAVACMD_OPTIONS"] = "-Xms2048M -Xmx2048M -XX:MaxPermSize=2048M -Djava.io.tmpdir=/data/work/osmose/tmp/"
            cmd  = [dc['common_osmosis_bin']]
            cmd += ["--read-xml", "file=%s"%dc[k[:-3]+"dst"]]
#            cmd += ["-quiet"]
            cmd += ["--write-pgsql", "database=%s"%dc['common_dbn'], "user=%s"%dc['common_dbu'], "password=%s"%dc['common_dbx']]
            logger.execute_err(cmd)

            # polygon
            logger.log(log_av_r+"create polygon column"+log_ap)
            cmd  = ["psql"]
            cmd += ["-d", dc['common_dbn']]
            cmd += ["-U", dc['common_dbu']]
            cmd += ["-f", dc['common_osmosis_create_polygon']]
            logger.execute_out(cmd)


            # rename table
            logger.log(log_av_r+"rename osmosis tables"+log_ap)
            from pyPgSQL import PgSQL
            gisconn = PgSQL.Connection(dc['common_dbs'])
            giscurs = gisconn.cursor()
            giscurs.execute("DROP SCHEMA IF EXISTS %s CASCADE" % dc[k[:-3]+"sis"])
            giscurs.execute("CREATE SCHEMA %s" % dc[k[:-3]+"sis"])

            for t in ["nodes", "ways", "way_nodes", "relations", "relation_members", "users"]:
                sql = "ALTER TABLE %s SET SCHEMA %s;" % (t, dc[k[:-3]+"sis"])
                giscurs.execute(sql)
            gisconn.commit()

            # free lock
            del osmosis_lock



    ##########################################################################
    ## analyses
    
    for x in analysers:
        if x+"_updt" in dc:
            logger.log(log_av_r+cl.common_country + " : "+x+log_ap)
            
            # analyse
            try:
                analysers[x].analyser(class2config(cl, x), logger.sub())
            except:
                s = StringIO()
                traceback.print_exc(file=s)
                logger.sub().log("error on analyse...")
                for l in s.getvalue().decode("utf8").split("\n"):
                    logger.sub().sub().log(l)
                continue
            
            # update
            logger.sub().log("update")
            tmp_req = urllib2.Request(dc["common_updt_url"])
            tmp_url = os.path.join(dc["common_results_url"], x + "-" + dc["common_country"] + ".xml" + (x == "analyser_sax" and ".bz2" or "")) 
            tmp_dat = urllib.urlencode([('url', tmp_url), ('code', dc[x+"_updt"])])
            fd = urllib2.urlopen(tmp_req, tmp_dat)
            dt = fd.read().decode("utf8").strip()
            if dt <> "OK":
                sys.stderr.write((u"UPDATE ERROR %s/%s : %s"%(cl.common_country, x, dt)).encode("utf8"))
            else:
                logger.sub().sub().log(dt)
            
    ##########################################################################
    ## vidange
    
    if ("--no-clean" in sys.argv):
        return
    if not dc["clean_at_end"]:
        return
    
    logger.log(log_av_r+u"nettoyage : "+cl.common_country+log_ap)
    
    from pyPgSQL import PgSQL
    gisconn = PgSQL.Connection(dc['common_dbs'])
    giscurs = gisconn.cursor()
    
    # liste des tables
    tables = []
    sql = "SELECT c.relname FROM pg_catalog.pg_class c LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace WHERE c.relkind='r' AND n.nspname <> 'pg_catalog' AND n.nspname !~ '^pg_toast' AND pg_catalog.pg_table_is_visible(c.oid);"
    giscurs.execute(sql)
    for res in giscurs.fetchall():
        tables.append(res[0])

    # drop des tables
    for k in dc:
        if not(k.startswith("download_") and k.endswith("_url")):
            continue
        if k[:-3]+"gis" not in dc:
            continue
        for t in tables:
            if t in [dc[k[:-3]+"gis"]+sufix for sufix in ["_line", "_nodes", "_point", "_polygon", "_rels", "_roads", "_ways"]]:
                logger.sub().log("DROP TABLE %s"%t)
                giscurs.execute("DROP TABLE %s;"%t)
                gisconn.commit()

    for k in dc:
        if not(k.startswith("download_") and k.endswith("_url")):
            continue
        if (k[:-3]+"sis" in dc) and (dc[k[:-3]+"sis"]):
            # drop des tables osmosis
            logger.sub().log("DROP SCHEMA %s" % dc[k[:-3]+"sis"])
            sql = "DROP SCHEMA %s CASCADE;" % dc[k[:-3]+"sis"]
            logger.sub().log(sql)
            giscurs.execute(sql)
            gisconn.commit()

    # drop des fichiers    
    for k in dc:
        if k.endswith("_dst"):
            f = ".osm".join(dc[k].split(".osm")[:-1])
#            for ext in ["osm", "osm.bz2", "ts", "osm.ts"]:
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
    
    #open("/tmp/argv","w").write(str(sys.argv))
    
    if "--list-analyser" in sys.argv:
        for fn in os.listdir(os.path.dirname(__file__)):
            if fn.startswith("analyser_") and fn.endswith(".py"):
                print fn[9:-3]
        sys.exit(0)
    
    if "--list-country" in sys.argv:
        for k in dir(config):
            if k.startswith("config_"):
                if k == "config_debug":
                    continue
                print k[7:]
        sys.exit(0)
        
    if "--cron" in sys.argv:
        output = sys.stdout
        #output = open(os.path.join(os.path.join(config.dir_work, "logs"),"analyse_"+time.strftime("%Y-%m-%d_%H-%M-%S.log")), "w")
        logger = OsmoseLog.logger(output, False)
    else:
        output = sys.stdout
        logger = OsmoseLog.logger(output, True)
        
    only_analyser = []
    only_country  = []
    skip_download = False
    for i in range(len(sys.argv)):
        if sys.argv[i] == "--country":
            only_country += sys.argv[i+1].split(",")
            for x in sys.argv[i+1].split(","):
                logger.log(log_av_b+"only "+x+log_ap)
        if sys.argv[i] == "--analyser":
            only_analyser += ["analyser_"+x for x in sys.argv[i+1].split(",")]
            for x in sys.argv[i+1].split(","):
                logger.log(log_av_b+"only "+x+log_ap)
        if sys.argv[i] == "--skip-download":
            skip_download = True
            logger.log(log_av_b+"skip downloads"+log_ap)

    #=====================================
    # chargement des analysers
    
    analysers = {}
    for fn in os.listdir(os.path.dirname(__file__)):
        if fn.startswith("analyser_") and fn.endswith(".py"):
            if only_analyser and fn[:-3] not in only_analyser:
                continue
            logger.log(log_av_v+"load "+fn[:-3]+log_ap)
            analysers[fn[:-3]] = __import__(fn[:-3])
    for k in only_analyser:
        if k not in analysers:
            logger.log(log_av_b+"not found "+fn[:-3]+log_ap)
            
    #=====================================
    # analyse
    
    for k in dir(config):
        
        # filter
        if not k.startswith("config_"):
            continue
        country = k[len("config_"):]
        if only_country and country not in only_country:
            continue
        if not only_country and k == "config_debug":
            continue
        
        # acquire lock
        try:
            lfil = "/tmp/analyse-%s"%country
            lock = lockfile(lfil)
        except:
            logger.log(log_av_r+"can't lock %s"%country+log_ap)
            if "--cron" in sys.argv:
                sys.stderr.write("can't lock %s\n"%country)
            for l in open(lfil).read().rstrip().split("\n"):
                logger.log("  "+l)
                if "--cron" in sys.argv:
                    sys.stderr.write("  "+l+"\n")
            if "--cron" in sys.argv:
                sys.stderr.flush()
            continue
        
        # analyse
        run(eval("config.%s"%k), logger, skip_download)
        
        # free lock
        del lock
            
    logger.log(log_av_v+u"fin des analyses"+log_ap)
