#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2011                                      ##
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

try:
    import builtins
except ImportError:
    import __builtin__ as builtins

import os
from inspect import getframeinfo, stack
from modules import OsmoseTranslation
from modules import SourceVersion


if not hasattr(builtins, "T_"):
    translate = OsmoseTranslation.OsmoseTranslation()
    builtins.T_ = translate.translate

if not hasattr(builtins, "T_f"):
    translate_format = OsmoseTranslation.OsmoseTranslation()
    builtins.T_f = translate.translate_format

class Analyser(object):

    def __init__(self, config, logger = None):
        self.config = config
        self.logger = logger
        self.error_file = config.error_file
        if not hasattr(builtins, "T_"):
            self.translate = OsmoseTranslation.OsmoseTranslation()
            builtins.T_ = self.translate.translate
        if not hasattr(builtins, "T_f"):
            self.translate = OsmoseTranslation.OsmoseTranslation()
            builtins.T_f = self.translate.translate_format

    def __enter__(self):
        self.open_error_file()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_error_file()

    def analyser_version(self):
        return SourceVersion.version(self.__class__)

    def timestamp(self):
        return None

    @classmethod
    def def_class_(cls, config, **kwargs):
        # Check keys
        diff_keys = set(kwargs.keys()) - set(['item', 'id', 'level', 'tags', 'title', 'detail', 'fix', 'trap', 'example', 'source', 'resource'])
        if len(diff_keys) > 0:
            raise Exception('Unknow key ' + ', '.join(diff_keys))

        if 'source' not in kwargs:
            caller = getframeinfo(stack()[2][0])
            kwargs['source'] = '{0}/analysers/{1}#L{2}'.format(config and hasattr(config, 'source_url') and config.source_url or None, os.path.basename(caller.filename), caller.lineno)

        return kwargs

    def def_class(self, **kwargs):
        return self.def_class_(self.config, **kwargs)

    @classmethod
    def merge_doc(cls, *docs):
        langs = set(sum(map(lambda d: list(d.keys()), docs), []))
        return dict(map(lambda l: [l, '\n\n'.join(map(lambda d: d.get(l, d.get('en')), docs))], langs))

    @classmethod
    def merge_docs(cls, base, **docs):
        base = dict(base)
        for key in ['title', 'detail', 'fix', 'trap', 'example']:
            if key not in docs:
                continue

            if key in base and key in docs:
                base[key] = cls.merge_doc(base[key], docs[key])
            elif key in docs:
                base[key] = docs[key]
        return base

    def open_error_file(self):
        if self.error_file:
            self.error_file.begin()

    def close_error_file(self):
        if self.error_file:
            self.error_file.end()

    def analyser(self):
        pass

    def analyser_deferred_clean(self):
        pass

    def analyser_change(self):
        self.analyser()

    def analyser_change_deferred_clean(self):
        pass

    def analyser_resume(self, timestamp, already_issued_objects):
        self.analyser()

    def analyser_resume_deferred_clean(self):
        pass


###########################################################################
import unittest
from modules import IssuesFileOsmose

