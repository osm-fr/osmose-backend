#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2013                                      ##
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

from Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


# http://de.wikipedia.org/wiki/Wikipedia:WikiProjekt_Georeferenzierung/Wikipedia-World/en

class _Analyser_Merge_Wikipedia(Analyser_Merge):

    create_table = """
        lang CHARACTER VARYING(10),
        titel CHARACTER VARYING(255),
        lat DOUBLE PRECISION,
        lon DOUBLE PRECISION,
        types CHARACTER VARYING(50),
        pop CHARACTER VARYING(50),
        "Height" CHARACTER VARYING(50),
        "Country" CHARACTER VARYING(10),
        "Subregion" CHARACTER VARYING(255),
        "Scale" CHARACTER VARYING(10),
        dim CHARACTER VARYING(30),
        psize DOUBLE PRECISION,
        STYLE CHARACTER VARYING(50),
        t CHARACTER VARYING(10),
        image CHARACTER VARYING(255),
        imagejpg CHARACTER VARYING(255),
        "name" CHARACTER VARYING(255),
        page_id DOUBLE PRECISION,
        "T_aa" CHARACTER VARYING(255),
        "T_ab" CHARACTER VARYING(255),
        "T_ace" CHARACTER VARYING(255),
        "T_af" CHARACTER VARYING(255),
        "T_ak" CHARACTER VARYING(255),
        "T_als" CHARACTER VARYING(255),
        "T_am" CHARACTER VARYING(255),
        "T_an" CHARACTER VARYING(255),
        "T_ang" CHARACTER VARYING(255),
        "T_ar" CHARACTER VARYING(255),
        "T_arc" CHARACTER VARYING(255),
        "T_arz" CHARACTER VARYING(255),
        "T_ast" CHARACTER VARYING(255),
        "T_av" CHARACTER VARYING(255),
        "T_ay" CHARACTER VARYING(255),
        "T_az" CHARACTER VARYING(255),
        "T_ba" CHARACTER VARYING(255),
        "T_bar" CHARACTER VARYING(255),
        "T_bat-smg" CHARACTER VARYING(255),
        "T_bcl" CHARACTER VARYING(255),
        "T_be" CHARACTER VARYING(255),
        "T_be-x-old" CHARACTER VARYING(255),
        "T_bg" CHARACTER VARYING(255),
        "T_bh" CHARACTER VARYING(255),
        "T_bi" CHARACTER VARYING(255),
        "T_bm" CHARACTER VARYING(255),
        "T_bn" CHARACTER VARYING(255),
        "T_bo" CHARACTER VARYING(255),
        "T_bpy" CHARACTER VARYING(255),
        "T_br" CHARACTER VARYING(255),
        "T_bs" CHARACTER VARYING(255),
        "T_bug" CHARACTER VARYING(255),
        "T_bxr" CHARACTER VARYING(255),
        "T_ca" CHARACTER VARYING(255),
        "T_cbk-zam" CHARACTER VARYING(255),
        "T_cdo" CHARACTER VARYING(255),
        "T_ce" CHARACTER VARYING(255),
        "T_ceb" CHARACTER VARYING(255),
        "T_ch" CHARACTER VARYING(255),
        "T_cho" CHARACTER VARYING(255),
        "T_chr" CHARACTER VARYING(255),
        "T_chy" CHARACTER VARYING(255),
        "T_ckb" CHARACTER VARYING(255),
        "T_co" CHARACTER VARYING(255),
        "T_cr" CHARACTER VARYING(255),
        "T_crh" CHARACTER VARYING(255),
        "T_cs" CHARACTER VARYING(255),
        "T_csb" CHARACTER VARYING(255),
        "T_cu" CHARACTER VARYING(255),
        "T_cv" CHARACTER VARYING(255),
        "T_cy" CHARACTER VARYING(255),
        "T_da" CHARACTER VARYING(255),
        "T_de" CHARACTER VARYING(255),
        "T_diq" CHARACTER VARYING(255),
        "T_dsb" CHARACTER VARYING(255),
        "T_dv" CHARACTER VARYING(255),
        "T_dz" CHARACTER VARYING(255),
        "T_ee" CHARACTER VARYING(255),
        "T_el" CHARACTER VARYING(255),
        "T_eml" CHARACTER VARYING(255),
        "T_en" CHARACTER VARYING(255),
        "T_en-simple" CHARACTER VARYING(255),
        "T_eo" CHARACTER VARYING(255),
        "T_es" CHARACTER VARYING(255),
        "T_et" CHARACTER VARYING(255),
        "T_eu" CHARACTER VARYING(255),
        "T_ext" CHARACTER VARYING(255),
        "T_fa" CHARACTER VARYING(255),
        "T_ff" CHARACTER VARYING(255),
        "T_fi" CHARACTER VARYING(255),
        "T_fiu-vro" CHARACTER VARYING(255),
        "T_fj" CHARACTER VARYING(255),
        "T_fo" CHARACTER VARYING(255),
        "T_fr" CHARACTER VARYING(255),
        "T_frp" CHARACTER VARYING(255),
        "T_fur" CHARACTER VARYING(255),
        "T_fy" CHARACTER VARYING(255),
        "T_ga" CHARACTER VARYING(255),
        "T_gan" CHARACTER VARYING(255),
        "T_gd" CHARACTER VARYING(255),
        "T_gl" CHARACTER VARYING(255),
        "T_glk" CHARACTER VARYING(255),
        "T_gn" CHARACTER VARYING(255),
        "T_got" CHARACTER VARYING(255),
        "T_gu" CHARACTER VARYING(255),
        "T_gv" CHARACTER VARYING(255),
        "T_ha" CHARACTER VARYING(255),
        "T_hak" CHARACTER VARYING(255),
        "T_haw" CHARACTER VARYING(255),
        "T_he" CHARACTER VARYING(255),
        "T_hi" CHARACTER VARYING(255),
        "T_hif" CHARACTER VARYING(255),
        "T_ho" CHARACTER VARYING(255),
        "T_hr" CHARACTER VARYING(255),
        "T_hsb" CHARACTER VARYING(255),
        "T_ht" CHARACTER VARYING(255),
        "T_hu" CHARACTER VARYING(255),
        "T_hy" CHARACTER VARYING(255),
        "T_hz" CHARACTER VARYING(255),
        "T_ia" CHARACTER VARYING(255),
        "T_id" CHARACTER VARYING(255),
        "T_ie" CHARACTER VARYING(255),
        "T_ig" CHARACTER VARYING(255),
        "T_ii" CHARACTER VARYING(255),
        "T_ik" CHARACTER VARYING(255),
        "T_ilo" CHARACTER VARYING(255),
        "T_io" CHARACTER VARYING(255),
        "T_is" CHARACTER VARYING(255),
        "T_it" CHARACTER VARYING(255),
        "T_iu" CHARACTER VARYING(255),
        "T_ja" CHARACTER VARYING(255),
        "T_jbo" CHARACTER VARYING(255),
        "T_jv" CHARACTER VARYING(255),
        "T_ka" CHARACTER VARYING(255),
        "T_kaa" CHARACTER VARYING(255),
        "T_kab" CHARACTER VARYING(255),
        "T_kg" CHARACTER VARYING(255),
        "T_ki" CHARACTER VARYING(255),
        "T_kj" CHARACTER VARYING(255),
        "T_kk" CHARACTER VARYING(255),
        "T_kl" CHARACTER VARYING(255),
        "T_km" CHARACTER VARYING(255),
        "T_kn" CHARACTER VARYING(255),
        "T_ko" CHARACTER VARYING(255),
        "T_kr" CHARACTER VARYING(255),
        "T_ks" CHARACTER VARYING(255),
        "T_ksh" CHARACTER VARYING(255),
        "T_ku" CHARACTER VARYING(255),
        "T_kv" CHARACTER VARYING(255),
        "T_kw" CHARACTER VARYING(255),
        "T_ky" CHARACTER VARYING(255),
        "T_la" CHARACTER VARYING(255),
        "T_lad" CHARACTER VARYING(255),
        "T_lb" CHARACTER VARYING(255),
        "T_lbe" CHARACTER VARYING(255),
        "T_lg" CHARACTER VARYING(255),
        "T_li" CHARACTER VARYING(255),
        "T_lij" CHARACTER VARYING(255),
        "T_lmo" CHARACTER VARYING(255),
        "T_ln" CHARACTER VARYING(255),
        "T_lo" CHARACTER VARYING(255),
        "T_lt" CHARACTER VARYING(255),
        "T_lv" CHARACTER VARYING(255),
        "T_map-bms" CHARACTER VARYING(255),
        "T_mdf" CHARACTER VARYING(255),
        "T_mg" CHARACTER VARYING(255),
        "T_mh" CHARACTER VARYING(255),
        "T_mhr" CHARACTER VARYING(255),
        "T_mi" CHARACTER VARYING(255),
        "T_mk" CHARACTER VARYING(255),
        "T_ml" CHARACTER VARYING(255),
        "T_mn" CHARACTER VARYING(255),
        "T_mo" CHARACTER VARYING(255),
        "T_mr" CHARACTER VARYING(255),
        "T_ms" CHARACTER VARYING(255),
        "T_mt" CHARACTER VARYING(255),
        "T_mus" CHARACTER VARYING(255),
        "T_mwl" CHARACTER VARYING(255),
        "T_my" CHARACTER VARYING(255),
        "T_myv" CHARACTER VARYING(255),
        "T_mzn" CHARACTER VARYING(255),
        "T_na" CHARACTER VARYING(255),
        "T_nah" CHARACTER VARYING(255),
        "T_nap" CHARACTER VARYING(255),
        "T_nds" CHARACTER VARYING(255),
        "T_nds-nl" CHARACTER VARYING(255),
        "T_ne" CHARACTER VARYING(255),
        "T_new" CHARACTER VARYING(255),
        "T_ng" CHARACTER VARYING(255),
        "T_nl" CHARACTER VARYING(255),
        "T_nn" CHARACTER VARYING(255),
        "T_no" CHARACTER VARYING(255),
        "T_nostalgia" CHARACTER VARYING(255),
        "T_nov" CHARACTER VARYING(255),
        "T_nrm" CHARACTER VARYING(255),
        "T_nv" CHARACTER VARYING(255),
        "T_ny" CHARACTER VARYING(255),
        "T_oc" CHARACTER VARYING(255),
        "T_om" CHARACTER VARYING(255),
        "T_or" CHARACTER VARYING(255),
        "T_os" CHARACTER VARYING(255),
        "T_pa" CHARACTER VARYING(255),
        "T_pag" CHARACTER VARYING(255),
        "T_pam" CHARACTER VARYING(255),
        "T_pap" CHARACTER VARYING(255),
        "T_pcd" CHARACTER VARYING(255),
        "T_pdc" CHARACTER VARYING(255),
        "T_pi" CHARACTER VARYING(255),
        "T_pih" CHARACTER VARYING(255),
        "T_pl" CHARACTER VARYING(255),
        "T_pms" CHARACTER VARYING(255),
        "T_pnb" CHARACTER VARYING(255),
        "T_pnt" CHARACTER VARYING(255),
        "T_ps" CHARACTER VARYING(255),
        "T_pt" CHARACTER VARYING(255),
        "T_qu" CHARACTER VARYING(255),
        "T_rm" CHARACTER VARYING(255),
        "T_rmy" CHARACTER VARYING(255),
        "T_rn" CHARACTER VARYING(255),
        "T_ro" CHARACTER VARYING(255),
        "T_roa-rup" CHARACTER VARYING(255),
        "T_roa-tara" CHARACTER VARYING(255),
        "T_ru" CHARACTER VARYING(255),
        "T_rw" CHARACTER VARYING(255),
        "T_sa" CHARACTER VARYING(255),
        "T_sah" CHARACTER VARYING(255),
        "T_sc" CHARACTER VARYING(255),
        "T_scn" CHARACTER VARYING(255),
        "T_sco" CHARACTER VARYING(255),
        "T_sd" CHARACTER VARYING(255),
        "T_se" CHARACTER VARYING(255),
        "T_sg" CHARACTER VARYING(255),
        "T_sh" CHARACTER VARYING(255),
        "T_si" CHARACTER VARYING(255),
        "T_simple" CHARACTER VARYING(255),
        "T_sk" CHARACTER VARYING(255),
        "T_sl" CHARACTER VARYING(255),
        "T_sm" CHARACTER VARYING(255),
        "T_sn" CHARACTER VARYING(255),
        "T_so" CHARACTER VARYING(255),
        "T_sq" CHARACTER VARYING(255),
        "T_sr" CHARACTER VARYING(255),
        "T_srn" CHARACTER VARYING(255),
        "T_ss" CHARACTER VARYING(255),
        "T_st" CHARACTER VARYING(255),
        "T_stq" CHARACTER VARYING(255),
        "T_su" CHARACTER VARYING(255),
        "T_sv" CHARACTER VARYING(255),
        "T_sw" CHARACTER VARYING(255),
        "T_szl" CHARACTER VARYING(255),
        "T_ta" CHARACTER VARYING(255),
        "T_te" CHARACTER VARYING(255),
        "T_tet" CHARACTER VARYING(255),
        "T_tg" CHARACTER VARYING(255),
        "T_th" CHARACTER VARYING(255),
        "T_ti" CHARACTER VARYING(255),
        "T_tk" CHARACTER VARYING(255),
        "T_tl" CHARACTER VARYING(255),
        "T_tlh" CHARACTER VARYING(255),
        "T_tn" CHARACTER VARYING(255),
        "T_to" CHARACTER VARYING(255),
        "T_tokipona" CHARACTER VARYING(255),
        "T_tpi" CHARACTER VARYING(255),
        "T_tr" CHARACTER VARYING(255),
        "T_ts" CHARACTER VARYING(255),
        "T_tt" CHARACTER VARYING(255),
        "T_tum" CHARACTER VARYING(255),
        "T_tw" CHARACTER VARYING(255),
        "T_ty" CHARACTER VARYING(255),
        "T_udm" CHARACTER VARYING(255),
        "T_ug" CHARACTER VARYING(255),
        "T_uk" CHARACTER VARYING(255),
        "T_ur" CHARACTER VARYING(255),
        "T_uz" CHARACTER VARYING(255),
        "T_ve" CHARACTER VARYING(255),
        "T_vec" CHARACTER VARYING(255),
        "T_vi" CHARACTER VARYING(255),
        "T_vls" CHARACTER VARYING(255),
        "T_vo" CHARACTER VARYING(255),
        "T_wa" CHARACTER VARYING(255),
        "T_war" CHARACTER VARYING(255),
        "T_wo" CHARACTER VARYING(255),
        "T_wuu" CHARACTER VARYING(255),
        "T_xal" CHARACTER VARYING(255),
        "T_xh" CHARACTER VARYING(255),
        "T_yi" CHARACTER VARYING(255),
        "T_yo" CHARACTER VARYING(255),
        "T_za" CHARACTER VARYING(255),
        "T_zea" CHARACTER VARYING(255),
        "T_zh" CHARACTER VARYING(255),
        "T_zh-classical" CHARACTER VARYING(255),
        "T_zh-min-nan" CHARACTER VARYING(255),
        "T_zh-yue" CHARACTER VARYING(255),
        "T_zu" CHARACTER VARYING(255),
        the_geom geometry
    """

    def __init__(self, config, classs, desc, wikiTypes, wikiCountry, wikiLang, starts, osmTags, osmTypes, conflationDistance, logger = None):
        self.possible_merge   = {"item":"8101", "class": classs, "level": 3, "tag": ["merge", "wikipedia"], "desc":desc }
        Analyser_Merge.__init__(self, config, logger,
            Source(
                url = "http://toolserver.org/~kolossos/wp-world/pg-dumps/wp-world/",
                name = "Wikipedia-World",
                file = "wikipedia_point_fr.csv.bz2",
                csv = CSV(csv = False, separator = None, null = None)),
            Load(("ST_X(the_geom)",), ("ST_Y(the_geom)",), table = "wikipedia_point_fr",
                create = self.create_table,
                select = {"lang": wikiLang, "Country": wikiCountry},
                where = (lambda res: not res["titel"].startswith("Liste ")) if starts == None else
                    (lambda res: res["titel"].startswith(starts)) ),
            Mapping(
                select = Select(
                    types = osmTypes,
                    tags = {"name": None}),
                osmRef = "wikipedia",
                conflationDistance = conflationDistance,
                generate = Generate(
                    mapping = {"wikipedia": lambda fields: fields["lang"]+":"+fields["titel"]},
                    text = lambda tags, fields: {fields["lang"]: fields["titel"]} )))

        if wikiTypes != None:
            self.load.select["types"] = wikiTypes # http://en.wikipedia.org/wiki/Wikipedia:GEO#type:T

        if isinstance(osmTags, dict):
            self.mapping.select.tags.update(osmTags)
        else:
            for t in osmTags:
                t.update(self.osmTags)
            self.mapping.select.tags = osmTags


