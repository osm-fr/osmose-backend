#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Josm_DutchSpecific(PluginMapCSS):

    MAPCSS_URL = 'https://github.com/Famlam/OsmMapcssValidationNL/blob/main/netherlands.validator.mapcss'

    only_for = ['NL']


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
        self.errors[8] = self.def_class(item = 9020, level = 3, tags = [], title = mapcss.tr('NL other'))

        self.re_076895f4 = re.compile(r'payment:O[vV][-_]?[cC]hipkaart')
        self.re_088b0835 = re.compile(r'^addr:')
        self.re_092e62c6 = re.compile(r'(?i)klanten|bezoek(ers)?|medewerkers')
        self.re_143f11c5 = re.compile(r'^(no|use_sidepath)$')
        self.re_1582ff37 = re.compile(r'(?i)bus\s?(baan|strook)')
        self.re_1705b261 = re.compile(r'(?i)(^|\sen\s)((on)?verplicht\s)?(\(?brom\)?)?fietspad$')
        self.re_17085e60 = re.compile(r'houseboat|static_caravan')
        self.re_1d0c9a01 = re.compile(r'^NL:zone[36]0$')
        self.re_1d5e121c = re.compile(r'(?i)(parkeren$|parkeerplaats$|^toegang(sweg)?\s|^richting\s|^naar\s|\svoor\s|drive.thro?u(gh)?)')
        self.re_1d614d5c = re.compile(r'^maxspeed(:forward|:backward|:both_ways)?$')
        self.re_2441139b = re.compile(r'(?i)\b(aansl|empl|goed|ind|inhaalsp|opstel|overloopw|racc|rang|terr)\b')
        self.re_29759ca2 = re.compile(r'^(Burg|Dr|Drs|Ds|Ing|Ir|Mr|Past|Prof|St) [A-Z]')
        self.re_2e9c161c = re.compile(r'[0-9]{4} ?[A-Z]{2}')
        self.re_30fdb33a = re.compile(r'(?i)^(lift)$')
        self.re_3b632660 = re.compile(r'^(Burg|Dr|Drs|Ds|Ing|Ir|Mr|Past|Prof|St) [A-Za-z]')
        self.re_3c163648 = re.compile(r'(?i)ball?(veld(je)?)?$')
        self.re_44720f99 = re.compile(r'(?i)^roltrap(pen)?$')
        self.re_467ce1ba = re.compile(r'(?i)(parkeren|parkeerplaats|parkeergarage|^garage)$')
        self.re_47aaa0f7 = re.compile(r'^(yes|designated)$')
        self.re_493c424f = re.compile(r'^(0031|\+31|0) ?[1-9]( ?[0-9]){9}')
        self.re_508e7773 = re.compile(r'^(\+|00)31 ?0?[0-9]{3,7}$')
        self.re_51d31414 = re.compile(r'[A-Z][a-z]+\.')
        self.re_51f98600 = re.compile(r'^yes$')
        self.re_543ffeee = re.compile(r'(?i)(rolstoel|invaliden)')
        self.re_550ffc74 = re.compile(r'^building(:part)?$')
        self.re_5578cc63 = re.compile(r'100.+19:00')
        self.re_5e498788 = re.compile(r'^(left|right|both|yes)$')
        self.re_5ed5036a = re.compile(r'(?i)^speeltuin$')
        self.re_5f5aa10b = re.compile(r'^footway(:left|:right|:both)?:')
        self.re_6211f625 = re.compile(r'(?i)(voormalige?)')
        self.re_65f97ba4 = re.compile(r'^(00|\+)31 ?0')
        self.re_6cd83c9e = re.compile(r'(?i)^gratis\s|gratis\)')
        self.re_7184e9bc = re.compile(r'^sidewalk:(left|right|both)$')
        self.re_71a0b33c = re.compile(r'(?i)(drinkwater|\swater|kraan)')
        self.re_798edef1 = re.compile(r'(?i)(aansl|empl|goed|ind|inhaalsp|opstel|overloopw|racc|rang|terr)\.')
        self.re_7acb98bb = re.compile(r'^maxspeed(:forward|:backward|:both_ways)?(:conditional)?$')
        self.re_7be1bafc = re.compile(r'^1[23]0$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_badPhoneNumber = False

        # node[contact:phone=~/^(00|\+)31 ?0/]
        # node[contact:mobile=~/^(00|\+)31 ?0/]
        # node[phone=~/^(00|\+)31 ?0/]
        if ('contact:mobile' in keys) or ('contact:phone' in keys) or ('phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_65f97ba4), mapcss._tag_capture(capture_tags, 0, tags, 'contact:phone'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_65f97ba4), mapcss._tag_capture(capture_tags, 0, tags, 'contact:mobile'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_65f97ba4), mapcss._tag_capture(capture_tags, 0, tags, 'phone'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .badPhoneNumber
                # group:tr("NL addresses and contacts")
                # throwWarning:tr("Invalid tag {0}: country code should not be followed by a 0","{0.key}")
                # assertMatch:"node phone=\"+31 06123456789\""
                # assertNoMatch:"node phone=\"+31 6123456789\""
                # assertMatch:"node phone=\"003106123456789\""
                # assertNoMatch:"node phone=\"00316123456789\""
                # assertNoMatch:"node phone=\"06123456789\""
                set_badPhoneNumber = True
                err.append({'class': 1, 'subclass': 1989771860, 'text': mapcss.tr('Invalid tag {0}: country code should not be followed by a 0', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # node[contact:phone=~/^(\+|00)31 ?0?[0-9]{3,7}$/]!.badPhoneNumber
        # node[contact:mobile=~/^(\+|00)31 ?0?[0-9]{3,7}$/]!.badPhoneNumber
        # node[phone=~/^(\+|00)31 ?0?[0-9]{3,7}$/]!.badPhoneNumber
        if ('contact:mobile' in keys) or ('contact:phone' in keys) or ('phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_badPhoneNumber) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_508e7773), mapcss._tag_capture(capture_tags, 0, tags, 'contact:phone'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_badPhoneNumber) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_508e7773), mapcss._tag_capture(capture_tags, 0, tags, 'contact:mobile'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_badPhoneNumber) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_508e7773), mapcss._tag_capture(capture_tags, 0, tags, 'phone'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .badPhoneNumber
                # group:tr("NL addresses and contacts")
                # throwWarning:tr("Invalid tag {0}: short phone numbers cannot be used with international prefix (or: wrong phone number length)","{0.key}")
                # assertMatch:"node phone=\"+31 08008844\""
                # assertNoMatch:"node phone=\"+31 6123456789\""
                # assertMatch:"node phone=\"+3114024\""
                # assertNoMatch:"node phone=\"00316123456789\""
                # assertMatch:"node phone=\"00318008844\""
                # assertNoMatch:"node phone=\"06123456789\""
                # assertNoMatch:"node phone=\"08008844\""
                # assertNoMatch:"node phone=\"14024\""
                set_badPhoneNumber = True
                err.append({'class': 1, 'subclass': 865550819, 'text': mapcss.tr('Invalid tag {0}: short phone numbers cannot be used with international prefix (or: wrong phone number length)', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # node[contact:phone=~/^(0031|\+31|0) ?[1-9]( ?[0-9]){9}/][inside("NL")]!.badPhoneNumber
        # node[contact:mobile=~/^(0031|\+31|0) ?[1-9]( ?[0-9]){9}/][inside("NL")]!.badPhoneNumber
        # node[phone=~/^(0031|\+31|0) ?[1-9]( ?[0-9]){9}/][inside("NL")]!.badPhoneNumber
        if ('contact:mobile' in keys) or ('contact:phone' in keys) or ('phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_badPhoneNumber) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_493c424f), mapcss._tag_capture(capture_tags, 0, tags, 'contact:phone'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_badPhoneNumber) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_493c424f), mapcss._tag_capture(capture_tags, 0, tags, 'contact:mobile'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_badPhoneNumber) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_493c424f), mapcss._tag_capture(capture_tags, 0, tags, 'phone'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL addresses and contacts")
                # throwWarning:tr("Invalid tag {0}: too many digits (or foreign number, if so: ignore)","{0.key}")
                # assertNoMatch:"node phone=\"+31 6 12345678\""
                # assertNoMatch:"node phone=\"0031612345678\""
                # assertNoMatch:"node phone=\"06 12345678\""
                err.append({'class': 1, 'subclass': 1083644254, 'text': mapcss.tr('Invalid tag {0}: too many digits (or foreign number, if so: ignore)', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

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

        # node[name][highway][name=~/(?i)^(lift)$/]
        # node[amenity=drinking_water][name=~/(?i)(drinkwater|\swater|kraan)/]
        # *[name][amenity^=parking][name=~/(?i)(parkeren|parkeerplaats|parkeergarage|^garage)$/]
        # *[name][name=~/(?i)^gratis\s|gratis\)/]
        # *[name][name=~/(?i)klanten|bezoek(ers)?|medewerkers/][!route]
        # *[name][leisure=playground][name=~/(?i)^speeltuin$/]
        # *[name][leisure=pitch][name=~/(?i)ball?(veld(je)?)?$/][!sport]
        if ('amenity' in keys and 'name' in keys) or ('highway' in keys and 'name' in keys) or ('leisure' in keys and 'name' in keys) or ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_30fdb33a), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'drinking_water')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_71a0b33c), mapcss._tag_capture(capture_tags, 1, tags, 'name'))))
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
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_092e62c6), mapcss._tag_capture(capture_tags, 1, tags, 'name'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'route')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'leisure') == mapcss._value_capture(capture_tags, 1, 'playground')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_5ed5036a), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'leisure') == mapcss._value_capture(capture_tags, 1, 'pitch')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3c163648), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'sport')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("descriptive name")
                err.append({'class': 3, 'subclass': 1639376910, 'text': mapcss.tr('descriptive name')})

        # *[name][name=~/(?i)(voormalige?)/][!historic][tourism!=information][!landuse]
        if ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6211f625), mapcss._tag_capture(capture_tags, 1, tags, 'name'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'historic')) and (mapcss._tag_capture(capture_tags, 3, tags, 'tourism') != mapcss._value_const_capture(capture_tags, 3, 'information', 'information')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'landuse')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("descriptive name")
                # suggestAlternative:"description=*"
                # suggestAlternative:"old_name=*"
                err.append({'class': 3, 'subclass': 38536799, 'text': mapcss.tr('descriptive name')})

        # *[name][highway][name=~/^(Burg|Dr|Drs|Ds|Ing|Ir|Mr|Past|Prof|St) [A-Za-z]/][inside("NL")]
        # *[addr:street][addr:street=~/[A-Z][a-z]+\./][inside("NL")]
        if ('addr:street' in keys) or ('highway' in keys and 'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3b632660), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'addr:street')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_51d31414), mapcss._tag_capture(capture_tags, 1, tags, 'addr:street'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("Straatnaam met afkorting")
                err.append({'class': 3, 'subclass': 414563913, 'text': mapcss.tr('Straatnaam met afkorting')})

        # *[railway][name][name=~/(?i)(aansl|empl|goed|ind|inhaalsp|opstel|overloopw|racc|rang|terr)\./][inside("NL")]
        # *[railway][name][name=~/(?i)\b(aansl|empl|goed|ind|inhaalsp|opstel|overloopw|racc|rang|terr)\b/][inside("NL")]
        if ('name' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_798edef1), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_2441139b), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("Spoorgebied met afgekorte naam")
                # suggestAlternative:"aansluiting, emplacement, goederen, industrieterrein, inhaalspoor, opstelterrein, overloopwissel, raccordement of rangeerterrein"
                # assertNoMatch:"node railway=tram_stop name=Landgoed"
                err.append({'class': 3, 'subclass': 884545585, 'text': mapcss.tr('Spoorgebied met afgekorte naam')})

        # *[name][place][name=~/^(Burg|Dr|Drs|Ds|Ing|Ir|Mr|Past|Prof|St) [A-Z]/][inside("NL")]
        # *[name][place][name=~/[A-Z][a-z]+\./][inside("NL")]
        if ('name' in keys and 'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'place')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_29759ca2), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'place')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_51d31414), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("Gebiedsnaam met afkorting")
                err.append({'class': 3, 'subclass': 1559900162, 'text': mapcss.tr('Gebiedsnaam met afkorting')})

        # *[name:nl][!name][inside("NL")][type!=route]
        if ('name:nl' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name:nl')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, 3, tags, 'type') != mapcss._value_const_capture(capture_tags, 3, 'route', 'route')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("{0} without {1}","{0.key}","{1.key}")
                # suggestAlternative:"name"
                # fixChangeKey:"{0.key}=>{1.key}"
                err.append({'class': 3, 'subclass': 152569614, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}')), 'allow_fix_override': True, 'fix': {
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

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_badPhoneNumber = False

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
        # way[highway][traffic_sign~="NL:G5"][highway!=living_street][highway!=construction]
        # way[highway][traffic_sign~="NL:G05"][highway!=living_street][highway!=construction]
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
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G5'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'living_street', 'living_street')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:G05'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'living_street', 'living_street')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
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
                err.append({'class': 5, 'subclass': 732431678, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

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

        # way[highway][traffic_sign~="NL:C1"][!vehicle][!vehicle:forward][!vehicle:backward][!vehicle:both_ways][!access][!access:forward][!access:backward][!access:both_ways]
        # way[highway][traffic_sign~="NL:C01"][!vehicle][!vehicle:forward][!vehicle:backward][!vehicle:both_ways][!access][!access:forward][!access:backward][!access:both_ways]
        # way[highway][traffic_sign~="NL:C6"][!motor_vehicle][!motor_vehicle:forward][!motor_vehicle:backward][!motor_vehicle:both_ways][!vehicle][!vehicle:forward][!vehicle:backward][!vehicle:both_ways][!access][!access:forward][!access:backward][!access:both_ways]
        # way[highway][traffic_sign~="NL:C06"][!motor_vehicle][!motor_vehicle:forward][!motor_vehicle:backward][!motor_vehicle:both_ways][!vehicle][!vehicle:forward][!vehicle:backward][!vehicle:both_ways][!access][!access:forward][!access:backward][!access:both_ways]
        # way[highway][traffic_sign~="NL:C7"][!hgv][!hgv:forward][!hgv:backward][!hgv:both_ways]
        # way[highway][traffic_sign~="NL:C07"][!hgv][!hgv:forward][!hgv:backward][!hgv:both_ways]
        # way[highway][traffic_sign~="NL:C9"][!bicycle][!bicycle:forward][!bicycle:backward][!bicycle:both_ways]
        # way[highway][traffic_sign~="NL:C9"][!moped][!moped:forward][!moped:backward][!moped:both_ways]
        # way[highway][traffic_sign~="NL:C09"][!bicycle][!bicycle:forward][!bicycle:backward][!bicycle:both_ways]
        # way[highway][traffic_sign~="NL:C09"][!moped][!moped:forward][!moped:backward][!moped:both_ways]
        # way[highway][traffic_sign~="NL:C10"][!trailer][!trailer:forward][!trailer:backward][!trailer:both_ways]
        # way[highway][traffic_sign~="NL:C11"][!motorcycle][!motorcycle:forward][!motorcycle:backward][!motorcycle:both_ways]
        # way[highway][traffic_sign~="NL:C12"][!motor_vehicle][!motor_vehicle:forward][!motor_vehicle:backward][!motor_vehicle:both_ways][!vehicle][!vehicle:forward][!vehicle:backward][!vehicle:both_ways][!access][!access:forward][!access:backward][!access:both_ways]
        # way[highway][traffic_sign~="NL:C13"][!moped][!moped:forward][!moped:backward][!moped:both_ways]
        # way[highway][traffic_sign~="NL:C14"][!bicycle][!bicycle:forward][!bicycle:backward][!bicycle:both_ways]
        # way[highway][traffic_sign~="NL:C15"][!bicycle][!bicycle:forward][!bicycle:backward][!bicycle:both_ways]
        # way[highway][traffic_sign~="NL:C15"][!moped][!moped:forward][!moped:backward][!moped:both_ways]
        # way[highway][traffic_sign~="NL:C16"][!foot][!foot:forward][!foot:backward][!foot:both_ways][!access][!access:forward][!access:backward][!access:both_ways][!vehicle][!vehicle:forward][!vehicle:backward][!vehicle:both_ways]
        if ('highway' in keys and 'traffic_sign' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C1'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'vehicle')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'vehicle:forward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'vehicle:backward')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'vehicle:both_ways')) and (not mapcss._tag_capture(capture_tags, 6, tags, 'access')) and (not mapcss._tag_capture(capture_tags, 7, tags, 'access:forward')) and (not mapcss._tag_capture(capture_tags, 8, tags, 'access:backward')) and (not mapcss._tag_capture(capture_tags, 9, tags, 'access:both_ways')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C01'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'vehicle')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'vehicle:forward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'vehicle:backward')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'vehicle:both_ways')) and (not mapcss._tag_capture(capture_tags, 6, tags, 'access')) and (not mapcss._tag_capture(capture_tags, 7, tags, 'access:forward')) and (not mapcss._tag_capture(capture_tags, 8, tags, 'access:backward')) and (not mapcss._tag_capture(capture_tags, 9, tags, 'access:both_ways')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C6'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motor_vehicle')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'motor_vehicle:forward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'motor_vehicle:backward')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'motor_vehicle:both_ways')) and (not mapcss._tag_capture(capture_tags, 6, tags, 'vehicle')) and (not mapcss._tag_capture(capture_tags, 7, tags, 'vehicle:forward')) and (not mapcss._tag_capture(capture_tags, 8, tags, 'vehicle:backward')) and (not mapcss._tag_capture(capture_tags, 9, tags, 'vehicle:both_ways')) and (not mapcss._tag_capture(capture_tags, 10, tags, 'access')) and (not mapcss._tag_capture(capture_tags, 11, tags, 'access:forward')) and (not mapcss._tag_capture(capture_tags, 12, tags, 'access:backward')) and (not mapcss._tag_capture(capture_tags, 13, tags, 'access:both_ways')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C06'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motor_vehicle')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'motor_vehicle:forward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'motor_vehicle:backward')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'motor_vehicle:both_ways')) and (not mapcss._tag_capture(capture_tags, 6, tags, 'vehicle')) and (not mapcss._tag_capture(capture_tags, 7, tags, 'vehicle:forward')) and (not mapcss._tag_capture(capture_tags, 8, tags, 'vehicle:backward')) and (not mapcss._tag_capture(capture_tags, 9, tags, 'vehicle:both_ways')) and (not mapcss._tag_capture(capture_tags, 10, tags, 'access')) and (not mapcss._tag_capture(capture_tags, 11, tags, 'access:forward')) and (not mapcss._tag_capture(capture_tags, 12, tags, 'access:backward')) and (not mapcss._tag_capture(capture_tags, 13, tags, 'access:both_ways')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C7'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'hgv')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'hgv:forward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'hgv:backward')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'hgv:both_ways')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C07'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'hgv')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'hgv:forward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'hgv:backward')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'hgv:both_ways')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C9'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bicycle')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'bicycle:forward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'bicycle:backward')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'bicycle:both_ways')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C9'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'moped:forward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'moped:backward')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'moped:both_ways')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C09'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bicycle')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'bicycle:forward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'bicycle:backward')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'bicycle:both_ways')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C09'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'moped:forward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'moped:backward')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'moped:both_ways')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C10'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'trailer')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'trailer:forward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'trailer:backward')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'trailer:both_ways')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C11'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motorcycle')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'motorcycle:forward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'motorcycle:backward')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'motorcycle:both_ways')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C12'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'motor_vehicle')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'motor_vehicle:forward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'motor_vehicle:backward')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'motor_vehicle:both_ways')) and (not mapcss._tag_capture(capture_tags, 6, tags, 'vehicle')) and (not mapcss._tag_capture(capture_tags, 7, tags, 'vehicle:forward')) and (not mapcss._tag_capture(capture_tags, 8, tags, 'vehicle:backward')) and (not mapcss._tag_capture(capture_tags, 9, tags, 'vehicle:both_ways')) and (not mapcss._tag_capture(capture_tags, 10, tags, 'access')) and (not mapcss._tag_capture(capture_tags, 11, tags, 'access:forward')) and (not mapcss._tag_capture(capture_tags, 12, tags, 'access:backward')) and (not mapcss._tag_capture(capture_tags, 13, tags, 'access:both_ways')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C13'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'moped:forward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'moped:backward')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'moped:both_ways')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C14'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bicycle')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'bicycle:forward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'bicycle:backward')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'bicycle:both_ways')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C15'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'bicycle')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'bicycle:forward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'bicycle:backward')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'bicycle:both_ways')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C15'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'moped')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'moped:forward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'moped:backward')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'moped:both_ways')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 1, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 1, 'NL:C16'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'foot')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'foot:forward')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'foot:backward')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'foot:both_ways')) and (not mapcss._tag_capture(capture_tags, 6, tags, 'access')) and (not mapcss._tag_capture(capture_tags, 7, tags, 'access:forward')) and (not mapcss._tag_capture(capture_tags, 8, tags, 'access:backward')) and (not mapcss._tag_capture(capture_tags, 9, tags, 'access:both_ways')) and (not mapcss._tag_capture(capture_tags, 10, tags, 'vehicle')) and (not mapcss._tag_capture(capture_tags, 11, tags, 'vehicle:forward')) and (not mapcss._tag_capture(capture_tags, 12, tags, 'vehicle:backward')) and (not mapcss._tag_capture(capture_tags, 13, tags, 'vehicle:both_ways')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL traffic signs")
                # throwWarning:tr("{0} without {1}","{1.tag}","{2.key}=no/private/destination/...")
                # assertMatch:"way highway=service traffic_sign=\"NL:C01\""
                # assertNoMatch:"way highway=service traffic_sign=\"NL:C01;NL:C16\" access=no"
                # assertMatch:"way highway=service traffic_sign=\"NL:C01;NL:OB58\""
                # assertNoMatch:"way highway=track traffic_sign=\"NL:C12\" motor_vehicle=no"
                err.append({'class': 5, 'subclass': 1346556208, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.key}=no/private/destination/...'))})

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

        # way[name][highway=service][name=~/(?i)(parkeren$|parkeerplaats$|^toegang(sweg)?\s|^richting\s|^naar\s|\svoor\s|drive.thro?u(gh)?)/]
        # way[name][highway][name=~/(?i)(^|\sen\s)((on)?verplicht\s)?(\(?brom\)?)?fietspad$/]
        # way[name][highway][name=~/(?i)^roltrap(pen)?$/]
        # way[name][highway][name=~/(?i)(rolstoel|invaliden)/]
        # way[name][highway][name=~/(?i)bus\s?(baan|strook)/][highway!=busway][highway!=service][highway!=construction]
        # *[name][amenity^=parking][name=~/(?i)(parkeren|parkeerplaats|parkeergarage|^garage)$/]
        # *[name][name=~/(?i)^gratis\s|gratis\)/]
        # *[name][name=~/(?i)klanten|bezoek(ers)?|medewerkers/][!route]
        # *[name][leisure=playground][name=~/(?i)^speeltuin$/]
        # *[name][leisure=pitch][name=~/(?i)ball?(veld(je)?)?$/][!sport]
        if ('amenity' in keys and 'name' in keys) or ('highway' in keys and 'name' in keys) or ('leisure' in keys and 'name' in keys) or ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway') == mapcss._value_capture(capture_tags, 1, 'service')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_1d5e121c), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
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
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_092e62c6), mapcss._tag_capture(capture_tags, 1, tags, 'name'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'route')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'leisure') == mapcss._value_capture(capture_tags, 1, 'playground')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_5ed5036a), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'leisure') == mapcss._value_capture(capture_tags, 1, 'pitch')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3c163648), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'sport')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("descriptive name")
                err.append({'class': 3, 'subclass': 656121223, 'text': mapcss.tr('descriptive name')})

        # *[name][name=~/(?i)(voormalige?)/][!historic][tourism!=information][!landuse]
        if ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6211f625), mapcss._tag_capture(capture_tags, 1, tags, 'name'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'historic')) and (mapcss._tag_capture(capture_tags, 3, tags, 'tourism') != mapcss._value_const_capture(capture_tags, 3, 'information', 'information')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'landuse')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("descriptive name")
                # suggestAlternative:"description=*"
                # suggestAlternative:"old_name=*"
                err.append({'class': 3, 'subclass': 38536799, 'text': mapcss.tr('descriptive name')})

        # *[name][highway][name=~/^(Burg|Dr|Drs|Ds|Ing|Ir|Mr|Past|Prof|St) [A-Za-z]/][inside("NL")]
        # *[addr:street][addr:street=~/[A-Z][a-z]+\./][inside("NL")]
        if ('addr:street' in keys) or ('highway' in keys and 'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3b632660), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'addr:street')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_51d31414), mapcss._tag_capture(capture_tags, 1, tags, 'addr:street'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("Straatnaam met afkorting")
                err.append({'class': 3, 'subclass': 414563913, 'text': mapcss.tr('Straatnaam met afkorting')})

        # *[railway][name][name=~/(?i)(aansl|empl|goed|ind|inhaalsp|opstel|overloopw|racc|rang|terr)\./][inside("NL")]
        # *[railway][name][name=~/(?i)\b(aansl|empl|goed|ind|inhaalsp|opstel|overloopw|racc|rang|terr)\b/][inside("NL")]
        if ('name' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_798edef1), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_2441139b), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("Spoorgebied met afgekorte naam")
                # suggestAlternative:"aansluiting, emplacement, goederen, industrieterrein, inhaalspoor, opstelterrein, overloopwissel, raccordement of rangeerterrein"
                err.append({'class': 3, 'subclass': 884545585, 'text': mapcss.tr('Spoorgebied met afgekorte naam')})

        # *[name][place][name=~/^(Burg|Dr|Drs|Ds|Ing|Ir|Mr|Past|Prof|St) [A-Z]/][inside("NL")]
        # *[name][place][name=~/[A-Z][a-z]+\./][inside("NL")]
        if ('name' in keys and 'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'place')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_29759ca2), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'place')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_51d31414), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("Gebiedsnaam met afkorting")
                err.append({'class': 3, 'subclass': 1559900162, 'text': mapcss.tr('Gebiedsnaam met afkorting')})

        # *[name:nl][!name][inside("NL")][type!=route]
        if ('name:nl' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name:nl')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, 3, tags, 'type') != mapcss._value_const_capture(capture_tags, 3, 'route', 'route')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("{0} without {1}","{0.key}","{1.key}")
                # suggestAlternative:"name"
                # fixChangeKey:"{0.key}=>{1.key}"
                err.append({'class': 3, 'subclass': 152569614, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}')), 'allow_fix_override': True, 'fix': {
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
        # way[maxspeed:type][!maxspeed][maxspeed:type^="NL:zone"][!maxspeed:both_ways][maxspeed:type!~/^NL:zone[36]0$/][highway]
        # way[maxspeed:type="NL:urban"][maxspeed!=50][maxspeed:both_ways!=50][highway]
        # way[maxspeed:type="NL:rural"][maxspeed!=80][maxspeed:both_ways!=80][highway]
        # way[traffic_sign][!maxspeed][traffic_sign^="NL:A1-"][!/^maxspeed(:forward|:backward|:both_ways)?(:conditional)?$/][highway]
        # way[traffic_sign][!maxspeed][traffic_sign^="NL:A01-"][!/^maxspeed(:forward|:backward|:both_ways)?(:conditional)?$/][highway]
        if ('highway' in keys) or ('highway' in keys and 'maxspeed:type' in keys) or ('highway' in keys and 'traffic_sign' in keys):
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
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:type')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss.startswith(mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed:type'), mapcss._value_capture(capture_tags, 2, 'NL:zone'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'maxspeed:both_ways')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 4, self.re_1d0c9a01, '^NL:zone[36]0$'), mapcss._tag_capture(capture_tags, 4, tags, 'maxspeed:type'))) and (mapcss._tag_capture(capture_tags, 5, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:type') == mapcss._value_capture(capture_tags, 0, 'NL:urban')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed') != mapcss._value_capture(capture_tags, 1, 50)) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed:both_ways') != mapcss._value_capture(capture_tags, 2, 50)) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:type') == mapcss._value_capture(capture_tags, 0, 'NL:rural')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed') != mapcss._value_capture(capture_tags, 1, 80)) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed:both_ways') != mapcss._value_capture(capture_tags, 2, 80)) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss.startswith(mapcss._tag_capture(capture_tags, 2, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 2, 'NL:A1-'))) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_7acb98bb)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss.startswith(mapcss._tag_capture(capture_tags, 2, tags, 'traffic_sign'), mapcss._value_capture(capture_tags, 2, 'NL:A01-'))) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_7acb98bb)) and (mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL speed limits")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.tag}")
                err.append({'class': 7, 'subclass': 1323990849, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

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
                # group:tr("NL other")
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
                # group:tr("NL other")
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
        set_badPhoneNumber = False

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

        # *[name][amenity^=parking][name=~/(?i)(parkeren|parkeerplaats|parkeergarage|^garage)$/]
        # *[name][name=~/(?i)^gratis\s|gratis\)/]
        # *[name][name=~/(?i)klanten|bezoek(ers)?|medewerkers/][!route]
        # *[name][leisure=playground][name=~/(?i)^speeltuin$/]
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
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_092e62c6), mapcss._tag_capture(capture_tags, 1, tags, 'name'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'route')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'leisure') == mapcss._value_capture(capture_tags, 1, 'playground')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_5ed5036a), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'leisure') == mapcss._value_capture(capture_tags, 1, 'pitch')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3c163648), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'sport')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("descriptive name")
                err.append({'class': 3, 'subclass': 340889626, 'text': mapcss.tr('descriptive name')})

        # *[name][name=~/(?i)(voormalige?)/][!historic][tourism!=information][!landuse]
        if ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6211f625), mapcss._tag_capture(capture_tags, 1, tags, 'name'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'historic')) and (mapcss._tag_capture(capture_tags, 3, tags, 'tourism') != mapcss._value_const_capture(capture_tags, 3, 'information', 'information')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'landuse')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("descriptive name")
                # suggestAlternative:"description=*"
                # suggestAlternative:"old_name=*"
                err.append({'class': 3, 'subclass': 38536799, 'text': mapcss.tr('descriptive name')})

        # *[name][highway][name=~/^(Burg|Dr|Drs|Ds|Ing|Ir|Mr|Past|Prof|St) [A-Za-z]/][inside("NL")]
        # *[addr:street][addr:street=~/[A-Z][a-z]+\./][inside("NL")]
        if ('addr:street' in keys) or ('highway' in keys and 'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3b632660), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'addr:street')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_51d31414), mapcss._tag_capture(capture_tags, 1, tags, 'addr:street'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("Straatnaam met afkorting")
                err.append({'class': 3, 'subclass': 414563913, 'text': mapcss.tr('Straatnaam met afkorting')})

        # *[railway][name][name=~/(?i)(aansl|empl|goed|ind|inhaalsp|opstel|overloopw|racc|rang|terr)\./][inside("NL")]
        # *[railway][name][name=~/(?i)\b(aansl|empl|goed|ind|inhaalsp|opstel|overloopw|racc|rang|terr)\b/][inside("NL")]
        if ('name' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_798edef1), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_2441139b), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("Spoorgebied met afgekorte naam")
                # suggestAlternative:"aansluiting, emplacement, goederen, industrieterrein, inhaalspoor, opstelterrein, overloopwissel, raccordement of rangeerterrein"
                err.append({'class': 3, 'subclass': 884545585, 'text': mapcss.tr('Spoorgebied met afgekorte naam')})

        # *[name][place][name=~/^(Burg|Dr|Drs|Ds|Ing|Ir|Mr|Past|Prof|St) [A-Z]/][inside("NL")]
        # *[name][place][name=~/[A-Z][a-z]+\./][inside("NL")]
        if ('name' in keys and 'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'place')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_29759ca2), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'place')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_51d31414), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'NL')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("Gebiedsnaam met afkorting")
                err.append({'class': 3, 'subclass': 1559900162, 'text': mapcss.tr('Gebiedsnaam met afkorting')})

        # *[name:nl][!name][inside("NL")][type!=route]
        if ('name:nl' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name:nl')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss.inside(self.father.config.options, 'NL')) and (mapcss._tag_capture(capture_tags, 3, tags, 'type') != mapcss._value_const_capture(capture_tags, 3, 'route', 'route')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("NL nomenclature")
                # throwWarning:tr("{0} without {1}","{0.key}","{1.key}")
                # suggestAlternative:"name"
                # fixChangeKey:"{0.key}=>{1.key}"
                err.append({'class': 3, 'subclass': 152569614, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}')), 'allow_fix_override': True, 'fix': {
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

        self.check_err(n.node(data, {'phone': '+31 06123456789'}), expected={'class': 1, 'subclass': 1989771860})
        self.check_not_err(n.node(data, {'phone': '+31 6123456789'}), expected={'class': 1, 'subclass': 1989771860})
        self.check_err(n.node(data, {'phone': '003106123456789'}), expected={'class': 1, 'subclass': 1989771860})
        self.check_not_err(n.node(data, {'phone': '00316123456789'}), expected={'class': 1, 'subclass': 1989771860})
        self.check_not_err(n.node(data, {'phone': '06123456789'}), expected={'class': 1, 'subclass': 1989771860})
        self.check_err(n.node(data, {'phone': '+31 08008844'}), expected={'class': 1, 'subclass': 865550819})
        self.check_not_err(n.node(data, {'phone': '+31 6123456789'}), expected={'class': 1, 'subclass': 865550819})
        self.check_err(n.node(data, {'phone': '+3114024'}), expected={'class': 1, 'subclass': 865550819})
        self.check_not_err(n.node(data, {'phone': '00316123456789'}), expected={'class': 1, 'subclass': 865550819})
        self.check_err(n.node(data, {'phone': '00318008844'}), expected={'class': 1, 'subclass': 865550819})
        self.check_not_err(n.node(data, {'phone': '06123456789'}), expected={'class': 1, 'subclass': 865550819})
        self.check_not_err(n.node(data, {'phone': '08008844'}), expected={'class': 1, 'subclass': 865550819})
        self.check_not_err(n.node(data, {'phone': '14024'}), expected={'class': 1, 'subclass': 865550819})
        self.check_not_err(n.node(data, {'phone': '+31 6 12345678'}), expected={'class': 1, 'subclass': 1083644254})
        self.check_not_err(n.node(data, {'phone': '0031612345678'}), expected={'class': 1, 'subclass': 1083644254})
        self.check_not_err(n.node(data, {'phone': '06 12345678'}), expected={'class': 1, 'subclass': 1083644254})
        self.check_not_err(n.node(data, {'name': 'Landgoed', 'railway': 'tram_stop'}), expected={'class': 3, 'subclass': 884545585})
        self.check_err(n.way(data, {'highway': 'service', 'traffic_sign': 'NL:C01'}, [0]), expected={'class': 5, 'subclass': 1346556208})
        self.check_not_err(n.way(data, {'access': 'no', 'highway': 'service', 'traffic_sign': 'NL:C01;NL:C16'}, [0]), expected={'class': 5, 'subclass': 1346556208})
        self.check_err(n.way(data, {'highway': 'service', 'traffic_sign': 'NL:C01;NL:OB58'}, [0]), expected={'class': 5, 'subclass': 1346556208})
        self.check_not_err(n.way(data, {'highway': 'track', 'motor_vehicle': 'no', 'traffic_sign': 'NL:C12'}, [0]), expected={'class': 5, 'subclass': 1346556208})
        self.check_err(n.way(data, {'highway': 'residential', 'parking:lane:both': 'no', 'traffic_sign:left': 'NL:E02'}, [0]), expected={'class': 5, 'subclass': 1501968560})
        self.check_err(n.way(data, {'highway': 'residential', 'parking:lane:left': 'no', 'traffic_sign:left': 'NL:E02'}, [0]), expected={'class': 5, 'subclass': 1501968560})
        self.check_not_err(n.way(data, {'highway': 'residential', 'parking:lane:left': 'parallel', 'traffic_sign:left': 'NL:E02'}, [0]), expected={'class': 5, 'subclass': 1501968560})
        self.check_not_err(n.way(data, {'highway': 'residential', 'parking:condition:both': 'no_stopping', 'parking:lane:both': 'no', 'traffic_sign:left': 'NL:E02', 'traffic_sign:right': 'NL:E02'}, [0]), expected={'class': 5, 'subclass': 1501968560})
