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

from modules import download
from modules.lockfile import lockfile
from modules.OsmState import OsmState
import sys, os
import psycopg2
import fileinput
import shutil
import datetime
import time


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
        osm_state_old = OsmState(os.path.join(diff_path, "state.txt.old"))
        giscurs.execute("UPDATE metainfo SET tstamp = %s, tstamp_action = %s", [osm_state.timestamp(), osm_state_old.timestamp()])

        gisconn.commit()
        giscurs.close()
        gisconn.close()

        return xml_change

    except:
        logger.log(logger.log_av_r+"got error, aborting"+logger.log_ap)
        shutil.copyfile(os.path.join(diff_path, "state.txt.old"),
                        os.path.join(diff_path, "state.txt"))

        raise


def run_osmosis_resume(conf, logger):
    logger.log(logger.log_av_r+"import osmosis resume post scripts"+logger.log_ap)
    set_pgsql_schema(conf, logger)
    for script in conf.osmosis_resume_init_post_scripts:
        cmd  = ["psql"]
        cmd += conf.db_psql_args
        cmd += ["-f", script]
        logger.execute_out(cmd)