# By Wikiepdia Types

class _Analyser_Merge_Wikipedia_Airport(_Analyser_Merge_Wikipedia):
    def __init__(self, config, country, lang, logger = None):
        _Analyser_Merge_Wikipedia.__init__(self, config,
            103,
            T_(u"Wikipedia, aerodrome integration suggestion"),
            "airport", country, lang,
            None,
            {"aeroway": ["aerodrome"]},
            ["nodes", "ways", "relations"],
            500,
            logger)

class _Analyser_Merge_Wikipedia_City(_Analyser_Merge_Wikipedia):
    def __init__(self, config, country, lang, logger = None):
        _Analyser_Merge_Wikipedia.__init__(self, config,
            113,
            T_(u"Wikipedia, city integration suggestion"),
            "city", country, lang,
            None,
            {"type": "boundary", "boundary": "administrative", "admin_level": "8"},
            ["relations"],
            1,
            logger)

class _Analyser_Merge_Wikipedia_Edu(_Analyser_Merge_Wikipedia):
    def __init__(self, config, country, lang, logger = None):
        _Analyser_Merge_Wikipedia.__init__(self, config,
            123,
            T_(u"Wikipedia, school integration suggestion"),
            "edu", country, lang,
            None,
            {"amenity": ["school", "university", "college"]},
            ["nodes", "ways", "relations"],
            100,
            logger)

