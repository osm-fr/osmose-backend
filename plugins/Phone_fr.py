from plugins.Plugin import Plugin


class Phone_FixByRegex(Plugin):

    only_for = ["fr"]

    def init(self, logger):
        Plugin.init(self, logger)

        import re
        self.BadShort = re.compile(r"^(\\+33 *)([0-9]{4})$")
        self.BadInter = re.compile(r"^(\\+33 *0)([0-9 ]{8,})$")
        self.National = re.compile(r"^(0 *)([1-9][0-9 ]{8,})$")
        self.errors[3092] = { "item": 3092, "level": 2, "tag": ["phone", "fix:chair"], "desc": T_(u"Badly written phone number") }
        self.errors[3093] = { "item": 3093, "level": 3, "tag": ["phone", "fix:chair"], "desc": T_(u"French phone number") }

    def node(self, data, tags):
        for tag in (u"contact:fax", u"contact:phone", u"fax", u"phone"):
            if tag not in tags:
                return
            phone = tags[tag]

            r = self.BadInter.match(phone)
            if r:
                return [(3092, "+33 0", {"fix": {tag: "+33 " + r.group(2)} })]

            r = self.BadShort.match(phone)
            if r:
                 return [(3092, "+33 3xxx", {"fix": {tag: r.group(2)} })]

            r = self.National.match(phone)
            if r:
                return [(3093, "National", {"fix": {tag: "+33 " + r.group(2)} })]

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


available_plugin_classes = []

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Phone_ByRegex(None)
        a.init(None)
        for (d, f) in [(u"+33 0102030405", u"+33 102030405"),
                       (u"+330102030405", u"+33 102030405"),
                       (u"+33 01 02 03 04 05", u"+33 1 02 03 04 05"),
                       (u"+33 3631", u"3631"),
                       (u"0102030405", u"+33 102030405"),
                       (u"01 02 03 04 05", u"+33 1 02 03 04 05"),
                       (u"118987", u"118987"),
                      ]:
            self.check_err(a.node(None, {"phone": d}), ("phone='%s'" % d))
            self.assertEquals(a.node(None, {"phone": d})[0][2]["fix"]["phone"], f)
            assert not a.node(None, {"phone": f}), ("phone='%s'" % f)

            self.check_err(a.way(None, {"phone": d}, None), ("phone='%s'" % d))