class TestAnalyser(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        import sys
        sys.path.append(".")
        import modules.OsmoseLog
        if not hasattr(cls, "logger"):
            cls.logger = modules.OsmoseLog.logger(sys.stdout, True)

    @classmethod
    def teardown_class(cls):
        pass

    @staticmethod
    def init_config(osm_file=None, dst=None, analyser_options=None):
        import os
        import osmose_run
        import osmose_config
        conf = osmose_config.template_config("test", analyser_options=analyser_options)
        conf.db_host = os.environ.get('DB_HOST', 'localhost')
        conf.db_base = os.environ.get('DB_BASE_TEST', 'osmose_test')
        conf.db_schema = conf.country
        conf.download["dst"] = osm_file
        conf.init()

        class options:
            plugin = None
            verbose = False
            change = False
        analyser_conf = osmose_run.analyser_config(conf, options(), None)
        analyser_conf.error_file = IssuesFileOsmose.IssuesFileOsmose(dst)

        return (conf, analyser_conf)

    @staticmethod
    def dict_sort_key(d):
        """
        Create a key from dict, with a string containing all keys and values,
        sorted by keys.
        """
        s = ""
        for k in sorted(d.keys()):
            v = d[k]
            if hasattr(v, 'items'):
                s += "%s-%s-" % (k, TestAnalyser.dict_sort_key(v))
            elif isinstance(v, list):
                s += "%s-" % k
                for l in v:
                    s += "%s_" % TestAnalyser.dict_sort_key(l)
            else:
                s += "%s-%s-" % (k, v)
        return s

    @staticmethod
    def normalise_dict(d):
        """
        Recursively convert dict-like object (eg OrderedDict) into plain dict.
        Sorts list values.
        """
        out = {}
        for k, v in dict(d).items():
            if hasattr(v, 'items'):
                out[k] = TestAnalyser.normalise_dict(v)
            elif isinstance(v, list):
                out[k] = []
                for item in sorted(v, key=TestAnalyser.dict_sort_key):
                    if hasattr(item, 'items'):
                        out[k].append(TestAnalyser.normalise_dict(item))
                    else:
                        out[k].append(item)
            else:
                out[k] = v
        return out

    @staticmethod
    def compare_list(a, b, ctx=u""):
        for k in range(min(len(a), len(b))):
            if a[k] != b[k]:
                if hasattr(a[k], 'items') and hasattr(b[k], 'items'):
                    return TestAnalyser.compare_dict(a[k], b[k], u"{0}.{1}".format(ctx, k))
                elif isinstance(a[k], list) and isinstance(b[k], list):
                    return TestAnalyser.compare_list(a[k], b[k], u"{0}.{1}".format(ctx, k))
                else:
                    return "key '%s' is different: '%s' != '%s' [%s]" % (k, a[k], b[k], ctx)
        if len(a) != len(b):
            return "length are different: %d != %d [%s]" % (len(a), len(b), ctx)
        return ""


    @staticmethod
    def compare_dict(a, b, ctx=u""):
        for k in a.keys():
            if k not in b:
                return "key '%s' is missing from b [%s]" % (k, ctx)

        for k in b.keys():
            if k not in a:
                return "key '%s' is missing from a [%s]" % (k, ctx)
            if a[k] != b[k]:
                if hasattr(a[k], 'items') and hasattr(b[k], 'items'):
                    return TestAnalyser.compare_dict(a[k], b[k], u"{0}.{1}".format(ctx, k))
                elif isinstance(a[k], list) and isinstance(b[k], list):
                    return TestAnalyser.compare_list(a[k], b[k], u"{0}.{1}".format(ctx, k))
                else:
                    return "key '%s' is different: '%s' != '%s' [%s]" % (k, a[k], b[k], ctx)

        return ""

    @staticmethod
    def convert_change_to_normal(a):
        # convert analyserChange to analyser, so that errors can be compared
        # between a normal run and a diff_full run

        if a["analysers"] is None:
            # skip conversion if analysers doesn't contain any analyser/analyserChange
            return

        if not "analyser" in a["analysers"]:
            a["analysers"]["analyser"] = a["analysers"]["analyserChange"]

        elif "analyserChange" in a["analysers"]:
            if not isinstance(a["analysers"]["analyser"]["class"], list):
                a["analysers"]["analyser"]["class"] = [a["analysers"]["analyser"]["class"]]

            if isinstance(a["analysers"]["analyserChange"]["class"], list):
                a["analysers"]["analyser"]["class"].extend(a["analysers"]["analyserChange"]["class"])
            else:
                a["analysers"]["analyser"]["class"].append(a["analysers"]["analyserChange"]["class"])

            if "error" in a["analysers"]["analyser"]:
                if not isinstance(a["analysers"]["analyser"]["error"], list):
                    a["analysers"]["analyser"]["error"] = [a["analysers"]["analyser"]["error"]]

                if "error" in a["analysers"]["analyserChange"]:
                    if isinstance(a["analysers"]["analyserChange"]["error"], list):
                        a["analysers"]["analyser"]["error"].extend(a["analysers"]["analyserChange"]["error"])
                    else:
                        a["analysers"]["analyser"]["error"].append(a["analysers"]["analyserChange"]["error"])

            elif "error" in a["analysers"]["analyserChange"]:
                a["analysers"]["analyser"]["error"] = a["analysers"]["analyserChange"]["error"]

        if "analyserChange" in a["analysers"]:
            del a["analysers"]["analyserChange"]

    @staticmethod
    def remove_non_checked_entries(a):

        if a["analysers"] is None:
            # skip conversion if analysers doesn't contain any analyser/analyserChange
            return

        if "analyser" in a["analysers"]:
            name_analyser = "analyser"
        elif "analyserChange" in a["analysers"]:
            name_analyser = "analyserChange"
        else:
            raise  # TODO


        a["analysers"]["@timestamp"] = "xxx"
        a["analysers"][name_analyser]["@timestamp"] = "xxx"
        a["analysers"][name_analyser]["@analyser_version"] = "xxx"

        # remove translations other than fr/en
        if isinstance(a["analysers"][name_analyser]["class"], list):
            for c in a["analysers"][name_analyser]["class"]:
                for k in ('classtext', 'detail', 'fix', 'trap', 'example'):
                    if k in c and isinstance(c[k], list):
                        for t in range(len(c[k])-1, -1, -1):
                            if c[k][t]["@lang"] not in ("en"):
                                del c[k][t]
                        if len(c[k]) == 1:
                            c[k] = c[k][0]
                if "@source" in c:
                    # remove line part
                    c["@source"] = c["@source"].split("#")[0]
        else:
            c = a["analysers"][name_analyser]["class"]
            for k in ('classtext', 'detail', 'fix', 'trap', 'example'):
                if k in c and isinstance(c[k], list):
                    for t in range(len(c[k])-1, -1, -1):
                        if c[k][t]["@lang"] not in ("en"):
                            del c[k][t]
                    if len(c[k]) == 1:
                        c[k] = c[k][0]
            if "@source" in c:
                # remove line part
                c["@source"] = c["@source"].split("#")[0]

        if "error" in a["analysers"][name_analyser]:
            if not isinstance(a["analysers"][name_analyser]["error"], list):
                a["analysers"][name_analyser]["error"] = [a["analysers"][name_analyser]["error"]]
            for e in a["analysers"][name_analyser]["error"]:
                if "text" in e and isinstance(e["text"], list):
                    for t in range(len(e["text"])-1, -1, -1):
                        if e["text"][t]["@lang"] not in ("en"):
                            del e["text"][t]
                    if len(e["text"]) == 1:
                        e["text"] = e["text"][0]

        if name_analyser == "analyser" and "delete" in a["analysers"][name_analyser]:
            del a["analysers"][name_analyser]["delete"]

    def compare_results(self, orig_xml=None, checked_xml=None, convert_checked_to_normal=False):
        if orig_xml is None:
            raise  # TODO
        if checked_xml is None:
            checked_xml = self.xml_res_file

        import xmltodict

        a = xmltodict.parse(open(orig_xml, mode='rb'))
        b = xmltodict.parse(open(checked_xml, mode='rb'))

        if convert_checked_to_normal:
            TestAnalyser.convert_change_to_normal(b)

        a = TestAnalyser.normalise_dict(a)
        b = TestAnalyser.normalise_dict(b)

        TestAnalyser.remove_non_checked_entries(a)
        TestAnalyser.remove_non_checked_entries(b)

        if a != b:
            s = TestAnalyser.compare_dict(a, b)
            print(s)
            assert s is None, "results differ"
            self.assertEqual(a, b, "results differ")


    def load_errors(self):
        import xml.etree.ElementTree as ET
        tree = ET.parse(self.xml_res_file)
        return tree.getroot()

    def check_err(self, cl=None, lat=None, lon=None, elems=None):
        for e in self.root_err.find("analyser").findall('error'):
            if cl is not None and e.attrib["class"] != cl:
                continue
            if lat is not None and e.find("location").attrib["lat"] != lat:
                continue
            if lon is not None and e.find("location").attrib["lon"] != lon:
                continue
            if elems is not None:
                xml_elems = []
                for t in ("node", "way", "relation"):
                    for err_elem in e.findall(t):
                        xml_elems.append((t, err_elem.attrib["id"]))
                if set(elems) != set(xml_elems):
                    continue
            return True

        assert False, "Error not found"

    def check_num_err(self, num=None, min=None, max=None):
        root_analyser = self.root_err.find("analyser")
        if root_analyser is None:
            root_analyser = self.root_err.find("analyserChange")

        if root_analyser is None:
            xml_num = 0
        else:
            xml_num = len(root_analyser.findall('error'))

        if num is not None:
            self.assertEqual(xml_num, num, "Found %d errors instead of %d" % (xml_num, num))
        if min is not None:
            self.assertGreaterEqual(xml_num, min, "Found %d errors instead of >= %d" % (xml_num, min))
        if max is not None:
            self.assertLessEqual(xml_num, max, "Found %d errors instead of <= %d" % (xml_num, max))


###########################################################################

class Test(unittest.TestCase):
    def test_compare_dict(self):
        a = TestAnalyser
        self.assertEqual(a.compare_dict({1:1, 2:2}, {1:1, 2:2}), u"")
        self.assertEqual(a.compare_dict({1:1, 2:2}, {2:2, 1:1}), u"")
        self.assertEqual(a.compare_dict({1:1, 2:2}, {1:0, 2:2}), u"key '1' is different: '1' != '0' []")
        self.assertEqual(a.compare_dict({1:1, 2:2}, {1:1, 3:3}), u"key '2' is missing from b []")
        self.assertEqual(a.compare_dict({1:1,    }, {1:1, 2:2}), u"key '2' is missing from a []")
        self.assertEqual(a.compare_dict({1:1, 2:2}, {1:1,    }), u"key '2' is missing from b []")

        self.assertEqual(a.compare_dict({1:[3,4], 2:2}, {1:[3,4], 2:2}), u"")
        self.assertEqual(a.compare_dict({1:[3,4], 2:2}, {1:[3,5], 2:2}), u"key '1' is different: '4' != '5' [.1]")
        self.assertEqual(a.compare_dict({1:[3  ], 2:2}, {1:[3,4], 2:2}), u"length are different: 1 != 2 [.1]")
        self.assertEqual(a.compare_dict({1:[3,4], 2:2}, {1:[3  ], 2:2}), u"length are different: 2 != 1 [.1]")

        self.assertEqual(a.compare_dict({1:{3:4}, 2:2}, {1:{3:4}, 2:2}), u"")
        self.assertEqual(a.compare_dict({1:{3:4}, 2:2}, {1:{3:5}, 2:2}), u"key '3' is different: '4' != '5' [.1]")
        self.assertEqual(a.compare_dict({1:{3:4}, 2:2}, {1:{4:5}, 2:2}), u"key '3' is missing from b [.1]")
        self.assertEqual(a.compare_dict({1:{   }, 2:2}, {1:{3:4}, 2:2}), u"key '3' is missing from a [.1]")
        self.assertEqual(a.compare_dict({1:{3:4}, 2:2}, {1:{   }, 2:2}), u"key '3' is missing from b [.1]")

    def test_merge_doc(self):
        self.assertEqual(Analyser.merge_doc({'en': 'a'}, {'en': 'b'}), {'en': 'a\n\nb'})
        self.assertEqual(Analyser.merge_doc({'en': '1', 'fr': '2'}, {'en': '3'}), {'en': '1\n\n3', 'fr': '2\n\n3'})
        self.assertEqual(Analyser.merge_doc({'en': '1', 'fr': '2'}, {'en': '3', 'fr': '4'}), {'en': '1\n\n3', 'fr': '2\n\n4'})

        self.assertEqual(Analyser.merge_docs({'A': {'en': 'a'}}, B = {'en': 'b'}), {'A': {'en': 'a'}, 'B': {'en': 'b'}})
        self.assertEqual(Analyser.merge_docs({'Z': {'en': 'a'}}, Z = {'en': 'b'}), {'Z': {'en': 'a\n\nb'}})