class _Analyser_Merge_Wikipedia_Forest(_Analyser_Merge_Wikipedia):
    def __init__(self, config, country, lang, logger = None):
        _Analyser_Merge_Wikipedia.__init__(self, config,
            133,
            T_(u"Wikipedia, forest integration suggestion"),
            "forest", country, lang,
            None,
            {"landuse": ["forest"]},
            ["ways", "relations"],
            1000,
            logger)

class _Analyser_Merge_Wikipedia_Glacier(_Analyser_Merge_Wikipedia):
    def __init__(self, config, country, lang, logger = None):
        _Analyser_Merge_Wikipedia.__init__(self, config,
            143,
            T_(u"Wikipedia, glacier integration suggestion"),
            "glacier", country, lang,
            None,
            {"natural": ["glacier"]},
            ["ways", "relations"],
            1000,
            logger)

class _Analyser_Merge_Wikipedia_Isle(_Analyser_Merge_Wikipedia):
    def __init__(self, config, country, lang, logger = None):
        _Analyser_Merge_Wikipedia.__init__(self, config,
            153,
            T_(u"Wikipedia, island integration suggestion"),
            "isle", country, lang,
            None,
            {"place": ["island"]},
            ["ways", "relations"],
            100,
            logger)

class _Analyser_Merge_Wikipedia_Mountain(_Analyser_Merge_Wikipedia):
    def __init__(self, config, country, lang, logger = None):
        _Analyser_Merge_Wikipedia.__init__(self, config,
            163,
            T_(u"Wikipedia, peak integration suggestion"),
            "mountain", country, lang,
            None,
            {"natural": ["peak"]},
            ["nodes"],
            500,
            logger)

