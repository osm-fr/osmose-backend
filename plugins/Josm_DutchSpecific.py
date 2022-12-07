#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Josm_DutchSpecific(PluginMapCSS):

    MAPCSS_URL = 'https://github.com/Famlam/OsmMapcssValidationNL/blob/main/netherlands.validator.mapcss'

    only_for = ['NL-ZH', 'NL-ZE', 'NL-NB', 'NL-LI', 'NL-GE', 'NL-OV', 'NL-DR', 'NL-FR', 'NL-GR', 'NL-FL', 'NL-UT', 'NL-NH']


    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[1] = self.def_class(item = 9020, level = 3, tags = [], title = mapcss.tr('NL addresses and contacts'))
        self.errors[2] = self.def_class(item = 9020, level = 3, tags = [], title = mapcss.tr('NL deprecated features'))
        self.errors[3] = self.def_class(item = 9020, level = 3, tags = [], title = mapcss.tr('NL nomenclature'))
        self.errors[4] = self.def_class(item = 9020, level = 3, tags = [], title = mapcss.tr('NL heritage'))
        self.errors[5] = self.def_class(item = 9020, level = 3, tags = [], title = mapcss.tr('NL traffic signs'))
        self.errors[6] = self.def_class(item = 9020, level = 3, tags = [], title = mapcss.tr('NL German style tagging'))
        self.errors[7] = self.def_class(item = 9020, level = 3, tags = [], title = mapcss.tr('NL speed limits'))
        self.errors[8] = self.def_class(item = 9020, level = 3, tags = [], title = mapcss.tr('NL mofa tagging'))

        self.re_011bedaa = re.compile(r'^hgv(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_023db19d = re.compile(r'^(motor_)?vehicle(:backward|:both_ways)?(:conditional)?$')
        self.re_033b234a = re.compile(r'^bicycle(:forward|:both_ways)?(:conditional)?$')
        self.re_0660931d = re.compile(r'(?i)(oplaad|laadpunt|laadpaal)')
        self.re_06bae8ee = re.compile(r'^maxspeed:advisory(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_076895f4 = re.compile(r'payment:O[vV][-_]?[cC]hipkaart')
        self.re_088b0835 = re.compile(r'^addr:')
        self.re_08935e4d = re.compile(r'^maxspeed:advisory(:forward|:both_ways)?(:conditional)?$')
        self.re_0c61efa0 = re.compile(r'^maxlength(:backward|:both_ways)?(:conditional)?$')
        self.re_0cbcfeaf = re.compile(r'^maxspeed(:forward|:both_ways)?(:conditional)?$')
        self.re_0f9e3c59 = re.compile(r'^foot(:forward|:both_ways)?(:conditional)?$')
        self.re_0ffb8103 = re.compile(r'^(0031|\+31|0) ?[1-9]( ?[0-9]){10}')
        self.re_143f11c5 = re.compile(r'^(no|use_sidepath)$')
        self.re_1582ff37 = re.compile(r'(?i)bus\s?(baan|strook)')
        self.re_1705b261 = re.compile(r'(?i)(^|\sen\s)((on)?verplicht\s)?(\(?brom\)?)?fietspad$')
        self.re_17085e60 = re.compile(r'houseboat|static_caravan')
        self.re_19dea621 = re.compile(r'(^|;)NL:C21\b')
        self.re_1aa298e1 = re.compile(r'^maxheight(:backward|:both_ways)?(:conditional)?$')
        self.re_1cc9227a = re.compile(r'^maxspeed(:backward|:both_ways)?(:conditional)?$')
        self.re_1d0c9a01 = re.compile(r'^NL:zone[36]0$')
        self.re_1d478f9e = re.compile(r'\bNL:C0?2\b')
        self.re_1d614d5c = re.compile(r'^maxspeed(:forward|:backward|:both_ways)?$')
        self.re_1faa7e13 = re.compile(r'^hgv(:forward|:both_ways)?(:conditional)?$')
        self.re_21dc697e = re.compile(r'^maxaxleload(:backward|:both_ways)?(:conditional)?$')
        self.re_2441139b = re.compile(r'(?i)\b(aansl|empl|goed|ind|inhaalsp|opstel|overloopw|racc|rang|terr)\b')
        self.re_25a62b9d = re.compile(r'^(motor_)?vehicle(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_26ae994a = re.compile(r'^motorcycle(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_2823d45d = re.compile(r'^maxlength(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_293c2706 = re.compile(r'^[A-Z][a-z]{1,4}\. ')
        self.re_2cd26805 = re.compile(r'^maxlength(:forward|:both_ways)?(:conditional)?$')
        self.re_2e9c161c = re.compile(r'[0-9]{4} ?[A-Z]{2}')
        self.re_3082f445 = re.compile(r'\b(Adm|Burg|Dr|Drs|Ds|Gen|Ing|Ir|Mr|Past|Prof|St|Weth)\.? [A-Za-z]')
        self.re_30fdb33a = re.compile(r'(?i)^(lift)$')
        self.re_31154585 = re.compile(r'^motorcycle(:forward|:both_ways)?(:conditional)?$')
        self.re_3254c1c6 = re.compile(r'(?i)(parkeren$|parkeerplaats$|^toegang(sweg)?\s|^richting\s|drive.thro?u(gh)?)')
        self.re_33480e64 = re.compile(r'^maxheight(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_339dfcbd = re.compile(r'^maxweight(:backward|:both_ways)?(:conditional)?$')
        self.re_33af5199 = re.compile(r'^motorcycle(:backward|:both_ways)?(:conditional)?$')
        self.re_33fbfa8d = re.compile(r'(?i)post\W?nl$')
        self.re_345ec50a = re.compile(r'^maxweight(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_367126ed = re.compile(r'^(yes|1)$')
        self.re_3894ceb2 = re.compile(r'^oneway:')
        self.re_389e57a2 = re.compile(r'(^|;)NL:C18\b')
        self.re_3b2cb1d7 = re.compile(r'(?i)(uit?laa[dt]|honden.*wandel|los.?loop)')
        self.re_3bd9d067 = re.compile(r'^(yes|-?1)$')
        self.re_3c163648 = re.compile(r'(?i)ball?(veld(je)?)?$')
        self.re_3cd0133e = re.compile(r'^access(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_44720f99 = re.compile(r'(?i)^roltrap(pen)?$')
        self.re_460900e8 = re.compile(r'^maxspeed:advisory(:backward|:both_ways)?(:conditional)?$')
        self.re_467ce1ba = re.compile(r'(?i)(parkeren|parkeerplaats|parkeergarage|^garage)$')
        self.re_47aaa0f7 = re.compile(r'^(yes|designated)$')
        self.re_4cfe628c = re.compile(r'^access(:forward|:both_ways)?(:conditional)?$')
        self.re_4d87e9ab = re.compile(r'^access(:backward|:both_ways)?(:conditional)?$')
        self.re_4e099629 = re.compile(r'^trailer(:forward|:both_ways)?(:conditional)?$')
        self.re_4e4468f8 = re.compile(r'^foot(:backward|:both_ways)?(:conditional)?$')
        self.re_508e7773 = re.compile(r'^(\+|00)31 ?0?[0-9]{3,7}$')
        self.re_51f98600 = re.compile(r'^yes$')
        self.re_52555563 = re.compile(r'(^|;)NL:C20\b')
        self.re_53816e1a = re.compile(r'^maxwidth(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_543ffeee = re.compile(r'(?i)(rolstoel|invaliden)')
        self.re_54b75cfc = re.compile(r'^maxwidth(:forward|:both_ways)?(:conditional)?$')
        self.re_550ffc74 = re.compile(r'^building(:part)?$')
        self.re_556f4d08 = re.compile(r'^maxweight(:forward|:both_ways)?(:conditional)?$')
        self.re_5577fcc2 = re.compile(r'^hgv(:backward|:both_ways)?(:conditional)?$')
        self.re_5578cc63 = re.compile(r'100.+19:00')
        self.re_5b4448e5 = re.compile(r'(?i)^(honden\s?)?(toilet|uitlaa[dt]|los.?loop)')
        self.re_5e498788 = re.compile(r'^(left|right|both|yes)$')
        self.re_5ed5036a = re.compile(r'(?i)^speeltuin$')
        self.re_5f5aa10b = re.compile(r'^footway(:left|:right|:both)?:')
        self.re_6211f625 = re.compile(r'(?i)(voormalige?)')
        self.re_63f5f8f1 = re.compile(r'^maxheight(:forward|:both_ways)?(:conditional)?$')
        self.re_640dd184 = re.compile(r'^trailer(:backward|:both_ways)?(:conditional)?$')
        self.re_65dfbf19 = re.compile(r'^(motor_)?vehicle(:forward|:both_ways)?(:conditional)?$')
        self.re_682234cc = re.compile(r'^foot(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_697de1f2 = re.compile(r'^moped(:forward|:both_ways)?(:conditional)?$')
        self.re_6b1906aa = re.compile(r'(?i)(klanten|bezoek(ers)?|medewerkers)\b')
        self.re_6b8a2885 = re.compile(r'^bicycle(:backward|:both_ways)?(:conditional)?$')
        self.re_6ca7b121 = re.compile(r'(^|;)NL:C19\b')
        self.re_6cd83c9e = re.compile(r'(?i)^gratis\s|gratis\)')
        self.re_6d837295 = re.compile(r'(^|;)NL:C17\b')
        self.re_7087ae0d = re.compile(r'^trailer(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_70de8f0d = re.compile(r'^(00|\+)31 ?0[0-9]{8,}')
        self.re_7184e9bc = re.compile(r'^sidewalk:(left|right|both)$')
        self.re_71a0b33c = re.compile(r'(?i)(drinkwater|\swater|kraan)')
        self.re_731d219b = re.compile(r'(^|;)NL:A0?1-')
        self.re_7372291c = re.compile(r'^bicycle(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_73d53d80 = re.compile(r'(^|;)NL:A0?4\b')
        self.re_73ea17b1 = re.compile(r'^moped(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_7531ba03 = re.compile(r'^maxaxleload(:forward|:both_ways)?(:conditional)?$')
        self.re_774d1ba2 = re.compile(r'^maxwidth(:backward|:both_ways)?(:conditional)?$')
        self.re_78809448 = re.compile(r'^moped(:backward|:both_ways)?(:conditional)?$')
        self.re_798edef1 = re.compile(r'(?i)(aansl|empl|goed|ind|inhaalsp|opstel|overloopw|racc|rang|terr)\.')
        self.re_7acb98bb = re.compile(r'^maxspeed(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_7be1bafc = re.compile(r'^1[23]0$')
        self.re_7d72e705 = re.compile(r'^maxaxleload(:forward|:backward|:both_ways)?(:conditional)?$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_abbrname = set_badPhoneNumber = False

        # node[contact:phone=~/^(00|\+)31 ?0[0-9]{8,}/]
        # node[contact:mobile=~/^(00|\+)31 ?0[0-9]{8,}/]
        # node[phone=~/^(00|\+)31 ?0[0-9]{8,}/]
        if ('contact:mobile' in keys) or ('contact:phone' in keys) or ('phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_70de8f0d), mapcss._tag_capture(capture_tags, 0, tags, 'contact:phone'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_70de8f0d), mapcss._tag_capture(capture_tags, 0, tags, 'contact:mobile'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_70de8f0d), mapcss._tag_capture(capture_tags, 0, tags, 'phone'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .badPhoneNumber
                # group:tr("NL addresses and contacts")
                # throwWarning:tr("Invalid tag {0}: country code should not be followed by a 0","{0.key}")
                # assertMatch:"node phone=\"+31 06123456789\""
                # assertNoMatch:"node phone=\"+31 08008844\""
                # assertNoMatch:"node phone=\"+31 6123456789\""
                # assertMatch:"node phone=\"003106123456789\""
                # assertNoMatch:"node phone=\"00316123456789\""
                # assertNoMatch:"node phone=\"06123456789\""
                set_badPhoneNumber = True
                err.append({'class': 1, 'subclass': 2136227068, 'text': mapcss.tr('Invalid tag {0}: country code should not be followed by a 0', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # node[contact:phone=~/^(\+|00)31 ?0?[0-9]{3,7}$/]
        # node[contact:mobile=~/^(\+|00)31 ?0?[0-9]{3,7}$/]
        # node[phone=~/^(\+|00)31 ?0?[0-9]{3,7}$/]
        if ('contact:mobile' in keys) or ('contact:phone' in keys) or ('phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_508e7773), mapcss._tag_capture(capture_tags, 0, tags, 'contact:phone'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_508e7773), mapcss._tag_capture(capture_tags, 0, tags, 'contact:mobile'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_508e7773), mapcss._tag_capture(capture_tags, 0, tags, 'phone'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .badPhoneNumber
                # group:tr("NL addresses and contacts")
                # throwWarning:tr("Invalid tag {0}: short phone numbers cannot be used with international prefix (or: wrong phone number length)","{0.key}")
                # assertMatch:"node phone=\"+31 08008844\""
                # assertNoMatch:"node phone=\"+31 6123456789\""
                # assertMatch:"node phone=\"+3114024\""
                # assertMatch:"node phone=\"+318008844\""
                # assertNoMatch:"node phone=\"00316123456789\""
                # assertMatch:"node phone=\"00318008844\""
                # assertNoMatch:"node phone=\"06123456789\""
                # assertNoMatch:"node phone=\"08008844\""
                # assertNoMatch:"node phone=\"14024\""
                set_badPhoneNumber = True
                err.append({'class': 1, 'subclass': 253472651, 'text': mapcss.tr('Invalid tag {0}: short phone numbers cannot be used with international prefix (or: wrong phone number length)', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # node[contact:phone=~/^(0031|\+31|0) ?[1-9]( ?[0-9]){10}/][inside("NL")]!.badPhoneNumber
        # node[contact:mobile=~/^(0031|\+31|0) ?[1-9]( ?[0-9]){10}/][inside("NL")]!.badPhoneNumber
        # node[phone=~/^(0031|\+31|0) ?[1-9]( ?[0-9]){10}/][inside("NL")]!.badPhoneNumber
        if ('contact:mobile' in keys) or ('contact:phone' in keys) or ('phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_badPhoneNumber) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_0ffb8103), mapcss._tag_capture(capture_tags, 0, tags, 'contact:phone'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_badPhoneNumber) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_0ffb8103), mapcss._tag_capture(capture_tags, 0, tags, 'contact:mobile'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_badPhoneNumber) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_0ffb8103), mapcss._tag_capture(capture_tags, 0, tags, 'phone'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL addresses and contacts")
                # throwWarning:tr("Invalid tag {0}: too many digits (or foreign number, if so: ignore)","{0.key}")
                # assertNoMatch:"node phone=\"+31 6 12345678\""
                # assertNoMatch:"node phone=\"0031612345678\""
                # assertNoMatch:"node phone=\"06 12345678\""
                # assertNoMatch:"node phone=\"0800 1234567\""
                err.append({'class': 1, 'subclass': 1429902606, 'text': mapcss.tr('Invalid tag {0}: too many digits (or foreign number, if so: ignore)', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # node["addr:postcode"]["addr:postcode"!~/[0-9]{4} ?[A-Z]{2}/][inside("NL")]
        if ('addr:postcode' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'addr:postcode')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_2e9c161c, '[0-9]{4} ?[A-Z]{2}'), mapcss._tag_capture(capture_tags, 1, tags, 'addr:postcode'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL addresses and contacts")
                # throwWarning:tr("Invalid tag {0}: expected 4 digits followed by 2 letters","{0.tag}")
                err.append({'class': 1, 'subclass': 1560886491, 'text': mapcss.tr('Invalid tag {0}: expected 4 digits followed by 2 letters', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[is_in=NL]
        # *[is_in:country][inside("NL")]
        # *[is_in:city][inside("NL")]
        # *[is_in:province][inside("NL")]
        # *[is_in:continent][inside("NL")]
        # *[is_in:country_code=NL]
        if ('is_in' in keys) or ('is_in:city' in keys) or ('is_in:continent' in keys) or ('is_in:country' in keys) or ('is_in:country_code' in keys) or ('is_in:province' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'is_in') == mapcss._value_capture(capture_tags, 0, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'is_in:country')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'is_in:city')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'is_in:province')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'is_in:continent')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'is_in:country_code') == mapcss._value_capture(capture_tags, 0, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixRemove:"{0.key}"
                err.append({'class': 2, 'subclass': 788111375, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # node[/payment:O[vV][-_]?[cC]hipkaart/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_076895f4)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"payment:ov-chipkaart"
                # fixChangeKey:"{0.key}=>payment:ov-chipkaart"
                err.append({'class': 2, 'subclass': 1555838972, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [(mapcss._tag_uncapture(capture_tags, '{0.key}=>payment:ov-chipkaart')).split('=>', 1)[1].strip(), mapcss.tag(tags, (mapcss._tag_uncapture(capture_tags, '{0.key}=>payment:ov-chipkaart')).split('=>', 1)[0].strip())]]),
                    '-': ([
                    (mapcss._tag_uncapture(capture_tags, '{0.key}=>payment:ov-chipkaart')).split('=>', 1)[0].strip()])
                }})

        # *[delivery:covid19][inside("NL")]
        # *[takeaway:covid19][inside("NL")]
        # *[opening_hours:covid19][inside("NL")]
        if ('delivery:covid19' in keys) or ('opening_hours:covid19' in keys) or ('takeaway:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'delivery:covid19')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'takeaway:covid19')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'opening_hours:covid19')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("There are no active covid-19 restrictions at the moment. Remove {0}.","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 2, 'subclass': 371241830, 'text': mapcss.tr('There are no active covid-19 restrictions at the moment. Remove {0}.', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # node[name][highway][name=~/(?i)^(lift)$/]
        # node[name][amenity=drinking_water][name=~/(?i)(drinkwater|\swater|kraan)/]
        # node[name][amenity=charging_station][name=~/(?i)(oplaad|laadpunt|laadpaal)/]
        # *[name][amenity^=parking][name=~/(?i)(parkeren|parkeerplaats|parkeergarage|^garage)$/]
        # *[name][name=~/(?i)^gratis\s|gratis\)/]
        # *[name][name=~/(?i)(klanten|bezoek(ers)?|medewerkers)\b/][!route]
        # *[name][leisure=playground][name=~/(?i)^speeltuin$/]
        # *[name][leisure^=dog][name=~/(?i)^(honden\s?)?(toilet|uitlaa[dt]|los.?loop)/]
        # *[name][leisure=pitch][name=~/(?i)ball?(veld(je)?)?$/][!sport]
        if ('amenity' in keys and 'name' in keys) or ('highway' in keys and 'name' in keys) or ('leisure' in keys and 'name' in keys) or ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_30fdb33a), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity') == mapcss._value_capture(capture_tags, 1, 'drinking_water')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_71a0b33c), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity') == mapcss._value_capture(capture_tags, 1, 'charging_station')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_0660931d), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.startswith(mapcss._tag_capture(capture_tags, 1, tags, 'amenity'), mapcss._value_capture(capture_tags, 1, 'parking'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_467ce1ba), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6cd83c9e), mapcss._tag_capture(capture_tags, 1, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6b1906aa), mapcss._tag_capture(capture_tags, 1, tags, 'name'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'route')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'leisure') == mapcss._value_capture(capture_tags, 1, 'playground')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_5ed5036a), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.startswith(mapcss._tag_capture(capture_tags, 1, tags, 'leisure'), mapcss._value_capture(capture_tags, 1, 'dog'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_5b4448e5), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'leisure') == mapcss._value_capture(capture_tags, 1, 'pitch')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3c163648), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'sport')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("descriptive name")
                err.append({'class': 3, 'subclass': 1416971555, 'text': mapcss.tr('descriptive name')})

        # *[name][name=~/(?i)(voormalige?)/][!historic][tourism!=information][!landuse][!highway][!boundary][!waterway]
        if ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6211f625), mapcss._tag_capture(capture_tags, 1, tags, 'name'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'historic')) and (mapcss._tag_capture(capture_tags, 3, tags, 'tourism') != mapcss._value_const_capture(capture_tags, 3, 'information', 'information')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'landuse')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 6, tags, 'boundary')) and (not mapcss._tag_capture(capture_tags, 7, tags, 'waterway')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("descriptive name")
                # suggestAlternative:"description=*"
                # suggestAlternative:"disused=yes"
                # suggestAlternative:"old_name=*"
                err.append({'class': 3, 'subclass': 538711457, 'text': mapcss.tr('descriptive name')})

        # *[name][place][name=~/\b(Adm|Burg|Dr|Drs|Ds|Gen|Ing|Ir|Mr|Past|Prof|St|Weth)\.? [A-Za-z]/][inside("NL")]!.abbrname
        # *[name][place][name=~/^[A-Z][a-z]{1,4}\. /][inside("NL")]!.abbrname
        if ('name' in keys and 'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_abbrname) and (mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'place')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3082f445), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_abbrname) and (mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'place')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_293c2706), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # set .abbrname
                # group:tr("NL nomenclature")
                # throwWarning:tr("Gebiedsnaam met afkorting")
                set_abbrname = True
                err.append({'class': 3, 'subclass': 1829114630, 'text': mapcss.tr('Gebiedsnaam met afkorting')})

        # *[railway][name][name=~/(?i)(aansl|empl|goed|ind|inhaalsp|opstel|overloopw|racc|rang|terr)\./][inside("NL")]!.abbrname
        # *[railway][name][name=~/(?i)\b(aansl|empl|goed|ind|inhaalsp|opstel|overloopw|racc|rang|terr)\b/][inside("NL")]!.abbrname
        if ('name' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_abbrname) and (mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_798edef1), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_abbrname) and (mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_2441139b), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # set .abbrname
                # group:tr("NL nomenclature")
                # throwWarning:tr("Spoorgebied met afgekorte naam")
                # suggestAlternative:"aansluiting, emplacement, goederen, industrieterrein, inhaalspoor, opstelterrein, overloopwissel, raccordement of rangeerterrein"
                # assertNoMatch:"node railway=tram_stop name=Landgoed"
                set_abbrname = True
                err.append({'class': 3, 'subclass': 1558593366, 'text': mapcss.tr('Spoorgebied met afgekorte naam')})

        # *[name:nl][!name][inside("NL")][type!=route][name:fy]["name:fy"=*"name:nl"]
        # *[name:nl][!name][inside("NL")][type!=route][!name:fy]
        if ('name:fy' in keys and 'name:nl' in keys) or ('name:nl' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name:nl')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, 3, tags, 'type') != mapcss._value_const_capture(capture_tags, 3, 'route', 'route')) and (mapcss._tag_capture(capture_tags, 4, tags, 'name:fy')) and (mapcss._tag_capture(capture_tags, 5, tags, 'name:fy') == mapcss._value_capture(capture_tags, 5, mapcss.tag(tags, 'name:nl'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name:nl')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, 3, tags, 'type') != mapcss._value_const_capture(capture_tags, 3, 'route', 'route')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'name:fy')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("{0} without {1}","{0.key}","{1.key}")
                # suggestAlternative:"name"
                # fixChangeKey:"{0.key}=>{1.key}"
                # assertNoMatch:"node name:nl=x name:fy=y"
                # assertNoMatch:"node name=x name:nl=x name:en=y"
                err.append({'class': 3, 'subclass': 1647353731, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [(mapcss._tag_uncapture(capture_tags, '{0.key}=>{1.key}')).split('=>', 1)[1].strip(), mapcss.tag(tags, (mapcss._tag_uncapture(capture_tags, '{0.key}=>{1.key}')).split('=>', 1)[0].strip())]]),
                    '-': ([
                    (mapcss._tag_uncapture(capture_tags, '{0.key}=>{1.key}')).split('=>', 1)[0].strip()])
                }})

        # node[operator][operator!=PostNL][operator=~/(?i)post\W?nl$/][amenity=post_box]
        if ('amenity' in keys and 'operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'operator')) and (mapcss._tag_capture(capture_tags, 1, tags, 'operator') != mapcss._value_const_capture(capture_tags, 1, 'PostNL', 'PostNL')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_33fbfa8d), mapcss._tag_capture(capture_tags, 2, tags, 'operator'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'amenity') == mapcss._value_capture(capture_tags, 3, 'post_box')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("Suspected typo in {0}","{0.tag}")
                # suggestAlternative:"operator=PostNL"
                # fixAdd:"operator=PostNL"
                # assertMatch:"node amenity=post_box operator=\"post nl\""
                # assertNoMatch:"node amenity=post_box operator=PostNL"
                # assertMatch:"node amenity=post_box operator=postnl"
                err.append({'class': 3, 'subclass': 1831362989, 'text': mapcss.tr('Suspected typo in {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['operator','PostNL']])
                }})

        # *[heritage=1][heritage:operator!=whc]
        # *[heritage=2][heritage:operator!=rce][inside("NL")]
        if ('heritage' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'heritage') == mapcss._value_capture(capture_tags, 0, 1)) and (mapcss._tag_capture(capture_tags, 1, tags, 'heritage:operator') != mapcss._value_const_capture(capture_tags, 1, 'whc', 'whc')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'heritage') == mapcss._value_capture(capture_tags, 0, 2)) and (mapcss._tag_capture(capture_tags, 1, tags, 'heritage:operator') != mapcss._value_const_capture(capture_tags, 1, 'rce', 'rce')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL heritage")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.tag}")
                # fixAdd:"{1.tag}"
                err.append({'class': 4, 'subclass': 166241851, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, '{1.tag}')).split('=', 1)])
                }})

        # *[ref:rce][!heritage:operator]
        if ('ref:rce' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:rce')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'heritage:operator')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL heritage")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}=*")
                # fixAdd:"heritage:operator=rce"
                err.append({'class': 4, 'subclass': 883322705, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}=*')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['heritage:operator','rce']])
                }})

        # *[heritage:operator=rce][!heritage]
        if ('heritage:operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'heritage:operator') == mapcss._value_capture(capture_tags, 0, 'rce')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'heritage')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL heritage")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}=*")
                # fixAdd:"heritage=2"
                err.append({'class': 4, 'subclass': 1486143485, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}=*')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['heritage','2']])
                }})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_abbrname = set_badPhoneNumber = False

        # way[highway=cycleway][traffic_sign~="NL:G11"][moped][moped=~/^(yes|designated)$/]
        # way[highway=cycleway][traffic_sign~="NL:G12a"][moped][moped=~/^(no|use_sidepath)$/]
        # way[highway=cycleway][traffic_sign~="NL:G12a"][mofa][mofa=~/^(no|use_sidepath)$/]
        # way[highway=cycleway][traffic_sign~="NL:G13"][moped][moped=~/^(yes|designated)$/]
        # way[highway=cycleway][traffic_sign~="NL:G13"][mofa][mofa=~/^(yes|designated)$/]
        # way[highway][traffic_sign~="NL:D103"][moped][moped=~/^(no|use_sidepath)$/][highway!=construction]
        # way[highway][traffic_sign~="NL:D104"][moped][moped=~/^(no|use_sidepath)$/][highway!=construction]
        if ('highway' in keys and 'mofa' in keys and 'traffic_sign' in keys) or ('highway' in keys and 'moped' in keys and 'traffic_sign' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'cycleway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G11'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'moped')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_47aaa0f7), mapcss._tag_capture(capture_tags, 3, tags, 'moped'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'cycleway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G12a'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'moped')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_143f11c5), mapcss._tag_capture(capture_tags, 3, tags, 'moped'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'cycleway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G12a'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'mofa')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_143f11c5), mapcss._tag_capture(capture_tags, 3, tags, 'mofa'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'cycleway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G13'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'moped')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_47aaa0f7), mapcss._tag_capture(capture_tags, 3, tags, 'moped'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'cycleway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G13'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'mofa')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_47aaa0f7), mapcss._tag_capture(capture_tags, 3, tags, 'mofa'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:D103'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'moped')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_143f11c5), mapcss._tag_capture(capture_tags, 3, tags, 'moped'))) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:D104'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'moped')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_143f11c5), mapcss._tag_capture(capture_tags, 3, tags, 'moped'))) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} together with {1}","{1.tag}","{2.tag}")
                err.append({'class': 5, 'subclass': 1876831340, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # way[highway][traffic_sign~="NL:D103"][!moped]
        # way[highway][traffic_sign~="NL:D104"][!moped]
        # way[highway=cycleway][traffic_sign~="NL:G12a"][!moped]
        if ('highway' in keys and 'traffic_sign' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:D103'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:D104'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'cycleway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G12a'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} without {1}","{1.tag}","moped=designated")
                err.append({'class': 5, 'subclass': 2100176109, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), 'moped=designated')})

        # way[highway=cycleway][traffic_sign~="NL:G11"][!mofa]
        # way[highway=cycleway][traffic_sign~="NL:G12a"][!mofa]
        if ('highway' in keys and 'traffic_sign' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'cycleway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G11'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'mofa')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'cycleway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G12a'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'mofa')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} without {1}","{1.tag}","{2.key}")
                err.append({'class': 5, 'subclass': 174004251, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.key}'))})

        # way[highway=cycleway][traffic_sign~="NL:G13"][!mofa][!motor_vehicle][!access]
        if ('highway' in keys and 'traffic_sign' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'cycleway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G13'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'mofa')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'motor_vehicle')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'access')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} without {1}","{1.tag}","mofa=no")
                err.append({'class': 5, 'subclass': 1059219548, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), 'mofa=no')})

        # way[highway][traffic_sign~="NL:F13"][!bus][!psv][highway!=busway][highway!=bus_guideway]
        # way[highway][traffic_sign~="NL:F17"][!bus][!psv][highway!=busway][highway!=bus_guideway]
        # way[highway][traffic_sign~="NL:F19"][!bus][!psv][highway!=busway][highway!=bus_guideway]
        # way[highway][traffic_sign~="NL:F19"][!hgv]
        # way[highway][traffic_sign~="NL:F21"][!hgv]
        if ('highway' in keys and 'traffic_sign' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:F13'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bus')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'psv')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'busway', 'busway')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'bus_guideway', 'bus_guideway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:F17'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bus')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'psv')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'busway', 'busway')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'bus_guideway', 'bus_guideway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:F19'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bus')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'psv')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'busway', 'busway')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'bus_guideway', 'bus_guideway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:F19'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'hgv')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:F21'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'hgv')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} without {1}","{1.tag}","{2.key}=designated")
                # fixAdd:"{2.key}=designated"
                err.append({'class': 5, 'subclass': 748238486, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.key}=designated')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, '{2.key}=designated')).split('=', 1)])
                }})

        # way[highway][traffic_sign~="NL:F13"][bus=no][highway!=construction]
        # way[highway][traffic_sign~="NL:F17"][bus=no][highway!=construction]
        # way[highway][traffic_sign~="NL:F19"][bus=no][highway!=construction]
        # way[highway][traffic_sign~="NL:F13"][psv=no][!bus][highway!=construction]
        # way[highway][traffic_sign~="NL:F17"][psv=no][!bus][highway!=construction]
        # way[highway][traffic_sign~="NL:F19"][psv=no][!bus][highway!=construction]
        # way[highway][traffic_sign~="NL:F19"][hgv=no][highway!=construction]
        # way[highway][traffic_sign~="NL:F21"][hgv=no][highway!=construction]
        if ('bus' in keys and 'highway' in keys and 'traffic_sign' in keys) or ('hgv' in keys and 'highway' in keys and 'traffic_sign' in keys) or ('highway' in keys and 'psv' in keys and 'traffic_sign' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:F13'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'bus') == mapcss._value_capture(capture_tags, 2, 'no')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:F17'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'bus') == mapcss._value_capture(capture_tags, 2, 'no')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:F19'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'bus') == mapcss._value_capture(capture_tags, 2, 'no')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:F13'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'psv') == mapcss._value_capture(capture_tags, 2, 'no')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'bus')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:F17'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'psv') == mapcss._value_capture(capture_tags, 2, 'no')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'bus')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:F19'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'psv') == mapcss._value_capture(capture_tags, 2, 'no')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'bus')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:F19'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'hgv') == mapcss._value_capture(capture_tags, 2, 'no')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:F21'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'hgv') == mapcss._value_capture(capture_tags, 2, 'no')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} together with {1}","{1.tag}","{2.tag}")
                err.append({'class': 5, 'subclass': 1630203133, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # way[highway][traffic_sign~="NL:F13"][highway!=busway][highway!=service][highway!=bus_guideway][highway!=construction]
        # way[highway][traffic_sign~="NL:G5"][highway!=living_street][highway!=construction][highway!=path][highway!=cycleway][highway!=pedestrian]
        # way[highway][traffic_sign~="NL:G05"][highway!=living_street][highway!=construction][highway!=path][highway!=cycleway][highway!=pedestrian]
        # way[highway][traffic_sign~="NL:G7"][highway!=footway][highway!=steps][highway!=pedestrian][highway!=construction]
        # way[highway][traffic_sign~="NL:G07"][highway!=footway][highway!=steps][highway!=pedestrian][highway!=construction]
        # way[highway][traffic_sign~="NL:G9"][highway!=bridleway][highway!=construction]
        # way[highway][traffic_sign~="NL:G09"][highway!=bridleway][highway!=construction]
        # way[highway][traffic_sign~="NL:G11"][highway!=cycleway][highway!=construction]
        # way[highway][traffic_sign~="NL:G12a"][highway!=cycleway][highway!=construction]
        # way[highway][traffic_sign~="NL:G13"][highway!=cycleway][highway!=construction]
        if ('highway' in keys and 'traffic_sign' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:F13'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'busway', 'busway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'service', 'service')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'bus_guideway', 'bus_guideway')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G5'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'living_street', 'living_street')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'path', 'path')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'cycleway', 'cycleway')) and (mapcss._tag_capture(capture_tags, 6, tags, 'highway') != mapcss._value_const_capture(capture_tags, 6, 'pedestrian', 'pedestrian')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G05'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'living_street', 'living_street')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'path', 'path')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'cycleway', 'cycleway')) and (mapcss._tag_capture(capture_tags, 6, tags, 'highway') != mapcss._value_const_capture(capture_tags, 6, 'pedestrian', 'pedestrian')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G7'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'footway', 'footway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'steps', 'steps')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'pedestrian', 'pedestrian')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G07'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'footway', 'footway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'steps', 'steps')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'pedestrian', 'pedestrian')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G9'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'bridleway', 'bridleway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G09'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'bridleway', 'bridleway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G11'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'cycleway', 'cycleway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G12a'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'cycleway', 'cycleway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G13'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'cycleway', 'cycleway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} together with {1}","{1.tag}","{0.tag}")
                err.append({'class': 5, 'subclass': 2032108943, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # way[highway][traffic_sign~="NL:L51"][!cyclestreet][highway!=construction]
        if ('highway' in keys and 'traffic_sign' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:L51'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'cyclestreet')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} without {1}","{1.tag}","cyclestreet=yes")
                err.append({'class': 5, 'subclass': 1438158018, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), 'cyclestreet=yes')})

        # way[highway][traffic_sign~="NL:C1"][!vehicle][!/^(motor_)?vehicle(:forward|:backward|:both_ways)?(:conditional)?$/][!/^access(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C1"][!vehicle:forward][!/^(motor_)?vehicle(:forward|:both_ways)?(:conditional)?$/][!/^access(:forward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C1"][!vehicle:backward][!/^(motor_)?vehicle(:backward|:both_ways)?(:conditional)?$/][!/^access(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway!=yes]
        # way[highway][traffic_sign~="NL:C01"][!vehicle][!/^(motor_)?vehicle(:forward|:backward|:both_ways)?(:conditional)?$/][!/^access(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C01"][!vehicle:forward][!/^(motor_)?vehicle(:forward|:both_ways)?(:conditional)?$/][!/^access(:forward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C01"][!vehicle:backward][!/^(motor_)?vehicle(:backward|:both_ways)?(:conditional)?$/][!/^access(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway!=yes]
        # way[highway][traffic_sign~="NL:C6"][!motor_vehicle][!/^(motor_)?vehicle(:forward|:backward|:both_ways)?(:conditional)?$/][!/^access(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C6"][!motor_vehicle:forward][!/^(motor_)?vehicle(:forward|:both_ways)?(:conditional)?$/][!/^access(:forward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C6"][!motor_vehicle:backward][!/^(motor_)?vehicle(:backward|:both_ways)?(:conditional)?$/][!/^access(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway!=yes][oneway:motor_vehicle!=yes]
        # way[highway][traffic_sign~="NL:C06"][!motor_vehicle][!/^(motor_)?vehicle(:forward|:backward|:both_ways)?(:conditional)?$/][!/^access(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C06"][!motor_vehicle:forward][!/^(motor_)?vehicle(:forward|:both_ways)?(:conditional)?$/][!/^access(:forward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C06"][!motor_vehicle:backward][!/^(motor_)?vehicle(:backward|:both_ways)?(:conditional)?$/][!/^access(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway!=yes][oneway:motor_vehicle!=yes]
        # way[highway][traffic_sign~="NL:C7"][!hgv][!/^hgv(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C7"][!hgv:forward][!/^hgv(:forward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C7"][!hgv:backward][!/^hgv(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway:hgv!=yes]
        # way[highway][traffic_sign~="NL:C07"][!hgv][!/^hgv(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C07"][!hgv:forward][!/^hgv(:forward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C07"][!hgv:backward][!/^hgv(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway:hgv!=yes]
        # way[highway][traffic_sign~="NL:C9"][!bicycle][!/^bicycle(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C9"][!bicycle:forward][!/^bicycle(:forward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C9"][!bicycle:backward][!/^bicycle(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway:bicycle!=yes]
        # way[highway][traffic_sign~="NL:C9"][!moped][!/^moped(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C9"][!moped:forward][!/^moped(:forward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C9"][!moped:backward][!/^moped(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway:moped!=yes]
        # way[highway][traffic_sign~="NL:C09"][!bicycle][!/^bicycle(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C09"][!bicycle:forward][!/^bicycle(:forward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C09"][!bicycle:backward][!/^bicycle(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway:bicycle!=yes]
        # way[highway][traffic_sign~="NL:C09"][!moped][!/^moped(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C09"][!moped:forward][!/^moped(:forward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C09"][!moped:backward][!/^moped(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway:moped!=yes]
        # way[highway][traffic_sign~="NL:C10"][!trailer][!/^trailer(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C10"][!trailer:forward][!/^trailer(:forward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C10"][!trailer:backward][!/^trailer(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway:trailer!=yes]
        # way[highway][traffic_sign~="NL:C11"][!motorcycle][!/^motorcycle(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C11"][!motorcycle:forward][!/^motorcycle(:forward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C11"][!motorcycle:backward][!/^motorcycle(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway:motorcycle!=yes]
        # way[highway][traffic_sign~="NL:C12"][!motor_vehicle][!/^(motor_)?vehicle(:forward|:backward|:both_ways)?(:conditional)?$/][!/^access(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C12"][!motor_vehicle:forward][!/^(motor_)?vehicle(:forward|:both_ways)?(:conditional)?$/][!/^access(:forward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C12"][!motor_vehicle:backward][!/^(motor_)?vehicle(:backward|:both_ways)?(:conditional)?$/][!/^access(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway!=yes][oneway:motor_vehicle!=yes]
        # way[highway][traffic_sign~="NL:C13"][!moped][!/^moped(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C13"][!moped:forward][!/^moped(:forward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C13"][!moped:backward][!/^moped(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway:moped!=yes]
        # way[highway][traffic_sign~="NL:C14"][!bicycle][!/^bicycle(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C14"][!bicycle:forward][!/^bicycle(:forward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C14"][!bicycle:backward][!/^bicycle(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway:bicycle!=yes]
        # way[highway][traffic_sign~="NL:C15"][!bicycle][!/^bicycle(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C15"][!bicycle:forward][!/^bicycle(:forward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C15"][!bicycle:backward][!/^bicycle(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway:bicycle!=yes]
        # way[highway][traffic_sign~="NL:C15"][!moped][!/^moped(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C15"][!moped:forward][!/^moped(:forward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C15"][!moped:backward][!/^moped(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway:moped!=yes]
        # way[highway][traffic_sign~="NL:C16"][!foot][!/^foot(:forward|:backward|:both_ways)?(:conditional)?$/][!/^access(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C16"][!foot:forward][!/^foot(:forward|:both_ways)?(:conditional)?$/][!/^access(:forward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C16"][!foot:backward][!/^foot(:backward|:both_ways)?(:conditional)?$/][!/^access(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway:foot!=yes]
        if ('highway' in keys and 'traffic_sign' in keys) or ('highway' in keys and 'traffic_sign:backward' in keys) or ('highway' in keys and 'traffic_sign:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C1'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'vehicle')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_25a62b9d)) and (not mapcss._tag_capture(capture_tags, 4, tags, self.re_3cd0133e)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C1'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'vehicle:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_65dfbf19)) and (not mapcss._tag_capture(capture_tags, 4, tags, self.re_4cfe628c)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C1'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'vehicle:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_023db19d)) and (not mapcss._tag_capture(capture_tags, 4, tags, self.re_4d87e9ab)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 6, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 6, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C01'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'vehicle')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_25a62b9d)) and (not mapcss._tag_capture(capture_tags, 4, tags, self.re_3cd0133e)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C01'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'vehicle:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_65dfbf19)) and (not mapcss._tag_capture(capture_tags, 4, tags, self.re_4cfe628c)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C01'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'vehicle:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_023db19d)) and (not mapcss._tag_capture(capture_tags, 4, tags, self.re_4d87e9ab)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 6, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 6, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C6'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motor_vehicle')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_25a62b9d)) and (not mapcss._tag_capture(capture_tags, 4, tags, self.re_3cd0133e)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C6'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motor_vehicle:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_65dfbf19)) and (not mapcss._tag_capture(capture_tags, 4, tags, self.re_4cfe628c)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C6'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motor_vehicle:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_023db19d)) and (not mapcss._tag_capture(capture_tags, 4, tags, self.re_4d87e9ab)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 6, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 6, 'yes', 'yes')) and (mapcss._tag_capture(capture_tags, 7, tags, 'oneway:motor_vehicle') != mapcss._value_const_capture(capture_tags, 7, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C06'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motor_vehicle')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_25a62b9d)) and (not mapcss._tag_capture(capture_tags, 4, tags, self.re_3cd0133e)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C06'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motor_vehicle:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_65dfbf19)) and (not mapcss._tag_capture(capture_tags, 4, tags, self.re_4cfe628c)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C06'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motor_vehicle:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_023db19d)) and (not mapcss._tag_capture(capture_tags, 4, tags, self.re_4d87e9ab)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 6, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 6, 'yes', 'yes')) and (mapcss._tag_capture(capture_tags, 7, tags, 'oneway:motor_vehicle') != mapcss._value_const_capture(capture_tags, 7, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C7'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'hgv')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_011bedaa)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C7'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'hgv:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_1faa7e13)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C7'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'hgv:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_5577fcc2)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'oneway:hgv') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C07'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'hgv')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_011bedaa)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C07'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'hgv:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_1faa7e13)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C07'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'hgv:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_5577fcc2)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'oneway:hgv') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C9'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bicycle')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_7372291c)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C9'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_033b234a)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C9'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_6b8a2885)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'oneway:bicycle') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C9'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_73ea17b1)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C9'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_697de1f2)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C9'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_78809448)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'oneway:moped') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C09'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bicycle')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_7372291c)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C09'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_033b234a)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C09'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_6b8a2885)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'oneway:bicycle') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C09'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_73ea17b1)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C09'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_697de1f2)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C09'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_78809448)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'oneway:moped') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C10'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'trailer')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_7087ae0d)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C10'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'trailer:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_4e099629)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C10'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'trailer:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_640dd184)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'oneway:trailer') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C11'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motorcycle')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_26ae994a)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C11'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motorcycle:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_31154585)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C11'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motorcycle:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_33af5199)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'oneway:motorcycle') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C12'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motor_vehicle')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_25a62b9d)) and (not mapcss._tag_capture(capture_tags, 4, tags, self.re_3cd0133e)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C12'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motor_vehicle:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_65dfbf19)) and (not mapcss._tag_capture(capture_tags, 4, tags, self.re_4cfe628c)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C12'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motor_vehicle:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_023db19d)) and (not mapcss._tag_capture(capture_tags, 4, tags, self.re_4d87e9ab)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 6, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 6, 'yes', 'yes')) and (mapcss._tag_capture(capture_tags, 7, tags, 'oneway:motor_vehicle') != mapcss._value_const_capture(capture_tags, 7, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C13'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_73ea17b1)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C13'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_697de1f2)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C13'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_78809448)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'oneway:moped') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C14'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bicycle')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_7372291c)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C14'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_033b234a)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C14'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_6b8a2885)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'oneway:bicycle') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C15'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bicycle')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_7372291c)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C15'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_033b234a)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C15'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_6b8a2885)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'oneway:bicycle') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C15'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_73ea17b1)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C15'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_697de1f2)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C15'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_78809448)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'oneway:moped') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C16'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'foot')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_682234cc)) and (not mapcss._tag_capture(capture_tags, 4, tags, self.re_3cd0133e)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C16'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'foot:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_0f9e3c59)) and (not mapcss._tag_capture(capture_tags, 4, tags, self.re_4cfe628c)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C16'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'foot:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_4e4468f8)) and (not mapcss._tag_capture(capture_tags, 4, tags, self.re_4d87e9ab)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 6, tags, 'oneway:foot') != mapcss._value_const_capture(capture_tags, 6, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} without {1}","{1.tag}","{2.key}=no/private/destination/...")
                # assertNoMatch:"way highway=service traffic_sign:backward=\"NL:C07;NL:C16\" hgv:backward=no foot=no"
                # assertNoMatch:"way highway=service traffic_sign:backward=\"NL:C07;NL:C16\" hgv=no foot=no"
                # assertMatch:"way highway=service traffic_sign:forward=\"NL:C9;NL:OB58\" traffic_sign:backward=\"NL:C1\" access:backward=no"
                # assertMatch:"way highway=service traffic_sign:forward=\"NL:C9;NL:OB58\""
                # assertMatch:"way highway=service traffic_sign=\"NL:C01\""
                # assertNoMatch:"way highway=service traffic_sign=\"NL:C01;NL:C16\" access=no"
                # assertNoMatch:"way highway=service traffic_sign=\"NL:C01;NL:OB51;NL:OB54\" motor_vehicle=no"
                # assertNoMatch:"way highway=track traffic_sign:backward=\"NL:C12\" oneway=yes oneway:bicycle=no"
                # assertNoMatch:"way highway=track traffic_sign=\"NL:C12\" motor_vehicle=no"
                err.append({'class': 5, 'subclass': 798095003, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.key}=no/private/destination/...'))})

        # way[traffic_sign][traffic_sign=~/(^|;)NL:C17\b/][!maxlength][!/^maxlength(:forward|:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:forward][traffic_sign:forward=~/(^|;)NL:C17\b/][!maxlength:forward][!/^maxlength(:forward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:backward][traffic_sign:backward=~/(^|;)NL:C17\b/][!maxlength:backward][!/^maxlength(:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign][traffic_sign=~/(^|;)NL:C18\b/][!maxwidth][!/^maxwidth(:forward|:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:forward][traffic_sign:forward=~/(^|;)NL:C18\b/][!maxwidth:forward][!/^maxwidth(:forward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:backward][traffic_sign:backward=~/(^|;)NL:C18\b/][!maxwidth:backward][!/^maxwidth(:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign][traffic_sign=~/(^|;)NL:C19\b/][!maxheight][!/^maxheight(:forward|:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:forward][traffic_sign:forward=~/(^|;)NL:C19\b/][!maxheight:forward][!/^maxheight(:forward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:backward][traffic_sign:backward=~/(^|;)NL:C19\b/][!maxheight:backward][!/^maxheight(:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign][traffic_sign=~/(^|;)NL:C20\b/][!maxaxleload][!/^maxaxleload(:forward|:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:forward][traffic_sign:forward=~/(^|;)NL:C20\b/][!maxaxleload:forward][!/^maxaxleload(:forward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:backward][traffic_sign:backward=~/(^|;)NL:C20\b/][!maxaxleload:backward][!/^maxaxleload(:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign][traffic_sign=~/(^|;)NL:C21\b/][!maxweight][!/^maxweight(:forward|:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:forward][traffic_sign:forward=~/(^|;)NL:C21\b/][!maxweight:forward][!/^maxweight(:forward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:backward][traffic_sign:backward=~/(^|;)NL:C21\b/][!maxweight:backward][!/^maxweight(:backward|:both_ways)?(:conditional)?$/][highway]
        if ('highway' in keys and 'traffic_sign' in keys) or ('highway' in keys and 'traffic_sign:backward' in keys) or ('highway' in keys and 'traffic_sign:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6d837295), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxlength')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_2823d45d)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:forward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6d837295), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxlength:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_2cd26805)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:backward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6d837295), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxlength:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_0c61efa0)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_389e57a2), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxwidth')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_53816e1a)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:forward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_389e57a2), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxwidth:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_54b75cfc)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:backward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_389e57a2), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxwidth:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_774d1ba2)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6ca7b121), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxheight')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_33480e64)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:forward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6ca7b121), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxheight:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_63f5f8f1)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:backward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6ca7b121), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxheight:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_1aa298e1)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_52555563), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxaxleload')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_7d72e705)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:forward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_52555563), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxaxleload:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_7531ba03)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:backward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_52555563), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxaxleload:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_21dc697e)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_19dea621), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxweight')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_345ec50a)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:forward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_19dea621), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxweight:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_556f4d08)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:backward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_19dea621), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxweight:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_339dfcbd)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} without {1}","{0.tag}","{2.key}")
                # assertNoMatch:"way highway=residential traffic_sign:backward=NL:C21[2.1] maxweight:backward=2.1"
                # assertMatch:"way highway=residential traffic_sign:forward=NL:C21[2.1]"
                # assertNoMatch:"way highway=residential traffic_sign=NL:C21[2.1] maxweight=2.1"
                # assertMatch:"way highway=residential traffic_sign=NL:C21[2.1]"
                err.append({'class': 5, 'subclass': 1126640278, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{2.key}'))})

        # way[highway][traffic_sign~="NL:C2"][oneway!=yes][/^oneway:/!~/^(yes|-?1)$/][oneway!=-1][highway!=construction]
        # way[highway][traffic_sign~="NL:C02"][oneway!=yes][/^oneway:/!~/^(yes|-?1)$/][oneway!=-1][highway!=construction]
        # way[highway][traffic_sign~="NL:C3"][oneway!=yes][/^oneway:/!~/^(yes|-?1)$/][oneway!=-1][highway!=construction]
        # way[highway][traffic_sign~="NL:C03"][oneway!=yes][/^oneway:/!~/^(yes|-?1)$/][oneway!=-1][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C3"][oneway!=yes][/^oneway:/!~/^(yes|1)$/][highway!=construction][traffic_sign:backward!~/\bNL:C0?2\b/]
        # way[highway][traffic_sign:forward~="NL:C03"][oneway!=yes][/^oneway:/!~/^(yes|1)$/][highway!=construction][traffic_sign:backward!~/\bNL:C0?2\b/]
        # way[highway][traffic_sign:backward~="NL:C2"][oneway!=yes][/^oneway:/!~/^(yes|1)$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C02"][oneway!=yes][/^oneway:/!~/^(yes|1)$/][highway!=construction]
        if ('highway' in keys and 'traffic_sign' in keys) or ('highway' in keys and 'traffic_sign:backward' in keys) or ('highway' in keys and 'traffic_sign:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C2'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')) and (not mapcss.regexp_test(self.re_3bd9d067, mapcss._match_regex(tags, self.re_3894ceb2))) and (mapcss._tag_capture(capture_tags, 4, tags, 'oneway') != mapcss._value_capture(capture_tags, 4, -1)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C02'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')) and (not mapcss.regexp_test(self.re_3bd9d067, mapcss._match_regex(tags, self.re_3894ceb2))) and (mapcss._tag_capture(capture_tags, 4, tags, 'oneway') != mapcss._value_capture(capture_tags, 4, -1)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C3'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')) and (not mapcss.regexp_test(self.re_3bd9d067, mapcss._match_regex(tags, self.re_3894ceb2))) and (mapcss._tag_capture(capture_tags, 4, tags, 'oneway') != mapcss._value_capture(capture_tags, 4, -1)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C03'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')) and (not mapcss.regexp_test(self.re_3bd9d067, mapcss._match_regex(tags, self.re_3894ceb2))) and (mapcss._tag_capture(capture_tags, 4, tags, 'oneway') != mapcss._value_capture(capture_tags, 4, -1)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C3'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')) and (not mapcss.regexp_test(self.re_367126ed, mapcss._match_regex(tags, self.re_3894ceb2))) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 5, self.re_1d478f9e, '\bNL:C0?2\b'), mapcss._tag_capture(capture_tags, 5, tags, 'traffic_sign:backward'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C03'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')) and (not mapcss.regexp_test(self.re_367126ed, mapcss._match_regex(tags, self.re_3894ceb2))) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 5, self.re_1d478f9e, '\bNL:C0?2\b'), mapcss._tag_capture(capture_tags, 5, tags, 'traffic_sign:backward'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C2'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')) and (not mapcss.regexp_test(self.re_367126ed, mapcss._match_regex(tags, self.re_3894ceb2))) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C02'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')) and (not mapcss.regexp_test(self.re_367126ed, mapcss._match_regex(tags, self.re_3894ceb2))) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} without {1}","{1.tag}","{2.tag}")
                # assertMatch:"way highway=residential traffic_sign:backward=\"NL:C02;NL:OB58\""
                # assertNoMatch:"way highway=residential traffic_sign:backward=\"NL:C2\" oneway:motor_vehicle=yes"
                # assertNoMatch:"way highway=residential traffic_sign:backward=\"NL:C2\" oneway=yes oneway:bicycle=no"
                # assertNoMatch:"way highway=residential traffic_sign:forward=\"NL:C3\" oneway:motor_vehicle=yes"
                # assertMatch:"way highway=residential traffic_sign:forward=\"NL:C3\" oneway=-1"
                # assertNoMatch:"way highway=residential traffic_sign:forward=\"NL:C3\" oneway=yes"
                # assertMatch:"way highway=residential traffic_sign:forward=\"NL:C3\""
                # assertMatch:"way highway=residential traffic_sign=\"NL:C02\""
                # assertNoMatch:"way highway=residential traffic_sign=\"NL:C02;NL:OB58\" oneway=-1"
                # assertNoMatch:"way highway=residential traffic_sign=\"NL:C02;NL:OB58\" oneway=yes"
                # assertNoMatch:"way highway=residential traffic_sign=\"NL:C3\" oneway:agricultural=no oneway:motor_vehicle=yes oneway:motorcycle=no oneway=no"
                # assertNoMatch:"way highway=residential traffic_sign=\"NL:C3\" oneway:motor_vehicle=-1"
                # assertNoMatch:"way highway=residential traffic_sign=\"NL:C3\" oneway:motor_vehicle=yes"
                # assertMatch:"way highway=residential traffic_sign=\"NL:C3;NL:OB58\""
                err.append({'class': 5, 'subclass': 1059189470, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # way[highway][traffic_sign~="NL:C5"][oneway?][highway!=construction]
        # way[highway][traffic_sign~="NL:C05"][oneway?][highway!=construction]
        if ('highway' in keys and 'oneway' in keys and 'traffic_sign' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C5'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'oneway') in ('yes', 'true', '1')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C05'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'oneway') in ('yes', 'true', '1')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} together with {1}","{1.tag}","{2.tag}")
                # suggestAlternative:"oneway=no"
                # assertMatch:"way highway=residential traffic_sign=\"NL:C05\" oneway=yes"
                # assertNoMatch:"way highway=residential traffic_sign=\"NL:C05\""
                # assertNoMatch:"way highway=residential traffic_sign=\"NL:C5;NL:OB58\" oneway=no"
                err.append({'class': 5, 'subclass': 560436831, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # way[highway][traffic_sign~="NL:D1"][junction!=roundabout][junction!=circular]
        # way[highway][traffic_sign~="NL:D01"][junction!=roundabout][junction!=circular]
        if ('highway' in keys and 'traffic_sign' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:D1'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'junction') != mapcss._value_const_capture(capture_tags, 2, 'roundabout', 'roundabout')) and (mapcss._tag_capture(capture_tags, 3, tags, 'junction') != mapcss._value_const_capture(capture_tags, 3, 'circular', 'circular')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:D01'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'junction') != mapcss._value_const_capture(capture_tags, 2, 'roundabout', 'roundabout')) and (mapcss._tag_capture(capture_tags, 3, tags, 'junction') != mapcss._value_const_capture(capture_tags, 3, 'circular', 'circular')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} without {1} or {2}","{1.tag}","{2.tag}","{3.tag}")
                # assertNoMatch:"way highway=residential traffic_sign=NL:D1 junction=circular"
                # assertNoMatch:"way highway=residential traffic_sign=NL:D1 junction=roundabout"
                # assertMatch:"way highway=residential traffic_sign=NL:D1 oneway=yes"
                err.append({'class': 5, 'subclass': 439012160, 'text': mapcss.tr('{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'), mapcss._tag_uncapture(capture_tags, '{3.tag}'))})

        # way[highway][traffic_sign~="NL:D1"][junction=circular][oneway!~/^(yes|-?1)$/]
        # way[highway][traffic_sign~="NL:D01"][junction=circular][oneway!~/^(yes|-?1)$/]
        if ('highway' in keys and 'junction' in keys and 'traffic_sign' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:D1'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'junction') == mapcss._value_capture(capture_tags, 2, 'circular')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_3bd9d067, '^(yes|-?1)$'), mapcss._tag_capture(capture_tags, 3, tags, 'oneway'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:D01'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'junction') == mapcss._value_capture(capture_tags, 2, 'circular')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_3bd9d067, '^(yes|-?1)$'), mapcss._tag_capture(capture_tags, 3, tags, 'oneway'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} together with {1} but without {2}","{2.tag}","{1.tag}","oneway=yes")
                # assertNoMatch:"way highway=residential traffic_sign=NL:D1 junction=circular oneway=-1"
                # assertNoMatch:"way highway=residential traffic_sign=NL:D1 junction=circular oneway=yes"
                # assertMatch:"way highway=residential traffic_sign=NL:D1 junction=circular"
                # assertMatch:"way highway=residential traffic_sign=NL:D1 oneway=no junction=circular"
                err.append({'class': 5, 'subclass': 1998584294, 'text': mapcss.tr('{0} together with {1} but without {2}', mapcss._tag_uncapture(capture_tags, '{2.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), 'oneway=yes')})

        # way[traffic_sign="NL:B1"][!priority_road][!priority_road:forward][!priority_road:backward][!priority_road:both_ways][highway]
        # way[traffic_sign="NL:B01"][!priority_road][!priority_road:forward][!priority_road:backward][!priority_road:both_ways][highway]
        # way[traffic_sign:forward="NL:B1"][!priority_road][!priority_road:forward][!priority_road:both_ways][highway]
        # way[traffic_sign:forward="NL:B01"][!priority_road][!priority_road:forward][!priority_road:both_ways][highway]
        # way[traffic_sign:backward="NL:B1"][!priority_road][!priority_road:backward][!priority_road:both_ways][highway]
        # way[traffic_sign:backward="NL:B01"][!priority_road][!priority_road:backward][!priority_road:both_ways][highway]
        if ('highway' in keys and 'traffic_sign' in keys) or ('highway' in keys and 'traffic_sign:backward' in keys) or ('highway' in keys and 'traffic_sign:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign') == mapcss._value_capture(capture_tags, 0, 'NL:B1')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'priority_road')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'priority_road:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'priority_road:backward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'priority_road:both_ways')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign') == mapcss._value_capture(capture_tags, 0, 'NL:B01')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'priority_road')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'priority_road:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'priority_road:backward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'priority_road:both_ways')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:forward') == mapcss._value_capture(capture_tags, 0, 'NL:B1')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'priority_road')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'priority_road:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'priority_road:both_ways')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:forward') == mapcss._value_capture(capture_tags, 0, 'NL:B01')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'priority_road')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'priority_road:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'priority_road:both_ways')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:backward') == mapcss._value_capture(capture_tags, 0, 'NL:B1')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'priority_road')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'priority_road:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'priority_road:both_ways')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:backward') == mapcss._value_capture(capture_tags, 0, 'NL:B01')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'priority_road')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'priority_road:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'priority_road:both_ways')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}")
                # suggestAlternative:"{0.key}=designated"
                err.append({'class': 5, 'subclass': 2073220392, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # way[parking:condition:both!=no_parking][traffic_sign~="NL:E01"][highway][parking:lane:both=no][parking:condition:right!=no_parking][parking:condition:left!=no_parking]
        # way[parking:condition:both!=no_parking][traffic_sign~="NL:E01"][highway][parking:lane:left=no][parking:lane:right=no][parking:condition:right!=no_parking][parking:condition:left!=no_parking]
        # way[parking:condition:both!=no_parking][traffic_sign~="NL:E1"][highway][parking:lane:both=no][parking:condition:right!=no_parking][parking:condition:left!=no_parking]
        # way[parking:condition:both!=no_parking][traffic_sign~="NL:E1"][highway][parking:lane:left=no][parking:lane:right=no][parking:condition:right!=no_parking][parking:condition:left!=no_parking]
        # way[parking:condition:right!=no_parking][traffic_sign:right~="NL:E01"][highway][parking:lane:both=no][parking:condition:both!=no_parking]
        # way[parking:condition:right!=no_parking][traffic_sign:right~="NL:E01"][highway][parking:lane:right=no][parking:condition:both!=no_parking]
        # way[parking:condition:right!=no_parking][traffic_sign:right~="NL:E1"][highway][parking:lane:both=no][parking:condition:both!=no_parking]
        # way[parking:condition:right!=no_parking][traffic_sign:right~="NL:E1"][highway][parking:lane:right=no][parking:condition:both!=no_parking]
        # way[parking:condition:left!=no_parking][traffic_sign:left~="NL:E01"][highway][parking:lane:both=no][parking:condition:both!=no_parking]
        # way[parking:condition:left!=no_parking][traffic_sign:left~="NL:E01"][highway][parking:lane:left=no][parking:condition:both!=no_parking]
        # way[parking:condition:left!=no_parking][traffic_sign:left~="NL:E1"][highway][parking:lane:both=no][parking:condition:both!=no_parking]
        # way[parking:condition:left!=no_parking][traffic_sign:left~="NL:E1"][highway][parking:lane:left=no][parking:condition:both!=no_parking]
        # way[parking:condition:both!=no_stopping][traffic_sign~="NL:E02"][highway][parking:lane:both=no][parking:condition:right!=no_stopping][parking:condition:left!=no_stopping]
        # way[parking:condition:both!=no_stopping][traffic_sign~="NL:E02"][highway][parking:lane:left=no][parking:lane:right=no][parking:condition:right!=no_stopping][parking:condition:left!=no_stopping]
        # way[parking:condition:both!=no_stopping][traffic_sign~="NL:E2"][highway][parking:lane:both=no][parking:condition:right!=no_stopping][parking:condition:left!=no_stopping]
        # way[parking:condition:both!=no_stopping][traffic_sign~="NL:E2"][highway][parking:lane:left=no][parking:lane:right=no][parking:condition:right!=no_stopping][parking:condition:left!=no_stopping]
        # way[parking:condition:right!=no_stopping][traffic_sign:right~="NL:E02"][highway][parking:lane:both=no][parking:condition:both!=no_stopping]
        # way[parking:condition:right!=no_stopping][traffic_sign:right~="NL:E02"][highway][parking:lane:right=no][parking:condition:both!=no_stopping]
        # way[parking:condition:right!=no_stopping][traffic_sign:right~="NL:E2"][highway][parking:lane:both=no][parking:condition:both!=no_stopping]
        # way[parking:condition:right!=no_stopping][traffic_sign:right~="NL:E2"][highway][parking:lane:right=no][parking:condition:both!=no_stopping]
        # way[parking:condition:left!=no_stopping][traffic_sign:left~="NL:E02"][highway][parking:lane:both=no][parking:condition:both!=no_stopping]
        # way[parking:condition:left!=no_stopping][traffic_sign:left~="NL:E02"][highway][parking:lane:left=no][parking:condition:both!=no_stopping]
        # way[parking:condition:left!=no_stopping][traffic_sign:left~="NL:E2"][highway][parking:lane:both=no][parking:condition:both!=no_stopping]
        # way[parking:condition:left!=no_stopping][traffic_sign:left~="NL:E2"][highway][parking:lane:left=no][parking:condition:both!=no_stopping]
        if ('highway' in keys and 'parking:lane:both' in keys and 'traffic_sign' in keys) or ('highway' in keys and 'parking:lane:both' in keys and 'traffic_sign:left' in keys) or ('highway' in keys and 'parking:lane:both' in keys and 'traffic_sign:right' in keys) or ('highway' in keys and 'parking:lane:left' in keys and 'parking:lane:right' in keys and 'traffic_sign' in keys) or ('highway' in keys and 'parking:lane:left' in keys and 'traffic_sign:left' in keys) or ('highway' in keys and 'parking:lane:right' in keys and 'traffic_sign:right' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:condition:both') != mapcss._value_const_capture(capture_tags, 0, 'no_parking', 'no_parking')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:E01'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:lane:both') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:condition:right') != mapcss._value_const_capture(capture_tags, 4, 'no_parking', 'no_parking')) and (mapcss._tag_capture(capture_tags, 5, tags, 'parking:condition:left') != mapcss._value_const_capture(capture_tags, 5, 'no_parking', 'no_parking')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:condition:both') != mapcss._value_const_capture(capture_tags, 0, 'no_parking', 'no_parking')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:E01'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:lane:left') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:lane:right') == mapcss._value_capture(capture_tags, 4, 'no')) and (mapcss._tag_capture(capture_tags, 5, tags, 'parking:condition:right') != mapcss._value_const_capture(capture_tags, 5, 'no_parking', 'no_parking')) and (mapcss._tag_capture(capture_tags, 6, tags, 'parking:condition:left') != mapcss._value_const_capture(capture_tags, 6, 'no_parking', 'no_parking')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:condition:both') != mapcss._value_const_capture(capture_tags, 0, 'no_parking', 'no_parking')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:E1'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:lane:both') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:condition:right') != mapcss._value_const_capture(capture_tags, 4, 'no_parking', 'no_parking')) and (mapcss._tag_capture(capture_tags, 5, tags, 'parking:condition:left') != mapcss._value_const_capture(capture_tags, 5, 'no_parking', 'no_parking')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:condition:both') != mapcss._value_const_capture(capture_tags, 0, 'no_parking', 'no_parking')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:E1'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:lane:left') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:lane:right') == mapcss._value_capture(capture_tags, 4, 'no')) and (mapcss._tag_capture(capture_tags, 5, tags, 'parking:condition:right') != mapcss._value_const_capture(capture_tags, 5, 'no_parking', 'no_parking')) and (mapcss._tag_capture(capture_tags, 6, tags, 'parking:condition:left') != mapcss._value_const_capture(capture_tags, 6, 'no_parking', 'no_parking')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:condition:right') != mapcss._value_const_capture(capture_tags, 0, 'no_parking', 'no_parking')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:right'), mapcss._value_capture(capture_tags, 1, 'NL:E01'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:lane:both') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:condition:both') != mapcss._value_const_capture(capture_tags, 4, 'no_parking', 'no_parking')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:condition:right') != mapcss._value_const_capture(capture_tags, 0, 'no_parking', 'no_parking')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:right'), mapcss._value_capture(capture_tags, 1, 'NL:E01'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:lane:right') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:condition:both') != mapcss._value_const_capture(capture_tags, 4, 'no_parking', 'no_parking')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:condition:right') != mapcss._value_const_capture(capture_tags, 0, 'no_parking', 'no_parking')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:right'), mapcss._value_capture(capture_tags, 1, 'NL:E1'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:lane:both') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:condition:both') != mapcss._value_const_capture(capture_tags, 4, 'no_parking', 'no_parking')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:condition:right') != mapcss._value_const_capture(capture_tags, 0, 'no_parking', 'no_parking')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:right'), mapcss._value_capture(capture_tags, 1, 'NL:E1'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:lane:right') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:condition:both') != mapcss._value_const_capture(capture_tags, 4, 'no_parking', 'no_parking')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:condition:left') != mapcss._value_const_capture(capture_tags, 0, 'no_parking', 'no_parking')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:left'), mapcss._value_capture(capture_tags, 1, 'NL:E01'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:lane:both') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:condition:both') != mapcss._value_const_capture(capture_tags, 4, 'no_parking', 'no_parking')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:condition:left') != mapcss._value_const_capture(capture_tags, 0, 'no_parking', 'no_parking')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:left'), mapcss._value_capture(capture_tags, 1, 'NL:E01'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:lane:left') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:condition:both') != mapcss._value_const_capture(capture_tags, 4, 'no_parking', 'no_parking')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:condition:left') != mapcss._value_const_capture(capture_tags, 0, 'no_parking', 'no_parking')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:left'), mapcss._value_capture(capture_tags, 1, 'NL:E1'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:lane:both') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:condition:both') != mapcss._value_const_capture(capture_tags, 4, 'no_parking', 'no_parking')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:condition:left') != mapcss._value_const_capture(capture_tags, 0, 'no_parking', 'no_parking')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:left'), mapcss._value_capture(capture_tags, 1, 'NL:E1'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:lane:left') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:condition:both') != mapcss._value_const_capture(capture_tags, 4, 'no_parking', 'no_parking')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:condition:both') != mapcss._value_const_capture(capture_tags, 0, 'no_stopping', 'no_stopping')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:E02'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:lane:both') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:condition:right') != mapcss._value_const_capture(capture_tags, 4, 'no_stopping', 'no_stopping')) and (mapcss._tag_capture(capture_tags, 5, tags, 'parking:condition:left') != mapcss._value_const_capture(capture_tags, 5, 'no_stopping', 'no_stopping')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:condition:both') != mapcss._value_const_capture(capture_tags, 0, 'no_stopping', 'no_stopping')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:E02'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:lane:left') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:lane:right') == mapcss._value_capture(capture_tags, 4, 'no')) and (mapcss._tag_capture(capture_tags, 5, tags, 'parking:condition:right') != mapcss._value_const_capture(capture_tags, 5, 'no_stopping', 'no_stopping')) and (mapcss._tag_capture(capture_tags, 6, tags, 'parking:condition:left') != mapcss._value_const_capture(capture_tags, 6, 'no_stopping', 'no_stopping')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:condition:both') != mapcss._value_const_capture(capture_tags, 0, 'no_stopping', 'no_stopping')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:E2'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:lane:both') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:condition:right') != mapcss._value_const_capture(capture_tags, 4, 'no_stopping', 'no_stopping')) and (mapcss._tag_capture(capture_tags, 5, tags, 'parking:condition:left') != mapcss._value_const_capture(capture_tags, 5, 'no_stopping', 'no_stopping')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:condition:both') != mapcss._value_const_capture(capture_tags, 0, 'no_stopping', 'no_stopping')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:E2'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:lane:left') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:lane:right') == mapcss._value_capture(capture_tags, 4, 'no')) and (mapcss._tag_capture(capture_tags, 5, tags, 'parking:condition:right') != mapcss._value_const_capture(capture_tags, 5, 'no_stopping', 'no_stopping')) and (mapcss._tag_capture(capture_tags, 6, tags, 'parking:condition:left') != mapcss._value_const_capture(capture_tags, 6, 'no_stopping', 'no_stopping')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:condition:right') != mapcss._value_const_capture(capture_tags, 0, 'no_stopping', 'no_stopping')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:right'), mapcss._value_capture(capture_tags, 1, 'NL:E02'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:lane:both') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:condition:both') != mapcss._value_const_capture(capture_tags, 4, 'no_stopping', 'no_stopping')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:condition:right') != mapcss._value_const_capture(capture_tags, 0, 'no_stopping', 'no_stopping')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:right'), mapcss._value_capture(capture_tags, 1, 'NL:E02'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:lane:right') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:condition:both') != mapcss._value_const_capture(capture_tags, 4, 'no_stopping', 'no_stopping')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:condition:right') != mapcss._value_const_capture(capture_tags, 0, 'no_stopping', 'no_stopping')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:right'), mapcss._value_capture(capture_tags, 1, 'NL:E2'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:lane:both') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:condition:both') != mapcss._value_const_capture(capture_tags, 4, 'no_stopping', 'no_stopping')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:condition:right') != mapcss._value_const_capture(capture_tags, 0, 'no_stopping', 'no_stopping')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:right'), mapcss._value_capture(capture_tags, 1, 'NL:E2'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:lane:right') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:condition:both') != mapcss._value_const_capture(capture_tags, 4, 'no_stopping', 'no_stopping')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:condition:left') != mapcss._value_const_capture(capture_tags, 0, 'no_stopping', 'no_stopping')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:left'), mapcss._value_capture(capture_tags, 1, 'NL:E02'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:lane:both') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:condition:both') != mapcss._value_const_capture(capture_tags, 4, 'no_stopping', 'no_stopping')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:condition:left') != mapcss._value_const_capture(capture_tags, 0, 'no_stopping', 'no_stopping')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:left'), mapcss._value_capture(capture_tags, 1, 'NL:E02'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:lane:left') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:condition:both') != mapcss._value_const_capture(capture_tags, 4, 'no_stopping', 'no_stopping')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:condition:left') != mapcss._value_const_capture(capture_tags, 0, 'no_stopping', 'no_stopping')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:left'), mapcss._value_capture(capture_tags, 1, 'NL:E2'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:lane:both') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:condition:both') != mapcss._value_const_capture(capture_tags, 4, 'no_stopping', 'no_stopping')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:condition:left') != mapcss._value_const_capture(capture_tags, 0, 'no_stopping', 'no_stopping')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:left'), mapcss._value_capture(capture_tags, 1, 'NL:E2'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:lane:left') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:condition:both') != mapcss._value_const_capture(capture_tags, 4, 'no_stopping', 'no_stopping')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} without {1}","{1.tag}","{0.tag}")
                # fixAdd:"{0.tag}"
                # assertMatch:"way highway=residential traffic_sign:left=NL:E02 parking:lane:both=no"
                # assertMatch:"way highway=residential traffic_sign:left=NL:E02 parking:lane:left=no"
                # assertNoMatch:"way highway=residential traffic_sign:left=NL:E02 parking:lane:left=parallel"
                # assertNoMatch:"way highway=residential traffic_sign:left=NL:E02 traffic_sign:right=NL:E02 parking:lane:both=no parking:condition:both=no_stopping"
                err.append({'class': 5, 'subclass': 1501968560, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, '{0.tag}')).split('=', 1)])
                }})

        # way[building][/^addr:/][amenity!=place_of_worship][building!~/houseboat|static_caravan/][inside("NL")]:closed
        if ('building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_088b0835)) and (mapcss._tag_capture(capture_tags, 2, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 2, 'place_of_worship', 'place_of_worship')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_17085e60, 'houseboat|static_caravan'), mapcss._tag_capture(capture_tags, 3, tags, 'building'))) and (mapcss.inside(self.father.config.options, 'NL')) and (nds[0] == nds[-1]))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL addresses and contacts")
                # throwWarning:tr("In Nederland is het gebouw niet gekoppeld aan het adres. Het adres is wel gekoppeld aan het gebruiksdoel.")
                err.append({'class': 1, 'subclass': 1966846168, 'text': mapcss.tr('In Nederland is het gebouw niet gekoppeld aan het adres. Het adres is wel gekoppeld aan het gebruiksdoel.')})

        # way[cycleway:surface][surface][highway=cycleway][surface=*"cycleway:surface"][inside("NL")]
        # way[footway:surface][surface][highway=footway][surface=*"footway:surface"][inside("NL")]
        if ('cycleway:surface' in keys and 'highway' in keys and 'surface' in keys) or ('footway:surface' in keys and 'highway' in keys and 'surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cycleway:surface')) and (mapcss._tag_capture(capture_tags, 1, tags, 'surface')) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') == mapcss._value_capture(capture_tags, 2, 'cycleway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'surface') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'cycleway:surface'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'footway:surface')) and (mapcss._tag_capture(capture_tags, 1, tags, 'surface')) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') == mapcss._value_capture(capture_tags, 2, 'footway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'surface') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'footway:surface'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL German style tagging")
                # throwWarning:tr("{0} together with {1} and {2}. Remove {0}.","{0.key}","{1.key}","{2.tag}")
                # fixRemove:"{0.key}"
                err.append({'class': 6, 'subclass': 731881046, 'text': mapcss.tr('{0} together with {1} and {2}. Remove {0}.', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # way[cycleway:surface][surface][highway=cycleway][surface!=*"cycleway:surface"][inside("NL")]
        # way[footway:surface][surface][highway=footway][surface!=*"footway:surface"][inside("NL")]
        if ('cycleway:surface' in keys and 'highway' in keys and 'surface' in keys) or ('footway:surface' in keys and 'highway' in keys and 'surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cycleway:surface')) and (mapcss._tag_capture(capture_tags, 1, tags, 'surface')) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') == mapcss._value_capture(capture_tags, 2, 'cycleway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'surface') != mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'cycleway:surface'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'footway:surface')) and (mapcss._tag_capture(capture_tags, 1, tags, 'surface')) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') == mapcss._value_capture(capture_tags, 2, 'footway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'surface') != mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'footway:surface'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL German style tagging")
                # throwWarning:tr("{0} and {1} together with {2} and conflicting values","{0.key}","{1.key}","{2.tag}")
                err.append({'class': 6, 'subclass': 719277245, 'text': mapcss.tr('{0} and {1} together with {2} and conflicting values', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # way[cycleway:surface][highway=cycleway][!surface][inside("NL")]
        # way[footway:surface][highway=footway][!surface][inside("NL")]
        if ('cycleway:surface' in keys and 'highway' in keys) or ('footway:surface' in keys and 'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cycleway:surface')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway') == mapcss._value_capture(capture_tags, 1, 'cycleway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'surface')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'footway:surface')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway') == mapcss._value_capture(capture_tags, 1, 'footway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'surface')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL German style tagging")
                # throwWarning:tr("{0} together with {1}","{0.key}","{1.tag}")
                # suggestAlternative:"surface=*"
                # fixChangeKey:"{0.key}=>surface"
                err.append({'class': 6, 'subclass': 264601774, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [(mapcss._tag_uncapture(capture_tags, '{0.key}=>surface')).split('=>', 1)[1].strip(), mapcss.tag(tags, (mapcss._tag_uncapture(capture_tags, '{0.key}=>surface')).split('=>', 1)[0].strip())]]),
                    '-': ([
                    (mapcss._tag_uncapture(capture_tags, '{0.key}=>surface')).split('=>', 1)[0].strip()])
                }})

        # way[footway:surface][cycleway:surface][segregated=no][highway][footway:surface!=*"cycleway:surface"][inside("NL")]
        if ('cycleway:surface' in keys and 'footway:surface' in keys and 'highway' in keys and 'segregated' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'footway:surface')) and (mapcss._tag_capture(capture_tags, 1, tags, 'cycleway:surface')) and (mapcss._tag_capture(capture_tags, 2, tags, 'segregated') == mapcss._value_capture(capture_tags, 2, 'no')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 4, tags, 'footway:surface') != mapcss._value_capture(capture_tags, 4, mapcss.tag(tags, 'cycleway:surface'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL German style tagging")
                # throwWarning:tr("{0} and {1} together with {2} and conflicting values","{0.key}","{1.key}","{2.tag}")
                err.append({'class': 6, 'subclass': 1915077278, 'text': mapcss.tr('{0} and {1} together with {2} and conflicting values', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # way[/^footway(:left|:right|:both)?:/][/^sidewalk:(left|right|both)$/][/^sidewalk:(left|right|both)$/=~/^yes$/][inside("NL")]
        # way[/^footway(:left|:right|:both)?:/][sidewalk][sidewalk=~/^(left|right|both|yes)$/][inside("NL")]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_5f5aa10b)) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_7184e9bc)) and (mapcss.regexp_test(self.re_51f98600, mapcss._match_regex(tags, self.re_7184e9bc))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_5f5aa10b)) and (mapcss._tag_capture(capture_tags, 1, tags, 'sidewalk')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_5e498788), mapcss._tag_capture(capture_tags, 2, tags, 'sidewalk'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL German style tagging")
                # throwWarning:tr("{0} together with {1}","{0.key}","{1.key}")
                # suggestAlternative:"sidewalk:*"
                err.append({'class': 6, 'subclass': 800706341, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # way[cycleway=opposite][inside("NL")]
        # way[cycleway:left=opposite][inside("NL")]
        # way[cycleway:right=opposite][inside("NL")]
        # way[cycleway:both=opposite][inside("NL")]
        if ('cycleway' in keys) or ('cycleway:both' in keys) or ('cycleway:left' in keys) or ('cycleway:right' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cycleway') == mapcss._value_capture(capture_tags, 0, 'opposite')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cycleway:left') == mapcss._value_capture(capture_tags, 0, 'opposite')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cycleway:right') == mapcss._value_capture(capture_tags, 0, 'opposite')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cycleway:both') == mapcss._value_capture(capture_tags, 0, 'opposite')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.value}")
                # suggestAlternative:"oneway:bicycle/mofa/moped=no"
                err.append({'class': 2, 'subclass': 1863791326, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.value}'))})

        # way[cycleway][cycleway^=opposite_][inside("NL")]
        # way[cycleway:left][cycleway:left^=opposite_][inside("NL")]
        # way[cycleway:right][cycleway:right^=opposite_][inside("NL")]
        # way[cycleway:both][cycleway:both^=opposite_][inside("NL")]
        if ('cycleway' in keys) or ('cycleway:both' in keys) or ('cycleway:left' in keys) or ('cycleway:right' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cycleway')) and (mapcss.startswith(mapcss._tag_capture(capture_tags, 1, tags, 'cycleway'), mapcss._value_capture(capture_tags, 1, 'opposite_'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cycleway:left')) and (mapcss.startswith(mapcss._tag_capture(capture_tags, 1, tags, 'cycleway:left'), mapcss._value_capture(capture_tags, 1, 'opposite_'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cycleway:right')) and (mapcss.startswith(mapcss._tag_capture(capture_tags, 1, tags, 'cycleway:right'), mapcss._value_capture(capture_tags, 1, 'opposite_'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cycleway:both')) and (mapcss.startswith(mapcss._tag_capture(capture_tags, 1, tags, 'cycleway:both'), mapcss._value_capture(capture_tags, 1, 'opposite_'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.value}")
                # suggestAlternative:"oneway:bicycle/mofa/moped=no + {0.key}=*[zonder opposite_]"
                err.append({'class': 2, 'subclass': 716321685, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.value}'))})

        # way[sidewalk=none][inside("NL")]
        if ('sidewalk' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sidewalk') == mapcss._value_capture(capture_tags, 0, 'none')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sidewalk=no"
                # fixAdd:"{0.key}=no"
                err.append({'class': 2, 'subclass': 2146573895, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, '{0.key}=no')).split('=', 1)])
                }})

        # way[postal_code][inside("NL")]
        if ('postal_code' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'postal_code')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"addr:postcode via BAG imports on addresses"
                err.append({'class': 2, 'subclass': 194633982, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # way[building=terrace][inside("NL")]
        if ('building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'terrace')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("Rijtjeshuizen ({0}) worden in Nederland individueel geïmporteerd uit de BAG","{0.tag}")
                # suggestAlternative:"leisure=outdoor_seating voor 'terrasjes'"
                # suggestAlternative:"building=house via een BAG importverzoek voor huizen"
                err.append({'class': 2, 'subclass': 239999292, 'text': mapcss.tr('Rijtjeshuizen ({0}) worden in Nederland individueel geïmporteerd uit de BAG', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[is_in=NL]
        # *[is_in:country][inside("NL")]
        # *[is_in:city][inside("NL")]
        # *[is_in:province][inside("NL")]
        # *[is_in:continent][inside("NL")]
        # *[is_in:country_code=NL]
        if ('is_in' in keys) or ('is_in:city' in keys) or ('is_in:continent' in keys) or ('is_in:country' in keys) or ('is_in:country_code' in keys) or ('is_in:province' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'is_in') == mapcss._value_capture(capture_tags, 0, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'is_in:country')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'is_in:city')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'is_in:province')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'is_in:continent')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'is_in:country_code') == mapcss._value_capture(capture_tags, 0, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixRemove:"{0.key}"
                err.append({'class': 2, 'subclass': 788111375, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # way[railway][tracks][tracks!=1][inside("NL")]
        if ('railway' in keys and 'tracks' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'tracks')) and (mapcss._tag_capture(capture_tags, 2, tags, 'tracks') != mapcss._value_capture(capture_tags, 2, 1)) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("Railway lines should be drawn as separate ways per track, rather than one way with {0}","{1.tag}")
                # suggestAlternative:"passenger_lines=* if the tracks are already drawn separately"
                err.append({'class': 2, 'subclass': 379490980, 'text': mapcss.tr('Railway lines should be drawn as separate ways per track, rather than one way with {0}', mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # way[addr:housename][/^building(:part)?$/][inside("NL")]
        # way[building:name][/^building(:part)?$/][inside("NL")]
        if ('addr:housename' in keys) or ('building:name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'addr:housename')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_550ffc74)) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:name')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_550ffc74)) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"name=*"
                err.append({'class': 2, 'subclass': 1181753177, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[delivery:covid19][inside("NL")]
        # *[takeaway:covid19][inside("NL")]
        # *[opening_hours:covid19][inside("NL")]
        if ('delivery:covid19' in keys) or ('opening_hours:covid19' in keys) or ('takeaway:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'delivery:covid19')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'takeaway:covid19')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'opening_hours:covid19')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("There are no active covid-19 restrictions at the moment. Remove {0}.","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 2, 'subclass': 371241830, 'text': mapcss.tr('There are no active covid-19 restrictions at the moment. Remove {0}.', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # way[name][highway=service][name=~/(?i)(parkeren$|parkeerplaats$|^toegang(sweg)?\s|^richting\s|drive.thro?u(gh)?)/]
        # way[name][highway][name=~/(?i)(^|\sen\s)((on)?verplicht\s)?(\(?brom\)?)?fietspad$/]
        # way[name][highway][name=~/(?i)^roltrap(pen)?$/]
        # way[name][highway][name=~/(?i)(rolstoel|invaliden)/]
        # way[name][highway][name=~/(?i)(uit?laa[dt]|honden.*wandel|los.?loop)/]
        # way[name][highway][name=~/(?i)bus\s?(baan|strook)/][highway!=busway][highway!=service][highway!=construction]
        # *[name][amenity^=parking][name=~/(?i)(parkeren|parkeerplaats|parkeergarage|^garage)$/]
        # *[name][name=~/(?i)^gratis\s|gratis\)/]
        # *[name][name=~/(?i)(klanten|bezoek(ers)?|medewerkers)\b/][!route]
        # *[name][leisure=playground][name=~/(?i)^speeltuin$/]
        # *[name][leisure^=dog][name=~/(?i)^(honden\s?)?(toilet|uitlaa[dt]|los.?loop)/]
        # *[name][leisure=pitch][name=~/(?i)ball?(veld(je)?)?$/][!sport]
        if ('amenity' in keys and 'name' in keys) or ('highway' in keys and 'name' in keys) or ('leisure' in keys and 'name' in keys) or ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway') == mapcss._value_capture(capture_tags, 1, 'service')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3254c1c6), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_1705b261), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_44720f99), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_543ffeee), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3b2cb1d7), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_1582ff37), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'busway', 'busway')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'service', 'service')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.startswith(mapcss._tag_capture(capture_tags, 1, tags, 'amenity'), mapcss._value_capture(capture_tags, 1, 'parking'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_467ce1ba), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6cd83c9e), mapcss._tag_capture(capture_tags, 1, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6b1906aa), mapcss._tag_capture(capture_tags, 1, tags, 'name'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'route')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'leisure') == mapcss._value_capture(capture_tags, 1, 'playground')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_5ed5036a), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.startswith(mapcss._tag_capture(capture_tags, 1, tags, 'leisure'), mapcss._value_capture(capture_tags, 1, 'dog'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_5b4448e5), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'leisure') == mapcss._value_capture(capture_tags, 1, 'pitch')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3c163648), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'sport')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("descriptive name")
                err.append({'class': 3, 'subclass': 563821884, 'text': mapcss.tr('descriptive name')})

        # *[name][name=~/(?i)(voormalige?)/][!historic][tourism!=information][!landuse][!highway][!boundary][!waterway]
        if ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6211f625), mapcss._tag_capture(capture_tags, 1, tags, 'name'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'historic')) and (mapcss._tag_capture(capture_tags, 3, tags, 'tourism') != mapcss._value_const_capture(capture_tags, 3, 'information', 'information')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'landuse')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 6, tags, 'boundary')) and (not mapcss._tag_capture(capture_tags, 7, tags, 'waterway')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("descriptive name")
                # suggestAlternative:"description=*"
                # suggestAlternative:"disused=yes"
                # suggestAlternative:"old_name=*"
                err.append({'class': 3, 'subclass': 538711457, 'text': mapcss.tr('descriptive name')})

        # way[name][highway][name=~/\b(Adm|Burg|Dr|Drs|Ds|Gen|Ing|Ir|Mr|Past|Prof|St|Weth)\.? [A-Za-z]/][inside("NL")]!.abbrname
        # way[name][highway][name=~/^[A-Z][a-z]{1,4}\. /][inside("NL")]!.abbrname
        if ('highway' in keys and 'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_abbrname) and (mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3082f445), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_abbrname) and (mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_293c2706), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # set .abbrname
                # group:tr("NL nomenclature")
                # throwWarning:tr("Straatnaam met afkorting")
                # assertNoMatch:"way highway=residential name=\"De Visserstraat\""
                # assertNoMatch:"way highway=residential name=\"J.T. de Visserstraat\""
                set_abbrname = True
                err.append({'class': 3, 'subclass': 275992542, 'text': mapcss.tr('Straatnaam met afkorting')})

        # *[name][place][name=~/\b(Adm|Burg|Dr|Drs|Ds|Gen|Ing|Ir|Mr|Past|Prof|St|Weth)\.? [A-Za-z]/][inside("NL")]!.abbrname
        # *[name][place][name=~/^[A-Z][a-z]{1,4}\. /][inside("NL")]!.abbrname
        if ('name' in keys and 'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_abbrname) and (mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'place')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3082f445), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_abbrname) and (mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'place')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_293c2706), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # set .abbrname
                # group:tr("NL nomenclature")
                # throwWarning:tr("Gebiedsnaam met afkorting")
                set_abbrname = True
                err.append({'class': 3, 'subclass': 1829114630, 'text': mapcss.tr('Gebiedsnaam met afkorting')})

        # *[railway][name][name=~/(?i)(aansl|empl|goed|ind|inhaalsp|opstel|overloopw|racc|rang|terr)\./][inside("NL")]!.abbrname
        # *[railway][name][name=~/(?i)\b(aansl|empl|goed|ind|inhaalsp|opstel|overloopw|racc|rang|terr)\b/][inside("NL")]!.abbrname
        if ('name' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_abbrname) and (mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_798edef1), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_abbrname) and (mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_2441139b), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # set .abbrname
                # group:tr("NL nomenclature")
                # throwWarning:tr("Spoorgebied met afgekorte naam")
                # suggestAlternative:"aansluiting, emplacement, goederen, industrieterrein, inhaalspoor, opstelterrein, overloopwissel, raccordement of rangeerterrein"
                set_abbrname = True
                err.append({'class': 3, 'subclass': 1558593366, 'text': mapcss.tr('Spoorgebied met afgekorte naam')})

        # *[name:nl][!name][inside("NL")][type!=route][name:fy]["name:fy"=*"name:nl"]
        # *[name:nl][!name][inside("NL")][type!=route][!name:fy]
        if ('name:fy' in keys and 'name:nl' in keys) or ('name:nl' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name:nl')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, 3, tags, 'type') != mapcss._value_const_capture(capture_tags, 3, 'route', 'route')) and (mapcss._tag_capture(capture_tags, 4, tags, 'name:fy')) and (mapcss._tag_capture(capture_tags, 5, tags, 'name:fy') == mapcss._value_capture(capture_tags, 5, mapcss.tag(tags, 'name:nl'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name:nl')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, 3, tags, 'type') != mapcss._value_const_capture(capture_tags, 3, 'route', 'route')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'name:fy')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("{0} without {1}","{0.key}","{1.key}")
                # suggestAlternative:"name"
                # fixChangeKey:"{0.key}=>{1.key}"
                err.append({'class': 3, 'subclass': 1647353731, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [(mapcss._tag_uncapture(capture_tags, '{0.key}=>{1.key}')).split('=>', 1)[1].strip(), mapcss.tag(tags, (mapcss._tag_uncapture(capture_tags, '{0.key}=>{1.key}')).split('=>', 1)[0].strip())]]),
                    '-': ([
                    (mapcss._tag_uncapture(capture_tags, '{0.key}=>{1.key}')).split('=>', 1)[0].strip()])
                }})

        # *[heritage=1][heritage:operator!=whc]
        # *[heritage=2][heritage:operator!=rce][inside("NL")]
        if ('heritage' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'heritage') == mapcss._value_capture(capture_tags, 0, 1)) and (mapcss._tag_capture(capture_tags, 1, tags, 'heritage:operator') != mapcss._value_const_capture(capture_tags, 1, 'whc', 'whc')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'heritage') == mapcss._value_capture(capture_tags, 0, 2)) and (mapcss._tag_capture(capture_tags, 1, tags, 'heritage:operator') != mapcss._value_const_capture(capture_tags, 1, 'rce', 'rce')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL heritage")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.tag}")
                # fixAdd:"{1.tag}"
                err.append({'class': 4, 'subclass': 166241851, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, '{1.tag}')).split('=', 1)])
                }})

        # *[ref:rce][!heritage:operator]
        if ('ref:rce' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:rce')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'heritage:operator')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL heritage")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}=*")
                # fixAdd:"heritage:operator=rce"
                err.append({'class': 4, 'subclass': 883322705, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}=*')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['heritage:operator','rce']])
                }})

        # *[heritage:operator=rce][!heritage]
        if ('heritage:operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'heritage:operator') == mapcss._value_capture(capture_tags, 0, 'rce')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'heritage')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL heritage")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}=*")
                # fixAdd:"heritage=2"
                err.append({'class': 4, 'subclass': 1486143485, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}=*')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['heritage','2']])
                }})

        # way[highway=living_street][maxspeed!=15][!/^maxspeed(:forward|:backward|:both_ways)?$/][inside("NL")]
        # way[maxspeed:type="NL:zone30"][maxspeed!=30][maxspeed:both_ways!=30][highway]
        # way[maxspeed:type="NL:zone60"][maxspeed!=60][maxspeed:both_ways!=60][highway]
        # way[maxspeed:type="NL:urban"][maxspeed!=50][maxspeed:both_ways!=50][highway]
        # way[maxspeed:type="NL:rural"][maxspeed!=80][maxspeed:both_ways!=80][highway]
        if ('highway' in keys) or ('highway' in keys and 'maxspeed:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'living_street')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed') != mapcss._value_capture(capture_tags, 1, 15)) and (not mapcss._tag_capture(capture_tags, 2, tags, self.re_1d614d5c)) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:type') == mapcss._value_capture(capture_tags, 0, 'NL:zone30')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed') != mapcss._value_capture(capture_tags, 1, 30)) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed:both_ways') != mapcss._value_capture(capture_tags, 2, 30)) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:type') == mapcss._value_capture(capture_tags, 0, 'NL:zone60')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed') != mapcss._value_capture(capture_tags, 1, 60)) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed:both_ways') != mapcss._value_capture(capture_tags, 2, 60)) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:type') == mapcss._value_capture(capture_tags, 0, 'NL:urban')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed') != mapcss._value_capture(capture_tags, 1, 50)) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed:both_ways') != mapcss._value_capture(capture_tags, 2, 50)) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:type') == mapcss._value_capture(capture_tags, 0, 'NL:rural')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed') != mapcss._value_capture(capture_tags, 1, 80)) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed:both_ways') != mapcss._value_capture(capture_tags, 2, 80)) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL speed limits")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.tag}")
                err.append({'class': 7, 'subclass': 1461368777, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # way[maxspeed:type][!maxspeed][maxspeed:type^="NL:zone"][!maxspeed:both_ways][maxspeed:type!~/^NL:zone[36]0$/][highway]
        # way[traffic_sign][!maxspeed][traffic_sign=~/(^|;)NL:A0?1-/][!/^maxspeed(:forward|:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:forward][!maxspeed:forward][traffic_sign:forward=~/(^|;)NL:A0?1-/][!/^maxspeed(:forward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:backward][!maxspeed:backward][traffic_sign:backward=~/(^|;)NL:A0?1-/][!/^maxspeed(:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign][!maxspeed:advisory][traffic_sign=~/(^|;)NL:A0?4\b/][!/^maxspeed:advisory(:forward|:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:forward][!maxspeed:advisory:forward][traffic_sign:forward=~/(^|;)NL:A0?4\b/][!/^maxspeed:advisory(:forward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:backward][!maxspeed:advisory:backward][traffic_sign:backward=~/(^|;)NL:A0?4\b/][!/^maxspeed:advisory(:backward|:both_ways)?(:conditional)?$/][highway]
        if ('highway' in keys and 'maxspeed:type' in keys) or ('highway' in keys and 'traffic_sign' in keys) or ('highway' in keys and 'traffic_sign:backward' in keys) or ('highway' in keys and 'traffic_sign:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:type')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss.startswith(mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed:type'), mapcss._value_capture(capture_tags, 2, 'NL:zone'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'maxspeed:both_ways')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 4, self.re_1d0c9a01, '^NL:zone[36]0$'), mapcss._tag_capture(capture_tags, 4, tags, 'maxspeed:type'))) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_731d219b), mapcss._tag_capture(capture_tags, 2, tags, 'traffic_sign'))) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_7acb98bb)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:forward')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:forward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_731d219b), mapcss._tag_capture(capture_tags, 2, tags, 'traffic_sign:forward'))) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_0cbcfeaf)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:backward')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:backward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_731d219b), mapcss._tag_capture(capture_tags, 2, tags, 'traffic_sign:backward'))) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_1cc9227a)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:advisory')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_73d53d80), mapcss._tag_capture(capture_tags, 2, tags, 'traffic_sign'))) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_06bae8ee)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:forward')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:advisory:forward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_73d53d80), mapcss._tag_capture(capture_tags, 2, tags, 'traffic_sign:forward'))) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_08935e4d)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:backward')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:advisory:backward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_73d53d80), mapcss._tag_capture(capture_tags, 2, tags, 'traffic_sign:backward'))) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_460900e8)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL speed limits")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}")
                # assertNoMatch:"way highway=residential traffic_sign:forward=NL:A1-30 maxspeed:forward=30"
                # assertMatch:"way highway=residential traffic_sign:forward=NL:A1-30"
                # assertNoMatch:"way highway=residential traffic_sign=NL:A01-30 maxspeed=30"
                # assertMatch:"way highway=residential traffic_sign=NL:A01-30"
                # assertMatch:"way highway=residential traffic_sign=NL:A04-30"
                # assertMatch:"way highway=residential traffic_sign=NL:A4"
                # assertNoMatch:"way highway=residential traffic_sign=NL:A4[50] maxspeed:advisory:both_ways=50"
                # assertMatch:"way highway=residential traffic_sign=NL:A4[60]"
                err.append({'class': 7, 'subclass': 678880168, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # way[highway=motorway][maxspeed][maxspeed=~/^1[23]0$/][maxspeed:conditional=~/100.+19:00/][inside("NL")]
        if ('highway' in keys and 'maxspeed' in keys and 'maxspeed:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'motorway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_7be1bafc), mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_5578cc63), mapcss._tag_capture(capture_tags, 3, tags, 'maxspeed:conditional'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL speed limits")
                # throwWarning:tr("Agreed upon was to use 100 as the maximum speed and {0} as the conditional maximum speed","{1.value}")
                err.append({'class': 7, 'subclass': 640790005, 'text': mapcss.tr('Agreed upon was to use 100 as the maximum speed and {0} as the conditional maximum speed', mapcss._tag_uncapture(capture_tags, '{1.value}'))})

        # way[highway=cycleway][maxspeed][maxspeed>40][!motor_vehicle][!vehicle][!access][inside("NL")]
        if ('highway' in keys and 'maxspeed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'cycleway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed') > mapcss._value_capture(capture_tags, 2, 40)) and (not mapcss._tag_capture(capture_tags, 3, tags, 'motor_vehicle')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'vehicle')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'access')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL speed limits")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                err.append({'class': 7, 'subclass': 244962748, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # way[oneway:bicycle?!][!oneway:mofa][oneway?][inside("NL")]
        if ('oneway' in keys and 'oneway:bicycle' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'oneway:bicycle') not in ('yes', 'true', '1')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'oneway:mofa')) and (mapcss._tag_capture(capture_tags, 2, tags, 'oneway') in ('yes', 'true', '1')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL mofa tagging")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}")
                err.append({'class': 8, 'subclass': 2063031692, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # way[bicycle:forward][moped:forward][bicycle:forward=*"moped:forward"][!mofa][!mofa:forward][bicycle:forward!=designated][bicycle:forward!=yes][inside("NL")]
        # way[bicycle:backward][moped:backward][bicycle:backward=*"moped:backward"][!mofa][!mofa:backward][bicycle:backward!=designated][bicycle:backward!=yes][inside("NL")]
        # way[bicycle:both_ways][moped:both_ways][bicycle:both_ways=*"moped:both_ways"][!mofa][!mofa:both_ways][bicycle:both_ways!=designated][bicycle:both_ways!=yes][inside("NL")]
        # way[bicycle][moped][bicycle=*moped][!mofa][bicycle!=designated][bicycle!=yes][inside("NL")]
        if ('bicycle' in keys and 'moped' in keys) or ('bicycle:backward' in keys and 'moped:backward' in keys) or ('bicycle:both_ways' in keys and 'moped:both_ways' in keys) or ('bicycle:forward' in keys and 'moped:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bicycle:forward')) and (mapcss._tag_capture(capture_tags, 1, tags, 'moped:forward')) and (mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:forward') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'moped:forward'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'mofa')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'mofa:forward')) and (mapcss._tag_capture(capture_tags, 5, tags, 'bicycle:forward') != mapcss._value_const_capture(capture_tags, 5, 'designated', 'designated')) and (mapcss._tag_capture(capture_tags, 6, tags, 'bicycle:forward') != mapcss._value_const_capture(capture_tags, 6, 'yes', 'yes')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bicycle:backward')) and (mapcss._tag_capture(capture_tags, 1, tags, 'moped:backward')) and (mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:backward') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'moped:backward'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'mofa')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'mofa:backward')) and (mapcss._tag_capture(capture_tags, 5, tags, 'bicycle:backward') != mapcss._value_const_capture(capture_tags, 5, 'designated', 'designated')) and (mapcss._tag_capture(capture_tags, 6, tags, 'bicycle:backward') != mapcss._value_const_capture(capture_tags, 6, 'yes', 'yes')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bicycle:both_ways')) and (mapcss._tag_capture(capture_tags, 1, tags, 'moped:both_ways')) and (mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:both_ways') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'moped:both_ways'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'mofa')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'mofa:both_ways')) and (mapcss._tag_capture(capture_tags, 5, tags, 'bicycle:both_ways') != mapcss._value_const_capture(capture_tags, 5, 'designated', 'designated')) and (mapcss._tag_capture(capture_tags, 6, tags, 'bicycle:both_ways') != mapcss._value_const_capture(capture_tags, 6, 'yes', 'yes')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bicycle')) and (mapcss._tag_capture(capture_tags, 1, tags, 'moped')) and (mapcss._tag_capture(capture_tags, 2, tags, 'bicycle') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'moped'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'mofa')) and (mapcss._tag_capture(capture_tags, 4, tags, 'bicycle') != mapcss._value_const_capture(capture_tags, 4, 'designated', 'designated')) and (mapcss._tag_capture(capture_tags, 5, tags, 'bicycle') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL mofa tagging")
                # throwWarning:tr("{0} and {1} without {2}","{0.tag}","{1.tag}","{3.key}={0.value}")
                # fixAdd:"{3.key}={0.value}"
                err.append({'class': 8, 'subclass': 1929817175, 'text': mapcss.tr('{0} and {1} without {2}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{3.key}={0.value}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, '{3.key}={0.value}')).split('=', 1)])
                }})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_abbrname = set_badPhoneNumber = False

        # relation[type=multipolygon][building][/^addr:/][amenity!=place_of_worship][building!~/houseboat|static_caravan/][inside("NL")]
        if ('building' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'multipolygon')) and (mapcss._tag_capture(capture_tags, 1, tags, 'building')) and (mapcss._tag_capture(capture_tags, 2, tags, self.re_088b0835)) and (mapcss._tag_capture(capture_tags, 3, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 3, 'place_of_worship', 'place_of_worship')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 4, self.re_17085e60, 'houseboat|static_caravan'), mapcss._tag_capture(capture_tags, 4, tags, 'building'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL addresses and contacts")
                # throwWarning:tr("In Nederland is het gebouw niet gekoppeld aan het adres. Het adres is wel gekoppeld aan het gebruiksdoel.")
                err.append({'class': 1, 'subclass': 1705589760, 'text': mapcss.tr('In Nederland is het gebouw niet gekoppeld aan het adres. Het adres is wel gekoppeld aan het gebruiksdoel.')})

        # relation[type=associatedStreet][inside("NL")]
        if ('type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'associatedStreet')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"geen relatie"
                # suggestAlternative:"type=street"
                err.append({'class': 2, 'subclass': 1207029826, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[is_in=NL]
        # *[is_in:country][inside("NL")]
        # *[is_in:city][inside("NL")]
        # *[is_in:province][inside("NL")]
        # *[is_in:continent][inside("NL")]
        # *[is_in:country_code=NL]
        if ('is_in' in keys) or ('is_in:city' in keys) or ('is_in:continent' in keys) or ('is_in:country' in keys) or ('is_in:country_code' in keys) or ('is_in:province' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'is_in') == mapcss._value_capture(capture_tags, 0, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'is_in:country')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'is_in:city')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'is_in:province')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'is_in:continent')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'is_in:country_code') == mapcss._value_capture(capture_tags, 0, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixRemove:"{0.key}"
                err.append({'class': 2, 'subclass': 788111375, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[delivery:covid19][inside("NL")]
        # *[takeaway:covid19][inside("NL")]
        # *[opening_hours:covid19][inside("NL")]
        if ('delivery:covid19' in keys) or ('opening_hours:covid19' in keys) or ('takeaway:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'delivery:covid19')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'takeaway:covid19')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'opening_hours:covid19')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("There are no active covid-19 restrictions at the moment. Remove {0}.","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 2, 'subclass': 371241830, 'text': mapcss.tr('There are no active covid-19 restrictions at the moment. Remove {0}.', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[name][amenity^=parking][name=~/(?i)(parkeren|parkeerplaats|parkeergarage|^garage)$/]
        # *[name][name=~/(?i)^gratis\s|gratis\)/]
        # *[name][name=~/(?i)(klanten|bezoek(ers)?|medewerkers)\b/][!route]
        # *[name][leisure=playground][name=~/(?i)^speeltuin$/]
        # *[name][leisure^=dog][name=~/(?i)^(honden\s?)?(toilet|uitlaa[dt]|los.?loop)/]
        # *[name][leisure=pitch][name=~/(?i)ball?(veld(je)?)?$/][!sport]
        if ('amenity' in keys and 'name' in keys) or ('leisure' in keys and 'name' in keys) or ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.startswith(mapcss._tag_capture(capture_tags, 1, tags, 'amenity'), mapcss._value_capture(capture_tags, 1, 'parking'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_467ce1ba), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6cd83c9e), mapcss._tag_capture(capture_tags, 1, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6b1906aa), mapcss._tag_capture(capture_tags, 1, tags, 'name'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'route')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'leisure') == mapcss._value_capture(capture_tags, 1, 'playground')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_5ed5036a), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.startswith(mapcss._tag_capture(capture_tags, 1, tags, 'leisure'), mapcss._value_capture(capture_tags, 1, 'dog'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_5b4448e5), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'leisure') == mapcss._value_capture(capture_tags, 1, 'pitch')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3c163648), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'sport')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("descriptive name")
                err.append({'class': 3, 'subclass': 1997744480, 'text': mapcss.tr('descriptive name')})

        # *[name][name=~/(?i)(voormalige?)/][!historic][tourism!=information][!landuse][!highway][!boundary][!waterway]
        if ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6211f625), mapcss._tag_capture(capture_tags, 1, tags, 'name'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'historic')) and (mapcss._tag_capture(capture_tags, 3, tags, 'tourism') != mapcss._value_const_capture(capture_tags, 3, 'information', 'information')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'landuse')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 6, tags, 'boundary')) and (not mapcss._tag_capture(capture_tags, 7, tags, 'waterway')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("descriptive name")
                # suggestAlternative:"description=*"
                # suggestAlternative:"disused=yes"
                # suggestAlternative:"old_name=*"
                err.append({'class': 3, 'subclass': 538711457, 'text': mapcss.tr('descriptive name')})

        # *[name][place][name=~/\b(Adm|Burg|Dr|Drs|Ds|Gen|Ing|Ir|Mr|Past|Prof|St|Weth)\.? [A-Za-z]/][inside("NL")]!.abbrname
        # *[name][place][name=~/^[A-Z][a-z]{1,4}\. /][inside("NL")]!.abbrname
        if ('name' in keys and 'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_abbrname) and (mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'place')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3082f445), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_abbrname) and (mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'place')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_293c2706), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # set .abbrname
                # group:tr("NL nomenclature")
                # throwWarning:tr("Gebiedsnaam met afkorting")
                set_abbrname = True
                err.append({'class': 3, 'subclass': 1829114630, 'text': mapcss.tr('Gebiedsnaam met afkorting')})

        # *[railway][name][name=~/(?i)(aansl|empl|goed|ind|inhaalsp|opstel|overloopw|racc|rang|terr)\./][inside("NL")]!.abbrname
        # *[railway][name][name=~/(?i)\b(aansl|empl|goed|ind|inhaalsp|opstel|overloopw|racc|rang|terr)\b/][inside("NL")]!.abbrname
        if ('name' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_abbrname) and (mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_798edef1), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_abbrname) and (mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_2441139b), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # set .abbrname
                # group:tr("NL nomenclature")
                # throwWarning:tr("Spoorgebied met afgekorte naam")
                # suggestAlternative:"aansluiting, emplacement, goederen, industrieterrein, inhaalspoor, opstelterrein, overloopwissel, raccordement of rangeerterrein"
                set_abbrname = True
                err.append({'class': 3, 'subclass': 1558593366, 'text': mapcss.tr('Spoorgebied met afgekorte naam')})

        # *[name:nl][!name][inside("NL")][type!=route][name:fy]["name:fy"=*"name:nl"]
        # *[name:nl][!name][inside("NL")][type!=route][!name:fy]
        if ('name:fy' in keys and 'name:nl' in keys) or ('name:nl' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name:nl')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, 3, tags, 'type') != mapcss._value_const_capture(capture_tags, 3, 'route', 'route')) and (mapcss._tag_capture(capture_tags, 4, tags, 'name:fy')) and (mapcss._tag_capture(capture_tags, 5, tags, 'name:fy') == mapcss._value_capture(capture_tags, 5, mapcss.tag(tags, 'name:nl'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name:nl')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, 3, tags, 'type') != mapcss._value_const_capture(capture_tags, 3, 'route', 'route')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'name:fy')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("{0} without {1}","{0.key}","{1.key}")
                # suggestAlternative:"name"
                # fixChangeKey:"{0.key}=>{1.key}"
                err.append({'class': 3, 'subclass': 1647353731, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [(mapcss._tag_uncapture(capture_tags, '{0.key}=>{1.key}')).split('=>', 1)[1].strip(), mapcss.tag(tags, (mapcss._tag_uncapture(capture_tags, '{0.key}=>{1.key}')).split('=>', 1)[0].strip())]]),
                    '-': ([
                    (mapcss._tag_uncapture(capture_tags, '{0.key}=>{1.key}')).split('=>', 1)[0].strip()])
                }})

        # *[heritage=1][heritage:operator!=whc]
        # *[heritage=2][heritage:operator!=rce][inside("NL")]
        if ('heritage' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'heritage') == mapcss._value_capture(capture_tags, 0, 1)) and (mapcss._tag_capture(capture_tags, 1, tags, 'heritage:operator') != mapcss._value_const_capture(capture_tags, 1, 'whc', 'whc')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'heritage') == mapcss._value_capture(capture_tags, 0, 2)) and (mapcss._tag_capture(capture_tags, 1, tags, 'heritage:operator') != mapcss._value_const_capture(capture_tags, 1, 'rce', 'rce')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL heritage")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.tag}")
                # fixAdd:"{1.tag}"
                err.append({'class': 4, 'subclass': 166241851, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, '{1.tag}')).split('=', 1)])
                }})

        # *[ref:rce][!heritage:operator]
        if ('ref:rce' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:rce')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'heritage:operator')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL heritage")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}=*")
                # fixAdd:"heritage:operator=rce"
                err.append({'class': 4, 'subclass': 883322705, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}=*')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['heritage:operator','rce']])
                }})

        # *[heritage:operator=rce][!heritage]
        if ('heritage:operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'heritage:operator') == mapcss._value_capture(capture_tags, 0, 'rce')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'heritage')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL heritage")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}=*")
                # fixAdd:"heritage=2"
                err.append({'class': 4, 'subclass': 1486143485, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}=*')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['heritage','2']])
                }})

        return err


