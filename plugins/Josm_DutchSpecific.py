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
        self.errors[90201] = self.def_class(item = 9020, level = 3, tags = [], title = mapcss.tr('NL addresses and contacts'))
        self.errors[90202] = self.def_class(item = 9020, level = 3, tags = [], title = mapcss.tr('NL deprecated features'))
        self.errors[90203] = self.def_class(item = 9020, level = 3, tags = [], title = mapcss.tr('NL nomenclature'))
        self.errors[90204] = self.def_class(item = 9020, level = 3, tags = [], title = mapcss.tr('NL heritage'))
        self.errors[90205] = self.def_class(item = 9020, level = 3, tags = [], title = mapcss.tr('NL traffic signs'))
        self.errors[90206] = self.def_class(item = 9020, level = 3, tags = [], title = mapcss.tr('NL German style tagging'))
        self.errors[90207] = self.def_class(item = 9020, level = 3, tags = [], title = mapcss.tr('NL speed limits'))
        self.errors[90208] = self.def_class(item = 9020, level = 3, tags = [], title = mapcss.tr('NL mofa tagging'))
        self.errors[90209] = self.def_class(item = 9020, level = 3, tags = [], title = mapcss.tr('NL unusual values'))

        self.re_011bedaa = re.compile(r'^hgv(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_033b234a = re.compile(r'^bicycle(:forward|:both_ways)?(:conditional)?$')
        self.re_0660931d = re.compile(r'(?i)(oplaad|laadpunt|laadpaal)')
        self.re_06bae8ee = re.compile(r'^maxspeed:advisory(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_06ddeafa = re.compile(r'\bbouwweg')
        self.re_076895f4 = re.compile(r'payment:O[vV][-_]?[cC]hipkaart')
        self.re_08935e4d = re.compile(r'^maxspeed:advisory(:forward|:both_ways)?(:conditional)?$')
        self.re_08ba1dfb = re.compile(r'(^|; ?)NL:C18\b')
        self.re_08f9030c = re.compile(r'(^|; ?)NL:L301\b')
        self.re_0abf5cfa = re.compile(r'(^|; ?)NL:C21\b')
        self.re_0c61efa0 = re.compile(r'^maxlength(:backward|:both_ways)?(:conditional)?$')
        self.re_0cbcfeaf = re.compile(r'^maxspeed(:forward|:both_ways)?(:conditional)?$')
        self.re_0e042431 = re.compile(r'^hazmat(:[A-E])?(:forward|:both_ways)?(:conditional)?$')
        self.re_0e900094 = re.compile(r'(^|; ?)NL:C17\b')
        self.re_0ec6b360 = re.compile(r'(?i)^speeltuin(tje)?$')
        self.re_0f9e3c59 = re.compile(r'^foot(:forward|:both_ways)?(:conditional)?$')
        self.re_110c89a2 = re.compile(r'(^|; ?)mofa(;|$)')
        self.re_143f11c5 = re.compile(r'^(no|use_sidepath)$')
        self.re_1582ff37 = re.compile(r'(?i)bus\s?(baan|strook)')
        self.re_1705b261 = re.compile(r'(?i)(^|\sen\s)((on)?verplicht\s)?(\(?brom\)?)?fietspad$')
        self.re_18c8cfbe = re.compile(r'^(container|houseboat|static_caravan)$')
        self.re_19b1af6a = re.compile(r'^paving_stones:([1-9])0$')
        self.re_1aa298e1 = re.compile(r'^maxheight(:backward|:both_ways)?(:conditional)?$')
        self.re_1cc9227a = re.compile(r'^maxspeed(:backward|:both_ways)?(:conditional)?$')
        self.re_1cfba619 = re.compile(r'^(access|vehicle|motor_vehicle)(:forward|:both_ways)?(:conditional)?$')
        self.re_1d0c9a01 = re.compile(r'^NL:zone[36]0$')
        self.re_1d478f9e = re.compile(r'\bNL:C0?2\b')
        self.re_1d614d5c = re.compile(r'^maxspeed(:forward|:backward|:both_ways)?$')
        self.re_1e92c009 = re.compile(r'^(path|cycleway|pedestrian|bridleway|steps)$')
        self.re_1faa7e13 = re.compile(r'^hgv(:forward|:both_ways)?(:conditional)?$')
        self.re_21dc697e = re.compile(r'^maxaxleload(:backward|:both_ways)?(:conditional)?$')
        self.re_229e1925 = re.compile(r'^hazmat(:[A-E])?(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_2441139b = re.compile(r'(?i)\b(aansl|empl|goed|ind|inhaalsp|opstel|overloopw|racc|rang|terr)\b')
        self.re_251abd6a = re.compile(r'^(residential|unclassified|tertiary|secondary|primary|trunk|motorway|busway)(_link)?$')
        self.re_252a5d6c = re.compile(r'forward')
        self.re_26516863 = re.compile(r'.:covid19$')
        self.re_26ae994a = re.compile(r'^motorcycle(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_26e04b1e = re.compile(r'\b(([Aa]f)?gesloten|[Gg]eopend)\b')
        self.re_2823d45d = re.compile(r'^maxlength(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_287f5dd8 = re.compile(r'^(\+|00)31 ?0?( ?[0-9]){3,6}$')
        self.re_293c2706 = re.compile(r'^[A-Z][a-z]{1,4}\. ')
        self.re_2cd26805 = re.compile(r'^maxlength(:forward|:both_ways)?(:conditional)?$')
        self.re_2f938f56 = re.compile(r'^(Adr|Anth?|Chr?|Corn|Fred|Hub|Jacq?|Joh|Jos|Mac|Nic|Ph|Th)\.')
        self.re_30fdb33a = re.compile(r'(?i)^(lift)$')
        self.re_31154585 = re.compile(r'^motorcycle(:forward|:both_ways)?(:conditional)?$')
        self.re_3254c1c6 = re.compile(r'(?i)(parkeren$|parkeerplaats$|^toegang(sweg)?\s|^richting\s|drive.thro?u(gh)?)')
        self.re_32d334cf = re.compile(r'(^|.+:)addr:street($|:.+)')
        self.re_33480e64 = re.compile(r'^maxheight(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_334bd9c9 = re.compile(r'\bhout|\bmetaal\b|^beton$|^brons$|steen\b|ijzer\b|staal\b')
        self.re_339dfcbd = re.compile(r'^maxweight(:backward|:both_ways)?(:conditional)?$')
        self.re_33af5199 = re.compile(r'^motorcycle(:backward|:both_ways)?(:conditional)?$')
        self.re_33fbfa8d = re.compile(r'(?i)post\W?nl$')
        self.re_345ec50a = re.compile(r'^maxweight(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_374703cf = re.compile(r'^(access|vehicle|motor_vehicle)(:backward|:both_ways)?(:conditional)?$')
        self.re_3894ceb2 = re.compile(r'^oneway:')
        self.re_39064d44 = re.compile(r'^(motorway(_link)?|trunk(_link)?|cycleway|service|busway|construction|proposed|raceway)$')
        self.re_3b2cb1d7 = re.compile(r'(?i)(uit?laa[dt]|honden.*wandel|los.?loop)')
        self.re_3bd9d067 = re.compile(r'^(yes|-?1)$')
        self.re_3c163648 = re.compile(r'(?i)ball?(veld(je)?)?$')
        self.re_3cd0133e = re.compile(r'^access(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_3da90af7 = re.compile(r'(^|; ?)rce(;|$)')
        self.re_4065f95d = re.compile(r'(^|; ?)NL:(C19|L0?1)\b')
        self.re_42dce20e = re.compile(r'^(no|0)*$')
        self.re_44720f99 = re.compile(r'(?i)^roltrap(pen)?$')
        self.re_4547b418 = re.compile(r'(^|; ?)NL:A0?1-')
        self.re_460900e8 = re.compile(r'^maxspeed:advisory(:backward|:both_ways)?(:conditional)?$')
        self.re_467ce1ba = re.compile(r'(?i)(parkeren|parkeerplaats|parkeergarage|^garage)$')
        self.re_47aaa0f7 = re.compile(r'^(yes|designated)$')
        self.re_49026388 = re.compile(r'(^|.+:)addr:housenumber($|:.+)')
        self.re_4cfe628c = re.compile(r'^access(:forward|:both_ways)?(:conditional)?$')
        self.re_4d17a717 = re.compile(r'^(no|-1|0)*$')
        self.re_4d87e9ab = re.compile(r'^access(:backward|:both_ways)?(:conditional)?$')
        self.re_4e099629 = re.compile(r'^trailer(:forward|:both_ways)?(:conditional)?$')
        self.re_4e4468f8 = re.compile(r'^foot(:backward|:both_ways)?(:conditional)?$')
        self.re_5012755c = re.compile(r'^priority:.')
        self.re_51f98600 = re.compile(r'^yes$')
        self.re_53816e1a = re.compile(r'^maxwidth(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_543ffeee = re.compile(r'(?i)(rolstoel|invaliden)')
        self.re_54b75cfc = re.compile(r'^maxwidth(:forward|:both_ways)?(:conditional)?$')
        self.re_54e14d8c = re.compile(r'(?i)^wadi$')
        self.re_550ffc74 = re.compile(r'^building(:part)?$')
        self.re_556f4d08 = re.compile(r'^maxweight(:forward|:both_ways)?(:conditional)?$')
        self.re_5577fcc2 = re.compile(r'^hgv(:backward|:both_ways)?(:conditional)?$')
        self.re_5578cc63 = re.compile(r'100.+19:00')
        self.re_561be3ff = re.compile(r'^addr:(city|postcode)$')
        self.re_594405dc = re.compile(r'^(00|\+)31 ?0( ?[0-9]){7,}')
        self.re_59aca94c = re.compile(r'(^|; ?)NL:C20\b')
        self.re_5a895116 = re.compile(r'(^|; ?)NL:A0?4\b')
        self.re_5b4448e5 = re.compile(r'(?i)^(honden\s?)?(toilet|uitlaa[dt]|los.?loop)')
        self.re_5e498788 = re.compile(r'^(left|right|both|yes)$')
        self.re_5ef8db88 = re.compile(r'^addr:(street|housenumber|postcode|city)$')
        self.re_5f5aa10b = re.compile(r'^footway(:left|:right|:both)?:')
        self.re_5f649d1b = re.compile(r'\bNL:(C0?1|C0?9|C14|C15|D103|D104)\b')
        self.re_5fbb635f = re.compile(r'[1-9]$')
        self.re_617e36ee = re.compile(r'^hazmat(:[A-E])?(:backward|:both_ways)?(:conditional)?$')
        self.re_619cd3d8 = re.compile(r'(^|; ?)NL:C22(\[[A-E]\])?(;|$)')
        self.re_6211f625 = re.compile(r'(?i)(voormalige?)')
        self.re_62e192cf = re.compile(r'^(motorway(_link)?|construction|proposed)$')
        self.re_63f5f8f1 = re.compile(r'^maxheight(:forward|:both_ways)?(:conditional)?$')
        self.re_640dd184 = re.compile(r'^trailer(:backward|:both_ways)?(:conditional)?$')
        self.re_6454d3f5 = re.compile(r'stenen$|^hout$|\bbestraa?t(ing)?$|grond$|^puin$|^grind$|zand$')
        self.re_6460cbf8 = re.compile(r'^(trunk|motorway|busway|path|busway|bridleway|footway|pedestrian)(_link)?$')
        self.re_6708cc9b = re.compile(r'(; ?|^)([0-9]{0,3}[1-9]|[0-9]{0,2}[1-9][0-9]|[0-9]?[1-9][0-9]{2})[0-9]{12}($|;)')
        self.re_676d2c9e = re.compile(r'\b(Adm|Br|Burg|Cmdt|Dr|Drs|Ds|Gebr|Gen|Ing|Ir|Jhr|Kard|Kon|Luit|Mej|Mevr|Mgr|Min|Mr|Past|Pr|Pres|Prof|St|Vr|Weth|Zr)\.? [A-Za-z]')
        self.re_682234cc = re.compile(r'^foot(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_68a71d57 = re.compile(r'backward')
        self.re_697de1f2 = re.compile(r'^moped(:forward|:both_ways)?(:conditional)?$')
        self.re_6b1906aa = re.compile(r'(?i)(klanten|bezoek(ers)?|medewerkers)\b')
        self.re_6b8a2885 = re.compile(r'^bicycle(:backward|:both_ways)?(:conditional)?$')
        self.re_6cd83c9e = re.compile(r'(?i)^gratis\s|gratis\)')
        self.re_6e264741 = re.compile(r'(?i)^(Geldmaat|ABN.?AMRO|ING|Rabobank|SNS)\b')
        self.re_7087ae0d = re.compile(r'^trailer(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_70e165b6 = re.compile(r'^(access|vehicle|motor_vehicle)(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_7184e9bc = re.compile(r'^sidewalk:(left|right|both)$')
        self.re_71a0b33c = re.compile(r'(?i)(drinkwater|\swater|kraan)')
        self.re_736e42c8 = re.compile(r'^(path|cycleway|bridleway)$')
        self.re_7372291c = re.compile(r'^bicycle(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_73ea17b1 = re.compile(r'^moped(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_745836a5 = re.compile(r'^(brand|name|operator)$')
        self.re_74d217a6 = re.compile(r'^(path|cycleway|bridleway|footway|living_street)$')
        self.re_74d9b833 = re.compile(r'^(.+):surface$')
        self.re_7531ba03 = re.compile(r'^maxaxleload(:forward|:both_ways)?(:conditional)?$')
        self.re_7537ca1e = re.compile(r'\bNL:G0?7\b')
        self.re_75b7dc3e = re.compile(r'^oneway:hazmat')
        self.re_774d1ba2 = re.compile(r'^maxwidth(:backward|:both_ways)?(:conditional)?$')
        self.re_78809448 = re.compile(r'^moped(:backward|:both_ways)?(:conditional)?$')
        self.re_798edef1 = re.compile(r'(?i)(aansl|empl|goed|ind|inhaalsp|opstel|overloopw|racc|rang|terr)\.')
        self.re_7acb98bb = re.compile(r'^maxspeed(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_7be1bafc = re.compile(r'^1[23]0$')
        self.re_7c3d18b2 = re.compile(r'^(0031|\+31|0) ?[1-9]( ?[0-9]){11}')
        self.re_7d72e705 = re.compile(r'^maxaxleload(:forward|:backward|:both_ways)?(:conditional)?$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_abbrname = set_addrOnBuilding = set_altLivingStreet = set_badPhoneNumber = set_completedSurfacePavingStonesNumber = set_hasAddMofaPositive = set_housenameWithFix = set_markedSteps = set_multipleGsigns = set_stepsWithBicycleRamp = False

        # node[traffic_sign~="NL:L2"][crossing!=zebra][crossing!=uncontrolled][crossing!=marked][highway=crossing][crossing!=traffic_signals][crossing_ref!=zebra]
        # node[traffic_sign~="NL:L02"][crossing!=zebra][crossing!=uncontrolled][crossing!=marked][highway=crossing][crossing!=traffic_signals][crossing_ref!=zebra]
        if ('highway' in keys and 'traffic_sign' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.list_contains(mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 0, 'NL:L2'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'crossing') != mapcss._value_const_capture(capture_tags, 1, 'zebra', 'zebra')) and (mapcss._tag_capture(capture_tags, 2, tags, 'crossing') != mapcss._value_const_capture(capture_tags, 2, 'uncontrolled', 'uncontrolled')) and (mapcss._tag_capture(capture_tags, 3, tags, 'crossing') != mapcss._value_const_capture(capture_tags, 3, 'marked', 'marked')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') == mapcss._value_capture(capture_tags, 4, 'crossing')) and (mapcss._tag_capture(capture_tags, 5, tags, 'crossing') != mapcss._value_const_capture(capture_tags, 5, 'traffic_signals', 'traffic_signals')) and (mapcss._tag_capture(capture_tags, 6, tags, 'crossing_ref') != mapcss._value_const_capture(capture_tags, 6, 'zebra', 'zebra')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.list_contains(mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 0, 'NL:L02'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'crossing') != mapcss._value_const_capture(capture_tags, 1, 'zebra', 'zebra')) and (mapcss._tag_capture(capture_tags, 2, tags, 'crossing') != mapcss._value_const_capture(capture_tags, 2, 'uncontrolled', 'uncontrolled')) and (mapcss._tag_capture(capture_tags, 3, tags, 'crossing') != mapcss._value_const_capture(capture_tags, 3, 'marked', 'marked')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') == mapcss._value_capture(capture_tags, 4, 'crossing')) and (mapcss._tag_capture(capture_tags, 5, tags, 'crossing') != mapcss._value_const_capture(capture_tags, 5, 'traffic_signals', 'traffic_signals')) and (mapcss._tag_capture(capture_tags, 6, tags, 'crossing_ref') != mapcss._value_const_capture(capture_tags, 6, 'zebra', 'zebra')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} without {1}, {2} or {3}","{0.tag}","{1.tag}","{2.tag} + crossing_ref=zebra","{3.tag} + crossing_ref=zebra")
                # assertNoMatch:"node traffic_sign=NL:L02 highway=crossing crossing=traffic_signals note=traffic_signals_combined_with_zebra"
                # assertMatch:"node traffic_sign=NL:L02;NL:J23 highway=crossing"
                # assertNoMatch:"node traffic_sign=NL:L2 direction=300"
                # assertNoMatch:"node traffic_sign=NL:L2 highway=crossing crossing=uncontrolled crossing_ref=zebra"
                # assertMatch:"node traffic_sign=NL:L2 highway=crossing"
                err.append({'class': 90205, 'subclass': 938076772, 'text': mapcss.tr('{0} without {1}, {2} or {3}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag} + crossing_ref=zebra'), mapcss._tag_uncapture(capture_tags, '{3.tag} + crossing_ref=zebra'))})

        # *[contact:phone=~/^(00|\+)31 ?0( ?[0-9]){7,}/]
        # *[contact:mobile=~/^(00|\+)31 ?0( ?[0-9]){7,}/]
        # *[contact:whatsapp=~/^(00|\+)31 ?0( ?[0-9]){7,}/]
        # *[phone=~/^(00|\+)31 ?0( ?[0-9]){7,}/]
        if ('contact:mobile' in keys) or ('contact:phone' in keys) or ('contact:whatsapp' in keys) or ('phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_594405dc), mapcss._tag_capture(capture_tags, 0, tags, 'contact:phone'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_594405dc), mapcss._tag_capture(capture_tags, 0, tags, 'contact:mobile'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_594405dc), mapcss._tag_capture(capture_tags, 0, tags, 'contact:whatsapp'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_594405dc), mapcss._tag_capture(capture_tags, 0, tags, 'phone'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .badPhoneNumber
                # group:tr("NL addresses and contacts")
                # throwWarning:tr("Invalid tag {0}: country code should not be followed by a 0","{0.key}")
                # assertMatch:"node phone=\"+31 06 1234 5678\""
                # assertMatch:"node phone=\"+31 0612345678\""
                # assertMatch:"node phone=\"+31 08008844\""
                # assertNoMatch:"node phone=\"+31 6 1234 5678\""
                # assertNoMatch:"node phone=\"+31 612345678\""
                # assertMatch:"node phone=\"00310612345678\""
                # assertNoMatch:"node phone=\"0031612345678\""
                # assertNoMatch:"node phone=\"06 12 34 56 78\""
                # assertNoMatch:"node phone=\"0612345678\""
                set_badPhoneNumber = True
                err.append({'class': 90201, 'subclass': 1739574763, 'text': mapcss.tr('Invalid tag {0}: country code should not be followed by a 0', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[contact:phone=~/^(\+|00)31 ?0?( ?[0-9]){3,6}$/]
        # *[contact:mobile=~/^(\+|00)31 ?0?( ?[0-9]){3,6}$/]
        # *[phone=~/^(\+|00)31 ?0?( ?[0-9]){3,6}$/]
        if ('contact:mobile' in keys) or ('contact:phone' in keys) or ('phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_287f5dd8), mapcss._tag_capture(capture_tags, 0, tags, 'contact:phone'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_287f5dd8), mapcss._tag_capture(capture_tags, 0, tags, 'contact:mobile'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_287f5dd8), mapcss._tag_capture(capture_tags, 0, tags, 'phone'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .badPhoneNumber
                # group:tr("NL addresses and contacts")
                # throwWarning:tr("Invalid tag {0}: short phone numbers cannot be used with international prefix (or: wrong phone number length)","{0.key}")
                # assertMatch:"node phone=\"+31 14 0245\""
                # assertMatch:"node phone=\"+31 140245\""
                # assertNoMatch:"node phone=\"+31 800 8844\""
                # assertMatch:"node phone=\"+3114024\""
                # assertNoMatch:"node phone=\"+318008844\""
                # assertMatch:"node phone=\"0031140245\""
                # assertNoMatch:"node phone=\"0031612345678\""
                # assertNoMatch:"node phone=\"00318008844\""
                # assertNoMatch:"node phone=\"0612345678\""
                # assertNoMatch:"node phone=\"0800 8844\""
                # assertNoMatch:"node phone=\"08008844\""
                # assertNoMatch:"node phone=\"14024\""
                # assertNoMatch:"node phone=\"140245\""
                set_badPhoneNumber = True
                err.append({'class': 90201, 'subclass': 345342642, 'text': mapcss.tr('Invalid tag {0}: short phone numbers cannot be used with international prefix (or: wrong phone number length)', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[contact:phone=~/^(0031|\+31|0) ?[1-9]( ?[0-9]){11}/][inside("NL")]!.badPhoneNumber
        # *[contact:mobile=~/^(0031|\+31|0) ?[1-9]( ?[0-9]){11}/][inside("NL")]!.badPhoneNumber
        # *[contact:whatsapp=~/^(0031|\+31|0) ?[1-9]( ?[0-9]){11}/][inside("NL")]!.badPhoneNumber
        # *[phone=~/^(0031|\+31|0) ?[1-9]( ?[0-9]){11}/][inside("NL")]!.badPhoneNumber
        if ('contact:mobile' in keys) or ('contact:phone' in keys) or ('contact:whatsapp' in keys) or ('phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_badPhoneNumber) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_7c3d18b2), mapcss._tag_capture(capture_tags, 0, tags, 'contact:phone'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_badPhoneNumber) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_7c3d18b2), mapcss._tag_capture(capture_tags, 0, tags, 'contact:mobile'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_badPhoneNumber) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_7c3d18b2), mapcss._tag_capture(capture_tags, 0, tags, 'contact:whatsapp'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_badPhoneNumber) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_7c3d18b2), mapcss._tag_capture(capture_tags, 0, tags, 'phone'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL addresses and contacts")
                # throwWarning:tr("Invalid tag {0}: too many digits (or foreign number, if so: ignore)","{0.key}")
                # assertNoMatch:"node contact:mobile=\"097 123456789\""
                # assertNoMatch:"node contact:whatsapp=\"+31 97 1234 567 89\""
                # assertNoMatch:"node contact:whatsapp=\"+3197 123456789\""
                # assertNoMatch:"node phone=\"+31 6 1234 5678\""
                # assertNoMatch:"node phone=\"+31 6 12345678\""
                # assertNoMatch:"node phone=\"0031612345678\""
                # assertNoMatch:"node phone=\"06 12345678\""
                # assertNoMatch:"node phone=\"0800 1234567\""
                err.append({'class': 90201, 'subclass': 50270752, 'text': mapcss.tr('Invalid tag {0}: too many digits (or foreign number, if so: ignore)', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # node[/^addr:(city|postcode)$/][!/(^|.+:)addr:housenumber($|:.+)/][!/(^|.+:)addr:street($|:.+)/][inside("NL")]
        # node[addr:street][!/(^|.+:)addr:housenumber($|:.+)/][!addr:interpolation][!addr:flats][inside("NL")]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_561be3ff)) and (not mapcss._tag_capture(capture_tags, 1, tags, self.re_49026388)) and (not mapcss._tag_capture(capture_tags, 2, tags, self.re_32d334cf)) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'addr:street')) and (not mapcss._tag_capture(capture_tags, 1, tags, self.re_49026388)) and (not mapcss._tag_capture(capture_tags, 2, tags, 'addr:interpolation')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'addr:flats')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL addresses and contacts")
                # throwWarning:tr("Incomplete address: {0} {1} {2} {3}",any(tag("addr:street"),"[street?]"),any(tag("addr:housenumber"),"[housenumber?]"),any(tag("addr:postcode"),""),any(tag("addr:city"),""))
                # assertNoMatch:"node addr:street=\"Pastoor Simonisplein\" addr:housenumber=2a addr:city=Milheeze amenity=atm"
                # assertNoMatch:"node addr:street=Ozingaloane addr:housenumber=1W-5 addr:city=Marrum power=generator"
                # assertNoMatch:"node addr:street=XXX addr:flats=1-3 addr:postcode=1234AB addr:city=XXX"
                # assertNoMatch:"node addr:street=XXX addr:housenumber:construction=123 addr:postcode=1234AB addr:city=XXX"
                # assertNoMatch:"node addr:street=XXX addr:housenumber=123 addr:postcode=1234AB addr:city=XXX"
                # assertNoMatch:"node addr:street=XXX proposed:addr:housenumber=123 addr:postcode=1234AB addr:city=XXX"
                err.append({'class': 90201, 'subclass': 509151640, 'text': mapcss.tr('Incomplete address: {0} {1} {2} {3}', mapcss.any_(mapcss.tag(tags, 'addr:street'), '[street?]'), mapcss.any_(mapcss.tag(tags, 'addr:housenumber'), '[housenumber?]'), mapcss.any_(mapcss.tag(tags, 'addr:postcode'), ''), mapcss.any_(mapcss.tag(tags, 'addr:city'), ''))})

        # node["addr:postcode"]["addr:postcode"!~/[0-9]{4} ?[A-Z]{2}/][inside("NL")]
        # Rule Blacklisted (id: 1560886491)

        # *[addr:interpolation][inside("NL")]
        if ('addr:interpolation' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'addr:interpolation')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("Adressen ({0}) worden in Nederland individueel geïmporteerd uit de BAG","{0.key}")
                # suggestAlternative:"meerdere addr:housenumber via een BAG importverzoek"
                err.append({'class': 90202, 'subclass': 864819394, 'text': mapcss.tr('Adressen ({0}) worden in Nederland individueel geïmporteerd uit de BAG', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

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
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 90202, 'subclass': 788111375, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
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
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"payment:ov-chipkaart"
                # fixChangeKey:"{0.key}=>payment:ov-chipkaart"
                err.append({'class': 90202, 'subclass': 1555838972, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [(mapcss._tag_uncapture(capture_tags, '{0.key}=>payment:ov-chipkaart')).split('=>', 1)[1].strip(), mapcss.tag(tags, (mapcss._tag_uncapture(capture_tags, '{0.key}=>payment:ov-chipkaart')).split('=>', 1)[0].strip())]]),
                    '-': ([
                    (mapcss._tag_uncapture(capture_tags, '{0.key}=>payment:ov-chipkaart')).split('=>', 1)[0].strip()])
                }})

        # *[/.:covid19$/][inside("NL")]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_26516863)) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("There are no active covid-19 restrictions at the moment. Remove {0}.","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 90202, 'subclass': 1496260396, 'text': mapcss.tr('There are no active covid-19 restrictions at the moment. Remove {0}.', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[material][material=~/\bhout|\bmetaal\b|^beton$|^brons$|steen\b|ijzer\b|staal\b/]
        if ('material' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'material')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_334bd9c9), mapcss._tag_capture(capture_tags, 1, tags, 'material'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("unusual value of {0}","{0.key}")
                # assertMatch:"node tourism=artwork material=brons"
                # assertMatch:"node tourism=artwork material=hout,metaal"
                err.append({'class': 90202, 'subclass': 1686750599, 'text': mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[surface][surface=~/^paving_stones:([1-9])0$/][inside("NL")]
        if ('surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'surface')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_19b1af6a), mapcss._tag_capture(capture_tags, 1, tags, 'surface'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"surface=paving_stones + paving_stones:shape=square + paving_stones:length=[length in meter, e.g. 0.3]"
                # fixAdd:concat("paving_stones:length=0.",get(regexp_match("^paving_stones:([1-9])0$",tag("surface")),1))
                # fixAdd:"paving_stones:shape=square"
                # fixAdd:"surface=paving_stones"
                err.append({'class': 90202, 'subclass': 1868473171, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('paving_stones:length=0.', mapcss.get(mapcss.regexp_match(self.re_19b1af6a, mapcss.tag(tags, 'surface')), 1))).split('=', 1),
                    ['paving_stones:shape','square'],
                    ['surface','paving_stones']])
                }})

        # *[/^(.+):surface$/][/^(.+):surface$/=~/^paving_stones:([1-9])0$/][count(tag_regex("^(.+):surface$"))==1][inside("NL")]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_74d9b833)) and (mapcss.regexp_test(self.re_19b1af6a, mapcss._match_regex(tags, self.re_74d9b833))) and (mapcss.count(mapcss.tag_regex(tags, self.re_74d9b833)) == 1) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # set .completedSurfacePavingStonesNumber
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"*:surface=paving_stones + *:paving_stones:shape=square + *:paving_stones:length=[length in meter, e.g. 0.3]"
                set_completedSurfacePavingStonesNumber = True
                err.append({'class': 90202, 'subclass': 1911834456, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[/^(.+):surface$/=~/^paving_stones:([1-9])0$/][inside("NL")]!.completedSurfacePavingStonesNumber
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_completedSurfacePavingStonesNumber) and (mapcss.regexp_test(self.re_19b1af6a, mapcss._match_regex(tags, self.re_74d9b833))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","*:surface=paving_stones:NN")
                # suggestAlternative:"*:surface=paving_stones + *:paving_stones:shape=square + *:paving_stones:length=[length in meter, e.g. 0.3]"
                err.append({'class': 90202, 'subclass': 1665978272, 'text': mapcss.tr('{0} is deprecated', '*:surface=paving_stones:NN')})

        # *[winkelnummer]
        if ('winkelnummer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'winkelnummer')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"ref=*"
                err.append({'class': 90202, 'subclass': 340349535, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # node[opening_hours="24/7"][amenity=atm][/^(brand|name|operator)$/=~/(?i)^(Geldmaat|ABN.?AMRO|ING|Rabobank|SNS)\b/][inside("NL")]
        if ('amenity' in keys and 'opening_hours' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'opening_hours') == mapcss._value_capture(capture_tags, 0, '24/7')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity') == mapcss._value_capture(capture_tags, 1, 'atm')) and (mapcss.regexp_test(self.re_6e264741, mapcss._match_regex(tags, self.re_745836a5))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL unusual values")
                # throwWarning:tr("{0} op {1} is onwaarschijnlijk, Geldmaten zijn niet de hele nacht geopend","{0.tag}","{1.tag}")
                err.append({'class': 90209, 'subclass': 1466427444, 'text': mapcss.tr('{0} op {1} is onwaarschijnlijk, Geldmaten zijn niet de hele nacht geopend', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # node[vehicle=designated][!amenity][!vehicle:conditional][inside("NL")]
        # node[motor_vehicle=designated][!amenity][!motor_vehicle:conditional][inside("NL")]
        if ('motor_vehicle' in keys) or ('vehicle' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'vehicle') == mapcss._value_capture(capture_tags, 0, 'designated')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'amenity')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'vehicle:conditional')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'motor_vehicle') == mapcss._value_capture(capture_tags, 0, 'designated')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'amenity')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motor_vehicle:conditional')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL unusual values")
                # throwWarning:tr("{0} on a node, such a traffic sign does not exist. Possibly a typo for destination?","{0.tag}")
                # suggestAlternative:"{0.key}=destination"
                # suggestAlternative:"{0.key}=yes"
                # assertNoMatch:"node motor_vehicle=designated amenity=charging_station"
                # assertNoMatch:"node motor_vehicle=designated amenity=parking_entrance"
                err.append({'class': 90209, 'subclass': 1720314934, 'text': mapcss.tr('{0} on a node, such a traffic sign does not exist. Possibly a typo for destination?', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # node[natural=tree][circumference][siunit_length(tag("circumference"))>10.32][siunit_length(tag("circumference"))<=45][inside("NL")]
        # node[natural=tree][height][siunit_length(tag("height"))>61.32][inside("NL")]
        if ('circumference' in keys and 'natural' in keys) or ('height' in keys and 'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'tree')) and (mapcss._tag_capture(capture_tags, 1, tags, 'circumference')) and (mapcss.siunit_length(mapcss.tag(tags, 'circumference')) > 10.32) and (mapcss.siunit_length(mapcss.tag(tags, 'circumference')) <= 45) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'tree')) and (mapcss._tag_capture(capture_tags, 1, tags, 'height')) and (mapcss.siunit_length(mapcss.tag(tags, 'height')) > 61.32) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL unusual values")
                # throwWarning:tr("Unusually large value of {0} ({1} m), did you mean `{1} cm` or `{1} mm`?","{1.key}",siunit_length("{1.value}"))
                # assertNoMatch:"node natural=tree circumference=8.6"
                # assertNoMatch:"node natural=tree height=\"288 cm\""
                # assertNoMatch:"node natural=tree height=51"
                err.append({'class': 90209, 'subclass': 68044720, 'text': mapcss.tr('Unusually large value of {0} ({1} m), did you mean `{1} cm` or `{1} mm`?', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss.siunit_length(mapcss._tag_uncapture(capture_tags, '{1.value}')))})

        # *[ref:bag][ref:bag!~/(; ?|^)([0-9]{0,3}[1-9]|[0-9]{0,2}[1-9][0-9]|[0-9]?[1-9][0-9]{2})[0-9]{12}($|;)/][inside("NL")]
        if ('ref:bag' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:bag')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_6708cc9b, '(; ?|^)([0-9]{0,3}[1-9]|[0-9]{0,2}[1-9][0-9]|[0-9]?[1-9][0-9]{2})[0-9]{12}($|;)'), mapcss._tag_capture(capture_tags, 1, tags, 'ref:bag'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL unusual values")
                # throwWarning:tr("Invalid value of {0}","{0.key}")
                err.append({'class': 90209, 'subclass': 2021092431, 'text': mapcss.tr('Invalid value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[leisure][surface=gravel][sport~="tennis"][inside("NL")]
        if ('leisure' in keys and 'sport' in keys and 'surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure')) and (mapcss._tag_capture(capture_tags, 1, tags, 'surface') == mapcss._value_capture(capture_tags, 1, 'gravel')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 2, tags, 'sport'), mapcss._value_capture(capture_tags, 2, 'tennis'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL unusual values")
                # throwWarning:tr("unusual value of {0} for {1} (`gravel` in English means `grind` in Dutch)","{1.key}","{2.tag}")
                # suggestAlternative:"surface=clay"
                err.append({'class': 90209, 'subclass': 1521090750, 'text': mapcss.tr('unusual value of {0} for {1} (`gravel` in English means `grind` in Dutch)', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # node[name][highway][name=~/(?i)^(lift)$/]
        # node[name][amenity=drinking_water][name=~/(?i)(drinkwater|\swater|kraan)/]
        # node[name][amenity=charging_station][name=~/(?i)(oplaad|laadpunt|laadpaal)/]
        # *[name][name="ijsbaan"]
        # *[name][name=~/\b(([Aa]f)?gesloten|[Gg]eopend)\b/]
        # *[name][amenity^=parking][name=~/(?i)(parkeren|parkeerplaats|parkeergarage|^garage)$/]
        # *[name][name=~/(?i)^gratis\s|gratis\)/]
        # *[name][name=~/(?i)(klanten|bezoek(ers)?|medewerkers)\b/][!route]
        # *[name][leisure=playground][name=~/(?i)^speeltuin(tje)?$/]
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
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name') == mapcss._value_capture(capture_tags, 1, 'ijsbaan')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_26e04b1e), mapcss._tag_capture(capture_tags, 1, tags, 'name'))))
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
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'leisure') == mapcss._value_capture(capture_tags, 1, 'playground')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_0ec6b360), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
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
                # assertMatch:"node amenity=drinking_water name=kraanwater"
                # assertMatch:"node amenity=parking_entrance name=\"parkeerplaats voor bezoekers\""
                # assertMatch:"node leisure=pitch name=\"voetbalveld\""
                # assertMatch:"node leisure=playground name=\"Abc (gesloten)\""
                err.append({'class': 90203, 'subclass': 1470133234, 'text': mapcss.tr('descriptive name')})

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
                err.append({'class': 90203, 'subclass': 538711457, 'text': mapcss.tr('descriptive name')})

        # *[name][place][name=~/\b(Adm|Br|Burg|Cmdt|Dr|Drs|Ds|Gebr|Gen|Ing|Ir|Jhr|Kard|Kon|Luit|Mej|Mevr|Mgr|Min|Mr|Past|Pr|Pres|Prof|St|Vr|Weth|Zr)\.? [A-Za-z]/][inside("NL")]!.abbrname
        # *[name][place][name=~/^[A-Z][a-z]{1,4}\. /][name!~/^(Adr|Anth?|Chr?|Corn|Fred|Hub|Jacq?|Joh|Jos|Mac|Nic|Ph|Th)\./][inside("NL")]!.abbrname
        if ('name' in keys and 'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_abbrname) and (mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'place')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_676d2c9e), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_abbrname) and (mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'place')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_293c2706), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_2f938f56, '^(Adr|Anth?|Chr?|Corn|Fred|Hub|Jacq?|Joh|Jos|Mac|Nic|Ph|Th)\\.'), mapcss._tag_capture(capture_tags, 3, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # set .abbrname
                # group:tr("NL nomenclature")
                # throwWarning:tr("Gebiedsnaam met afkorting")
                set_abbrname = True
                err.append({'class': 90203, 'subclass': 1573033356, 'text': mapcss.tr('Gebiedsnaam met afkorting')})

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
                err.append({'class': 90203, 'subclass': 1558593366, 'text': mapcss.tr('Spoorgebied met afgekorte naam')})

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
                err.append({'class': 90203, 'subclass': 1647353731, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}')), 'allow_fix_override': True, 'fix': {
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
                err.append({'class': 90203, 'subclass': 1831362989, 'text': mapcss.tr('Suspected typo in {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['operator','PostNL']])
                }})

        # *[heritage=2][heritage:operator!=rce][heritage:operator!~/(^|; ?)rce(;|$)/][inside("NL")]
        if ('heritage' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'heritage') == mapcss._value_capture(capture_tags, 0, 2)) and (mapcss._tag_capture(capture_tags, 1, tags, 'heritage:operator') != mapcss._value_const_capture(capture_tags, 1, 'rce', 'rce')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_3da90af7, '(^|; ?)rce(;|$)'), mapcss._tag_capture(capture_tags, 2, tags, 'heritage:operator'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL heritage")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.tag}")
                # fixAdd:"heritage:operator=rce"
                # assertNoMatch:"node heritage=2 heritage:operator=\"rce; Stichting ABCDE\""
                err.append({'class': 90204, 'subclass': 675628887, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['heritage:operator','rce']])
                }})

        # *[heritage:operator=rce][!heritage][inside("NL")]
        if ('heritage:operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'heritage:operator') == mapcss._value_capture(capture_tags, 0, 'rce')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'heritage')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL heritage")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}=*")
                # fixAdd:"heritage=2"
                err.append({'class': 90204, 'subclass': 1113141518, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}=*')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['heritage','2']])
                }})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_abbrname = set_addrOnBuilding = set_altLivingStreet = set_badPhoneNumber = set_completedSurfacePavingStonesNumber = set_hasAddMofaPositive = set_housenameWithFix = set_markedSteps = set_multipleGsigns = set_stepsWithBicycleRamp = False

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
                err.append({'class': 90205, 'subclass': 1876831340, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

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
                err.append({'class': 90205, 'subclass': 2100176109, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), 'moped=designated')})

        # way[highway=cycleway][traffic_sign~="NL:G12a"][!mofa]
        if ('highway' in keys and 'traffic_sign' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'cycleway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G12a'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'mofa')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} without {1}","{1.tag}","{2.key}")
                err.append({'class': 90205, 'subclass': 1066589580, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.key}'))})

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
                err.append({'class': 90205, 'subclass': 1059219548, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), 'mofa=no')})

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
                err.append({'class': 90205, 'subclass': 748238486, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.key}=designated')), 'allow_fix_override': True, 'fix': {
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
                err.append({'class': 90205, 'subclass': 1630203133, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # way[highway=steps][traffic_sign=~/(^|; ?)NL:L301\b/]
        if ('highway' in keys and 'traffic_sign' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'steps')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_08f9030c), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .markedSteps
                set_markedSteps = True

        # way[highway=steps][ramp=yes]
        # way[highway=steps][ramp:bicycle=yes]
        if ('highway' in keys and 'ramp' in keys) or ('highway' in keys and 'ramp:bicycle' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'steps')) and (mapcss._tag_capture(capture_tags, 1, tags, 'ramp') == mapcss._value_capture(capture_tags, 1, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'steps')) and (mapcss._tag_capture(capture_tags, 1, tags, 'ramp:bicycle') == mapcss._value_capture(capture_tags, 1, 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # set .stepsWithBicycleRamp
                set_stepsWithBicycleRamp = True

        # way[highway][traffic_sign*="NL:G"][count(split(";NL:G",concat(";",replace(tag("traffic_sign")," ",""))))>2]
        if ('highway' in keys and 'traffic_sign' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.string_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G'))) and (mapcss.count(mapcss.split(';NL:G', mapcss.concat(';', mapcss.replace(mapcss.tag(tags, 'traffic_sign'), ' ', '')))) > 2))
                except mapcss.RuleAbort: pass
            if match:
                # set multipleGsigns
                set_multipleGsigns = True

        # way[living_street=yes][highway][highway!~/^(residential|unclassified|tertiary|secondary|primary|trunk|motorway|busway)(_link)?$/]
        if ('highway' in keys and 'living_street' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'living_street') == mapcss._value_capture(capture_tags, 0, 'yes')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_251abd6a, '^(residential|unclassified|tertiary|secondary|primary|trunk|motorway|busway)(_link)?$'), mapcss._tag_capture(capture_tags, 2, tags, 'highway'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .altLivingStreet
                set_altLivingStreet = True

        # way[highway][traffic_sign~="NL:F13"][highway!=busway][highway!=service][highway!=bus_guideway][highway!=construction]
        # way[highway][traffic_sign~="NL:G5"][highway!=living_street][highway!=construction][highway!=path][highway!=cycleway][highway!=pedestrian][highway!=bridleway][highway!=steps]!.altLivingStreet
        # way[highway][traffic_sign~="NL:G05"][highway!=living_street][highway!=construction][highway!=path][highway!=cycleway][highway!=pedestrian][highway!=bridleway][highway!=steps]!.altLivingStreet
        # way[highway][traffic_sign~="NL:G7"][highway!=footway][highway!=steps][highway!=pedestrian][highway!=construction]!.multipleGsigns
        # way[highway][traffic_sign~="NL:G07"][highway!=footway][highway!=steps][highway!=pedestrian][highway!=construction]!.multipleGsigns
        # way[highway][traffic_sign~="NL:G7-ZB"][highway!=footway][highway!=steps][highway!=pedestrian][highway!=construction]!.multipleGsigns
        # way[highway][traffic_sign~="NL:G07-ZB"][highway!=footway][highway!=steps][highway!=pedestrian][highway!=construction]!.multipleGsigns
        # way[highway][traffic_sign~="NL:G9"][highway!=bridleway][highway!=construction]!.multipleGsigns!.markedSteps
        # way[highway][traffic_sign~="NL:G09"][highway!=bridleway][highway!=construction]!.multipleGsigns!.markedSteps
        # way[highway][traffic_sign~="NL:G11"][highway!=cycleway][highway!=construction]!.multipleGsigns!.markedSteps!.stepsWithBicycleRamp
        # way[highway][traffic_sign~="NL:G12a"][highway!=cycleway][highway!=construction]!.multipleGsigns!.markedSteps
        # way[highway][traffic_sign~="NL:G13"][highway!=cycleway][highway!=construction]!.multipleGsigns!.markedSteps!.stepsWithBicycleRamp
        # way[highway][traffic_sign*="NL:L301"][highway!=steps][highway!=construction][traffic_sign=~/(^|; ?)NL:L301\b/]
        if ('highway' in keys and 'traffic_sign' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:F13'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'busway', 'busway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'service', 'service')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'bus_guideway', 'bus_guideway')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_altLivingStreet) and (mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G5'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'living_street', 'living_street')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'path', 'path')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'cycleway', 'cycleway')) and (mapcss._tag_capture(capture_tags, 6, tags, 'highway') != mapcss._value_const_capture(capture_tags, 6, 'pedestrian', 'pedestrian')) and (mapcss._tag_capture(capture_tags, 7, tags, 'highway') != mapcss._value_const_capture(capture_tags, 7, 'bridleway', 'bridleway')) and (mapcss._tag_capture(capture_tags, 8, tags, 'highway') != mapcss._value_const_capture(capture_tags, 8, 'steps', 'steps')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_altLivingStreet) and (mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G05'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'living_street', 'living_street')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'path', 'path')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'cycleway', 'cycleway')) and (mapcss._tag_capture(capture_tags, 6, tags, 'highway') != mapcss._value_const_capture(capture_tags, 6, 'pedestrian', 'pedestrian')) and (mapcss._tag_capture(capture_tags, 7, tags, 'highway') != mapcss._value_const_capture(capture_tags, 7, 'bridleway', 'bridleway')) and (mapcss._tag_capture(capture_tags, 8, tags, 'highway') != mapcss._value_const_capture(capture_tags, 8, 'steps', 'steps')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_multipleGsigns) and (mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G7'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'footway', 'footway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'steps', 'steps')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'pedestrian', 'pedestrian')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_multipleGsigns) and (mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G07'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'footway', 'footway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'steps', 'steps')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'pedestrian', 'pedestrian')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_multipleGsigns) and (mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G7-ZB'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'footway', 'footway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'steps', 'steps')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'pedestrian', 'pedestrian')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_multipleGsigns) and (mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G07-ZB'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'footway', 'footway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'steps', 'steps')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'pedestrian', 'pedestrian')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_multipleGsigns) and (not set_markedSteps) and (mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G9'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'bridleway', 'bridleway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_multipleGsigns) and (not set_markedSteps) and (mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G09'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'bridleway', 'bridleway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_multipleGsigns) and (not set_markedSteps) and (not set_stepsWithBicycleRamp) and (mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G11'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'cycleway', 'cycleway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_multipleGsigns) and (not set_markedSteps) and (mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G12a'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'cycleway', 'cycleway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_multipleGsigns) and (not set_markedSteps) and (not set_stepsWithBicycleRamp) and (mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G13'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'cycleway', 'cycleway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.string_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:L301'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'steps', 'steps')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 4, self.re_08f9030c), mapcss._tag_capture(capture_tags, 4, tags, 'traffic_sign'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} together with {1}","{1.tag}","{0.tag}")
                # assertMatch:"way highway=cycleway traffic_sign=\"NL:G13; NL:L301-A\""
                # assertNoMatch:"way highway=cycleway traffic_sign=\"NL:J1; NL:G11; NL:G07; OB109\""
                # assertNoMatch:"way highway=cycleway traffic_sign=NL:G11;NL:G07"
                # assertNoMatch:"way highway=cycleway traffic_sign=NL:G11;NL:G07;OB109"
                # assertNoMatch:"way highway=cycleway traffic_sign=NL:G11;OB109;NL:G07"
                # assertNoMatch:"way highway=cycleway traffic_sign=NL:G13"
                # assertMatch:"way highway=cycleway traffic_sign=NL:G13;NL:L301-A"
                # assertMatch:"way highway=cycleway traffic_sign=NL:G7"
                # assertMatch:"way highway=cycleway traffic_sign=NL:G7;OB109"
                # assertNoMatch:"way highway=cycleway traffic_sign=NL:J1;NL:G11;OB109;NL:G07"
                # assertMatch:"way highway=cycleway traffic_sign=NL:J1;NL:G7"
                # assertMatch:"way highway=cycleway traffic_sign=NL:J1;NL:G7;OB109"
                # assertMatch:"way highway=cycleway traffic_sign=NL:L301"
                # assertNoMatch:"way highway=residential traffic_sign=NL:G12;NL:G10"
                # assertMatch:"way highway=residential traffic_sign=NL:G5 living_street=yes"
                # assertNoMatch:"way highway=service traffic_sign=NL:G5 living_street=yes"
                # assertMatch:"way highway=service traffic_sign=NL:G5"
                # assertNoMatch:"way highway=steps traffic_sign=\"NL:G13; NL:L301-B\""
                # assertNoMatch:"way highway=steps traffic_sign=NL:G13 ramp:bicycle=yes"
                # assertNoMatch:"way highway=steps traffic_sign=NL:G13;NL:L301-B"
                err.append({'class': 90205, 'subclass': 932689435, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # way[highway][traffic_sign~="NL:G5"][highway=~/^(path|cycleway|pedestrian|bridleway|steps)$/][moped][moped!~/^(no|use_sidepath)$/]!.altLivingStreet
        # way[highway][traffic_sign~="NL:G05"][highway=~/^(path|cycleway|pedestrian|bridleway|steps)$/][moped][moped!~/^(no|use_sidepath)$/]!.altLivingStreet
        if ('highway' in keys and 'moped' in keys and 'traffic_sign' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_altLivingStreet) and (mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G5'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_1e92c009), mapcss._tag_capture(capture_tags, 2, tags, 'highway'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'moped')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 4, self.re_143f11c5, '^(no|use_sidepath)$'), mapcss._tag_capture(capture_tags, 4, tags, 'moped'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_altLivingStreet) and (mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G05'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_1e92c009), mapcss._tag_capture(capture_tags, 2, tags, 'highway'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'moped')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 4, self.re_143f11c5, '^(no|use_sidepath)$'), mapcss._tag_capture(capture_tags, 4, tags, 'moped'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} together with {1} but without {2}","{1.tag}","{0.tag}","living_street=yes")
                # assertNoMatch:"way highway=cycleway traffic_sign=NL:G05 living_street=yes moped=designated"
                # assertNoMatch:"way highway=cycleway traffic_sign=NL:G05 moped=use_sidepath"
                # assertNoMatch:"way highway=living_street traffic_sign=NL:G05 moped=yes"
                err.append({'class': 90205, 'subclass': 1097965115, 'text': mapcss.tr('{0} together with {1} but without {2}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{0.tag}'), 'living_street=yes')})

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
                err.append({'class': 90205, 'subclass': 1438158018, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), 'cyclestreet=yes')})

        # way[highway][traffic_sign~="NL:C1"][!vehicle][!/^(access|vehicle|motor_vehicle)(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C1"][!vehicle:forward][!/^(access|vehicle|motor_vehicle)(:forward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C1"][!vehicle:backward][!/^(access|vehicle|motor_vehicle)(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway!=yes]
        # way[highway][traffic_sign~="NL:C01"][!vehicle][!/^(access|vehicle|motor_vehicle)(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C01"][!vehicle:forward][!/^(access|vehicle|motor_vehicle)(:forward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C01"][!vehicle:backward][!/^(access|vehicle|motor_vehicle)(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway!=yes]
        # way[highway][traffic_sign~="NL:C6"][!motor_vehicle][!/^(access|vehicle|motor_vehicle)(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C6"][!motor_vehicle:forward][!/^(access|vehicle|motor_vehicle)(:forward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C6"][!motor_vehicle:backward][!/^(access|vehicle|motor_vehicle)(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway!=yes][oneway:motor_vehicle!=yes]
        # way[highway][traffic_sign~="NL:C06"][!motor_vehicle][!/^(access|vehicle|motor_vehicle)(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C06"][!motor_vehicle:forward][!/^(access|vehicle|motor_vehicle)(:forward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C06"][!motor_vehicle:backward][!/^(access|vehicle|motor_vehicle)(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway!=yes][oneway:motor_vehicle!=yes]
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
        # way[highway][traffic_sign~="NL:C12"][!motor_vehicle][!/^(access|vehicle|motor_vehicle)(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C12"][!motor_vehicle:forward][!/^(access|vehicle|motor_vehicle)(:forward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C12"][!motor_vehicle:backward][!/^(access|vehicle|motor_vehicle)(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway!=yes][oneway:motor_vehicle!=yes]
        # way[highway][traffic_sign~="NL:C13"][!moped][!/^moped(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction][highway!=footway]
        # way[highway][traffic_sign:forward~="NL:C13"][!moped:forward][!/^moped(:forward|:both_ways)?(:conditional)?$/][highway!=construction][highway!=footway]
        # way[highway][traffic_sign:backward~="NL:C13"][!moped:backward][!/^moped(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway:moped!=yes][highway!=footway]
        # way[highway][traffic_sign~="NL:C14"][!bicycle][!/^bicycle(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction][highway!=footway]
        # way[highway][traffic_sign:forward~="NL:C14"][!bicycle:forward][!/^bicycle(:forward|:both_ways)?(:conditional)?$/][highway!=construction][highway!=footway]
        # way[highway][traffic_sign:backward~="NL:C14"][!bicycle:backward][!/^bicycle(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway:bicycle!=yes][highway!=footway]
        # way[highway][traffic_sign~="NL:C15"][!bicycle][!/^bicycle(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction][highway!=footway]
        # way[highway][traffic_sign:forward~="NL:C15"][!bicycle:forward][!/^bicycle(:forward|:both_ways)?(:conditional)?$/][highway!=construction][highway!=footway]
        # way[highway][traffic_sign:backward~="NL:C15"][!bicycle:backward][!/^bicycle(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway:bicycle!=yes][highway!=footway]
        # way[highway][traffic_sign~="NL:C15"][!moped][!/^moped(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction][highway!=footway]
        # way[highway][traffic_sign:forward~="NL:C15"][!moped:forward][!/^moped(:forward|:both_ways)?(:conditional)?$/][highway!=construction][highway!=footway]
        # way[highway][traffic_sign:backward~="NL:C15"][!moped:backward][!/^moped(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway:moped!=yes][highway!=footway]
        # way[highway][traffic_sign~="NL:C16"][!foot][!/^foot(:forward|:backward|:both_ways)?(:conditional)?$/][!/^access(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C16"][!foot:forward][!/^foot(:forward|:both_ways)?(:conditional)?$/][!/^access(:forward|:both_ways)?(:conditional)?$/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C16"][!foot:backward][!/^foot(:backward|:both_ways)?(:conditional)?$/][!/^access(:backward|:both_ways)?(:conditional)?$/][highway!=construction][oneway:foot!=yes]
        if ('highway' in keys and 'traffic_sign' in keys) or ('highway' in keys and 'traffic_sign:backward' in keys) or ('highway' in keys and 'traffic_sign:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C1'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'vehicle')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_70e165b6)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C1'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'vehicle:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_1cfba619)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C1'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'vehicle:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_374703cf)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C01'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'vehicle')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_70e165b6)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C01'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'vehicle:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_1cfba619)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C01'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'vehicle:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_374703cf)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C6'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motor_vehicle')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_70e165b6)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C6'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motor_vehicle:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_1cfba619)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C6'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motor_vehicle:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_374703cf)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')) and (mapcss._tag_capture(capture_tags, 6, tags, 'oneway:motor_vehicle') != mapcss._value_const_capture(capture_tags, 6, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C06'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motor_vehicle')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_70e165b6)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C06'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motor_vehicle:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_1cfba619)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C06'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motor_vehicle:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_374703cf)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')) and (mapcss._tag_capture(capture_tags, 6, tags, 'oneway:motor_vehicle') != mapcss._value_const_capture(capture_tags, 6, 'yes', 'yes')))
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
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C12'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motor_vehicle')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_70e165b6)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C12'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motor_vehicle:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_1cfba619)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C12'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motor_vehicle:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_374703cf)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')) and (mapcss._tag_capture(capture_tags, 6, tags, 'oneway:motor_vehicle') != mapcss._value_const_capture(capture_tags, 6, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C13'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_73ea17b1)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'footway', 'footway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C13'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_697de1f2)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'footway', 'footway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C13'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_78809448)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'oneway:moped') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')) and (mapcss._tag_capture(capture_tags, 6, tags, 'highway') != mapcss._value_const_capture(capture_tags, 6, 'footway', 'footway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C14'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bicycle')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_7372291c)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'footway', 'footway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C14'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_033b234a)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'footway', 'footway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C14'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_6b8a2885)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'oneway:bicycle') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')) and (mapcss._tag_capture(capture_tags, 6, tags, 'highway') != mapcss._value_const_capture(capture_tags, 6, 'footway', 'footway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C15'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bicycle')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_7372291c)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'footway', 'footway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C15'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_033b234a)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'footway', 'footway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C15'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_6b8a2885)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'oneway:bicycle') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')) and (mapcss._tag_capture(capture_tags, 6, tags, 'highway') != mapcss._value_const_capture(capture_tags, 6, 'footway', 'footway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C15'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_73ea17b1)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'footway', 'footway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C15'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_697de1f2)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'footway', 'footway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C15'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_78809448)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'oneway:moped') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')) and (mapcss._tag_capture(capture_tags, 6, tags, 'highway') != mapcss._value_const_capture(capture_tags, 6, 'footway', 'footway')))
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
                # assertNoMatch:"way highway=service traffic_sign:backward=\"NL:C14\" oneway:bicycle=yes"
                # assertNoMatch:"way highway=service traffic_sign:backward=\"NL:C14\" oneway=yes oneway:bicycle=no bicycle:backward=destination"
                # assertMatch:"way highway=service traffic_sign:backward=\"NL:C14\" oneway=yes oneway:bicycle=no"
                # assertMatch:"way highway=service traffic_sign:forward=\"NL:C9;NL:OB58\" traffic_sign:backward=\"NL:C1\" access:backward=no"
                # assertMatch:"way highway=service traffic_sign:forward=\"NL:C9;NL:OB58\""
                # assertMatch:"way highway=service traffic_sign=\"NL:C01\""
                # assertNoMatch:"way highway=service traffic_sign=\"NL:C01;NL:C16\" access=no"
                # assertNoMatch:"way highway=service traffic_sign=\"NL:C01;NL:OB51;NL:OB54\" motor_vehicle=no"
                # assertNoMatch:"way highway=track traffic_sign:backward=\"NL:C12\" oneway=yes oneway:bicycle=no"
                # assertNoMatch:"way highway=track traffic_sign=\"NL:C12\" motor_vehicle=no"
                err.append({'class': 90205, 'subclass': 767847379, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.key}=no/private/destination/...'))})

        # way[traffic_sign][traffic_sign=~/(^|; ?)NL:C22(\[[A-E]\])?(;|$)/][!/^hazmat(:[A-E])?(:forward|:backward|:both_ways)?(:conditional)?$/][!/^(access|vehicle|motor_vehicle)(:forward|:backward|:both_ways)?(:conditional)?$/][highway!=construction][highway]
        # way[traffic_sign:forward][traffic_sign:forward=~/(^|; ?)NL:C22(\[[A-E]\])?(;|$)/][!/^hazmat(:[A-E])?(:forward|:both_ways)?(:conditional)?$/][!/^(access|vehicle|motor_vehicle)(:forward|:both_ways)?(:conditional)?$/][highway!=construction][highway]
        # way[traffic_sign:backward][traffic_sign:backward=~/(^|; ?)NL:C22(\[[A-E]\])?(;|$)/][!/^hazmat(:[A-E])?(:backward|:both_ways)?(:conditional)?$/][!/^(access|vehicle|motor_vehicle)(:backward|:both_ways)?(:conditional)?$/][highway!=construction][highway][/^oneway:hazmat/!~/^yes$/]
        if ('highway' in keys and 'traffic_sign' in keys) or ('highway' in keys and 'traffic_sign:backward' in keys) or ('highway' in keys and 'traffic_sign:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_619cd3d8), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'))) and (not mapcss._tag_capture(capture_tags, 2, tags, self.re_229e1925)) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_70e165b6)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:forward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_619cd3d8), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'))) and (not mapcss._tag_capture(capture_tags, 2, tags, self.re_0e042431)) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_1cfba619)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:backward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_619cd3d8), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'))) and (not mapcss._tag_capture(capture_tags, 2, tags, self.re_617e36ee)) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_374703cf)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway')) and (not mapcss.regexp_test(self.re_51f98600, mapcss._match_regex(tags, self.re_75b7dc3e))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} without {1} or {2}","{0.tag}","hazmat=no/private/destination/...","hazmat:A-E=no/private/destination/...")
                # assertNoMatch:"way highway=service traffic_sign:backward=\"NL:C22[A]\" hazmat:A:backward=no"
                # assertNoMatch:"way highway=service traffic_sign:backward=\"NL:C22[A]\" oneway:hazmat=yes"
                # assertMatch:"way highway=service traffic_sign:backward=\"NL:C22[A]\" oneway=yes oneway:hazmat=no"
                # assertNoMatch:"way highway=service traffic_sign:backward=\"NL:C22[C]\" oneway:hazmat:C=yes"
                # assertMatch:"way highway=service traffic_sign:forward=\"NL:C16; NL:C22[A]; NL:OB58\""
                # assertMatch:"way highway=service traffic_sign:forward=\"NL:C22[A];NL:OB58\""
                # assertNoMatch:"way highway=service traffic_sign=\"NL:C22\" access=no"
                # assertNoMatch:"way highway=service traffic_sign=\"NL:C22\" hazmat=no"
                # assertMatch:"way highway=service traffic_sign=\"NL:C22\""
                # assertNoMatch:"way highway=service traffic_sign=\"NL:C22a\""
                err.append({'class': 90205, 'subclass': 326989948, 'text': mapcss.tr('{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), 'hazmat=no/private/destination/...', 'hazmat:A-E=no/private/destination/...')})

        # way[traffic_sign][traffic_sign=~/(^|; ?)NL:C17\b/][!maxlength][!/^maxlength(:forward|:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:forward][traffic_sign:forward=~/(^|; ?)NL:C17\b/][!maxlength:forward][!/^maxlength(:forward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:backward][traffic_sign:backward=~/(^|; ?)NL:C17\b/][!maxlength:backward][!/^maxlength(:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign][traffic_sign=~/(^|; ?)NL:C18\b/][!maxwidth][!/^maxwidth(:forward|:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:forward][traffic_sign:forward=~/(^|; ?)NL:C18\b/][!maxwidth:forward][!/^maxwidth(:forward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:backward][traffic_sign:backward=~/(^|; ?)NL:C18\b/][!maxwidth:backward][!/^maxwidth(:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign][traffic_sign=~/(^|; ?)NL:(C19|L0?1)\b/][!maxheight][!/^maxheight(:forward|:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:forward][traffic_sign:forward=~/(^|; ?)NL:(C19|L0?1)\b/][!maxheight:forward][!/^maxheight(:forward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:backward][traffic_sign:backward=~/(^|; ?)NL:(C19|L0?1)\b/][!maxheight:backward][!/^maxheight(:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign][traffic_sign=~/(^|; ?)NL:C20\b/][!maxaxleload][!/^maxaxleload(:forward|:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:forward][traffic_sign:forward=~/(^|; ?)NL:C20\b/][!maxaxleload:forward][!/^maxaxleload(:forward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:backward][traffic_sign:backward=~/(^|; ?)NL:C20\b/][!maxaxleload:backward][!/^maxaxleload(:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign][traffic_sign=~/(^|; ?)NL:C21\b/][!maxweight][!/^maxweight(:forward|:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:forward][traffic_sign:forward=~/(^|; ?)NL:C21\b/][!maxweight:forward][!/^maxweight(:forward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:backward][traffic_sign:backward=~/(^|; ?)NL:C21\b/][!maxweight:backward][!/^maxweight(:backward|:both_ways)?(:conditional)?$/][highway]
        if ('highway' in keys and 'traffic_sign' in keys) or ('highway' in keys and 'traffic_sign:backward' in keys) or ('highway' in keys and 'traffic_sign:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_0e900094), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxlength')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_2823d45d)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:forward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_0e900094), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxlength:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_2cd26805)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:backward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_0e900094), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxlength:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_0c61efa0)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_08ba1dfb), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxwidth')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_53816e1a)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:forward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_08ba1dfb), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxwidth:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_54b75cfc)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:backward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_08ba1dfb), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxwidth:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_774d1ba2)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_4065f95d), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxheight')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_33480e64)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:forward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_4065f95d), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxheight:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_63f5f8f1)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:backward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_4065f95d), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxheight:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_1aa298e1)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_59aca94c), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxaxleload')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_7d72e705)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:forward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_59aca94c), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxaxleload:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_7531ba03)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:backward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_59aca94c), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxaxleload:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_21dc697e)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_0abf5cfa), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxweight')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_345ec50a)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:forward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_0abf5cfa), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxweight:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_556f4d08)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:backward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_0abf5cfa), mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxweight:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_339dfcbd)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} without {1}","{0.tag}","{2.key}")
                # assertNoMatch:"way highway=residential traffic_sign:backward=\"NL:C21[2.1]\" maxweight:backward=2.1"
                # assertMatch:"way highway=residential traffic_sign:forward=\"NL:C19[2.1]\""
                # assertMatch:"way highway=residential traffic_sign:forward=\"NL:C21[2.1]\""
                # assertMatch:"way highway=residential traffic_sign:forward=\"NL:J19; NL:L01[4.1]; NL:OB108\""
                # assertMatch:"way highway=residential traffic_sign:forward=\"NL:J19;NL:L01[4.1];NL:OB108\""
                # assertNoMatch:"way highway=residential traffic_sign=\"NL:C19[2.1]\" maxheight=2.1"
                # assertMatch:"way highway=residential traffic_sign=\"NL:C21[2.1]\""
                # assertNoMatch:"way highway=residential traffic_sign=\"NL:J19;NL:C21[2.1];NL:OB108\" maxweight:conditional=xxx"
                err.append({'class': 90205, 'subclass': 991745921, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{2.key}'))})

        # way[highway][traffic_sign~="NL:C2"][oneway!=yes][regexp_test("^(no|0)*$",join_list("",tag_regex("^oneway:")))][oneway!=-1][highway!=construction]
        # way[highway][traffic_sign~="NL:C02"][oneway!=yes][regexp_test("^(no|0)*$",join_list("",tag_regex("^oneway:")))][oneway!=-1][highway!=construction]
        # way[highway][traffic_sign~="NL:C3"][oneway!=yes][regexp_test("^(no|0)*$",join_list("",tag_regex("^oneway:")))][oneway!=-1][highway!=construction]
        # way[highway][traffic_sign~="NL:C03"][oneway!=yes][regexp_test("^(no|0)*$",join_list("",tag_regex("^oneway:")))][oneway!=-1][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:C3"][oneway!=yes][regexp_test("^(no|-1|0)*$",join_list("",tag_regex("^oneway:")))][highway!=construction][traffic_sign:backward!~/\bNL:C0?2\b/]
        # way[highway][traffic_sign:forward~="NL:C03"][oneway!=yes][regexp_test("^(no|-1|0)*$",join_list("",tag_regex("^oneway:")))][highway!=construction][traffic_sign:backward!~/\bNL:C0?2\b/]
        # way[highway][traffic_sign:backward~="NL:C2"][oneway!=yes][regexp_test("^(no|-1|0)*$",join_list("",tag_regex("^oneway:")))][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:C02"][oneway!=yes][regexp_test("^(no|-1|0)*$",join_list("",tag_regex("^oneway:")))][highway!=construction]
        if ('highway' in keys and 'traffic_sign' in keys) or ('highway' in keys and 'traffic_sign:backward' in keys) or ('highway' in keys and 'traffic_sign:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C2'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')) and (mapcss.regexp_test(self.re_42dce20e, mapcss.join_list('', mapcss.tag_regex(tags, self.re_3894ceb2)))) and (mapcss._tag_capture(capture_tags, 4, tags, 'oneway') != mapcss._value_capture(capture_tags, 4, -1)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C02'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')) and (mapcss.regexp_test(self.re_42dce20e, mapcss.join_list('', mapcss.tag_regex(tags, self.re_3894ceb2)))) and (mapcss._tag_capture(capture_tags, 4, tags, 'oneway') != mapcss._value_capture(capture_tags, 4, -1)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C3'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')) and (mapcss.regexp_test(self.re_42dce20e, mapcss.join_list('', mapcss.tag_regex(tags, self.re_3894ceb2)))) and (mapcss._tag_capture(capture_tags, 4, tags, 'oneway') != mapcss._value_capture(capture_tags, 4, -1)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C03'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')) and (mapcss.regexp_test(self.re_42dce20e, mapcss.join_list('', mapcss.tag_regex(tags, self.re_3894ceb2)))) and (mapcss._tag_capture(capture_tags, 4, tags, 'oneway') != mapcss._value_capture(capture_tags, 4, -1)) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C3'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')) and (mapcss.regexp_test(self.re_4d17a717, mapcss.join_list('', mapcss.tag_regex(tags, self.re_3894ceb2)))) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 5, self.re_1d478f9e, '\\bNL:C0?2\\b'), mapcss._tag_capture(capture_tags, 5, tags, 'traffic_sign:backward'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:C03'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')) and (mapcss.regexp_test(self.re_4d17a717, mapcss.join_list('', mapcss.tag_regex(tags, self.re_3894ceb2)))) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 5, self.re_1d478f9e, '\\bNL:C0?2\\b'), mapcss._tag_capture(capture_tags, 5, tags, 'traffic_sign:backward'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C2'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')) and (mapcss.regexp_test(self.re_4d17a717, mapcss.join_list('', mapcss.tag_regex(tags, self.re_3894ceb2)))) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:C02'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')) and (mapcss.regexp_test(self.re_4d17a717, mapcss.join_list('', mapcss.tag_regex(tags, self.re_3894ceb2)))) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} without {1}","{1.tag}","{2.tag}")
                # assertMatch:"way highway=residential traffic_sign:backward=\"NL:C02;NL:OB58\""
                # assertNoMatch:"way highway=residential traffic_sign:backward=\"NL:C2\" oneway:motor_vehicle=yes"
                # assertNoMatch:"way highway=residential traffic_sign:backward=\"NL:C2\" oneway=yes oneway:bicycle=no"
                # assertMatch:"way highway=residential traffic_sign:forward=\"NL:C3\" oneway:motor_vehicle=-1"
                # assertNoMatch:"way highway=residential traffic_sign:forward=\"NL:C3\" oneway:motor_vehicle=yes"
                # assertMatch:"way highway=residential traffic_sign:forward=\"NL:C3\" oneway=-1"
                # assertNoMatch:"way highway=residential traffic_sign:forward=\"NL:C3\" oneway=yes"
                # assertMatch:"way highway=residential traffic_sign:forward=\"NL:C3\""
                # assertMatch:"way highway=residential traffic_sign=\"NL:C02\" oneway:bicycle=no oneway=no"
                # assertMatch:"way highway=residential traffic_sign=\"NL:C02\""
                # assertNoMatch:"way highway=residential traffic_sign=\"NL:C02;NL:OB58\" oneway=-1"
                # assertNoMatch:"way highway=residential traffic_sign=\"NL:C02;NL:OB58\" oneway=yes"
                # assertNoMatch:"way highway=residential traffic_sign=\"NL:C3\" oneway:agricultural=no oneway:motor_vehicle=yes oneway:motorcycle=no oneway=no"
                # assertNoMatch:"way highway=residential traffic_sign=\"NL:C3\" oneway:motor_vehicle=-1"
                # assertNoMatch:"way highway=residential traffic_sign=\"NL:C3\" oneway:motor_vehicle=yes"
                # assertMatch:"way highway=residential traffic_sign=\"NL:C3;NL:OB58\""
                err.append({'class': 90205, 'subclass': 2031953960, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

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
                err.append({'class': 90205, 'subclass': 560436831, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

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
                err.append({'class': 90205, 'subclass': 439012160, 'text': mapcss.tr('{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'), mapcss._tag_uncapture(capture_tags, '{3.tag}'))})

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
                err.append({'class': 90205, 'subclass': 1998584294, 'text': mapcss.tr('{0} together with {1} but without {2}', mapcss._tag_uncapture(capture_tags, '{2.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), 'oneway=yes')})

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
                err.append({'class': 90205, 'subclass': 2073220392, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # way[parking:both:restriction!=no_parking][traffic_sign~="NL:E01"][highway][parking:both=no][parking:right:restriction!=no_parking][parking:left:restriction!=no_parking]
        # way[parking:both:restriction!=no_parking][traffic_sign~="NL:E01"][highway][parking:left=no][parking:lane:right=no][parking:right:restriction!=no_parking][parking:left:restriction!=no_parking]
        # way[parking:both:restriction!=no_parking][traffic_sign~="NL:E1"][highway][parking:both=no][parking:right:restriction!=no_parking][parking:left:restriction!=no_parking]
        # way[parking:both:restriction!=no_parking][traffic_sign~="NL:E1"][highway][parking:left=no][parking:lane:right=no][parking:right:restriction!=no_parking][parking:left:restriction!=no_parking]
        # way[parking:right:restriction!=no_parking][traffic_sign:right~="NL:E01"][highway][parking:both=no][parking:both:restriction!=no_parking]
        # way[parking:right:restriction!=no_parking][traffic_sign:right~="NL:E01"][highway][parking:right=no][parking:both:restriction!=no_parking]
        # way[parking:right:restriction!=no_parking][traffic_sign:right~="NL:E1"][highway][parking:both=no][parking:both:restriction!=no_parking]
        # way[parking:right:restriction!=no_parking][traffic_sign:right~="NL:E1"][highway][parking:right=no][parking:both:restriction!=no_parking]
        # way[parking:left:restriction!=no_parking][traffic_sign:left~="NL:E01"][highway][parking:both=no][parking:both:restriction!=no_parking]
        # way[parking:left:restriction!=no_parking][traffic_sign:left~="NL:E01"][highway][parking:left=no][parking:both:restriction!=no_parking]
        # way[parking:left:restriction!=no_parking][traffic_sign:left~="NL:E1"][highway][parking:both=no][parking:both:restriction!=no_parking]
        # way[parking:left:restriction!=no_parking][traffic_sign:left~="NL:E1"][highway][parking:left=no][parking:both:restriction!=no_parking]
        # way[parking:both:restriction!=no_stopping][traffic_sign~="NL:E02"][highway][parking:both=no][parking:right:restriction!=no_stopping][parking:left:restriction!=no_stopping]
        # way[parking:both:restriction!=no_stopping][traffic_sign~="NL:E02"][highway][parking:left=no][parking:right=no][parking:right:restriction!=no_stopping][parking:left:restriction!=no_stopping]
        # way[parking:both:restriction!=no_stopping][traffic_sign~="NL:E2"][highway][parking:both=no][parking:right:restriction!=no_stopping][parking:left:restriction!=no_stopping]
        # way[parking:both:restriction!=no_stopping][traffic_sign~="NL:E2"][highway][parking:left=no][parking:right=no][parking:right:restriction!=no_stopping][parking:left:restriction!=no_stopping]
        # way[parking:right:restriction!=no_stopping][traffic_sign:right~="NL:E02"][highway][parking:both=no][parking:both:restriction!=no_stopping]
        # way[parking:right:restriction!=no_stopping][traffic_sign:right~="NL:E02"][highway][parking:right=no][parking:both:restriction!=no_stopping]
        # way[parking:right:restriction!=no_stopping][traffic_sign:right~="NL:E2"][highway][parking:both=no][parking:both:restriction!=no_stopping]
        # way[parking:right:restriction!=no_stopping][traffic_sign:right~="NL:E2"][highway][parking:right=no][parking:both:restriction!=no_stopping]
        # way[parking:left:restriction!=no_stopping][traffic_sign:left~="NL:E02"][highway][parking:both=no][parking:both:restriction!=no_stopping]
        # way[parking:left:restriction!=no_stopping][traffic_sign:left~="NL:E02"][highway][parking:left=no][parking:both:restriction!=no_stopping]
        # way[parking:left:restriction!=no_stopping][traffic_sign:left~="NL:E2"][highway][parking:both=no][parking:both:restriction!=no_stopping]
        # way[parking:left:restriction!=no_stopping][traffic_sign:left~="NL:E2"][highway][parking:left=no][parking:both:restriction!=no_stopping]
        if ('highway' in keys and 'parking:both' in keys and 'traffic_sign' in keys) or ('highway' in keys and 'parking:both' in keys and 'traffic_sign:left' in keys) or ('highway' in keys and 'parking:both' in keys and 'traffic_sign:right' in keys) or ('highway' in keys and 'parking:lane:right' in keys and 'parking:left' in keys and 'traffic_sign' in keys) or ('highway' in keys and 'parking:left' in keys and 'parking:right' in keys and 'traffic_sign' in keys) or ('highway' in keys and 'parking:left' in keys and 'traffic_sign:left' in keys) or ('highway' in keys and 'parking:right' in keys and 'traffic_sign:right' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:both:restriction') != mapcss._value_const_capture(capture_tags, 0, 'no_parking', 'no_parking')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:E01'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:both') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:right:restriction') != mapcss._value_const_capture(capture_tags, 4, 'no_parking', 'no_parking')) and (mapcss._tag_capture(capture_tags, 5, tags, 'parking:left:restriction') != mapcss._value_const_capture(capture_tags, 5, 'no_parking', 'no_parking')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:both:restriction') != mapcss._value_const_capture(capture_tags, 0, 'no_parking', 'no_parking')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:E01'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:left') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:lane:right') == mapcss._value_capture(capture_tags, 4, 'no')) and (mapcss._tag_capture(capture_tags, 5, tags, 'parking:right:restriction') != mapcss._value_const_capture(capture_tags, 5, 'no_parking', 'no_parking')) and (mapcss._tag_capture(capture_tags, 6, tags, 'parking:left:restriction') != mapcss._value_const_capture(capture_tags, 6, 'no_parking', 'no_parking')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:both:restriction') != mapcss._value_const_capture(capture_tags, 0, 'no_parking', 'no_parking')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:E1'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:both') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:right:restriction') != mapcss._value_const_capture(capture_tags, 4, 'no_parking', 'no_parking')) and (mapcss._tag_capture(capture_tags, 5, tags, 'parking:left:restriction') != mapcss._value_const_capture(capture_tags, 5, 'no_parking', 'no_parking')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:both:restriction') != mapcss._value_const_capture(capture_tags, 0, 'no_parking', 'no_parking')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:E1'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:left') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:lane:right') == mapcss._value_capture(capture_tags, 4, 'no')) and (mapcss._tag_capture(capture_tags, 5, tags, 'parking:right:restriction') != mapcss._value_const_capture(capture_tags, 5, 'no_parking', 'no_parking')) and (mapcss._tag_capture(capture_tags, 6, tags, 'parking:left:restriction') != mapcss._value_const_capture(capture_tags, 6, 'no_parking', 'no_parking')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:right:restriction') != mapcss._value_const_capture(capture_tags, 0, 'no_parking', 'no_parking')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:right'), mapcss._value_capture(capture_tags, 1, 'NL:E01'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:both') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:both:restriction') != mapcss._value_const_capture(capture_tags, 4, 'no_parking', 'no_parking')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:right:restriction') != mapcss._value_const_capture(capture_tags, 0, 'no_parking', 'no_parking')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:right'), mapcss._value_capture(capture_tags, 1, 'NL:E01'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:right') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:both:restriction') != mapcss._value_const_capture(capture_tags, 4, 'no_parking', 'no_parking')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:right:restriction') != mapcss._value_const_capture(capture_tags, 0, 'no_parking', 'no_parking')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:right'), mapcss._value_capture(capture_tags, 1, 'NL:E1'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:both') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:both:restriction') != mapcss._value_const_capture(capture_tags, 4, 'no_parking', 'no_parking')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:right:restriction') != mapcss._value_const_capture(capture_tags, 0, 'no_parking', 'no_parking')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:right'), mapcss._value_capture(capture_tags, 1, 'NL:E1'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:right') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:both:restriction') != mapcss._value_const_capture(capture_tags, 4, 'no_parking', 'no_parking')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:left:restriction') != mapcss._value_const_capture(capture_tags, 0, 'no_parking', 'no_parking')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:left'), mapcss._value_capture(capture_tags, 1, 'NL:E01'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:both') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:both:restriction') != mapcss._value_const_capture(capture_tags, 4, 'no_parking', 'no_parking')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:left:restriction') != mapcss._value_const_capture(capture_tags, 0, 'no_parking', 'no_parking')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:left'), mapcss._value_capture(capture_tags, 1, 'NL:E01'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:left') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:both:restriction') != mapcss._value_const_capture(capture_tags, 4, 'no_parking', 'no_parking')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:left:restriction') != mapcss._value_const_capture(capture_tags, 0, 'no_parking', 'no_parking')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:left'), mapcss._value_capture(capture_tags, 1, 'NL:E1'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:both') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:both:restriction') != mapcss._value_const_capture(capture_tags, 4, 'no_parking', 'no_parking')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:left:restriction') != mapcss._value_const_capture(capture_tags, 0, 'no_parking', 'no_parking')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:left'), mapcss._value_capture(capture_tags, 1, 'NL:E1'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:left') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:both:restriction') != mapcss._value_const_capture(capture_tags, 4, 'no_parking', 'no_parking')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:both:restriction') != mapcss._value_const_capture(capture_tags, 0, 'no_stopping', 'no_stopping')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:E02'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:both') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:right:restriction') != mapcss._value_const_capture(capture_tags, 4, 'no_stopping', 'no_stopping')) and (mapcss._tag_capture(capture_tags, 5, tags, 'parking:left:restriction') != mapcss._value_const_capture(capture_tags, 5, 'no_stopping', 'no_stopping')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:both:restriction') != mapcss._value_const_capture(capture_tags, 0, 'no_stopping', 'no_stopping')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:E02'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:left') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:right') == mapcss._value_capture(capture_tags, 4, 'no')) and (mapcss._tag_capture(capture_tags, 5, tags, 'parking:right:restriction') != mapcss._value_const_capture(capture_tags, 5, 'no_stopping', 'no_stopping')) and (mapcss._tag_capture(capture_tags, 6, tags, 'parking:left:restriction') != mapcss._value_const_capture(capture_tags, 6, 'no_stopping', 'no_stopping')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:both:restriction') != mapcss._value_const_capture(capture_tags, 0, 'no_stopping', 'no_stopping')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:E2'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:both') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:right:restriction') != mapcss._value_const_capture(capture_tags, 4, 'no_stopping', 'no_stopping')) and (mapcss._tag_capture(capture_tags, 5, tags, 'parking:left:restriction') != mapcss._value_const_capture(capture_tags, 5, 'no_stopping', 'no_stopping')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:both:restriction') != mapcss._value_const_capture(capture_tags, 0, 'no_stopping', 'no_stopping')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:E2'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:left') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:right') == mapcss._value_capture(capture_tags, 4, 'no')) and (mapcss._tag_capture(capture_tags, 5, tags, 'parking:right:restriction') != mapcss._value_const_capture(capture_tags, 5, 'no_stopping', 'no_stopping')) and (mapcss._tag_capture(capture_tags, 6, tags, 'parking:left:restriction') != mapcss._value_const_capture(capture_tags, 6, 'no_stopping', 'no_stopping')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:right:restriction') != mapcss._value_const_capture(capture_tags, 0, 'no_stopping', 'no_stopping')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:right'), mapcss._value_capture(capture_tags, 1, 'NL:E02'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:both') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:both:restriction') != mapcss._value_const_capture(capture_tags, 4, 'no_stopping', 'no_stopping')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:right:restriction') != mapcss._value_const_capture(capture_tags, 0, 'no_stopping', 'no_stopping')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:right'), mapcss._value_capture(capture_tags, 1, 'NL:E02'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:right') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:both:restriction') != mapcss._value_const_capture(capture_tags, 4, 'no_stopping', 'no_stopping')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:right:restriction') != mapcss._value_const_capture(capture_tags, 0, 'no_stopping', 'no_stopping')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:right'), mapcss._value_capture(capture_tags, 1, 'NL:E2'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:both') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:both:restriction') != mapcss._value_const_capture(capture_tags, 4, 'no_stopping', 'no_stopping')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:right:restriction') != mapcss._value_const_capture(capture_tags, 0, 'no_stopping', 'no_stopping')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:right'), mapcss._value_capture(capture_tags, 1, 'NL:E2'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:right') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:both:restriction') != mapcss._value_const_capture(capture_tags, 4, 'no_stopping', 'no_stopping')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:left:restriction') != mapcss._value_const_capture(capture_tags, 0, 'no_stopping', 'no_stopping')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:left'), mapcss._value_capture(capture_tags, 1, 'NL:E02'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:both') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:both:restriction') != mapcss._value_const_capture(capture_tags, 4, 'no_stopping', 'no_stopping')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:left:restriction') != mapcss._value_const_capture(capture_tags, 0, 'no_stopping', 'no_stopping')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:left'), mapcss._value_capture(capture_tags, 1, 'NL:E02'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:left') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:both:restriction') != mapcss._value_const_capture(capture_tags, 4, 'no_stopping', 'no_stopping')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:left:restriction') != mapcss._value_const_capture(capture_tags, 0, 'no_stopping', 'no_stopping')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:left'), mapcss._value_capture(capture_tags, 1, 'NL:E2'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:both') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:both:restriction') != mapcss._value_const_capture(capture_tags, 4, 'no_stopping', 'no_stopping')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking:left:restriction') != mapcss._value_const_capture(capture_tags, 0, 'no_stopping', 'no_stopping')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:left'), mapcss._value_capture(capture_tags, 1, 'NL:E2'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking:left') == mapcss._value_capture(capture_tags, 3, 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'parking:both:restriction') != mapcss._value_const_capture(capture_tags, 4, 'no_stopping', 'no_stopping')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} without {1}","{1.tag}","{0.tag}")
                # fixAdd:"{0.tag}"
                # assertMatch:"way highway=residential traffic_sign:left=NL:E02 parking:both=no"
                # assertMatch:"way highway=residential traffic_sign:left=NL:E02 parking:left=no"
                # assertNoMatch:"way highway=residential traffic_sign:left=NL:E02 parking:left=parallel"
                # assertNoMatch:"way highway=residential traffic_sign:left=NL:E02 traffic_sign:right=NL:E02 parking:both=no parking:both:restriction=no_stopping"
                # assertNoMatch:"way highway=residential traffic_sign=NL:E01 parking:both=no parking:left:restriction=no_parking parking:right:restriction=no_parking"
                err.append({'class': 90205, 'subclass': 1049002673, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, '{0.tag}')).split('=', 1)])
                }})

        # way[highway][traffic_sign~="NL:F5"][!priority][!/^priority:./][highway!=construction]
        # way[highway][traffic_sign~="NL:F05"][!priority][!/^priority:./][highway!=construction]
        # way[highway][traffic_sign~="NL:F6"][!priority][!/^priority:./][highway!=construction]
        # way[highway][traffic_sign~="NL:F06"][!priority][!/^priority:./][highway!=construction]
        if ('highway' in keys and 'traffic_sign' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:F5'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'priority')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_5012755c)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:F05'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'priority')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_5012755c)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:F6'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'priority')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_5012755c)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:F06'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'priority')) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_5012755c)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} without {1} or {2}","{1.tag}","{2.key}=forward","{2.key}=backward")
                # assertNoMatch:"way highway=residential traffic_sign=\"NL:F6;NL:F5\" priority=forward"
                # assertNoMatch:"way highway=residential traffic_sign=\"NL:F6;OB05\" priority:agricultural=forward"
                # assertMatch:"way highway=residential traffic_sign=\"NL:F6;OB05\""
                err.append({'class': 90205, 'subclass': 1040610185, 'text': mapcss.tr('{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.key}=forward'), mapcss._tag_uncapture(capture_tags, '{2.key}=backward'))})

        # way[highway][traffic_sign:forward~="NL:F5"][priority!=backward][/^priority:./!~/backward/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:F05"][priority!=backward][/^priority:./!~/backward/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:F6"][priority!=backward][/^priority:./!~/backward/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:F06"][priority!=backward][/^priority:./!~/backward/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:F5"][priority!=forward][/^priority:./!~/forward/][highway!=construction]
        # way[highway][traffic_sign:backward~="NL:F05"][priority!=forward][/^priority:./!~/forward/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:F6"][priority!=forward][/^priority:./!~/forward/][highway!=construction]
        # way[highway][traffic_sign:forward~="NL:F06"][priority!=forward][/^priority:./!~/forward/][highway!=construction]
        if ('highway' in keys and 'traffic_sign:backward' in keys) or ('highway' in keys and 'traffic_sign:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:F5'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'priority') != mapcss._value_const_capture(capture_tags, 2, 'backward', 'backward')) and (not mapcss.regexp_test(self.re_68a71d57, mapcss._match_regex(tags, self.re_5012755c))) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:F05'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'priority') != mapcss._value_const_capture(capture_tags, 2, 'backward', 'backward')) and (not mapcss.regexp_test(self.re_68a71d57, mapcss._match_regex(tags, self.re_5012755c))) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:F6'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'priority') != mapcss._value_const_capture(capture_tags, 2, 'backward', 'backward')) and (not mapcss.regexp_test(self.re_68a71d57, mapcss._match_regex(tags, self.re_5012755c))) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:F06'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'priority') != mapcss._value_const_capture(capture_tags, 2, 'backward', 'backward')) and (not mapcss.regexp_test(self.re_68a71d57, mapcss._match_regex(tags, self.re_5012755c))) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:F5'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'priority') != mapcss._value_const_capture(capture_tags, 2, 'forward', 'forward')) and (not mapcss.regexp_test(self.re_252a5d6c, mapcss._match_regex(tags, self.re_5012755c))) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:backward'), mapcss._value_capture(capture_tags, 1, 'NL:F05'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'priority') != mapcss._value_const_capture(capture_tags, 2, 'forward', 'forward')) and (not mapcss.regexp_test(self.re_252a5d6c, mapcss._match_regex(tags, self.re_5012755c))) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:F6'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'priority') != mapcss._value_const_capture(capture_tags, 2, 'forward', 'forward')) and (not mapcss.regexp_test(self.re_252a5d6c, mapcss._match_regex(tags, self.re_5012755c))) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign:forward'), mapcss._value_capture(capture_tags, 1, 'NL:F06'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'priority') != mapcss._value_const_capture(capture_tags, 2, 'forward', 'forward')) and (not mapcss.regexp_test(self.re_252a5d6c, mapcss._match_regex(tags, self.re_5012755c))) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} without {1}","{1.tag}","{2.tag}")
                # assertMatch:"way highway=residential traffic_sign:backward=\"NL:F05\" priority=backward"
                # assertNoMatch:"way highway=residential traffic_sign:backward=\"NL:F6\" priority=backward"
                # assertNoMatch:"way highway=residential traffic_sign:forward=\"NL:F5\" priority=backward"
                # assertMatch:"way highway=residential traffic_sign:forward=\"NL:F5\" priority=forward"
                # assertNoMatch:"way highway=residential traffic_sign:forward=\"NL:F6\" priority:conditional=\"forward @ (10:00-12:00)\""
                # assertMatch:"way highway=residential traffic_sign:forward=\"NL:F6\" priority=backward"
                # assertNoMatch:"way highway=residential traffic_sign:forward=\"NL:F6\" priority=forward"
                # assertMatch:"way highway=residential traffic_sign:forward=\"NL:F6\""
                # assertMatch:"way highway=residential traffic_sign:forward=\"NL:F6;OB05\" priority:agricultural=backward"
                # assertNoMatch:"way highway=residential traffic_sign:forward=\"NL:F6;OB05\" priority:agricultural=forward"
                err.append({'class': 90205, 'subclass': 1108961023, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # *[contact:phone=~/^(00|\+)31 ?0( ?[0-9]){7,}/]
        # *[contact:mobile=~/^(00|\+)31 ?0( ?[0-9]){7,}/]
        # *[contact:whatsapp=~/^(00|\+)31 ?0( ?[0-9]){7,}/]
        # *[phone=~/^(00|\+)31 ?0( ?[0-9]){7,}/]
        if ('contact:mobile' in keys) or ('contact:phone' in keys) or ('contact:whatsapp' in keys) or ('phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_594405dc), mapcss._tag_capture(capture_tags, 0, tags, 'contact:phone'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_594405dc), mapcss._tag_capture(capture_tags, 0, tags, 'contact:mobile'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_594405dc), mapcss._tag_capture(capture_tags, 0, tags, 'contact:whatsapp'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_594405dc), mapcss._tag_capture(capture_tags, 0, tags, 'phone'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .badPhoneNumber
                # group:tr("NL addresses and contacts")
                # throwWarning:tr("Invalid tag {0}: country code should not be followed by a 0","{0.key}")
                set_badPhoneNumber = True
                err.append({'class': 90201, 'subclass': 1739574763, 'text': mapcss.tr('Invalid tag {0}: country code should not be followed by a 0', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[contact:phone=~/^(\+|00)31 ?0?( ?[0-9]){3,6}$/]
        # *[contact:mobile=~/^(\+|00)31 ?0?( ?[0-9]){3,6}$/]
        # *[phone=~/^(\+|00)31 ?0?( ?[0-9]){3,6}$/]
        if ('contact:mobile' in keys) or ('contact:phone' in keys) or ('phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_287f5dd8), mapcss._tag_capture(capture_tags, 0, tags, 'contact:phone'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_287f5dd8), mapcss._tag_capture(capture_tags, 0, tags, 'contact:mobile'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_287f5dd8), mapcss._tag_capture(capture_tags, 0, tags, 'phone'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .badPhoneNumber
                # group:tr("NL addresses and contacts")
                # throwWarning:tr("Invalid tag {0}: short phone numbers cannot be used with international prefix (or: wrong phone number length)","{0.key}")
                set_badPhoneNumber = True
                err.append({'class': 90201, 'subclass': 345342642, 'text': mapcss.tr('Invalid tag {0}: short phone numbers cannot be used with international prefix (or: wrong phone number length)', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[contact:phone=~/^(0031|\+31|0) ?[1-9]( ?[0-9]){11}/][inside("NL")]!.badPhoneNumber
        # *[contact:mobile=~/^(0031|\+31|0) ?[1-9]( ?[0-9]){11}/][inside("NL")]!.badPhoneNumber
        # *[contact:whatsapp=~/^(0031|\+31|0) ?[1-9]( ?[0-9]){11}/][inside("NL")]!.badPhoneNumber
        # *[phone=~/^(0031|\+31|0) ?[1-9]( ?[0-9]){11}/][inside("NL")]!.badPhoneNumber
        if ('contact:mobile' in keys) or ('contact:phone' in keys) or ('contact:whatsapp' in keys) or ('phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_badPhoneNumber) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_7c3d18b2), mapcss._tag_capture(capture_tags, 0, tags, 'contact:phone'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_badPhoneNumber) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_7c3d18b2), mapcss._tag_capture(capture_tags, 0, tags, 'contact:mobile'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_badPhoneNumber) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_7c3d18b2), mapcss._tag_capture(capture_tags, 0, tags, 'contact:whatsapp'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_badPhoneNumber) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_7c3d18b2), mapcss._tag_capture(capture_tags, 0, tags, 'phone'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL addresses and contacts")
                # throwWarning:tr("Invalid tag {0}: too many digits (or foreign number, if so: ignore)","{0.key}")
                err.append({'class': 90201, 'subclass': 50270752, 'text': mapcss.tr('Invalid tag {0}: too many digits (or foreign number, if so: ignore)', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # area[building][/^addr:(street|housenumber|postcode|city)$/][amenity!=place_of_worship][shop!=mall][building!~/^(container|houseboat|static_caravan)$/][inside("NL")]:closed
        if ('building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_5ef8db88)) and (mapcss._tag_capture(capture_tags, 2, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 2, 'place_of_worship', 'place_of_worship')) and (mapcss._tag_capture(capture_tags, 3, tags, 'shop') != mapcss._value_const_capture(capture_tags, 3, 'mall', 'mall')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 4, self.re_18c8cfbe, '^(container|houseboat|static_caravan)$'), mapcss._tag_capture(capture_tags, 4, tags, 'building'))) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')) and (nds[0] == nds[-1]))
                except mapcss.RuleAbort: pass
            if match:
                # set .addrOnBuilding
                # group:tr("NL addresses and contacts")
                # throwWarning:tr("In Nederland is het gebouw niet gekoppeld aan het adres. Het adres is wel gekoppeld aan het gebruiksdoel.")
                set_addrOnBuilding = True
                err.append({'class': 90201, 'subclass': 1486034706, 'text': mapcss.tr('In Nederland is het gebouw niet gekoppeld aan het adres. Het adres is wel gekoppeld aan het gebruiksdoel.')})

        # area[/^addr:(city|postcode)$/][!/(^|.+:)addr:housenumber($|:.+)/][!/(^|.+:)addr:street($|:.+)/][inside("NL")]!.addrOnBuilding
        # area[addr:street][!/(^|.+:)addr:housenumber($|:.+)/][!addr:interpolation][!addr:flats][inside("NL")]!.addrOnBuilding
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_addrOnBuilding) and (mapcss._tag_capture(capture_tags, 0, tags, self.re_561be3ff)) and (not mapcss._tag_capture(capture_tags, 1, tags, self.re_49026388)) and (not mapcss._tag_capture(capture_tags, 2, tags, self.re_32d334cf)) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_addrOnBuilding) and (mapcss._tag_capture(capture_tags, 0, tags, 'addr:street')) and (not mapcss._tag_capture(capture_tags, 1, tags, self.re_49026388)) and (not mapcss._tag_capture(capture_tags, 2, tags, 'addr:interpolation')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'addr:flats')) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL addresses and contacts")
                # throwWarning:tr("Incomplete address: {0} {1} {2} {3}",any(tag("addr:street"),"[street?]"),any(tag("addr:housenumber"),"[housenumber?]"),any(tag("addr:postcode"),""),any(tag("addr:city"),""))
                err.append({'class': 90201, 'subclass': 2087285475, 'text': mapcss.tr('Incomplete address: {0} {1} {2} {3}', mapcss.any_(mapcss.tag(tags, 'addr:street'), '[street?]'), mapcss.any_(mapcss.tag(tags, 'addr:housenumber'), '[housenumber?]'), mapcss.any_(mapcss.tag(tags, 'addr:postcode'), ''), mapcss.any_(mapcss.tag(tags, 'addr:city'), ''))})

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
                err.append({'class': 90206, 'subclass': 731881046, 'text': mapcss.tr('{0} together with {1} and {2}. Remove {0}.', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.tag}')), 'allow_fix_override': True, 'fix': {
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
                err.append({'class': 90206, 'subclass': 719277245, 'text': mapcss.tr('{0} and {1} together with {2} and conflicting values', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

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
                err.append({'class': 90206, 'subclass': 264601774, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
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
                err.append({'class': 90206, 'subclass': 1915077278, 'text': mapcss.tr('{0} and {1} together with {2} and conflicting values', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

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
                err.append({'class': 90206, 'subclass': 800706341, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # way[highway=footway][cycleway][cycleway!=no][cycleway!=lane][traffic_sign!~/\bNL:G0?7\b/][inside("NL")]
        # way[highway=footway][segregated=yes][traffic_sign!~/\bNL:G0?7\b/][inside("NL")]
        if ('cycleway' in keys and 'highway' in keys) or ('highway' in keys and 'segregated' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'footway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'cycleway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'cycleway') != mapcss._value_const_capture(capture_tags, 2, 'no', 'no')) and (mapcss._tag_capture(capture_tags, 3, tags, 'cycleway') != mapcss._value_const_capture(capture_tags, 3, 'lane', 'lane')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 4, self.re_7537ca1e, '\\bNL:G0?7\\b'), mapcss._tag_capture(capture_tags, 4, tags, 'traffic_sign'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'footway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'segregated') == mapcss._value_capture(capture_tags, 1, 'yes')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_7537ca1e, '\\bNL:G0?7\\b'), mapcss._tag_capture(capture_tags, 2, tags, 'traffic_sign'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL German style tagging")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # suggestAlternative:"highway=cycleway"
                # suggestAlternative:"highway=path"
                # assertNoMatch:"way highway=footway cycleway=lane traffic_sign=NL:G07-ZB"
                # assertNoMatch:"way highway=footway cycleway=no"
                # assertNoMatch:"way highway=footway segregated=yes traffic_sign=NL:G07-ZB"
                # assertNoMatch:"way highway=footway segregated=yes traffic_sign=NL:G7"
                err.append({'class': 90206, 'subclass': 1018129333, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

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
                err.append({'class': 90202, 'subclass': 2146573895, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
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
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"addr:postcode via BAG imports on addresses"
                # fixRemove:"{0.key}"
                err.append({'class': 90202, 'subclass': 194633982, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # area[building=terrace][inside("NL")]
        if ('building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'terrace')) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("Een rij met rijtjeshuizen ({0}) wordt in Nederland per huis geïmporteerd uit de BAG","{0.tag}")
                # suggestAlternative:"leisure=outdoor_seating voor 'terrasjes'"
                # suggestAlternative:"building=house + house=terraced voor een individueel rijtjeshuis"
                # suggestAlternative:"building=house via een BAG importverzoek voor huizen"
                err.append({'class': 90202, 'subclass': 2130098421, 'text': mapcss.tr('Een rij met rijtjeshuizen ({0}) wordt in Nederland per huis geïmporteerd uit de BAG', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[addr:interpolation][inside("NL")]
        if ('addr:interpolation' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'addr:interpolation')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("Adressen ({0}) worden in Nederland individueel geïmporteerd uit de BAG","{0.key}")
                # suggestAlternative:"meerdere addr:housenumber via een BAG importverzoek"
                err.append({'class': 90202, 'subclass': 864819394, 'text': mapcss.tr('Adressen ({0}) worden in Nederland individueel geïmporteerd uit de BAG', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

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
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 90202, 'subclass': 788111375, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
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
                err.append({'class': 90202, 'subclass': 379490980, 'text': mapcss.tr('Railway lines should be drawn as separate ways per track, rather than one way with {0}', mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # area[addr:housename][/^building(:part)?$/][inside("NL")][!name]
        # area[building:name][/^building(:part)?$/][inside("NL")][!name]
        if ('addr:housename' in keys) or ('building:name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'addr:housename')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_550ffc74)) and (mapcss.inside(self.father.config.options, 'NL')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'name')) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:name')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_550ffc74)) and (mapcss.inside(self.father.config.options, 'NL')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'name')) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # set .housenameWithFix
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"name=*"
                # fixChangeKey:"{0.key}=>name"
                set_housenameWithFix = True
                err.append({'class': 90202, 'subclass': 797359946, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [(mapcss._tag_uncapture(capture_tags, '{0.key}=>name')).split('=>', 1)[1].strip(), mapcss.tag(tags, (mapcss._tag_uncapture(capture_tags, '{0.key}=>name')).split('=>', 1)[0].strip())]]),
                    '-': ([
                    (mapcss._tag_uncapture(capture_tags, '{0.key}=>name')).split('=>', 1)[0].strip()])
                }})

        # area[addr:housename][/^building(:part)?$/][inside("NL")][name=*"addr:housename"]!.housenameWithFix
        # area[building:name][/^building(:part)?$/][inside("NL")][name=*"building:name"]!.housenameWithFix
        if ('addr:housename' in keys and 'name' in keys) or ('building:name' in keys and 'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_housenameWithFix) and (mapcss._tag_capture(capture_tags, 0, tags, 'addr:housename')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_550ffc74)) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, 3, tags, 'name') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'addr:housename'))) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_housenameWithFix) and (mapcss._tag_capture(capture_tags, 0, tags, 'building:name')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_550ffc74)) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, 3, tags, 'name') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'building:name'))) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # set .housenameWithFix
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"name=*"
                # fixRemove:"{0.key}"
                set_housenameWithFix = True
                err.append({'class': 90202, 'subclass': 464057822, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # area[addr:housename][/^building(:part)?$/][inside("NL")][name]!.housenameWithFix
        # area[building:name][/^building(:part)?$/][inside("NL")][name]!.housenameWithFix
        if ('addr:housename' in keys and 'name' in keys) or ('building:name' in keys and 'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_housenameWithFix) and (mapcss._tag_capture(capture_tags, 0, tags, 'addr:housename')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_550ffc74)) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, 3, tags, 'name')) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_housenameWithFix) and (mapcss._tag_capture(capture_tags, 0, tags, 'building:name')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_550ffc74)) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, 3, tags, 'name')) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"name=*"
                err.append({'class': 90202, 'subclass': 1635606421, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[/.:covid19$/][inside("NL")]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_26516863)) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("There are no active covid-19 restrictions at the moment. Remove {0}.","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 90202, 'subclass': 1496260396, 'text': mapcss.tr('There are no active covid-19 restrictions at the moment. Remove {0}.', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # way[bicycle_road?][inside("NL")]
        if ('bicycle_road' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bicycle_road') in ('yes', 'true', '1')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("Het concept {0} bestaat niet in Nederland","{0.key}")
                # suggestAlternative:"highway=* + cyclestreet=yes (fietsstraat)"
                # suggestAlternative:"highway=* + cycleway=* (fietsstrook)"
                # suggestAlternative:"highway=cycleway (fietspad)"
                err.append({'class': 90202, 'subclass': 1111134078, 'text': mapcss.tr('Het concept {0} bestaat niet in Nederland', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # way[surface][surface=~/stenen$|^hout$|\bbestraa?t(ing)?$|grond$|^puin$|^grind$|zand$/]
        # *[material][material=~/\bhout|\bmetaal\b|^beton$|^brons$|steen\b|ijzer\b|staal\b/]
        if ('material' in keys) or ('surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'surface')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6454d3f5), mapcss._tag_capture(capture_tags, 1, tags, 'surface'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'material')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_334bd9c9), mapcss._tag_capture(capture_tags, 1, tags, 'material'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("unusual value of {0}","{0.key}")
                # assertMatch:"way highway=service surface=\"niet bestraat\""
                # assertNoMatch:"way highway=service surface=paving_stones"
                # assertMatch:"way highway=service surface=straatstenen"
                # assertNoMatch:"way tourism=artwork material=bronze"
                err.append({'class': 90202, 'subclass': 1205828493, 'text': mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[surface][surface=~/^paving_stones:([1-9])0$/][inside("NL")]
        if ('surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'surface')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_19b1af6a), mapcss._tag_capture(capture_tags, 1, tags, 'surface'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"surface=paving_stones + paving_stones:shape=square + paving_stones:length=[length in meter, e.g. 0.3]"
                # fixAdd:concat("paving_stones:length=0.",get(regexp_match("^paving_stones:([1-9])0$",tag("surface")),1))
                # fixAdd:"paving_stones:shape=square"
                # fixAdd:"surface=paving_stones"
                # assertNoMatch:"way highway=footway surface=paving_stones"
                err.append({'class': 90202, 'subclass': 1868473171, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('paving_stones:length=0.', mapcss.get(mapcss.regexp_match(self.re_19b1af6a, mapcss.tag(tags, 'surface')), 1))).split('=', 1),
                    ['paving_stones:shape','square'],
                    ['surface','paving_stones']])
                }})

        # *[/^(.+):surface$/][/^(.+):surface$/=~/^paving_stones:([1-9])0$/][count(tag_regex("^(.+):surface$"))==1][inside("NL")]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_74d9b833)) and (mapcss.regexp_test(self.re_19b1af6a, mapcss._match_regex(tags, self.re_74d9b833))) and (mapcss.count(mapcss.tag_regex(tags, self.re_74d9b833)) == 1) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # set .completedSurfacePavingStonesNumber
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"*:surface=paving_stones + *:paving_stones:shape=square + *:paving_stones:length=[length in meter, e.g. 0.3]"
                # assertNoMatch:"way highway=residential sidewalk:surface=paving_stones cycleway:surface=paving_stones:20"
                # assertNoMatch:"way highway=residential sidewalk:surface=paving_stones:30 cycleway:surface=paving_stones:20"
                set_completedSurfacePavingStonesNumber = True
                err.append({'class': 90202, 'subclass': 1911834456, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[/^(.+):surface$/=~/^paving_stones:([1-9])0$/][inside("NL")]!.completedSurfacePavingStonesNumber
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_completedSurfacePavingStonesNumber) and (mapcss.regexp_test(self.re_19b1af6a, mapcss._match_regex(tags, self.re_74d9b833))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","*:surface=paving_stones:NN")
                # suggestAlternative:"*:surface=paving_stones + *:paving_stones:shape=square + *:paving_stones:length=[length in meter, e.g. 0.3]"
                err.append({'class': 90202, 'subclass': 1665978272, 'text': mapcss.tr('{0} is deprecated', '*:surface=paving_stones:NN')})

        # *[winkelnummer]
        if ('winkelnummer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'winkelnummer')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"ref=*"
                err.append({'class': 90202, 'subclass': 340349535, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # way[highway=cycleway][vehicle=no][!bicycle][traffic_sign!~/\bNL:(C0?1|C0?9|C14|C15|D103|D104)\b/][!vehicle:conditional][!bicycle:conditional][inside("NL")]
        if ('highway' in keys and 'vehicle' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'cycleway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'vehicle') == mapcss._value_capture(capture_tags, 1, 'no')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bicycle')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_5f649d1b, '\\bNL:(C0?1|C0?9|C14|C15|D103|D104)\\b'), mapcss._tag_capture(capture_tags, 3, tags, 'traffic_sign'))) and (not mapcss._tag_capture(capture_tags, 4, tags, 'vehicle:conditional')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'bicycle:conditional')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL unusual values")
                # throwWarning:tr("Suspicious combination: {0} together with {1} equals {2}","{0.tag}","{1.tag}","{2.key}={1.value}")
                # assertNoMatch:"way highway=cycleway vehicle=no bicycle:conditional=\"yes @ (sunrise-sunset)\""
                # assertNoMatch:"way highway=cycleway vehicle=no traffic_sign=NL:C01"
                # assertNoMatch:"way highway=cycleway vehicle=no traffic_sign=NL:D104 moped=designated"
                err.append({'class': 90209, 'subclass': 48304768, 'text': mapcss.tr('Suspicious combination: {0} together with {1} equals {2}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.key}={1.value}'))})

        # *[ref:bag][ref:bag!~/(; ?|^)([0-9]{0,3}[1-9]|[0-9]{0,2}[1-9][0-9]|[0-9]?[1-9][0-9]{2})[0-9]{12}($|;)/][inside("NL")]
        if ('ref:bag' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:bag')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_6708cc9b, '(; ?|^)([0-9]{0,3}[1-9]|[0-9]{0,2}[1-9][0-9]|[0-9]?[1-9][0-9]{2})[0-9]{12}($|;)'), mapcss._tag_capture(capture_tags, 1, tags, 'ref:bag'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL unusual values")
                # throwWarning:tr("Invalid value of {0}","{0.key}")
                err.append({'class': 90209, 'subclass': 2021092431, 'text': mapcss.tr('Invalid value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[leisure][surface=gravel][sport~="tennis"][inside("NL")]
        if ('leisure' in keys and 'sport' in keys and 'surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure')) and (mapcss._tag_capture(capture_tags, 1, tags, 'surface') == mapcss._value_capture(capture_tags, 1, 'gravel')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 2, tags, 'sport'), mapcss._value_capture(capture_tags, 2, 'tennis'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL unusual values")
                # throwWarning:tr("unusual value of {0} for {1} (`gravel` in English means `grind` in Dutch)","{1.key}","{2.tag}")
                # suggestAlternative:"surface=clay"
                # assertNoMatch:"way leisure=pitch sport=boules surface=gravel"
                err.append({'class': 90209, 'subclass': 1521090750, 'text': mapcss.tr('unusual value of {0} for {1} (`gravel` in English means `grind` in Dutch)', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # way[name][highway=service][name=~/(?i)(parkeren$|parkeerplaats$|^toegang(sweg)?\s|^richting\s|drive.thro?u(gh)?)/]
        # way[name][highway][name=~/(?i)(^|\sen\s)((on)?verplicht\s)?(\(?brom\)?)?fietspad$/]
        # way[name][highway][name=~/(?i)^roltrap(pen)?$/]
        # way[name][highway][name=~/(?i)(rolstoel|invaliden)/]
        # way[name][highway][name=~/(?i)(uit?laa[dt]|honden.*wandel|los.?loop)/]
        # way[name][highway][name=~/(?i)bus\s?(baan|strook)/][highway!=busway][highway!=service][highway!=construction]
        # way[name][highway][name=~/\bbouwweg/]
        # area[name][name=~/(?i)^wadi$/][tag("natural")||tag("landuse")]
        # area[name][natural=water][name=visvijver]
        # *[name][name="ijsbaan"]
        # *[name][name=~/\b(([Aa]f)?gesloten|[Gg]eopend)\b/]
        # *[name][amenity^=parking][name=~/(?i)(parkeren|parkeerplaats|parkeergarage|^garage)$/]
        # *[name][name=~/(?i)^gratis\s|gratis\)/]
        # *[name][name=~/(?i)(klanten|bezoek(ers)?|medewerkers)\b/][!route]
        # *[name][leisure=playground][name=~/(?i)^speeltuin(tje)?$/]
        # *[name][leisure^=dog][name=~/(?i)^(honden\s?)?(toilet|uitlaa[dt]|los.?loop)/]
        # *[name][leisure=pitch][name=~/(?i)ball?(veld(je)?)?$/][!sport]
        if ('amenity' in keys and 'name' in keys) or ('highway' in keys and 'name' in keys) or ('leisure' in keys and 'name' in keys) or ('name' in keys) or ('name' in keys and 'natural' in keys):
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
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_06ddeafa), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_54e14d8c), mapcss._tag_capture(capture_tags, 1, tags, 'name'))) and (mapcss.tag(tags, 'natural') or mapcss.tag(tags, 'landuse')) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'natural') == mapcss._value_capture(capture_tags, 1, 'water')) and (mapcss._tag_capture(capture_tags, 2, tags, 'name') == mapcss._value_capture(capture_tags, 2, 'visvijver')) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name') == mapcss._value_capture(capture_tags, 1, 'ijsbaan')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_26e04b1e), mapcss._tag_capture(capture_tags, 1, tags, 'name'))))
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
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'leisure') == mapcss._value_capture(capture_tags, 1, 'playground')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_0ec6b360), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
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
                # assertMatch:"way highway=service name=\"McDonalds drive through\""
                # assertMatch:"way highway=service name=\"fiets- en bromfietspad\""
                # assertMatch:"way highway=service name=\"onverplicht fietspad\""
                # assertMatch:"way highway=service name=\"parkeerplaats voor bezoekers\""
                # assertMatch:"way highway=service name=rolstoelpad"
                # assertNoMatch:"way highway=unclassified name=\"Gesloten Stad\""
                # assertNoMatch:"way highway=unclassified name=Landbouwweg"
                err.append({'class': 90203, 'subclass': 2144375058, 'text': mapcss.tr('descriptive name')})

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
                err.append({'class': 90203, 'subclass': 538711457, 'text': mapcss.tr('descriptive name')})

        # way[name][highway][name=~/\b(Adm|Br|Burg|Cmdt|Dr|Drs|Ds|Gebr|Gen|Ing|Ir|Jhr|Kard|Kon|Luit|Mej|Mevr|Mgr|Min|Mr|Past|Pr|Pres|Prof|St|Vr|Weth|Zr)\.? [A-Za-z]/][inside("NL")]!.abbrname
        # way[name][highway][name=~/^[A-Z][a-z]{1,4}\. /][name!~/^(Adr|Anth?|Chr?|Corn|Fred|Hub|Jacq?|Joh|Jos|Mac|Nic|Ph|Th)\./][inside("NL")]!.abbrname
        if ('highway' in keys and 'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_abbrname) and (mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_676d2c9e), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_abbrname) and (mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_293c2706), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_2f938f56, '^(Adr|Anth?|Chr?|Corn|Fred|Hub|Jacq?|Joh|Jos|Mac|Nic|Ph|Th)\\.'), mapcss._tag_capture(capture_tags, 3, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # set .abbrname
                # group:tr("NL nomenclature")
                # throwWarning:tr("Straatnaam met afkorting")
                # assertNoMatch:"way highway=residential name=\"De Visserstraat\""
                # assertNoMatch:"way highway=residential name=\"J.T. de Visserstraat\""
                # assertNoMatch:"way highway=residential name=\"Jac. P. Thijsseplein\""
                # assertNoMatch:"way highway=residential name=\"Th. Weeversweg\""
                # assertNoMatch:"way highway=residential name=\"Wim Kan Dreef\""
                set_abbrname = True
                err.append({'class': 90203, 'subclass': 397885213, 'text': mapcss.tr('Straatnaam met afkorting')})

        # *[name][place][name=~/\b(Adm|Br|Burg|Cmdt|Dr|Drs|Ds|Gebr|Gen|Ing|Ir|Jhr|Kard|Kon|Luit|Mej|Mevr|Mgr|Min|Mr|Past|Pr|Pres|Prof|St|Vr|Weth|Zr)\.? [A-Za-z]/][inside("NL")]!.abbrname
        # *[name][place][name=~/^[A-Z][a-z]{1,4}\. /][name!~/^(Adr|Anth?|Chr?|Corn|Fred|Hub|Jacq?|Joh|Jos|Mac|Nic|Ph|Th)\./][inside("NL")]!.abbrname
        if ('name' in keys and 'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_abbrname) and (mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'place')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_676d2c9e), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_abbrname) and (mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'place')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_293c2706), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_2f938f56, '^(Adr|Anth?|Chr?|Corn|Fred|Hub|Jacq?|Joh|Jos|Mac|Nic|Ph|Th)\\.'), mapcss._tag_capture(capture_tags, 3, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # set .abbrname
                # group:tr("NL nomenclature")
                # throwWarning:tr("Gebiedsnaam met afkorting")
                set_abbrname = True
                err.append({'class': 90203, 'subclass': 1573033356, 'text': mapcss.tr('Gebiedsnaam met afkorting')})

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
                err.append({'class': 90203, 'subclass': 1558593366, 'text': mapcss.tr('Spoorgebied met afgekorte naam')})

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
                err.append({'class': 90203, 'subclass': 1647353731, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [(mapcss._tag_uncapture(capture_tags, '{0.key}=>{1.key}')).split('=>', 1)[1].strip(), mapcss.tag(tags, (mapcss._tag_uncapture(capture_tags, '{0.key}=>{1.key}')).split('=>', 1)[0].strip())]]),
                    '-': ([
                    (mapcss._tag_uncapture(capture_tags, '{0.key}=>{1.key}')).split('=>', 1)[0].strip()])
                }})

        # *[heritage=2][heritage:operator!=rce][heritage:operator!~/(^|; ?)rce(;|$)/][inside("NL")]
        if ('heritage' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'heritage') == mapcss._value_capture(capture_tags, 0, 2)) and (mapcss._tag_capture(capture_tags, 1, tags, 'heritage:operator') != mapcss._value_const_capture(capture_tags, 1, 'rce', 'rce')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_3da90af7, '(^|; ?)rce(;|$)'), mapcss._tag_capture(capture_tags, 2, tags, 'heritage:operator'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL heritage")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.tag}")
                # fixAdd:"heritage:operator=rce"
                err.append({'class': 90204, 'subclass': 675628887, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['heritage:operator','rce']])
                }})

        # *[heritage:operator=rce][!heritage][inside("NL")]
        if ('heritage:operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'heritage:operator') == mapcss._value_capture(capture_tags, 0, 'rce')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'heritage')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL heritage")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}=*")
                # fixAdd:"heritage=2"
                err.append({'class': 90204, 'subclass': 1113141518, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}=*')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['heritage','2']])
                }})

        # way[highway=living_street][maxspeed!=15][!/^maxspeed(:forward|:backward|:both_ways)?$/][inside("NL")]
        # way[living_street=yes][maxspeed!=15][!/^maxspeed(:forward|:backward|:both_ways)?$/][inside("NL")][highway=~/^(path|cycleway|bridleway)$/][moped][moped!~/^(no|use_sidepath)$/]
        # way[living_street=yes][maxspeed!=15][!/^maxspeed(:forward|:backward|:both_ways)?$/][inside("NL")][highway!~/^(path|cycleway|bridleway|footway|living_street)$/]
        # way[maxspeed:type="NL:zone30"][maxspeed!=30][!maxspeed][maxspeed:both_ways!=30][highway]
        # way[maxspeed:type="NL:zone60"][maxspeed!=60][!maxspeed][maxspeed:both_ways!=60][highway]
        # way[maxspeed:type="NL:urban"][maxspeed!=50][!maxspeed][maxspeed:both_ways!=50][highway][highway!=cycleway]
        # way[maxspeed:type="NL:rural"][maxspeed!=80][!maxspeed][maxspeed:both_ways!=80][highway][highway!=cycleway]
        if ('highway' in keys) or ('highway' in keys and 'living_street' in keys and 'moped' in keys) or ('highway' in keys and 'maxspeed:type' in keys) or ('living_street' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'living_street')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed') != mapcss._value_capture(capture_tags, 1, 15)) and (not mapcss._tag_capture(capture_tags, 2, tags, self.re_1d614d5c)) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'living_street') == mapcss._value_capture(capture_tags, 0, 'yes')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed') != mapcss._value_capture(capture_tags, 1, 15)) and (not mapcss._tag_capture(capture_tags, 2, tags, self.re_1d614d5c)) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 4, self.re_736e42c8), mapcss._tag_capture(capture_tags, 4, tags, 'highway'))) and (mapcss._tag_capture(capture_tags, 5, tags, 'moped')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 6, self.re_143f11c5, '^(no|use_sidepath)$'), mapcss._tag_capture(capture_tags, 6, tags, 'moped'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'living_street') == mapcss._value_capture(capture_tags, 0, 'yes')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed') != mapcss._value_capture(capture_tags, 1, 15)) and (not mapcss._tag_capture(capture_tags, 2, tags, self.re_1d614d5c)) and (mapcss.inside(self.father.config.options, 'NL')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 4, self.re_74d217a6, '^(path|cycleway|bridleway|footway|living_street)$'), mapcss._tag_capture(capture_tags, 4, tags, 'highway'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:type') == mapcss._value_capture(capture_tags, 0, 'NL:zone30')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed') != mapcss._value_capture(capture_tags, 1, 30)) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed')) and (mapcss._tag_capture(capture_tags, 3, tags, 'maxspeed:both_ways') != mapcss._value_capture(capture_tags, 3, 30)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:type') == mapcss._value_capture(capture_tags, 0, 'NL:zone60')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed') != mapcss._value_capture(capture_tags, 1, 60)) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed')) and (mapcss._tag_capture(capture_tags, 3, tags, 'maxspeed:both_ways') != mapcss._value_capture(capture_tags, 3, 60)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:type') == mapcss._value_capture(capture_tags, 0, 'NL:urban')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed') != mapcss._value_capture(capture_tags, 1, 50)) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed')) and (mapcss._tag_capture(capture_tags, 3, tags, 'maxspeed:both_ways') != mapcss._value_capture(capture_tags, 3, 50)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'cycleway', 'cycleway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:type') == mapcss._value_capture(capture_tags, 0, 'NL:rural')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed') != mapcss._value_capture(capture_tags, 1, 80)) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed')) and (mapcss._tag_capture(capture_tags, 3, tags, 'maxspeed:both_ways') != mapcss._value_capture(capture_tags, 3, 80)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway') != mapcss._value_const_capture(capture_tags, 5, 'cycleway', 'cycleway')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL speed limits")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.tag}")
                # assertNoMatch:"way highway=cycleway living_street=yes moped=no"
                # assertNoMatch:"way highway=cycleway living_street=yes moped=yes maxspeed=15"
                # assertNoMatch:"way highway=cycleway living_street=yes"
                # assertNoMatch:"way highway=cycleway maxspeed:type=NL:rural"
                # assertNoMatch:"way highway=footway living_street=yes"
                # assertNoMatch:"way highway=living_street maxspeed=10 traffic_sign=\"NL:A01-10\""
                # assertNoMatch:"way highway=living_street maxspeed=18"
                # assertMatch:"way highway=residential maxspeed:type=NL:rural"
                # assertNoMatch:"way highway=residential source:maxspeed=NL:rural"
                err.append({'class': 90207, 'subclass': 1217260303, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # way[maxspeed:type="NL:zone30"][maxspeed][maxspeed!=30][highway]
        # way[maxspeed:type="NL:zone60"][maxspeed][maxspeed!=60][highway]
        # way[maxspeed:type="NL:urban"][maxspeed][maxspeed!=50][highway][highway!=cycleway]
        # way[maxspeed:type="NL:rural"][maxspeed][maxspeed!=80][highway][highway!=cycleway]
        # way[source:maxspeed="NL:zone30"][maxspeed][maxspeed!=30][highway]
        # way[source:maxspeed="NL:zone60"][maxspeed][maxspeed!=60][highway]
        # way[source:maxspeed="NL:urban"][maxspeed][maxspeed!=50][highway][highway!=cycleway]
        # way[source:maxspeed="NL:rural"][maxspeed][maxspeed!=80][highway][highway!=cycleway]
        if ('highway' in keys and 'maxspeed' in keys and 'maxspeed:type' in keys) or ('highway' in keys and 'maxspeed' in keys and 'source:maxspeed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:type') == mapcss._value_capture(capture_tags, 0, 'NL:zone30')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed') != mapcss._value_capture(capture_tags, 2, 30)) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:type') == mapcss._value_capture(capture_tags, 0, 'NL:zone60')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed') != mapcss._value_capture(capture_tags, 2, 60)) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:type') == mapcss._value_capture(capture_tags, 0, 'NL:urban')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed') != mapcss._value_capture(capture_tags, 2, 50)) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'cycleway', 'cycleway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:type') == mapcss._value_capture(capture_tags, 0, 'NL:rural')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed') != mapcss._value_capture(capture_tags, 2, 80)) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'cycleway', 'cycleway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:maxspeed') == mapcss._value_capture(capture_tags, 0, 'NL:zone30')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed') != mapcss._value_capture(capture_tags, 2, 30)) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:maxspeed') == mapcss._value_capture(capture_tags, 0, 'NL:zone60')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed') != mapcss._value_capture(capture_tags, 2, 60)) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:maxspeed') == mapcss._value_capture(capture_tags, 0, 'NL:urban')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed') != mapcss._value_capture(capture_tags, 2, 50)) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'cycleway', 'cycleway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:maxspeed') == mapcss._value_capture(capture_tags, 0, 'NL:rural')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed') != mapcss._value_capture(capture_tags, 2, 80)) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway') != mapcss._value_const_capture(capture_tags, 4, 'cycleway', 'cycleway')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL speed limits")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # assertMatch:"way highway=primary maxspeed:type=NL:rural maxspeed=50"
                # assertNoMatch:"way highway=primary maxspeed:type=NL:zone30"
                # assertMatch:"way highway=primary source:maxspeed=NL:zone60 maxspeed=50"
                err.append({'class': 90207, 'subclass': 1487727138, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # way[maxspeed:type][!maxspeed][maxspeed:type^="NL:zone"][!maxspeed:both_ways][maxspeed:type!~/^NL:zone[36]0$/][highway]
        # way[traffic_sign][!maxspeed][traffic_sign=~/(^|; ?)NL:A0?1-/][!/^maxspeed(:forward|:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:forward][!maxspeed:forward][traffic_sign:forward=~/(^|; ?)NL:A0?1-/][!/^maxspeed(:forward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:backward][!maxspeed:backward][traffic_sign:backward=~/(^|; ?)NL:A0?1-/][!/^maxspeed(:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign][!maxspeed:advisory][traffic_sign=~/(^|; ?)NL:A0?4\b/][!/^maxspeed:advisory(:forward|:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:forward][!maxspeed:advisory:forward][traffic_sign:forward=~/(^|; ?)NL:A0?4\b/][!/^maxspeed:advisory(:forward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign:backward][!maxspeed:advisory:backward][traffic_sign:backward=~/(^|; ?)NL:A0?4\b/][!/^maxspeed:advisory(:backward|:both_ways)?(:conditional)?$/][highway]
        if ('highway' in keys and 'maxspeed:type' in keys) or ('highway' in keys and 'traffic_sign' in keys) or ('highway' in keys and 'traffic_sign:backward' in keys) or ('highway' in keys and 'traffic_sign:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:type')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss.startswith(mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed:type'), mapcss._value_capture(capture_tags, 2, 'NL:zone'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'maxspeed:both_ways')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 4, self.re_1d0c9a01, '^NL:zone[36]0$'), mapcss._tag_capture(capture_tags, 4, tags, 'maxspeed:type'))) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_4547b418), mapcss._tag_capture(capture_tags, 2, tags, 'traffic_sign'))) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_7acb98bb)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:forward')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:forward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_4547b418), mapcss._tag_capture(capture_tags, 2, tags, 'traffic_sign:forward'))) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_0cbcfeaf)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:backward')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:backward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_4547b418), mapcss._tag_capture(capture_tags, 2, tags, 'traffic_sign:backward'))) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_1cc9227a)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:advisory')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_5a895116), mapcss._tag_capture(capture_tags, 2, tags, 'traffic_sign'))) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_06bae8ee)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:forward')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:advisory:forward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_5a895116), mapcss._tag_capture(capture_tags, 2, tags, 'traffic_sign:forward'))) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_08935e4d)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign:backward')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:advisory:backward')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_5a895116), mapcss._tag_capture(capture_tags, 2, tags, 'traffic_sign:backward'))) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_460900e8)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL speed limits")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}")
                # assertNoMatch:"way highway=residential maxspeed:type=\"NL:zone20\" maxspeed=20"
                # assertMatch:"way highway=residential maxspeed:type=\"NL:zone20\""
                # assertNoMatch:"way highway=residential traffic_sign:forward=NL:A1-30 maxspeed:forward=30"
                # assertMatch:"way highway=residential traffic_sign:forward=NL:A1-30-ZB"
                # assertNoMatch:"way highway=residential traffic_sign=\"NL:A4[50]\" maxspeed:advisory:both_ways=50"
                # assertMatch:"way highway=residential traffic_sign=\"NL:A4[60]\""
                # assertMatch:"way highway=residential traffic_sign=\"NL:C16; NL:A01-30\""
                # assertMatch:"way highway=residential traffic_sign=\"NL:C16;NL:A01-30\""
                # assertNoMatch:"way highway=residential traffic_sign=NL:A01-30 maxspeed=30"
                # assertMatch:"way highway=residential traffic_sign=NL:A01-30"
                # assertMatch:"way highway=residential traffic_sign=NL:A04-30"
                # assertMatch:"way highway=residential traffic_sign=NL:A4"
                err.append({'class': 90207, 'subclass': 1250414020, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

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
                err.append({'class': 90207, 'subclass': 640790005, 'text': mapcss.tr('Agreed upon was to use 100 as the maximum speed and {0} as the conditional maximum speed', mapcss._tag_uncapture(capture_tags, '{1.value}'))})

        # way[highway=motorway][maxspeed][maxspeed>130][inside("NL")]
        # way[highway=motorway_link][maxspeed][maxspeed>130][inside("NL")]
        # way[highway=trunk][maxspeed][maxspeed>100][inside("NL")]
        # way[highway=trunk_link][maxspeed][maxspeed>100][inside("NL")]
        # way[motorroad=yes][maxspeed][maxspeed>100][inside("NL")][highway!~/^(motorway(_link)?|construction|proposed)$/]
        # way[highway][maxspeed][maxspeed>80][highway!~/^(motorway(_link)?|trunk(_link)?|cycleway|service|busway|construction|proposed|raceway)$/][motorroad!=yes][inside("NL")]
        # way[highway=cycleway][maxspeed][maxspeed>40][!/^(access|vehicle|motor_vehicle)(:forward|:backward|:both_ways)?(:conditional)?$/][inside("NL")]
        if ('highway' in keys and 'maxspeed' in keys) or ('maxspeed' in keys and 'motorroad' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'motorway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed') > mapcss._value_capture(capture_tags, 2, 130)) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'motorway_link')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed') > mapcss._value_capture(capture_tags, 2, 130)) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'trunk')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed') > mapcss._value_capture(capture_tags, 2, 100)) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'trunk_link')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed') > mapcss._value_capture(capture_tags, 2, 100)) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'motorroad') == mapcss._value_capture(capture_tags, 0, 'yes')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed') > mapcss._value_capture(capture_tags, 2, 100)) and (mapcss.inside(self.father.config.options, 'NL')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 4, self.re_62e192cf, '^(motorway(_link)?|construction|proposed)$'), mapcss._tag_capture(capture_tags, 4, tags, 'highway'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed') > mapcss._value_capture(capture_tags, 2, 80)) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_39064d44, '^(motorway(_link)?|trunk(_link)?|cycleway|service|busway|construction|proposed|raceway)$'), mapcss._tag_capture(capture_tags, 3, tags, 'highway'))) and (mapcss._tag_capture(capture_tags, 4, tags, 'motorroad') != mapcss._value_const_capture(capture_tags, 4, 'yes', 'yes')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'cycleway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed') > mapcss._value_capture(capture_tags, 2, 40)) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_70e165b6)) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL speed limits")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # assertNoMatch:"way highway=cycleway maxspeed=80 motor_vehicle:conditional=\"yes @ Sa-Su\""
                # assertNoMatch:"way highway=cycleway maxspeed=80 motor_vehicle=destination"
                # assertNoMatch:"way highway=motorway maxspeed=120"
                # assertNoMatch:"way highway=motorway_link motorroad=yes maxspeed=130"
                # assertNoMatch:"way highway=tertiary motorroad=yes maxspeed=100"
                # assertNoMatch:"way highway=trunk maxspeed=90"
                # assertNoMatch:"way highway=trunk_link maxspeed=100"
                # assertNoMatch:"way highway=unclassified maxspeed=80"
                err.append({'class': 90207, 'subclass': 2041800782, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # way[maxspeed:mofa][maxspeed:mofa>25][inside("NL")]
        # way[maxspeed:moped][maxspeed:moped>45][inside("NL")]
        # way[maxspeed:bus][maxspeed:bus>100][inside("NL")]
        # way[maxspeed:trailer][maxspeed:trailer>90][inside("NL")]
        # way[maxspeed:hgv][maxspeed:hgv>80][inside("NL")]
        if ('maxspeed:bus' in keys) or ('maxspeed:hgv' in keys) or ('maxspeed:mofa' in keys) or ('maxspeed:moped' in keys) or ('maxspeed:trailer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:mofa')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:mofa') > mapcss._value_capture(capture_tags, 1, 25)) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:moped')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:moped') > mapcss._value_capture(capture_tags, 1, 45)) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:bus')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:bus') > mapcss._value_capture(capture_tags, 1, 100)) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:trailer')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:trailer') > mapcss._value_capture(capture_tags, 1, 90)) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:hgv')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:hgv') > mapcss._value_capture(capture_tags, 1, 80)) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL speed limits")
                # throwWarning:tr("{0} overschrijdt de maximumsnelheid van RVV art. 22","{0.tag}")
                # assertNoMatch:"way highway=unclassified maxspeed:moped=45"
                err.append({'class': 90207, 'subclass': 790150725, 'text': mapcss.tr('{0} overschrijdt de maximumsnelheid van RVV art. 22', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # way[highway=living_street][maxspeed][maxspeed>15][inside("NL")][maxspeed<=20]
        # way[living_street=yes][maxspeed][maxspeed>15][highway!=living_street][inside("NL")]
        if ('highway' in keys and 'maxspeed' in keys) or ('living_street' in keys and 'maxspeed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'living_street')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed') > mapcss._value_capture(capture_tags, 2, 15)) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, 4, tags, 'maxspeed') <= mapcss._value_capture(capture_tags, 4, 20)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'living_street') == mapcss._value_capture(capture_tags, 0, 'yes')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed') > mapcss._value_capture(capture_tags, 2, 15)) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'living_street', 'living_street')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL speed limits")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # assertNoMatch:"way highway=living_street maxspeed=10 traffic_sign=\"NL:A01-10\""
                err.append({'class': 90207, 'subclass': 1145458059, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # way[maxspeed][maxspeed=~/[1-9]$/][maxspeed!=5][maxspeed!=15][highway=~/^(residential|unclassified|tertiary|secondary|primary|trunk|motorway|busway)(_link)?$/][!access][!vehicle][!motor_vehicle][inside("NL")]
        # way[maxspeed=20][highway=~/^(residential|unclassified|tertiary|secondary|primary|trunk|motorway|busway)(_link)?$/][!access][!vehicle][!motor_vehicle][source:maxspeed!="NL:zone20"][maxspeed:type!="NL:zone20"][inside("NL")]
        # way[maxspeed=40][highway=~/^(residential|unclassified|tertiary|secondary|primary|trunk|motorway|busway)(_link)?$/][!access][!vehicle][!motor_vehicle][source:maxspeed!="NL:zone40"][maxspeed:type!="NL:zone40"][inside("NL")]
        if ('highway' in keys and 'maxspeed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5fbb635f), mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed') != mapcss._value_capture(capture_tags, 2, 5)) and (mapcss._tag_capture(capture_tags, 3, tags, 'maxspeed') != mapcss._value_capture(capture_tags, 3, 15)) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 4, self.re_251abd6a), mapcss._tag_capture(capture_tags, 4, tags, 'highway'))) and (not mapcss._tag_capture(capture_tags, 5, tags, 'access')) and (not mapcss._tag_capture(capture_tags, 6, tags, 'vehicle')) and (not mapcss._tag_capture(capture_tags, 7, tags, 'motor_vehicle')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed') == mapcss._value_capture(capture_tags, 0, 20)) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_251abd6a), mapcss._tag_capture(capture_tags, 1, tags, 'highway'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'access')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'vehicle')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'motor_vehicle')) and (mapcss._tag_capture(capture_tags, 5, tags, 'source:maxspeed') != mapcss._value_const_capture(capture_tags, 5, 'NL:zone20', 'NL:zone20')) and (mapcss._tag_capture(capture_tags, 6, tags, 'maxspeed:type') != mapcss._value_const_capture(capture_tags, 6, 'NL:zone20', 'NL:zone20')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed') == mapcss._value_capture(capture_tags, 0, 40)) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_251abd6a), mapcss._tag_capture(capture_tags, 1, tags, 'highway'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'access')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'vehicle')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'motor_vehicle')) and (mapcss._tag_capture(capture_tags, 5, tags, 'source:maxspeed') != mapcss._value_const_capture(capture_tags, 5, 'NL:zone40', 'NL:zone40')) and (mapcss._tag_capture(capture_tags, 6, tags, 'maxspeed:type') != mapcss._value_const_capture(capture_tags, 6, 'NL:zone40', 'NL:zone40')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL speed limits")
                # throwWarning:tr("{0} is a non-standard speed limit. Possibly this is an advisory speed limit instead?","{0.tag}")
                # assertNoMatch:"way highway=cycleway maxspeed=40"
                # assertNoMatch:"way highway=residential maxspeed=30"
                # assertNoMatch:"way highway=unclassified access=permissive note=eigen_weg maxspeed=25"
                err.append({'class': 90207, 'subclass': 293871183, 'text': mapcss.tr('{0} is a non-standard speed limit. Possibly this is an advisory speed limit instead?', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # way[bicycle:conditional][moped:conditional][bicycle:conditional=*"moped:conditional"][!mofa:conditional][inside("NL")]
        # way[bicycle:forward][moped:forward][bicycle:forward=*"moped:forward"][!mofa:forward][!mofa][!mofa:both_ways][bicycle:forward!=designated][bicycle:forward!=yes][inside("NL")]
        # way[bicycle:backward][moped:backward][bicycle:backward=*"moped:backward"][!mofa:backward][!mofa][!mofa:both_ways][bicycle:backward!=designated][bicycle:backward!=yes][inside("NL")]
        # way[bicycle:both_ways][moped:both_ways][bicycle:both_ways=*"moped:both_ways"][!mofa:both_ways][!mofa][bicycle:both_ways!=designated][bicycle:both_ways!=yes][inside("NL")]
        # way[bicycle][moped][bicycle=*moped][!mofa][bicycle!=designated][bicycle!=yes][inside("NL")]
        if ('bicycle' in keys and 'moped' in keys) or ('bicycle:backward' in keys and 'moped:backward' in keys) or ('bicycle:both_ways' in keys and 'moped:both_ways' in keys) or ('bicycle:conditional' in keys and 'moped:conditional' in keys) or ('bicycle:forward' in keys and 'moped:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bicycle:conditional')) and (mapcss._tag_capture(capture_tags, 1, tags, 'moped:conditional')) and (mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:conditional') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'moped:conditional'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'mofa:conditional')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bicycle:forward')) and (mapcss._tag_capture(capture_tags, 1, tags, 'moped:forward')) and (mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:forward') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'moped:forward'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'mofa:forward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'mofa')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'mofa:both_ways')) and (mapcss._tag_capture(capture_tags, 6, tags, 'bicycle:forward') != mapcss._value_const_capture(capture_tags, 6, 'designated', 'designated')) and (mapcss._tag_capture(capture_tags, 7, tags, 'bicycle:forward') != mapcss._value_const_capture(capture_tags, 7, 'yes', 'yes')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bicycle:backward')) and (mapcss._tag_capture(capture_tags, 1, tags, 'moped:backward')) and (mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:backward') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'moped:backward'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'mofa:backward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'mofa')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'mofa:both_ways')) and (mapcss._tag_capture(capture_tags, 6, tags, 'bicycle:backward') != mapcss._value_const_capture(capture_tags, 6, 'designated', 'designated')) and (mapcss._tag_capture(capture_tags, 7, tags, 'bicycle:backward') != mapcss._value_const_capture(capture_tags, 7, 'yes', 'yes')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bicycle:both_ways')) and (mapcss._tag_capture(capture_tags, 1, tags, 'moped:both_ways')) and (mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:both_ways') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'moped:both_ways'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'mofa:both_ways')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'mofa')) and (mapcss._tag_capture(capture_tags, 5, tags, 'bicycle:both_ways') != mapcss._value_const_capture(capture_tags, 5, 'designated', 'designated')) and (mapcss._tag_capture(capture_tags, 6, tags, 'bicycle:both_ways') != mapcss._value_const_capture(capture_tags, 6, 'yes', 'yes')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bicycle')) and (mapcss._tag_capture(capture_tags, 1, tags, 'moped')) and (mapcss._tag_capture(capture_tags, 2, tags, 'bicycle') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'moped'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'mofa')) and (mapcss._tag_capture(capture_tags, 4, tags, 'bicycle') != mapcss._value_const_capture(capture_tags, 4, 'designated', 'designated')) and (mapcss._tag_capture(capture_tags, 5, tags, 'bicycle') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL mofa tagging")
                # throwWarning:tr("{0} and {1} without {2}","{0.tag}","{1.tag}","{3.key}={0.value}")
                # fixAdd:"{3.key}={0.value}"
                err.append({'class': 90208, 'subclass': 643990767, 'text': mapcss.tr('{0} and {1} without {2}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{3.key}={0.value}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, '{3.key}={0.value}')).split('=', 1)])
                }})

        # way[bicycle:forward][moped:forward][bicycle:forward=*"moped:forward"][!mofa:forward][/^(access|vehicle|motor_vehicle)(:forward|:both_ways)?(:conditional)?$/][!mofa][!mofa:both_ways][bicycle:forward=~/^(yes|designated)$/][join_list(";",uniq_list(tag_regex("^(access|vehicle|motor_vehicle)(:forward|:both_ways)?(:conditional)?$")))!=tag("bicycle:forward")][inside("NL")]
        # way[bicycle:backward][moped:backward][bicycle:backward=*"moped:backward"][!mofa:backward][/^(access|vehicle|motor_vehicle)(:backward|:both_ways)?(:conditional)?$/][!mofa][!mofa:both_ways][bicycle:backward=~/^(yes|designated)$/][join_list(";",uniq_list(tag_regex("^(access|vehicle|motor_vehicle)(:backward|:both_ways)?(:conditional)?$")))!=tag("bicycle:backward")][inside("NL")]
        # way[bicycle][moped][bicycle=*moped][!mofa][/^(access|vehicle|motor_vehicle)(:forward|:backward|:both_ways)?(:conditional)?$/][!mofa:both_ways][bicycle=~/^(yes|designated)$/][join_list(";",uniq_list(tag_regex("^(access|vehicle|motor_vehicle)(:forward|:backward|:both_ways)?(:conditional)?$")))!=tag("bicycle")][inside("NL")]
        if ('bicycle' in keys and 'moped' in keys) or ('bicycle:backward' in keys and 'moped:backward' in keys) or ('bicycle:forward' in keys and 'moped:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bicycle:forward')) and (mapcss._tag_capture(capture_tags, 1, tags, 'moped:forward')) and (mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:forward') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'moped:forward'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'mofa:forward')) and (mapcss._tag_capture(capture_tags, 4, tags, self.re_1cfba619)) and (not mapcss._tag_capture(capture_tags, 5, tags, 'mofa')) and (not mapcss._tag_capture(capture_tags, 6, tags, 'mofa:both_ways')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 7, self.re_47aaa0f7), mapcss._tag_capture(capture_tags, 7, tags, 'bicycle:forward'))) and (mapcss.join_list(';', mapcss.uniq_list(mapcss.tag_regex(tags, self.re_1cfba619))) != mapcss.tag(tags, 'bicycle:forward')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bicycle:backward')) and (mapcss._tag_capture(capture_tags, 1, tags, 'moped:backward')) and (mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:backward') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'moped:backward'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'mofa:backward')) and (mapcss._tag_capture(capture_tags, 4, tags, self.re_374703cf)) and (not mapcss._tag_capture(capture_tags, 5, tags, 'mofa')) and (not mapcss._tag_capture(capture_tags, 6, tags, 'mofa:both_ways')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 7, self.re_47aaa0f7), mapcss._tag_capture(capture_tags, 7, tags, 'bicycle:backward'))) and (mapcss.join_list(';', mapcss.uniq_list(mapcss.tag_regex(tags, self.re_374703cf))) != mapcss.tag(tags, 'bicycle:backward')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bicycle')) and (mapcss._tag_capture(capture_tags, 1, tags, 'moped')) and (mapcss._tag_capture(capture_tags, 2, tags, 'bicycle') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'moped'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'mofa')) and (mapcss._tag_capture(capture_tags, 4, tags, self.re_70e165b6)) and (not mapcss._tag_capture(capture_tags, 5, tags, 'mofa:both_ways')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 6, self.re_47aaa0f7), mapcss._tag_capture(capture_tags, 6, tags, 'bicycle'))) and (mapcss.join_list(';', mapcss.uniq_list(mapcss.tag_regex(tags, self.re_70e165b6))) != mapcss.tag(tags, 'bicycle')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasAddMofaPositive
                # group:tr("NL mofa tagging")
                # throwWarning:tr("{0}, {1} and {2} without {3}","{0.tag}","{1.tag}","{4.tag}","{3.key}={0.value}")
                # fixAdd:"{3.key}={0.value}"
                # assertNoMatch:"way bicycle=designated moped=designated highway=residential access=designated"
                # assertNoMatch:"way bicycle=designated moped=designated highway=residential"
                # assertNoMatch:"way bicycle=designated moped=designated mofa=designated highway=residential access=no"
                set_hasAddMofaPositive = True
                err.append({'class': 90208, 'subclass': 2061019359, 'text': mapcss.tr('{0}, {1} and {2} without {3}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{4.tag}'), mapcss._tag_uncapture(capture_tags, '{3.key}={0.value}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, '{3.key}={0.value}')).split('=', 1)])
                }})

        # way[bicycle:forward][moped:forward][bicycle:forward=*"moped:forward"][!mofa:forward][!mofa][!mofa:both_ways][bicycle:forward=~/^(yes|designated)$/][highway=~/^(trunk|motorway|busway|path|busway|bridleway|footway|pedestrian)(_link)?$/][inside("NL")]!.hasAddMofaPositive
        # way[bicycle:backward][moped:backward][bicycle:backward=*"moped:backward"][!mofa:backward][!mofa][!mofa:both_ways][bicycle:backward=~/^(yes|designated)$/][highway=~/^(trunk|motorway|busway|path|busway|bridleway|footway|pedestrian)(_link)?$/][inside("NL")]!.hasAddMofaPositive
        # way[bicycle][moped][bicycle=*moped][!mofa][!mofa:both_ways][bicycle=~/^(yes|designated)$/][highway=~/^(trunk|motorway|busway|path|busway|bridleway|footway|pedestrian)(_link)?$/][inside("NL")]!.hasAddMofaPositive
        # way[bicycle:forward][moped:forward][bicycle:forward=*"moped:forward"][!mofa:forward][!mofa][!mofa:both_ways][bicycle:forward=~/^(yes|designated)$/][!highway][inside("NL")]!.hasAddMofaPositive
        # way[bicycle:backward][moped:backward][bicycle:backward=*"moped:backward"][!mofa:backward][!mofa][!mofa:both_ways][bicycle:backward=~/^(yes|designated)$/][!highway][inside("NL")]!.hasAddMofaPositive
        # way[bicycle][moped][bicycle=*moped][!mofa][!mofa:both_ways][bicycle=~/^(yes|designated)$/][!highway][inside("NL")]!.hasAddMofaPositive
        if ('bicycle' in keys and 'highway' in keys and 'moped' in keys) or ('bicycle' in keys and 'moped' in keys) or ('bicycle:backward' in keys and 'highway' in keys and 'moped:backward' in keys) or ('bicycle:backward' in keys and 'moped:backward' in keys) or ('bicycle:forward' in keys and 'highway' in keys and 'moped:forward' in keys) or ('bicycle:forward' in keys and 'moped:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasAddMofaPositive) and (mapcss._tag_capture(capture_tags, 0, tags, 'bicycle:forward')) and (mapcss._tag_capture(capture_tags, 1, tags, 'moped:forward')) and (mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:forward') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'moped:forward'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'mofa:forward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'mofa')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'mofa:both_ways')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 6, self.re_47aaa0f7), mapcss._tag_capture(capture_tags, 6, tags, 'bicycle:forward'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 7, self.re_6460cbf8), mapcss._tag_capture(capture_tags, 7, tags, 'highway'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasAddMofaPositive) and (mapcss._tag_capture(capture_tags, 0, tags, 'bicycle:backward')) and (mapcss._tag_capture(capture_tags, 1, tags, 'moped:backward')) and (mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:backward') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'moped:backward'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'mofa:backward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'mofa')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'mofa:both_ways')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 6, self.re_47aaa0f7), mapcss._tag_capture(capture_tags, 6, tags, 'bicycle:backward'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 7, self.re_6460cbf8), mapcss._tag_capture(capture_tags, 7, tags, 'highway'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasAddMofaPositive) and (mapcss._tag_capture(capture_tags, 0, tags, 'bicycle')) and (mapcss._tag_capture(capture_tags, 1, tags, 'moped')) and (mapcss._tag_capture(capture_tags, 2, tags, 'bicycle') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'moped'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'mofa')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'mofa:both_ways')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 5, self.re_47aaa0f7), mapcss._tag_capture(capture_tags, 5, tags, 'bicycle'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 6, self.re_6460cbf8), mapcss._tag_capture(capture_tags, 6, tags, 'highway'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasAddMofaPositive) and (mapcss._tag_capture(capture_tags, 0, tags, 'bicycle:forward')) and (mapcss._tag_capture(capture_tags, 1, tags, 'moped:forward')) and (mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:forward') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'moped:forward'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'mofa:forward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'mofa')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'mofa:both_ways')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 6, self.re_47aaa0f7), mapcss._tag_capture(capture_tags, 6, tags, 'bicycle:forward'))) and (not mapcss._tag_capture(capture_tags, 7, tags, 'highway')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasAddMofaPositive) and (mapcss._tag_capture(capture_tags, 0, tags, 'bicycle:backward')) and (mapcss._tag_capture(capture_tags, 1, tags, 'moped:backward')) and (mapcss._tag_capture(capture_tags, 2, tags, 'bicycle:backward') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'moped:backward'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'mofa:backward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'mofa')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'mofa:both_ways')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 6, self.re_47aaa0f7), mapcss._tag_capture(capture_tags, 6, tags, 'bicycle:backward'))) and (not mapcss._tag_capture(capture_tags, 7, tags, 'highway')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasAddMofaPositive) and (mapcss._tag_capture(capture_tags, 0, tags, 'bicycle')) and (mapcss._tag_capture(capture_tags, 1, tags, 'moped')) and (mapcss._tag_capture(capture_tags, 2, tags, 'bicycle') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'moped'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'mofa')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'mofa:both_ways')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 5, self.re_47aaa0f7), mapcss._tag_capture(capture_tags, 5, tags, 'bicycle'))) and (not mapcss._tag_capture(capture_tags, 6, tags, 'highway')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasAddMofaPositive
                # group:tr("NL mofa tagging")
                # throwWarning:tr("{0} and {1} without {2}","{0.tag}","{1.tag}","{3.key}={0.value}")
                # fixAdd:"{3.key}={0.value}"
                # assertNoMatch:"way bicycle=designated moped=designated highway=residential"
                # assertNoMatch:"way bicycle=designated moped=designated mofa=designated highway=busway"
                # assertNoMatch:"way bicycle=designated moped=destination highway=busway"
                set_hasAddMofaPositive = True
                err.append({'class': 90208, 'subclass': 1443086133, 'text': mapcss.tr('{0} and {1} without {2}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{3.key}={0.value}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, '{3.key}={0.value}')).split('=', 1)])
                }})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_abbrname = set_addrOnBuilding = set_altLivingStreet = set_badPhoneNumber = set_completedSurfacePavingStonesNumber = set_hasAddMofaPositive = set_housenameWithFix = set_markedSteps = set_multipleGsigns = set_stepsWithBicycleRamp = False

        # *[contact:phone=~/^(00|\+)31 ?0( ?[0-9]){7,}/]
        # *[contact:mobile=~/^(00|\+)31 ?0( ?[0-9]){7,}/]
        # *[contact:whatsapp=~/^(00|\+)31 ?0( ?[0-9]){7,}/]
        # *[phone=~/^(00|\+)31 ?0( ?[0-9]){7,}/]
        if ('contact:mobile' in keys) or ('contact:phone' in keys) or ('contact:whatsapp' in keys) or ('phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_594405dc), mapcss._tag_capture(capture_tags, 0, tags, 'contact:phone'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_594405dc), mapcss._tag_capture(capture_tags, 0, tags, 'contact:mobile'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_594405dc), mapcss._tag_capture(capture_tags, 0, tags, 'contact:whatsapp'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_594405dc), mapcss._tag_capture(capture_tags, 0, tags, 'phone'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .badPhoneNumber
                # group:tr("NL addresses and contacts")
                # throwWarning:tr("Invalid tag {0}: country code should not be followed by a 0","{0.key}")
                set_badPhoneNumber = True
                err.append({'class': 90201, 'subclass': 1739574763, 'text': mapcss.tr('Invalid tag {0}: country code should not be followed by a 0', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[contact:phone=~/^(\+|00)31 ?0?( ?[0-9]){3,6}$/]
        # *[contact:mobile=~/^(\+|00)31 ?0?( ?[0-9]){3,6}$/]
        # *[phone=~/^(\+|00)31 ?0?( ?[0-9]){3,6}$/]
        if ('contact:mobile' in keys) or ('contact:phone' in keys) or ('phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_287f5dd8), mapcss._tag_capture(capture_tags, 0, tags, 'contact:phone'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_287f5dd8), mapcss._tag_capture(capture_tags, 0, tags, 'contact:mobile'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_287f5dd8), mapcss._tag_capture(capture_tags, 0, tags, 'phone'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .badPhoneNumber
                # group:tr("NL addresses and contacts")
                # throwWarning:tr("Invalid tag {0}: short phone numbers cannot be used with international prefix (or: wrong phone number length)","{0.key}")
                set_badPhoneNumber = True
                err.append({'class': 90201, 'subclass': 345342642, 'text': mapcss.tr('Invalid tag {0}: short phone numbers cannot be used with international prefix (or: wrong phone number length)', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[contact:phone=~/^(0031|\+31|0) ?[1-9]( ?[0-9]){11}/][inside("NL")]!.badPhoneNumber
        # *[contact:mobile=~/^(0031|\+31|0) ?[1-9]( ?[0-9]){11}/][inside("NL")]!.badPhoneNumber
        # *[contact:whatsapp=~/^(0031|\+31|0) ?[1-9]( ?[0-9]){11}/][inside("NL")]!.badPhoneNumber
        # *[phone=~/^(0031|\+31|0) ?[1-9]( ?[0-9]){11}/][inside("NL")]!.badPhoneNumber
        if ('contact:mobile' in keys) or ('contact:phone' in keys) or ('contact:whatsapp' in keys) or ('phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_badPhoneNumber) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_7c3d18b2), mapcss._tag_capture(capture_tags, 0, tags, 'contact:phone'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_badPhoneNumber) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_7c3d18b2), mapcss._tag_capture(capture_tags, 0, tags, 'contact:mobile'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_badPhoneNumber) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_7c3d18b2), mapcss._tag_capture(capture_tags, 0, tags, 'contact:whatsapp'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_badPhoneNumber) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_7c3d18b2), mapcss._tag_capture(capture_tags, 0, tags, 'phone'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL addresses and contacts")
                # throwWarning:tr("Invalid tag {0}: too many digits (or foreign number, if so: ignore)","{0.key}")
                err.append({'class': 90201, 'subclass': 50270752, 'text': mapcss.tr('Invalid tag {0}: too many digits (or foreign number, if so: ignore)', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # area[building][/^addr:(street|housenumber|postcode|city)$/][amenity!=place_of_worship][shop!=mall][building!~/^(container|houseboat|static_caravan)$/][inside("NL")]:closed
        if ('building' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_5ef8db88)) and (mapcss._tag_capture(capture_tags, 2, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 2, 'place_of_worship', 'place_of_worship')) and (mapcss._tag_capture(capture_tags, 3, tags, 'shop') != mapcss._value_const_capture(capture_tags, 3, 'mall', 'mall')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 4, self.re_18c8cfbe, '^(container|houseboat|static_caravan)$'), mapcss._tag_capture(capture_tags, 4, tags, 'building'))) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')) and (mapcss._tag_capture(capture_tags, -2, tags, 'type') == mapcss._value_capture(capture_tags, -2, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if match:
                # set .addrOnBuilding
                # group:tr("NL addresses and contacts")
                # throwWarning:tr("In Nederland is het gebouw niet gekoppeld aan het adres. Het adres is wel gekoppeld aan het gebruiksdoel.")
                # assertNoMatch:"relation type=multipolygon building=house"
                # assertNoMatch:"relation type=multipolygon building=houseboat addr:housenumber=2"
                # assertNoMatch:"relation type=multipolygon building=yes addr:housename=huis"
                set_addrOnBuilding = True
                err.append({'class': 90201, 'subclass': 1486034706, 'text': mapcss.tr('In Nederland is het gebouw niet gekoppeld aan het adres. Het adres is wel gekoppeld aan het gebruiksdoel.')})

        # area[/^addr:(city|postcode)$/][!/(^|.+:)addr:housenumber($|:.+)/][!/(^|.+:)addr:street($|:.+)/][inside("NL")]!.addrOnBuilding
        # area[addr:street][!/(^|.+:)addr:housenumber($|:.+)/][!addr:interpolation][!addr:flats][inside("NL")]!.addrOnBuilding
        if ('addr:street' in keys and 'type' in keys) or ('type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_addrOnBuilding) and (mapcss._tag_capture(capture_tags, 0, tags, self.re_561be3ff)) and (not mapcss._tag_capture(capture_tags, 1, tags, self.re_49026388)) and (not mapcss._tag_capture(capture_tags, 2, tags, self.re_32d334cf)) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_addrOnBuilding) and (mapcss._tag_capture(capture_tags, 0, tags, 'addr:street')) and (not mapcss._tag_capture(capture_tags, 1, tags, self.re_49026388)) and (not mapcss._tag_capture(capture_tags, 2, tags, 'addr:interpolation')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'addr:flats')) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL addresses and contacts")
                # throwWarning:tr("Incomplete address: {0} {1} {2} {3}",any(tag("addr:street"),"[street?]"),any(tag("addr:housenumber"),"[housenumber?]"),any(tag("addr:postcode"),""),any(tag("addr:city"),""))
                err.append({'class': 90201, 'subclass': 2087285475, 'text': mapcss.tr('Incomplete address: {0} {1} {2} {3}', mapcss.any_(mapcss.tag(tags, 'addr:street'), '[street?]'), mapcss.any_(mapcss.tag(tags, 'addr:housenumber'), '[housenumber?]'), mapcss.any_(mapcss.tag(tags, 'addr:postcode'), ''), mapcss.any_(mapcss.tag(tags, 'addr:city'), ''))})

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
                err.append({'class': 90202, 'subclass': 1207029826, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # area[building=terrace][inside("NL")]
        if ('building' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'terrace')) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("Een rij met rijtjeshuizen ({0}) wordt in Nederland per huis geïmporteerd uit de BAG","{0.tag}")
                # suggestAlternative:"leisure=outdoor_seating voor 'terrasjes'"
                # suggestAlternative:"building=house + house=terraced voor een individueel rijtjeshuis"
                # suggestAlternative:"building=house via een BAG importverzoek voor huizen"
                err.append({'class': 90202, 'subclass': 2130098421, 'text': mapcss.tr('Een rij met rijtjeshuizen ({0}) wordt in Nederland per huis geïmporteerd uit de BAG', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[addr:interpolation][inside("NL")]
        if ('addr:interpolation' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'addr:interpolation')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("Adressen ({0}) worden in Nederland individueel geïmporteerd uit de BAG","{0.key}")
                # suggestAlternative:"meerdere addr:housenumber via een BAG importverzoek"
                err.append({'class': 90202, 'subclass': 864819394, 'text': mapcss.tr('Adressen ({0}) worden in Nederland individueel geïmporteerd uit de BAG', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

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
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 90202, 'subclass': 788111375, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # area[addr:housename][/^building(:part)?$/][inside("NL")][!name]
        # area[building:name][/^building(:part)?$/][inside("NL")][!name]
        if ('addr:housename' in keys and 'type' in keys) or ('building:name' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'addr:housename')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_550ffc74)) and (mapcss.inside(self.father.config.options, 'NL')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'name')) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:name')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_550ffc74)) and (mapcss.inside(self.father.config.options, 'NL')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'name')) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if match:
                # set .housenameWithFix
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"name=*"
                # fixChangeKey:"{0.key}=>name"
                set_housenameWithFix = True
                err.append({'class': 90202, 'subclass': 797359946, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [(mapcss._tag_uncapture(capture_tags, '{0.key}=>name')).split('=>', 1)[1].strip(), mapcss.tag(tags, (mapcss._tag_uncapture(capture_tags, '{0.key}=>name')).split('=>', 1)[0].strip())]]),
                    '-': ([
                    (mapcss._tag_uncapture(capture_tags, '{0.key}=>name')).split('=>', 1)[0].strip()])
                }})

        # area[addr:housename][/^building(:part)?$/][inside("NL")][name=*"addr:housename"]!.housenameWithFix
        # area[building:name][/^building(:part)?$/][inside("NL")][name=*"building:name"]!.housenameWithFix
        if ('addr:housename' in keys and 'name' in keys and 'type' in keys) or ('building:name' in keys and 'name' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_housenameWithFix) and (mapcss._tag_capture(capture_tags, 0, tags, 'addr:housename')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_550ffc74)) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, 3, tags, 'name') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'addr:housename'))) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_housenameWithFix) and (mapcss._tag_capture(capture_tags, 0, tags, 'building:name')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_550ffc74)) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, 3, tags, 'name') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'building:name'))) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if match:
                # set .housenameWithFix
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"name=*"
                # fixRemove:"{0.key}"
                set_housenameWithFix = True
                err.append({'class': 90202, 'subclass': 464057822, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # area[addr:housename][/^building(:part)?$/][inside("NL")][name]!.housenameWithFix
        # area[building:name][/^building(:part)?$/][inside("NL")][name]!.housenameWithFix
        if ('addr:housename' in keys and 'name' in keys and 'type' in keys) or ('building:name' in keys and 'name' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_housenameWithFix) and (mapcss._tag_capture(capture_tags, 0, tags, 'addr:housename')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_550ffc74)) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, 3, tags, 'name')) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_housenameWithFix) and (mapcss._tag_capture(capture_tags, 0, tags, 'building:name')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_550ffc74)) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, 3, tags, 'name')) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"name=*"
                err.append({'class': 90202, 'subclass': 1635606421, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[/.:covid19$/][inside("NL")]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_26516863)) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("There are no active covid-19 restrictions at the moment. Remove {0}.","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 90202, 'subclass': 1496260396, 'text': mapcss.tr('There are no active covid-19 restrictions at the moment. Remove {0}.', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[material][material=~/\bhout|\bmetaal\b|^beton$|^brons$|steen\b|ijzer\b|staal\b/]
        if ('material' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'material')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_334bd9c9), mapcss._tag_capture(capture_tags, 1, tags, 'material'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("unusual value of {0}","{0.key}")
                err.append({'class': 90202, 'subclass': 1686750599, 'text': mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[surface][surface=~/^paving_stones:([1-9])0$/][inside("NL")]
        if ('surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'surface')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_19b1af6a), mapcss._tag_capture(capture_tags, 1, tags, 'surface'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"surface=paving_stones + paving_stones:shape=square + paving_stones:length=[length in meter, e.g. 0.3]"
                # fixAdd:concat("paving_stones:length=0.",get(regexp_match("^paving_stones:([1-9])0$",tag("surface")),1))
                # fixAdd:"paving_stones:shape=square"
                # fixAdd:"surface=paving_stones"
                err.append({'class': 90202, 'subclass': 1868473171, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('paving_stones:length=0.', mapcss.get(mapcss.regexp_match(self.re_19b1af6a, mapcss.tag(tags, 'surface')), 1))).split('=', 1),
                    ['paving_stones:shape','square'],
                    ['surface','paving_stones']])
                }})

        # *[/^(.+):surface$/][/^(.+):surface$/=~/^paving_stones:([1-9])0$/][count(tag_regex("^(.+):surface$"))==1][inside("NL")]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_74d9b833)) and (mapcss.regexp_test(self.re_19b1af6a, mapcss._match_regex(tags, self.re_74d9b833))) and (mapcss.count(mapcss.tag_regex(tags, self.re_74d9b833)) == 1) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # set .completedSurfacePavingStonesNumber
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"*:surface=paving_stones + *:paving_stones:shape=square + *:paving_stones:length=[length in meter, e.g. 0.3]"
                set_completedSurfacePavingStonesNumber = True
                err.append({'class': 90202, 'subclass': 1911834456, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[/^(.+):surface$/=~/^paving_stones:([1-9])0$/][inside("NL")]!.completedSurfacePavingStonesNumber
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_completedSurfacePavingStonesNumber) and (mapcss.regexp_test(self.re_19b1af6a, mapcss._match_regex(tags, self.re_74d9b833))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","*:surface=paving_stones:NN")
                # suggestAlternative:"*:surface=paving_stones + *:paving_stones:shape=square + *:paving_stones:length=[length in meter, e.g. 0.3]"
                err.append({'class': 90202, 'subclass': 1665978272, 'text': mapcss.tr('{0} is deprecated', '*:surface=paving_stones:NN')})

        # *[winkelnummer]
        if ('winkelnummer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'winkelnummer')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL deprecated features")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"ref=*"
                err.append({'class': 90202, 'subclass': 340349535, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[ref:bag][ref:bag!~/(; ?|^)([0-9]{0,3}[1-9]|[0-9]{0,2}[1-9][0-9]|[0-9]?[1-9][0-9]{2})[0-9]{12}($|;)/][inside("NL")]
        if ('ref:bag' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:bag')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_6708cc9b, '(; ?|^)([0-9]{0,3}[1-9]|[0-9]{0,2}[1-9][0-9]|[0-9]?[1-9][0-9]{2})[0-9]{12}($|;)'), mapcss._tag_capture(capture_tags, 1, tags, 'ref:bag'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL unusual values")
                # throwWarning:tr("Invalid value of {0}","{0.key}")
                # assertNoMatch:"relation type=multipolygon ref:bag=\"0004567890123456; 1234567890123456\""
                # assertNoMatch:"relation type=multipolygon ref:bag=0004567890123456"
                # assertNoMatch:"relation type=multipolygon ref:bag=0050123456789012"
                # assertNoMatch:"relation type=multipolygon ref:bag=0200123456789012"
                # assertNoMatch:"relation type=multipolygon ref:bag=0234567890123456"
                # assertNoMatch:"relation type=multipolygon ref:bag=0310123456789012"
                # assertNoMatch:"relation type=multipolygon ref:bag=050123456789012"
                # assertNoMatch:"relation type=multipolygon ref:bag=1234567890123456"
                # assertNoMatch:"relation type=multipolygon ref:bag=200123456789012"
                # assertNoMatch:"relation type=multipolygon ref:bag=310123456789012"
                # assertNoMatch:"relation type=multipolygon ref:bag=4567890123456"
                # assertNoMatch:"relation type=multipolygon ref:bag=50123456789012"
                err.append({'class': 90209, 'subclass': 2021092431, 'text': mapcss.tr('Invalid value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[leisure][surface=gravel][sport~="tennis"][inside("NL")]
        if ('leisure' in keys and 'sport' in keys and 'surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure')) and (mapcss._tag_capture(capture_tags, 1, tags, 'surface') == mapcss._value_capture(capture_tags, 1, 'gravel')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 2, tags, 'sport'), mapcss._value_capture(capture_tags, 2, 'tennis'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL unusual values")
                # throwWarning:tr("unusual value of {0} for {1} (`gravel` in English means `grind` in Dutch)","{1.key}","{2.tag}")
                # suggestAlternative:"surface=clay"
                err.append({'class': 90209, 'subclass': 1521090750, 'text': mapcss.tr('unusual value of {0} for {1} (`gravel` in English means `grind` in Dutch)', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # *[name][name="ijsbaan"]
        # *[name][name=~/\b(([Aa]f)?gesloten|[Gg]eopend)\b/]
        # *[name][amenity^=parking][name=~/(?i)(parkeren|parkeerplaats|parkeergarage|^garage)$/]
        # *[name][name=~/(?i)^gratis\s|gratis\)/]
        # *[name][name=~/(?i)(klanten|bezoek(ers)?|medewerkers)\b/][!route]
        # *[name][leisure=playground][name=~/(?i)^speeltuin(tje)?$/]
        # *[name][leisure^=dog][name=~/(?i)^(honden\s?)?(toilet|uitlaa[dt]|los.?loop)/]
        # *[name][leisure=pitch][name=~/(?i)ball?(veld(je)?)?$/][!sport]
        # area[name][name=~/(?i)^wadi$/][tag("natural")||tag("landuse")]
        # area[name][natural=water][name=visvijver]
        if ('amenity' in keys and 'name' in keys) or ('leisure' in keys and 'name' in keys) or ('name' in keys) or ('name' in keys and 'natural' in keys and 'type' in keys) or ('name' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name') == mapcss._value_capture(capture_tags, 1, 'ijsbaan')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_26e04b1e), mapcss._tag_capture(capture_tags, 1, tags, 'name'))))
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
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'leisure') == mapcss._value_capture(capture_tags, 1, 'playground')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_0ec6b360), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.startswith(mapcss._tag_capture(capture_tags, 1, tags, 'leisure'), mapcss._value_capture(capture_tags, 1, 'dog'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_5b4448e5), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'leisure') == mapcss._value_capture(capture_tags, 1, 'pitch')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3c163648), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'sport')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_54e14d8c), mapcss._tag_capture(capture_tags, 1, tags, 'name'))) and (mapcss.tag(tags, 'natural') or mapcss.tag(tags, 'landuse')) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'natural') == mapcss._value_capture(capture_tags, 1, 'water')) and (mapcss._tag_capture(capture_tags, 2, tags, 'name') == mapcss._value_capture(capture_tags, 2, 'visvijver')) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("descriptive name")
                err.append({'class': 90203, 'subclass': 147135230, 'text': mapcss.tr('descriptive name')})

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
                err.append({'class': 90203, 'subclass': 538711457, 'text': mapcss.tr('descriptive name')})

        # *[name][place][name=~/\b(Adm|Br|Burg|Cmdt|Dr|Drs|Ds|Gebr|Gen|Ing|Ir|Jhr|Kard|Kon|Luit|Mej|Mevr|Mgr|Min|Mr|Past|Pr|Pres|Prof|St|Vr|Weth|Zr)\.? [A-Za-z]/][inside("NL")]!.abbrname
        # *[name][place][name=~/^[A-Z][a-z]{1,4}\. /][name!~/^(Adr|Anth?|Chr?|Corn|Fred|Hub|Jacq?|Joh|Jos|Mac|Nic|Ph|Th)\./][inside("NL")]!.abbrname
        if ('name' in keys and 'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_abbrname) and (mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'place')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_676d2c9e), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_abbrname) and (mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'place')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_293c2706), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_2f938f56, '^(Adr|Anth?|Chr?|Corn|Fred|Hub|Jacq?|Joh|Jos|Mac|Nic|Ph|Th)\\.'), mapcss._tag_capture(capture_tags, 3, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # set .abbrname
                # group:tr("NL nomenclature")
                # throwWarning:tr("Gebiedsnaam met afkorting")
                set_abbrname = True
                err.append({'class': 90203, 'subclass': 1573033356, 'text': mapcss.tr('Gebiedsnaam met afkorting')})

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
                err.append({'class': 90203, 'subclass': 1558593366, 'text': mapcss.tr('Spoorgebied met afgekorte naam')})

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
                err.append({'class': 90203, 'subclass': 1647353731, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [(mapcss._tag_uncapture(capture_tags, '{0.key}=>{1.key}')).split('=>', 1)[1].strip(), mapcss.tag(tags, (mapcss._tag_uncapture(capture_tags, '{0.key}=>{1.key}')).split('=>', 1)[0].strip())]]),
                    '-': ([
                    (mapcss._tag_uncapture(capture_tags, '{0.key}=>{1.key}')).split('=>', 1)[0].strip()])
                }})

        # *[heritage=2][heritage:operator!=rce][heritage:operator!~/(^|; ?)rce(;|$)/][inside("NL")]
        if ('heritage' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'heritage') == mapcss._value_capture(capture_tags, 0, 2)) and (mapcss._tag_capture(capture_tags, 1, tags, 'heritage:operator') != mapcss._value_const_capture(capture_tags, 1, 'rce', 'rce')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_3da90af7, '(^|; ?)rce(;|$)'), mapcss._tag_capture(capture_tags, 2, tags, 'heritage:operator'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL heritage")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.tag}")
                # fixAdd:"heritage:operator=rce"
                err.append({'class': 90204, 'subclass': 675628887, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['heritage:operator','rce']])
                }})

        # *[heritage:operator=rce][!heritage][inside("NL")]
        if ('heritage:operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'heritage:operator') == mapcss._value_capture(capture_tags, 0, 'rce')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'heritage')) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL heritage")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}=*")
                # fixAdd:"heritage=2"
                err.append({'class': 90204, 'subclass': 1113141518, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}=*')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['heritage','2']])
                }})

        # relation[except][except~=bicycle][except~=moped][except!~/(^|; ?)mofa(;|$)/]
        if ('except' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'except')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'except'), mapcss._value_capture(capture_tags, 1, 'bicycle'))) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 2, tags, 'except'), mapcss._value_capture(capture_tags, 2, 'moped'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_110c89a2, '(^|; ?)mofa(;|$)'), mapcss._tag_capture(capture_tags, 3, tags, 'except'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL mofa tagging")
                # throwWarning:tr("{0} without {1}","{0.tag}","mofa")
                # suggestAlternative:"{0.tag};mofa"
                # fixAdd:"{0.key}={0.value};mofa"
                # assertNoMatch:"relation type=restriction except=bicycle"
                # assertNoMatch:"relation type=restriction except=bicycle;mofa;moped"
                err.append({'class': 90208, 'subclass': 92591020, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), 'mofa'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, '{0.key}={0.value};mofa')).split('=', 1)])
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

        self.check_not_err(n.node(data, {'crossing': 'traffic_signals', 'highway': 'crossing', 'note': 'traffic_signals_combined_with_zebra', 'traffic_sign': 'NL:L02'}), expected={'class': 90205, 'subclass': 938076772})
        self.check_err(n.node(data, {'highway': 'crossing', 'traffic_sign': 'NL:L02;NL:J23'}), expected={'class': 90205, 'subclass': 938076772})
        self.check_not_err(n.node(data, {'direction': '300', 'traffic_sign': 'NL:L2'}), expected={'class': 90205, 'subclass': 938076772})
        self.check_not_err(n.node(data, {'crossing': 'uncontrolled', 'crossing_ref': 'zebra', 'highway': 'crossing', 'traffic_sign': 'NL:L2'}), expected={'class': 90205, 'subclass': 938076772})
        self.check_err(n.node(data, {'highway': 'crossing', 'traffic_sign': 'NL:L2'}), expected={'class': 90205, 'subclass': 938076772})
        self.check_err(n.node(data, {'phone': '+31 06 1234 5678'}), expected={'class': 90201, 'subclass': 1739574763})
        self.check_err(n.node(data, {'phone': '+31 0612345678'}), expected={'class': 90201, 'subclass': 1739574763})
        self.check_err(n.node(data, {'phone': '+31 08008844'}), expected={'class': 90201, 'subclass': 1739574763})
        self.check_not_err(n.node(data, {'phone': '+31 6 1234 5678'}), expected={'class': 90201, 'subclass': 1739574763})
        self.check_not_err(n.node(data, {'phone': '+31 612345678'}), expected={'class': 90201, 'subclass': 1739574763})
        self.check_err(n.node(data, {'phone': '00310612345678'}), expected={'class': 90201, 'subclass': 1739574763})
        self.check_not_err(n.node(data, {'phone': '0031612345678'}), expected={'class': 90201, 'subclass': 1739574763})
        self.check_not_err(n.node(data, {'phone': '06 12 34 56 78'}), expected={'class': 90201, 'subclass': 1739574763})
        self.check_not_err(n.node(data, {'phone': '0612345678'}), expected={'class': 90201, 'subclass': 1739574763})
        self.check_err(n.node(data, {'phone': '+31 14 0245'}), expected={'class': 90201, 'subclass': 345342642})
        self.check_err(n.node(data, {'phone': '+31 140245'}), expected={'class': 90201, 'subclass': 345342642})
        self.check_not_err(n.node(data, {'phone': '+31 800 8844'}), expected={'class': 90201, 'subclass': 345342642})
        self.check_err(n.node(data, {'phone': '+3114024'}), expected={'class': 90201, 'subclass': 345342642})
        self.check_not_err(n.node(data, {'phone': '+318008844'}), expected={'class': 90201, 'subclass': 345342642})
        self.check_err(n.node(data, {'phone': '0031140245'}), expected={'class': 90201, 'subclass': 345342642})
        self.check_not_err(n.node(data, {'phone': '0031612345678'}), expected={'class': 90201, 'subclass': 345342642})
        self.check_not_err(n.node(data, {'phone': '00318008844'}), expected={'class': 90201, 'subclass': 345342642})
        self.check_not_err(n.node(data, {'phone': '0612345678'}), expected={'class': 90201, 'subclass': 345342642})
        self.check_not_err(n.node(data, {'phone': '0800 8844'}), expected={'class': 90201, 'subclass': 345342642})
        self.check_not_err(n.node(data, {'phone': '08008844'}), expected={'class': 90201, 'subclass': 345342642})
        self.check_not_err(n.node(data, {'phone': '14024'}), expected={'class': 90201, 'subclass': 345342642})
        self.check_not_err(n.node(data, {'phone': '140245'}), expected={'class': 90201, 'subclass': 345342642})
        self.check_not_err(n.node(data, {'contact:mobile': '097 123456789'}), expected={'class': 90201, 'subclass': 50270752})
        self.check_not_err(n.node(data, {'contact:whatsapp': '+31 97 1234 567 89'}), expected={'class': 90201, 'subclass': 50270752})
        self.check_not_err(n.node(data, {'contact:whatsapp': '+3197 123456789'}), expected={'class': 90201, 'subclass': 50270752})
        self.check_not_err(n.node(data, {'phone': '+31 6 1234 5678'}), expected={'class': 90201, 'subclass': 50270752})
        self.check_not_err(n.node(data, {'phone': '+31 6 12345678'}), expected={'class': 90201, 'subclass': 50270752})
        self.check_not_err(n.node(data, {'phone': '0031612345678'}), expected={'class': 90201, 'subclass': 50270752})
        self.check_not_err(n.node(data, {'phone': '06 12345678'}), expected={'class': 90201, 'subclass': 50270752})
        self.check_not_err(n.node(data, {'phone': '0800 1234567'}), expected={'class': 90201, 'subclass': 50270752})
        self.check_not_err(n.node(data, {'addr:city': 'Milheeze', 'addr:housenumber': '2a', 'addr:street': 'Pastoor Simonisplein', 'amenity': 'atm'}), expected={'class': 90201, 'subclass': 509151640})
        self.check_not_err(n.node(data, {'addr:city': 'Marrum', 'addr:housenumber': '1W-5', 'addr:street': 'Ozingaloane', 'power': 'generator'}), expected={'class': 90201, 'subclass': 509151640})
        self.check_not_err(n.node(data, {'addr:city': 'XXX', 'addr:flats': '1-3', 'addr:postcode': '1234AB', 'addr:street': 'XXX'}), expected={'class': 90201, 'subclass': 509151640})
        self.check_not_err(n.node(data, {'addr:city': 'XXX', 'addr:housenumber:construction': '123', 'addr:postcode': '1234AB', 'addr:street': 'XXX'}), expected={'class': 90201, 'subclass': 509151640})
        self.check_not_err(n.node(data, {'addr:city': 'XXX', 'addr:housenumber': '123', 'addr:postcode': '1234AB', 'addr:street': 'XXX'}), expected={'class': 90201, 'subclass': 509151640})
        self.check_not_err(n.node(data, {'addr:city': 'XXX', 'addr:postcode': '1234AB', 'addr:street': 'XXX', 'proposed:addr:housenumber': '123'}), expected={'class': 90201, 'subclass': 509151640})
        self.check_err(n.node(data, {'material': 'brons', 'tourism': 'artwork'}), expected={'class': 90202, 'subclass': 1686750599})
        self.check_err(n.node(data, {'material': 'hout,metaal', 'tourism': 'artwork'}), expected={'class': 90202, 'subclass': 1686750599})
        self.check_not_err(n.node(data, {'amenity': 'charging_station', 'motor_vehicle': 'designated'}), expected={'class': 90209, 'subclass': 1720314934})
        self.check_not_err(n.node(data, {'amenity': 'parking_entrance', 'motor_vehicle': 'designated'}), expected={'class': 90209, 'subclass': 1720314934})
        self.check_not_err(n.node(data, {'circumference': '8.6', 'natural': 'tree'}), expected={'class': 90209, 'subclass': 68044720})
        self.check_not_err(n.node(data, {'height': '288 cm', 'natural': 'tree'}), expected={'class': 90209, 'subclass': 68044720})
        self.check_not_err(n.node(data, {'height': '51', 'natural': 'tree'}), expected={'class': 90209, 'subclass': 68044720})
        self.check_err(n.node(data, {'amenity': 'drinking_water', 'name': 'kraanwater'}), expected={'class': 90203, 'subclass': 1470133234})
        self.check_err(n.node(data, {'amenity': 'parking_entrance', 'name': 'parkeerplaats voor bezoekers'}), expected={'class': 90203, 'subclass': 1470133234})
        self.check_err(n.node(data, {'leisure': 'pitch', 'name': 'voetbalveld'}), expected={'class': 90203, 'subclass': 1470133234})
        self.check_err(n.node(data, {'leisure': 'playground', 'name': 'Abc (gesloten)'}), expected={'class': 90203, 'subclass': 1470133234})
        self.check_not_err(n.node(data, {'name': 'Landgoed', 'railway': 'tram_stop'}), expected={'class': 90203, 'subclass': 1558593366})
        self.check_not_err(n.node(data, {'name:fy': 'y', 'name:nl': 'x'}), expected={'class': 90203, 'subclass': 1647353731})
        self.check_not_err(n.node(data, {'name': 'x', 'name:en': 'y', 'name:nl': 'x'}), expected={'class': 90203, 'subclass': 1647353731})
        self.check_err(n.node(data, {'amenity': 'post_box', 'operator': 'post nl'}), expected={'class': 90203, 'subclass': 1831362989})
        self.check_not_err(n.node(data, {'amenity': 'post_box', 'operator': 'PostNL'}), expected={'class': 90203, 'subclass': 1831362989})
        self.check_err(n.node(data, {'amenity': 'post_box', 'operator': 'postnl'}), expected={'class': 90203, 'subclass': 1831362989})
        self.check_not_err(n.node(data, {'heritage': '2', 'heritage:operator': 'rce; Stichting ABCDE'}), expected={'class': 90204, 'subclass': 675628887})
        self.check_err(n.way(data, {'highway': 'cycleway', 'traffic_sign': 'NL:G13; NL:L301-A'}, [0]), expected={'class': 90205, 'subclass': 932689435})
        self.check_not_err(n.way(data, {'highway': 'cycleway', 'traffic_sign': 'NL:J1; NL:G11; NL:G07; OB109'}, [0]), expected={'class': 90205, 'subclass': 932689435})
        self.check_not_err(n.way(data, {'highway': 'cycleway', 'traffic_sign': 'NL:G11;NL:G07'}, [0]), expected={'class': 90205, 'subclass': 932689435})
        self.check_not_err(n.way(data, {'highway': 'cycleway', 'traffic_sign': 'NL:G11;NL:G07;OB109'}, [0]), expected={'class': 90205, 'subclass': 932689435})
        self.check_not_err(n.way(data, {'highway': 'cycleway', 'traffic_sign': 'NL:G11;OB109;NL:G07'}, [0]), expected={'class': 90205, 'subclass': 932689435})
        self.check_not_err(n.way(data, {'highway': 'cycleway', 'traffic_sign': 'NL:G13'}, [0]), expected={'class': 90205, 'subclass': 932689435})
        self.check_err(n.way(data, {'highway': 'cycleway', 'traffic_sign': 'NL:G13;NL:L301-A'}, [0]), expected={'class': 90205, 'subclass': 932689435})
        self.check_err(n.way(data, {'highway': 'cycleway', 'traffic_sign': 'NL:G7'}, [0]), expected={'class': 90205, 'subclass': 932689435})
        self.check_err(n.way(data, {'highway': 'cycleway', 'traffic_sign': 'NL:G7;OB109'}, [0]), expected={'class': 90205, 'subclass': 932689435})
        self.check_not_err(n.way(data, {'highway': 'cycleway', 'traffic_sign': 'NL:J1;NL:G11;OB109;NL:G07'}, [0]), expected={'class': 90205, 'subclass': 932689435})
        self.check_err(n.way(data, {'highway': 'cycleway', 'traffic_sign': 'NL:J1;NL:G7'}, [0]), expected={'class': 90205, 'subclass': 932689435})
        self.check_err(n.way(data, {'highway': 'cycleway', 'traffic_sign': 'NL:J1;NL:G7;OB109'}, [0]), expected={'class': 90205, 'subclass': 932689435})
        self.check_err(n.way(data, {'highway': 'cycleway', 'traffic_sign': 'NL:L301'}, [0]), expected={'class': 90205, 'subclass': 932689435})
        self.check_not_err(n.way(data, {'highway': 'residential', 'traffic_sign': 'NL:G12;NL:G10'}, [0]), expected={'class': 90205, 'subclass': 932689435})
        self.check_err(n.way(data, {'highway': 'residential', 'living_street': 'yes', 'traffic_sign': 'NL:G5'}, [0]), expected={'class': 90205, 'subclass': 932689435})
        self.check_not_err(n.way(data, {'highway': 'service', 'living_street': 'yes', 'traffic_sign': 'NL:G5'}, [0]), expected={'class': 90205, 'subclass': 932689435})
        self.check_err(n.way(data, {'highway': 'service', 'traffic_sign': 'NL:G5'}, [0]), expected={'class': 90205, 'subclass': 932689435})
        self.check_not_err(n.way(data, {'highway': 'steps', 'traffic_sign': 'NL:G13; NL:L301-B'}, [0]), expected={'class': 90205, 'subclass': 932689435})
        self.check_not_err(n.way(data, {'highway': 'steps', 'ramp:bicycle': 'yes', 'traffic_sign': 'NL:G13'}, [0]), expected={'class': 90205, 'subclass': 932689435})
        self.check_not_err(n.way(data, {'highway': 'steps', 'traffic_sign': 'NL:G13;NL:L301-B'}, [0]), expected={'class': 90205, 'subclass': 932689435})
        self.check_not_err(n.way(data, {'highway': 'cycleway', 'living_street': 'yes', 'moped': 'designated', 'traffic_sign': 'NL:G05'}, [0]), expected={'class': 90205, 'subclass': 1097965115})
        self.check_not_err(n.way(data, {'highway': 'cycleway', 'moped': 'use_sidepath', 'traffic_sign': 'NL:G05'}, [0]), expected={'class': 90205, 'subclass': 1097965115})
        self.check_not_err(n.way(data, {'highway': 'living_street', 'moped': 'yes', 'traffic_sign': 'NL:G05'}, [0]), expected={'class': 90205, 'subclass': 1097965115})
        self.check_not_err(n.way(data, {'foot': 'no', 'hgv:backward': 'no', 'highway': 'service', 'traffic_sign:backward': 'NL:C07;NL:C16'}, [0]), expected={'class': 90205, 'subclass': 767847379})
        self.check_not_err(n.way(data, {'foot': 'no', 'hgv': 'no', 'highway': 'service', 'traffic_sign:backward': 'NL:C07;NL:C16'}, [0]), expected={'class': 90205, 'subclass': 767847379})
        self.check_not_err(n.way(data, {'highway': 'service', 'oneway:bicycle': 'yes', 'traffic_sign:backward': 'NL:C14'}, [0]), expected={'class': 90205, 'subclass': 767847379})
        self.check_not_err(n.way(data, {'bicycle:backward': 'destination', 'highway': 'service', 'oneway': 'yes', 'oneway:bicycle': 'no', 'traffic_sign:backward': 'NL:C14'}, [0]), expected={'class': 90205, 'subclass': 767847379})
        self.check_err(n.way(data, {'highway': 'service', 'oneway': 'yes', 'oneway:bicycle': 'no', 'traffic_sign:backward': 'NL:C14'}, [0]), expected={'class': 90205, 'subclass': 767847379})
        self.check_err(n.way(data, {'access:backward': 'no', 'highway': 'service', 'traffic_sign:backward': 'NL:C1', 'traffic_sign:forward': 'NL:C9;NL:OB58'}, [0]), expected={'class': 90205, 'subclass': 767847379})
        self.check_err(n.way(data, {'highway': 'service', 'traffic_sign:forward': 'NL:C9;NL:OB58'}, [0]), expected={'class': 90205, 'subclass': 767847379})
        self.check_err(n.way(data, {'highway': 'service', 'traffic_sign': 'NL:C01'}, [0]), expected={'class': 90205, 'subclass': 767847379})
        self.check_not_err(n.way(data, {'access': 'no', 'highway': 'service', 'traffic_sign': 'NL:C01;NL:C16'}, [0]), expected={'class': 90205, 'subclass': 767847379})
        self.check_not_err(n.way(data, {'highway': 'service', 'motor_vehicle': 'no', 'traffic_sign': 'NL:C01;NL:OB51;NL:OB54'}, [0]), expected={'class': 90205, 'subclass': 767847379})
        self.check_not_err(n.way(data, {'highway': 'track', 'oneway': 'yes', 'oneway:bicycle': 'no', 'traffic_sign:backward': 'NL:C12'}, [0]), expected={'class': 90205, 'subclass': 767847379})
        self.check_not_err(n.way(data, {'highway': 'track', 'motor_vehicle': 'no', 'traffic_sign': 'NL:C12'}, [0]), expected={'class': 90205, 'subclass': 767847379})
        self.check_not_err(n.way(data, {'hazmat:A:backward': 'no', 'highway': 'service', 'traffic_sign:backward': 'NL:C22[A]'}, [0]), expected={'class': 90205, 'subclass': 326989948})
        self.check_not_err(n.way(data, {'highway': 'service', 'oneway:hazmat': 'yes', 'traffic_sign:backward': 'NL:C22[A]'}, [0]), expected={'class': 90205, 'subclass': 326989948})
        self.check_err(n.way(data, {'highway': 'service', 'oneway': 'yes', 'oneway:hazmat': 'no', 'traffic_sign:backward': 'NL:C22[A]'}, [0]), expected={'class': 90205, 'subclass': 326989948})
        self.check_not_err(n.way(data, {'highway': 'service', 'oneway:hazmat:C': 'yes', 'traffic_sign:backward': 'NL:C22[C]'}, [0]), expected={'class': 90205, 'subclass': 326989948})
        self.check_err(n.way(data, {'highway': 'service', 'traffic_sign:forward': 'NL:C16; NL:C22[A]; NL:OB58'}, [0]), expected={'class': 90205, 'subclass': 326989948})
        self.check_err(n.way(data, {'highway': 'service', 'traffic_sign:forward': 'NL:C22[A];NL:OB58'}, [0]), expected={'class': 90205, 'subclass': 326989948})
        self.check_not_err(n.way(data, {'access': 'no', 'highway': 'service', 'traffic_sign': 'NL:C22'}, [0]), expected={'class': 90205, 'subclass': 326989948})
        self.check_not_err(n.way(data, {'hazmat': 'no', 'highway': 'service', 'traffic_sign': 'NL:C22'}, [0]), expected={'class': 90205, 'subclass': 326989948})
        self.check_err(n.way(data, {'highway': 'service', 'traffic_sign': 'NL:C22'}, [0]), expected={'class': 90205, 'subclass': 326989948})
        self.check_not_err(n.way(data, {'highway': 'service', 'traffic_sign': 'NL:C22a'}, [0]), expected={'class': 90205, 'subclass': 326989948})
        self.check_not_err(n.way(data, {'highway': 'residential', 'maxweight:backward': '2.1', 'traffic_sign:backward': 'NL:C21[2.1]'}, [0]), expected={'class': 90205, 'subclass': 991745921})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign:forward': 'NL:C19[2.1]'}, [0]), expected={'class': 90205, 'subclass': 991745921})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign:forward': 'NL:C21[2.1]'}, [0]), expected={'class': 90205, 'subclass': 991745921})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign:forward': 'NL:J19; NL:L01[4.1]; NL:OB108'}, [0]), expected={'class': 90205, 'subclass': 991745921})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign:forward': 'NL:J19;NL:L01[4.1];NL:OB108'}, [0]), expected={'class': 90205, 'subclass': 991745921})
        self.check_not_err(n.way(data, {'highway': 'residential', 'maxheight': '2.1', 'traffic_sign': 'NL:C19[2.1]'}, [0]), expected={'class': 90205, 'subclass': 991745921})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign': 'NL:C21[2.1]'}, [0]), expected={'class': 90205, 'subclass': 991745921})
        self.check_not_err(n.way(data, {'highway': 'residential', 'maxweight:conditional': 'xxx', 'traffic_sign': 'NL:J19;NL:C21[2.1];NL:OB108'}, [0]), expected={'class': 90205, 'subclass': 991745921})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign:backward': 'NL:C02;NL:OB58'}, [0]), expected={'class': 90205, 'subclass': 2031953960})
        self.check_not_err(n.way(data, {'highway': 'residential', 'oneway:motor_vehicle': 'yes', 'traffic_sign:backward': 'NL:C2'}, [0]), expected={'class': 90205, 'subclass': 2031953960})
        self.check_not_err(n.way(data, {'highway': 'residential', 'oneway': 'yes', 'oneway:bicycle': 'no', 'traffic_sign:backward': 'NL:C2'}, [0]), expected={'class': 90205, 'subclass': 2031953960})
        self.check_err(n.way(data, {'highway': 'residential', 'oneway:motor_vehicle': '-1', 'traffic_sign:forward': 'NL:C3'}, [0]), expected={'class': 90205, 'subclass': 2031953960})
        self.check_not_err(n.way(data, {'highway': 'residential', 'oneway:motor_vehicle': 'yes', 'traffic_sign:forward': 'NL:C3'}, [0]), expected={'class': 90205, 'subclass': 2031953960})
        self.check_err(n.way(data, {'highway': 'residential', 'oneway': '-1', 'traffic_sign:forward': 'NL:C3'}, [0]), expected={'class': 90205, 'subclass': 2031953960})
        self.check_not_err(n.way(data, {'highway': 'residential', 'oneway': 'yes', 'traffic_sign:forward': 'NL:C3'}, [0]), expected={'class': 90205, 'subclass': 2031953960})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign:forward': 'NL:C3'}, [0]), expected={'class': 90205, 'subclass': 2031953960})
        self.check_err(n.way(data, {'highway': 'residential', 'oneway': 'no', 'oneway:bicycle': 'no', 'traffic_sign': 'NL:C02'}, [0]), expected={'class': 90205, 'subclass': 2031953960})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign': 'NL:C02'}, [0]), expected={'class': 90205, 'subclass': 2031953960})
        self.check_not_err(n.way(data, {'highway': 'residential', 'oneway': '-1', 'traffic_sign': 'NL:C02;NL:OB58'}, [0]), expected={'class': 90205, 'subclass': 2031953960})
        self.check_not_err(n.way(data, {'highway': 'residential', 'oneway': 'yes', 'traffic_sign': 'NL:C02;NL:OB58'}, [0]), expected={'class': 90205, 'subclass': 2031953960})
        self.check_not_err(n.way(data, {'highway': 'residential', 'oneway': 'no', 'oneway:agricultural': 'no', 'oneway:motor_vehicle': 'yes', 'oneway:motorcycle': 'no', 'traffic_sign': 'NL:C3'}, [0]), expected={'class': 90205, 'subclass': 2031953960})
        self.check_not_err(n.way(data, {'highway': 'residential', 'oneway:motor_vehicle': '-1', 'traffic_sign': 'NL:C3'}, [0]), expected={'class': 90205, 'subclass': 2031953960})
        self.check_not_err(n.way(data, {'highway': 'residential', 'oneway:motor_vehicle': 'yes', 'traffic_sign': 'NL:C3'}, [0]), expected={'class': 90205, 'subclass': 2031953960})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign': 'NL:C3;NL:OB58'}, [0]), expected={'class': 90205, 'subclass': 2031953960})
        self.check_err(n.way(data, {'highway': 'residential', 'oneway': 'yes', 'traffic_sign': 'NL:C05'}, [0]), expected={'class': 90205, 'subclass': 560436831})
        self.check_not_err(n.way(data, {'highway': 'residential', 'traffic_sign': 'NL:C05'}, [0]), expected={'class': 90205, 'subclass': 560436831})
        self.check_not_err(n.way(data, {'highway': 'residential', 'oneway': 'no', 'traffic_sign': 'NL:C5;NL:OB58'}, [0]), expected={'class': 90205, 'subclass': 560436831})
        self.check_not_err(n.way(data, {'highway': 'residential', 'junction': 'circular', 'traffic_sign': 'NL:D1'}, [0]), expected={'class': 90205, 'subclass': 439012160})
        self.check_not_err(n.way(data, {'highway': 'residential', 'junction': 'roundabout', 'traffic_sign': 'NL:D1'}, [0]), expected={'class': 90205, 'subclass': 439012160})
        self.check_err(n.way(data, {'highway': 'residential', 'oneway': 'yes', 'traffic_sign': 'NL:D1'}, [0]), expected={'class': 90205, 'subclass': 439012160})
        self.check_not_err(n.way(data, {'highway': 'residential', 'junction': 'circular', 'oneway': '-1', 'traffic_sign': 'NL:D1'}, [0]), expected={'class': 90205, 'subclass': 1998584294})
        self.check_not_err(n.way(data, {'highway': 'residential', 'junction': 'circular', 'oneway': 'yes', 'traffic_sign': 'NL:D1'}, [0]), expected={'class': 90205, 'subclass': 1998584294})
        self.check_err(n.way(data, {'highway': 'residential', 'junction': 'circular', 'traffic_sign': 'NL:D1'}, [0]), expected={'class': 90205, 'subclass': 1998584294})
        self.check_err(n.way(data, {'highway': 'residential', 'junction': 'circular', 'oneway': 'no', 'traffic_sign': 'NL:D1'}, [0]), expected={'class': 90205, 'subclass': 1998584294})
        self.check_err(n.way(data, {'highway': 'residential', 'parking:both': 'no', 'traffic_sign:left': 'NL:E02'}, [0]), expected={'class': 90205, 'subclass': 1049002673})
        self.check_err(n.way(data, {'highway': 'residential', 'parking:left': 'no', 'traffic_sign:left': 'NL:E02'}, [0]), expected={'class': 90205, 'subclass': 1049002673})
        self.check_not_err(n.way(data, {'highway': 'residential', 'parking:left': 'parallel', 'traffic_sign:left': 'NL:E02'}, [0]), expected={'class': 90205, 'subclass': 1049002673})
        self.check_not_err(n.way(data, {'highway': 'residential', 'parking:both': 'no', 'parking:both:restriction': 'no_stopping', 'traffic_sign:left': 'NL:E02', 'traffic_sign:right': 'NL:E02'}, [0]), expected={'class': 90205, 'subclass': 1049002673})
        self.check_not_err(n.way(data, {'highway': 'residential', 'parking:both': 'no', 'parking:left:restriction': 'no_parking', 'parking:right:restriction': 'no_parking', 'traffic_sign': 'NL:E01'}, [0]), expected={'class': 90205, 'subclass': 1049002673})
        self.check_not_err(n.way(data, {'highway': 'residential', 'priority': 'forward', 'traffic_sign': 'NL:F6;NL:F5'}, [0]), expected={'class': 90205, 'subclass': 1040610185})
        self.check_not_err(n.way(data, {'highway': 'residential', 'priority:agricultural': 'forward', 'traffic_sign': 'NL:F6;OB05'}, [0]), expected={'class': 90205, 'subclass': 1040610185})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign': 'NL:F6;OB05'}, [0]), expected={'class': 90205, 'subclass': 1040610185})
        self.check_err(n.way(data, {'highway': 'residential', 'priority': 'backward', 'traffic_sign:backward': 'NL:F05'}, [0]), expected={'class': 90205, 'subclass': 1108961023})
        self.check_not_err(n.way(data, {'highway': 'residential', 'priority': 'backward', 'traffic_sign:backward': 'NL:F6'}, [0]), expected={'class': 90205, 'subclass': 1108961023})
        self.check_not_err(n.way(data, {'highway': 'residential', 'priority': 'backward', 'traffic_sign:forward': 'NL:F5'}, [0]), expected={'class': 90205, 'subclass': 1108961023})
        self.check_err(n.way(data, {'highway': 'residential', 'priority': 'forward', 'traffic_sign:forward': 'NL:F5'}, [0]), expected={'class': 90205, 'subclass': 1108961023})
        self.check_not_err(n.way(data, {'highway': 'residential', 'priority:conditional': 'forward @ (10:00-12:00)', 'traffic_sign:forward': 'NL:F6'}, [0]), expected={'class': 90205, 'subclass': 1108961023})
        self.check_err(n.way(data, {'highway': 'residential', 'priority': 'backward', 'traffic_sign:forward': 'NL:F6'}, [0]), expected={'class': 90205, 'subclass': 1108961023})
        self.check_not_err(n.way(data, {'highway': 'residential', 'priority': 'forward', 'traffic_sign:forward': 'NL:F6'}, [0]), expected={'class': 90205, 'subclass': 1108961023})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign:forward': 'NL:F6'}, [0]), expected={'class': 90205, 'subclass': 1108961023})
        self.check_err(n.way(data, {'highway': 'residential', 'priority:agricultural': 'backward', 'traffic_sign:forward': 'NL:F6;OB05'}, [0]), expected={'class': 90205, 'subclass': 1108961023})
        self.check_not_err(n.way(data, {'highway': 'residential', 'priority:agricultural': 'forward', 'traffic_sign:forward': 'NL:F6;OB05'}, [0]), expected={'class': 90205, 'subclass': 1108961023})
        self.check_not_err(n.way(data, {'cycleway': 'lane', 'highway': 'footway', 'traffic_sign': 'NL:G07-ZB'}, [0]), expected={'class': 90206, 'subclass': 1018129333})
        self.check_not_err(n.way(data, {'cycleway': 'no', 'highway': 'footway'}, [0]), expected={'class': 90206, 'subclass': 1018129333})
        self.check_not_err(n.way(data, {'highway': 'footway', 'segregated': 'yes', 'traffic_sign': 'NL:G07-ZB'}, [0]), expected={'class': 90206, 'subclass': 1018129333})
        self.check_not_err(n.way(data, {'highway': 'footway', 'segregated': 'yes', 'traffic_sign': 'NL:G7'}, [0]), expected={'class': 90206, 'subclass': 1018129333})
        self.check_err(n.way(data, {'highway': 'service', 'surface': 'niet bestraat'}, [0]), expected={'class': 90202, 'subclass': 1205828493})
        self.check_not_err(n.way(data, {'highway': 'service', 'surface': 'paving_stones'}, [0]), expected={'class': 90202, 'subclass': 1205828493})
        self.check_err(n.way(data, {'highway': 'service', 'surface': 'straatstenen'}, [0]), expected={'class': 90202, 'subclass': 1205828493})
        self.check_not_err(n.way(data, {'material': 'bronze', 'tourism': 'artwork'}, [0]), expected={'class': 90202, 'subclass': 1205828493})
        self.check_not_err(n.way(data, {'highway': 'footway', 'surface': 'paving_stones'}, [0]), expected={'class': 90202, 'subclass': 1868473171})
        self.check_not_err(n.way(data, {'cycleway:surface': 'paving_stones:20', 'highway': 'residential', 'sidewalk:surface': 'paving_stones'}, [0]), expected={'class': 90202, 'subclass': 1911834456})
        self.check_not_err(n.way(data, {'cycleway:surface': 'paving_stones:20', 'highway': 'residential', 'sidewalk:surface': 'paving_stones:30'}, [0]), expected={'class': 90202, 'subclass': 1911834456})
        self.check_not_err(n.way(data, {'bicycle:conditional': 'yes @ (sunrise-sunset)', 'highway': 'cycleway', 'vehicle': 'no'}, [0]), expected={'class': 90209, 'subclass': 48304768})
        self.check_not_err(n.way(data, {'highway': 'cycleway', 'traffic_sign': 'NL:C01', 'vehicle': 'no'}, [0]), expected={'class': 90209, 'subclass': 48304768})
        self.check_not_err(n.way(data, {'highway': 'cycleway', 'moped': 'designated', 'traffic_sign': 'NL:D104', 'vehicle': 'no'}, [0]), expected={'class': 90209, 'subclass': 48304768})
        self.check_not_err(n.way(data, {'leisure': 'pitch', 'sport': 'boules', 'surface': 'gravel'}, [0]), expected={'class': 90209, 'subclass': 1521090750})
        self.check_err(n.way(data, {'highway': 'service', 'name': 'McDonalds drive through'}, [0]), expected={'class': 90203, 'subclass': 2144375058})
        self.check_err(n.way(data, {'highway': 'service', 'name': 'fiets- en bromfietspad'}, [0]), expected={'class': 90203, 'subclass': 2144375058})
        self.check_err(n.way(data, {'highway': 'service', 'name': 'onverplicht fietspad'}, [0]), expected={'class': 90203, 'subclass': 2144375058})
        self.check_err(n.way(data, {'highway': 'service', 'name': 'parkeerplaats voor bezoekers'}, [0]), expected={'class': 90203, 'subclass': 2144375058})
        self.check_err(n.way(data, {'highway': 'service', 'name': 'rolstoelpad'}, [0]), expected={'class': 90203, 'subclass': 2144375058})
        self.check_not_err(n.way(data, {'highway': 'unclassified', 'name': 'Gesloten Stad'}, [0]), expected={'class': 90203, 'subclass': 2144375058})
        self.check_not_err(n.way(data, {'highway': 'unclassified', 'name': 'Landbouwweg'}, [0]), expected={'class': 90203, 'subclass': 2144375058})
        self.check_not_err(n.way(data, {'highway': 'residential', 'name': 'De Visserstraat'}, [0]), expected={'class': 90203, 'subclass': 397885213})
        self.check_not_err(n.way(data, {'highway': 'residential', 'name': 'J.T. de Visserstraat'}, [0]), expected={'class': 90203, 'subclass': 397885213})
        self.check_not_err(n.way(data, {'highway': 'residential', 'name': 'Jac. P. Thijsseplein'}, [0]), expected={'class': 90203, 'subclass': 397885213})
        self.check_not_err(n.way(data, {'highway': 'residential', 'name': 'Th. Weeversweg'}, [0]), expected={'class': 90203, 'subclass': 397885213})
        self.check_not_err(n.way(data, {'highway': 'residential', 'name': 'Wim Kan Dreef'}, [0]), expected={'class': 90203, 'subclass': 397885213})
        self.check_not_err(n.way(data, {'highway': 'cycleway', 'living_street': 'yes', 'moped': 'no'}, [0]), expected={'class': 90207, 'subclass': 1217260303})
        self.check_not_err(n.way(data, {'highway': 'cycleway', 'living_street': 'yes', 'maxspeed': '15', 'moped': 'yes'}, [0]), expected={'class': 90207, 'subclass': 1217260303})
        self.check_not_err(n.way(data, {'highway': 'cycleway', 'living_street': 'yes'}, [0]), expected={'class': 90207, 'subclass': 1217260303})
        self.check_not_err(n.way(data, {'highway': 'cycleway', 'maxspeed:type': 'NL:rural'}, [0]), expected={'class': 90207, 'subclass': 1217260303})
        self.check_not_err(n.way(data, {'highway': 'footway', 'living_street': 'yes'}, [0]), expected={'class': 90207, 'subclass': 1217260303})
        self.check_not_err(n.way(data, {'highway': 'living_street', 'maxspeed': '10', 'traffic_sign': 'NL:A01-10'}, [0]), expected={'class': 90207, 'subclass': 1217260303})
        self.check_not_err(n.way(data, {'highway': 'living_street', 'maxspeed': '18'}, [0]), expected={'class': 90207, 'subclass': 1217260303})
        self.check_err(n.way(data, {'highway': 'residential', 'maxspeed:type': 'NL:rural'}, [0]), expected={'class': 90207, 'subclass': 1217260303})
        self.check_not_err(n.way(data, {'highway': 'residential', 'source:maxspeed': 'NL:rural'}, [0]), expected={'class': 90207, 'subclass': 1217260303})
        self.check_err(n.way(data, {'highway': 'primary', 'maxspeed': '50', 'maxspeed:type': 'NL:rural'}, [0]), expected={'class': 90207, 'subclass': 1487727138})
        self.check_not_err(n.way(data, {'highway': 'primary', 'maxspeed:type': 'NL:zone30'}, [0]), expected={'class': 90207, 'subclass': 1487727138})
        self.check_err(n.way(data, {'highway': 'primary', 'maxspeed': '50', 'source:maxspeed': 'NL:zone60'}, [0]), expected={'class': 90207, 'subclass': 1487727138})
        self.check_not_err(n.way(data, {'highway': 'residential', 'maxspeed': '20', 'maxspeed:type': 'NL:zone20'}, [0]), expected={'class': 90207, 'subclass': 1250414020})
        self.check_err(n.way(data, {'highway': 'residential', 'maxspeed:type': 'NL:zone20'}, [0]), expected={'class': 90207, 'subclass': 1250414020})
        self.check_not_err(n.way(data, {'highway': 'residential', 'maxspeed:forward': '30', 'traffic_sign:forward': 'NL:A1-30'}, [0]), expected={'class': 90207, 'subclass': 1250414020})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign:forward': 'NL:A1-30-ZB'}, [0]), expected={'class': 90207, 'subclass': 1250414020})
        self.check_not_err(n.way(data, {'highway': 'residential', 'maxspeed:advisory:both_ways': '50', 'traffic_sign': 'NL:A4[50]'}, [0]), expected={'class': 90207, 'subclass': 1250414020})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign': 'NL:A4[60]'}, [0]), expected={'class': 90207, 'subclass': 1250414020})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign': 'NL:C16; NL:A01-30'}, [0]), expected={'class': 90207, 'subclass': 1250414020})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign': 'NL:C16;NL:A01-30'}, [0]), expected={'class': 90207, 'subclass': 1250414020})
        self.check_not_err(n.way(data, {'highway': 'residential', 'maxspeed': '30', 'traffic_sign': 'NL:A01-30'}, [0]), expected={'class': 90207, 'subclass': 1250414020})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign': 'NL:A01-30'}, [0]), expected={'class': 90207, 'subclass': 1250414020})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign': 'NL:A04-30'}, [0]), expected={'class': 90207, 'subclass': 1250414020})
        self.check_err(n.way(data, {'highway': 'residential', 'traffic_sign': 'NL:A4'}, [0]), expected={'class': 90207, 'subclass': 1250414020})
        self.check_not_err(n.way(data, {'highway': 'cycleway', 'maxspeed': '80', 'motor_vehicle:conditional': 'yes @ Sa-Su'}, [0]), expected={'class': 90207, 'subclass': 2041800782})
        self.check_not_err(n.way(data, {'highway': 'cycleway', 'maxspeed': '80', 'motor_vehicle': 'destination'}, [0]), expected={'class': 90207, 'subclass': 2041800782})
        self.check_not_err(n.way(data, {'highway': 'motorway', 'maxspeed': '120'}, [0]), expected={'class': 90207, 'subclass': 2041800782})
        self.check_not_err(n.way(data, {'highway': 'motorway_link', 'maxspeed': '130', 'motorroad': 'yes'}, [0]), expected={'class': 90207, 'subclass': 2041800782})
        self.check_not_err(n.way(data, {'highway': 'tertiary', 'maxspeed': '100', 'motorroad': 'yes'}, [0]), expected={'class': 90207, 'subclass': 2041800782})
        self.check_not_err(n.way(data, {'highway': 'trunk', 'maxspeed': '90'}, [0]), expected={'class': 90207, 'subclass': 2041800782})
        self.check_not_err(n.way(data, {'highway': 'trunk_link', 'maxspeed': '100'}, [0]), expected={'class': 90207, 'subclass': 2041800782})
        self.check_not_err(n.way(data, {'highway': 'unclassified', 'maxspeed': '80'}, [0]), expected={'class': 90207, 'subclass': 2041800782})
        self.check_not_err(n.way(data, {'highway': 'unclassified', 'maxspeed:moped': '45'}, [0]), expected={'class': 90207, 'subclass': 790150725})
        self.check_not_err(n.way(data, {'highway': 'living_street', 'maxspeed': '10', 'traffic_sign': 'NL:A01-10'}, [0]), expected={'class': 90207, 'subclass': 1145458059})
        self.check_not_err(n.way(data, {'highway': 'cycleway', 'maxspeed': '40'}, [0]), expected={'class': 90207, 'subclass': 293871183})
        self.check_not_err(n.way(data, {'highway': 'residential', 'maxspeed': '30'}, [0]), expected={'class': 90207, 'subclass': 293871183})
        self.check_not_err(n.way(data, {'access': 'permissive', 'highway': 'unclassified', 'maxspeed': '25', 'note': 'eigen_weg'}, [0]), expected={'class': 90207, 'subclass': 293871183})
        self.check_not_err(n.way(data, {'access': 'designated', 'bicycle': 'designated', 'highway': 'residential', 'moped': 'designated'}, [0]), expected={'class': 90208, 'subclass': 2061019359})
        self.check_not_err(n.way(data, {'bicycle': 'designated', 'highway': 'residential', 'moped': 'designated'}, [0]), expected={'class': 90208, 'subclass': 2061019359})
        self.check_not_err(n.way(data, {'access': 'no', 'bicycle': 'designated', 'highway': 'residential', 'mofa': 'designated', 'moped': 'designated'}, [0]), expected={'class': 90208, 'subclass': 2061019359})
        self.check_not_err(n.way(data, {'bicycle': 'designated', 'highway': 'residential', 'moped': 'designated'}, [0]), expected={'class': 90208, 'subclass': 1443086133})
        self.check_not_err(n.way(data, {'bicycle': 'designated', 'highway': 'busway', 'mofa': 'designated', 'moped': 'designated'}, [0]), expected={'class': 90208, 'subclass': 1443086133})
        self.check_not_err(n.way(data, {'bicycle': 'designated', 'highway': 'busway', 'moped': 'destination'}, [0]), expected={'class': 90208, 'subclass': 1443086133})
        self.check_not_err(n.relation(data, {'building': 'house', 'type': 'multipolygon'}, []), expected={'class': 90201, 'subclass': 1486034706})
        self.check_not_err(n.relation(data, {'addr:housenumber': '2', 'building': 'houseboat', 'type': 'multipolygon'}, []), expected={'class': 90201, 'subclass': 1486034706})
        self.check_not_err(n.relation(data, {'addr:housename': 'huis', 'building': 'yes', 'type': 'multipolygon'}, []), expected={'class': 90201, 'subclass': 1486034706})
        self.check_not_err(n.relation(data, {'ref:bag': '0004567890123456; 1234567890123456', 'type': 'multipolygon'}, []), expected={'class': 90209, 'subclass': 2021092431})
        self.check_not_err(n.relation(data, {'ref:bag': '0004567890123456', 'type': 'multipolygon'}, []), expected={'class': 90209, 'subclass': 2021092431})
        self.check_not_err(n.relation(data, {'ref:bag': '0050123456789012', 'type': 'multipolygon'}, []), expected={'class': 90209, 'subclass': 2021092431})
        self.check_not_err(n.relation(data, {'ref:bag': '0200123456789012', 'type': 'multipolygon'}, []), expected={'class': 90209, 'subclass': 2021092431})
        self.check_not_err(n.relation(data, {'ref:bag': '0234567890123456', 'type': 'multipolygon'}, []), expected={'class': 90209, 'subclass': 2021092431})
        self.check_not_err(n.relation(data, {'ref:bag': '0310123456789012', 'type': 'multipolygon'}, []), expected={'class': 90209, 'subclass': 2021092431})
        self.check_not_err(n.relation(data, {'ref:bag': '050123456789012', 'type': 'multipolygon'}, []), expected={'class': 90209, 'subclass': 2021092431})
        self.check_not_err(n.relation(data, {'ref:bag': '1234567890123456', 'type': 'multipolygon'}, []), expected={'class': 90209, 'subclass': 2021092431})
        self.check_not_err(n.relation(data, {'ref:bag': '200123456789012', 'type': 'multipolygon'}, []), expected={'class': 90209, 'subclass': 2021092431})
        self.check_not_err(n.relation(data, {'ref:bag': '310123456789012', 'type': 'multipolygon'}, []), expected={'class': 90209, 'subclass': 2021092431})
        self.check_not_err(n.relation(data, {'ref:bag': '4567890123456', 'type': 'multipolygon'}, []), expected={'class': 90209, 'subclass': 2021092431})
        self.check_not_err(n.relation(data, {'ref:bag': '50123456789012', 'type': 'multipolygon'}, []), expected={'class': 90209, 'subclass': 2021092431})
        self.check_not_err(n.relation(data, {'except': 'bicycle', 'type': 'restriction'}, []), expected={'class': 90208, 'subclass': 92591020})
        self.check_not_err(n.relation(data, {'except': 'bicycle;mofa;moped', 'type': 'restriction'}, []), expected={'class': 90208, 'subclass': 92591020})