class _Analyser_Merge_Wikipedia_Pass(_Analyser_Merge_Wikipedia):
    def __init__(self, config, country, lang, logger = None):
        _Analyser_Merge_Wikipedia.__init__(self, config,
            173,
            T_(u"Wikipedia, mountain pass integration suggestion"),
            "pass", country, lang,
            None,
            {"mountain_pass": None},
            ["nodes"],
            200,
            logger)

class _Analyser_Merge_Wikipedia_RailwayStation(_Analyser_Merge_Wikipedia):
    def __init__(self, config, country, lang, logger = None):
        _Analyser_Merge_Wikipedia.__init__(self, config,
            183,
            T_(u"Wikipedia, railway station integration suggestion"),
            "railwaystation", country, lang,
            None,
            {"railway": ["station"]},
            ["nodes", "ways", "relations"],
            500,
            logger)

class _Analyser_Merge_Wikipedia_Waterbody(_Analyser_Merge_Wikipedia):
    def __init__(self, config, country, lang, logger = None):
        _Analyser_Merge_Wikipedia.__init__(self, config,
            193,
            T_(u"Wikipedia, water area integration suggestion"),
            "waterbody", country, lang,
            None,
            {"natural": ["water"]},
            ["ways", "relations"],
            200,
            logger)

# By title string

class _Analyser_Merge_Wikipedia_fr_Chateau(_Analyser_Merge_Wikipedia):
    def __init__(self, config, country, logger = None):
        _Analyser_Merge_Wikipedia.__init__(self, config,
            203,
            T_(u"Wikipedia, castle integration suggestion"),
            None, country, "fr",
            u"Château ",
            {"historic": "castle"},
            ["nodes", "ways"],
            200,
            logger)

class _Analyser_Merge_Wikipedia_fr_Eglise(_Analyser_Merge_Wikipedia):
    def __init__(self, config, country, logger = None):
        _Analyser_Merge_Wikipedia.__init__(self, config,
            213,
            T_(u"Wikipedia, church integration suggestion"),
            None, country, "fr",
            u"Église ",
            {"amenity": "place_of_worship"},
            ["nodes", "ways"],
            200,
            logger)