from plugins.PluginMapCSS import TestPluginMapcss


class Test(TestPluginMapcss):
    def test(self):
        n = Josm_DutchSpecific(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.node(data, {'phone': '+31 06123456789'}), expected={'class': 1, 'subclass': 2136227068})
        self.check_not_err(n.node(data, {'phone': '+31 08008844'}), expected={'class': 1, 'subclass': 2136227068})
        self.check_not_err(n.node(data, {'phone': '+31 6123456789'}), expected={'class': 1, 'subclass': 2136227068})
        self.check_err(n.node(data, {'phone': '003106123456789'}), expected={'class': 1, 'subclass': 2136227068})
        self.check_not_err(n.node(data, {'phone': '00316123456789'}), expected={'class': 1, 'subclass': 2136227068})
        self.check_not_err(n.node(data, {'phone': '06123456789'}), expected={'class': 1, 'subclass': 2136227068})
        self.check_err(n.node(data, {'phone': '+31 08008844'}), expected={'class': 1, 'subclass': 253472651})
        self.check_not_err(n.node(data, {'phone': '+31 6123456789'}), expected={'class': 1, 'subclass': 253472651})
        self.check_err(n.node(data, {'phone': '+3114024'}), expected={'class': 1, 'subclass': 253472651})
        self.check_err(n.node(data, {'phone': '+318008844'}), expected={'class': 1, 'subclass': 253472651})
        self.check_not_err(n.node(data, {'phone': '00316123456789'}), expected={'class': 1, 'subclass': 253472651})
        self.check_err(n.node(data, {'phone': '00318008844'}), expected={'class': 1, 'subclass': 253472651})
        self.check_not_err(n.node(data, {'phone': '06123456789'}), expected={'class': 1, 'subclass': 253472651})
        self.check_not_err(n.node(data, {'phone': '08008844'}), expected={'class': 1, 'subclass': 253472651})
        self.check_not_err(n.node(data, {'phone': '14024'}), expected={'class': 1, 'subclass': 253472651})
        self.check_not_err(n.node(data, {'phone': '+31 6 12345678'}), expected={'class': 1, 'subclass': 1429902606})
        self.check_not_err(n.node(data, {'phone': '0031612345678'}), expected={'class': 1, 'subclass': 1429902606})
        self.check_not_err(n.node(data, {'phone': '06 12345678'}), expected={'class': 1, 'subclass': 1429902606})
        self.check_not_err(n.node(data, {'phone': '0800 1234567'}), expected={'class': 1, 'subclass': 1429902606})
        self.check_not_err(n.node(data, {'name': 'Landgoed', 'railway': 'tram_stop'}), expected={'class': 3, 'subclass': 1558593366})
        self.check_not_err(n.node(data, {'name:fy': 'y', 'name:nl': 'x'}), expected={'class': 3, 'subclass': 1647353731})
        self.check_not_err(n.node(data, {'name': 'x', 'name:en': 'y', 'name:nl': 'x'}), expected={'class': 3, 'subclass': 1647353731})
        self.check_err(n.node(data, {'amenity': 'post_box', 'operator': 'post nl'}), expected={'class': 3, 'subclass': 1831362989})
        self.check_not_err(n.node(data, {'amenity': 'post_box', 'operator': 'PostNL'}), expected={'class': 3, 'subclass': 1831362989})
        self.check_err(n.node(data, {'amenity': 'post_box', 'operator': 'postnl'}), expected={'class': 3, 'subclass': 1831362989})
        self.check_not_err(n.way(data, {'foot': 'no', 'hgv:backward': 'no', 'highway': 'service', 'traffic_sign:backward': 'NL:C07;NL:C16'}, [0]), expected={'class': 5, 'subclass': 798095003})
        self.check_not_err(n.way(data, {'foot': 'no', 'hgv': 'no', 'highway': 'service', 'traffic_sign:backward': 'NL:C07;NL:C16'}, [0]), expected={'class': 5, 'subclass': 798095003})
        self.check_err(n.way(data, {'access:backward': 'no', 'highway': 'service', 'traffic_sign:backward': 'NL:C1', 'traffic_sign:forward': 'NL:C9;NL:OB58'}, [0]), expected={'class': 5, 'subclass': 798095003})
        self.check_err(n.way(data, {'highway': 'service', 'traffic_sign:forward': 'NL:C9;NL:OB58'}, [0]), expected={'class': 5, 'subclass': 798095003})
        self.check_err(n.way(data, {'highway': 'service', 'traffic_sign': 'NL:C01'}, [0]), expected={'class': 5, 'subclass': 798095003})
        self.check_not_err(n.way(data, {'access': 'no', 'highway': 'service', 'traffic_sign': 'NL:C01;NL:C16'}, [0]), expected={'class': 5, 'subclass': 798095003})
        self.check_not_err(n.way(data, {'highway': 'service', 'motor_vehicle': 'no', 'traffic_sign': 'NL:C01;NL:OB51;NL:OB54'}, [0]), expected={'class': 5, 'subclass': 798095003})
        self.check_not_err(n.way(data, {'highway': 'track', 'oneway': 'yes', 'oneway:bicycle': 'no', 'traffic_sign:backward': 'NL:C12'}, [0]), expected={'class': 5, 'subclass': 798095003})
        self.check_not_err(n.way(data, {'highway': 'track', 'motor_vehicle': 'no', 'traffic_sign': 'NL:C12'}, [0]), expected={'class': 5, 'subclass': 798095003})
        self.check_not_err(n.way(data, {'highway': 'residential', 'maxweight:backward': '2.1', 'traffic_sign:backward': 'NL:C21[2.1]'}, [0]), expected={'class': 5, 'subclass': 1126640278})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign:forward': 'NL:C21[2.1]'}, [0]), expected={'class': 5, 'subclass': 1126640278})
        self.check_not_err(n.way(data, {'highway': 'residential', 'maxweight': '2.1', 'traffic_sign': 'NL:C21[2.1]'}, [0]), expected={'class': 5, 'subclass': 1126640278})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign': 'NL:C21[2.1]'}, [0]), expected={'class': 5, 'subclass': 1126640278})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign:backward': 'NL:C02;NL:OB58'}, [0]), expected={'class': 5, 'subclass': 1059189470})
        self.check_not_err(n.way(data, {'highway': 'residential', 'oneway:motor_vehicle': 'yes', 'traffic_sign:backward': 'NL:C2'}, [0]), expected={'class': 5, 'subclass': 1059189470})
        self.check_not_err(n.way(data, {'highway': 'residential', 'oneway': 'yes', 'oneway:bicycle': 'no', 'traffic_sign:backward': 'NL:C2'}, [0]), expected={'class': 5, 'subclass': 1059189470})
        self.check_not_err(n.way(data, {'highway': 'residential', 'oneway:motor_vehicle': 'yes', 'traffic_sign:forward': 'NL:C3'}, [0]), expected={'class': 5, 'subclass': 1059189470})
        self.check_err(n.way(data, {'highway': 'residential', 'oneway': '-1', 'traffic_sign:forward': 'NL:C3'}, [0]), expected={'class': 5, 'subclass': 1059189470})
        self.check_not_err(n.way(data, {'highway': 'residential', 'oneway': 'yes', 'traffic_sign:forward': 'NL:C3'}, [0]), expected={'class': 5, 'subclass': 1059189470})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign:forward': 'NL:C3'}, [0]), expected={'class': 5, 'subclass': 1059189470})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign': 'NL:C02'}, [0]), expected={'class': 5, 'subclass': 1059189470})
        self.check_not_err(n.way(data, {'highway': 'residential', 'oneway': '-1', 'traffic_sign': 'NL:C02;NL:OB58'}, [0]), expected={'class': 5, 'subclass': 1059189470})
        self.check_not_err(n.way(data, {'highway': 'residential', 'oneway': 'yes', 'traffic_sign': 'NL:C02;NL:OB58'}, [0]), expected={'class': 5, 'subclass': 1059189470})
        self.check_not_err(n.way(data, {'highway': 'residential', 'oneway': 'no', 'oneway:agricultural': 'no', 'oneway:motor_vehicle': 'yes', 'oneway:motorcycle': 'no', 'traffic_sign': 'NL:C3'}, [0]), expected={'class': 5, 'subclass': 1059189470})
        self.check_not_err(n.way(data, {'highway': 'residential', 'oneway:motor_vehicle': '-1', 'traffic_sign': 'NL:C3'}, [0]), expected={'class': 5, 'subclass': 1059189470})
        self.check_not_err(n.way(data, {'highway': 'residential', 'oneway:motor_vehicle': 'yes', 'traffic_sign': 'NL:C3'}, [0]), expected={'class': 5, 'subclass': 1059189470})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign': 'NL:C3;NL:OB58'}, [0]), expected={'class': 5, 'subclass': 1059189470})
        self.check_err(n.way(data, {'highway': 'residential', 'oneway': 'yes', 'traffic_sign': 'NL:C05'}, [0]), expected={'class': 5, 'subclass': 560436831})
        self.check_not_err(n.way(data, {'highway': 'residential', 'traffic_sign': 'NL:C05'}, [0]), expected={'class': 5, 'subclass': 560436831})
        self.check_not_err(n.way(data, {'highway': 'residential', 'oneway': 'no', 'traffic_sign': 'NL:C5;NL:OB58'}, [0]), expected={'class': 5, 'subclass': 560436831})
        self.check_not_err(n.way(data, {'highway': 'residential', 'junction': 'circular', 'traffic_sign': 'NL:D1'}, [0]), expected={'class': 5, 'subclass': 439012160})
        self.check_not_err(n.way(data, {'highway': 'residential', 'junction': 'roundabout', 'traffic_sign': 'NL:D1'}, [0]), expected={'class': 5, 'subclass': 439012160})
        self.check_err(n.way(data, {'highway': 'residential', 'oneway': 'yes', 'traffic_sign': 'NL:D1'}, [0]), expected={'class': 5, 'subclass': 439012160})
        self.check_not_err(n.way(data, {'highway': 'residential', 'junction': 'circular', 'oneway': '-1', 'traffic_sign': 'NL:D1'}, [0]), expected={'class': 5, 'subclass': 1998584294})
        self.check_not_err(n.way(data, {'highway': 'residential', 'junction': 'circular', 'oneway': 'yes', 'traffic_sign': 'NL:D1'}, [0]), expected={'class': 5, 'subclass': 1998584294})
        self.check_err(n.way(data, {'highway': 'residential', 'junction': 'circular', 'traffic_sign': 'NL:D1'}, [0]), expected={'class': 5, 'subclass': 1998584294})
        self.check_err(n.way(data, {'highway': 'residential', 'junction': 'circular', 'oneway': 'no', 'traffic_sign': 'NL:D1'}, [0]), expected={'class': 5, 'subclass': 1998584294})
        self.check_err(n.way(data, {'highway': 'residential', 'parking:lane:both': 'no', 'traffic_sign:left': 'NL:E02'}, [0]), expected={'class': 5, 'subclass': 1501968560})
        self.check_err(n.way(data, {'highway': 'residential', 'parking:lane:left': 'no', 'traffic_sign:left': 'NL:E02'}, [0]), expected={'class': 5, 'subclass': 1501968560})
        self.check_not_err(n.way(data, {'highway': 'residential', 'parking:lane:left': 'parallel', 'traffic_sign:left': 'NL:E02'}, [0]), expected={'class': 5, 'subclass': 1501968560})
        self.check_not_err(n.way(data, {'highway': 'residential', 'parking:condition:both': 'no_stopping', 'parking:lane:both': 'no', 'traffic_sign:left': 'NL:E02', 'traffic_sign:right': 'NL:E02'}, [0]), expected={'class': 5, 'subclass': 1501968560})
        self.check_not_err(n.way(data, {'highway': 'residential', 'name': 'De Visserstraat'}, [0]), expected={'class': 3, 'subclass': 275992542})
        self.check_not_err(n.way(data, {'highway': 'residential', 'name': 'J.T. de Visserstraat'}, [0]), expected={'class': 3, 'subclass': 275992542})
        self.check_not_err(n.way(data, {'highway': 'residential', 'maxspeed:forward': '30', 'traffic_sign:forward': 'NL:A1-30'}, [0]), expected={'class': 7, 'subclass': 678880168})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign:forward': 'NL:A1-30'}, [0]), expected={'class': 7, 'subclass': 678880168})
        self.check_not_err(n.way(data, {'highway': 'residential', 'maxspeed': '30', 'traffic_sign': 'NL:A01-30'}, [0]), expected={'class': 7, 'subclass': 678880168})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign': 'NL:A01-30'}, [0]), expected={'class': 7, 'subclass': 678880168})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign': 'NL:A04-30'}, [0]), expected={'class': 7, 'subclass': 678880168})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign': 'NL:A4'}, [0]), expected={'class': 7, 'subclass': 678880168})
        self.check_not_err(n.way(data, {'highway': 'residential', 'maxspeed:advisory:both_ways': '50', 'traffic_sign': 'NL:A4[50]'}, [0]), expected={'class': 7, 'subclass': 678880168})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign': 'NL:A4[60]'}, [0]), expected={'class': 7, 'subclass': 678880168})
