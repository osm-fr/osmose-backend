# coding: utf-8

import os as _os
import re as _re

import unittest as _unittest

import lark as _lark
from lark.lexer import Token as _Token


def get_parser():
    """
        Returns a Lark parser able to parse a valid field.
    """
    base_dir = _os.path.dirname(_os.path.realpath(__file__))
    with open(_os.path.join(base_dir, "field.ebnf"), 'rb') as f:
        grammar = f.read().decode("UTF-8")
    return _lark.Lark(grammar, start="time_domain", parser="earley")


# TODO: Fix 'Mo,SH'


PARSER = get_parser()


class SanitizeError(Exception):
    """
    Raised when something goes wrong during sanitizing.
    """
    pass


class InconsistentField(SanitizeError):
    """
    Raised when a field contains an error which can't be
    corrected automatically. Inherits from SanitizeError.
    """
    pass


class SanitizerTransformer(_lark.Transformer):
    def _call_userfunc(self, tree, new_children=None):
        # Comes from "lark/visitors.py", to avoid raising of a "VisitError".
        children = new_children if new_children is not None else tree.children
        try:
            f = getattr(self, tree.data)
        except AttributeError:
            return self.__default__(tree.data, children, tree.meta)
        else:
            if getattr(f, 'meta', False):
                return f(children, tree.meta)
            elif getattr(f, 'inline', False):
                return f(*children)
            elif getattr(f, 'whole_tree', False):
                if new_children is not None:
                    raise NotImplementedError("Doesn't work with the base Transformer class")
                return f(tree)
            else:
                return f(children)

    def time_domain(self, args):
        parts = []
        for arg in args:
            if isinstance(arg, _Token):
                parts.append(
                    {';': '; ', ',': ',', '||': ' || '}.get(arg.value.strip())
                )
            else:
                parts.append(arg)
        return ''.join(parts)

    def rule_sequence(self, args):
        if len(args) == 1 and isinstance(args[0], _Token):  # "off"
            return args[0].value.lower()
        return ' '.join(args)

    def always_open(self, args):
        return "24/7"

    def selector_sequence(self, args):
        if len(args) == 1:  # time_selector
            return args[0]
        elif args[0] == '': # same as below with an empty range_selectors
            return args[1]
        else:  # range_selectors " " time_selector
            return (args[0] + ' ' + args[1])

    def small_range_selectors(self, args):
        return args[0] + ' ' + args[-1]

    def range_selectors(self, args):
        return ' '.join(args).replace(' :', ':')

    # Dates
    def monthday_selector(self, args):
        return ','.join(args)

    def monthday_range(self, args):
        return '-'.join(args)

    def monthday_date(self, args):
        return ''.join(args)

    def monthday_date_day_to_day(self, args):
        year = args.pop(0) if len(args) == 4 else None
        month = args[0].value.capitalize()
        monthday_from = int(args[1].value)
        monthday_to = int(args[2].value)
        if year:
            return "{} {} {}-{}".format(year, month, monthday_from, monthday_to)
        else:
            return "{} {}-{}".format(month, monthday_from, monthday_to)

    def monthday_date_monthday(self, args):
        year = args.pop(0) if len(args) == 3 else None
        month = args[0].value.capitalize()
        monthday = int(args[1].value)
        if year:
            return "{} {} {}".format(year, month, monthday)
        else:
            return "{} {}".format(month, monthday)

    def monthday_date_month(self, args):
        year = args.pop(0) if len(args) == 2 else None
        month = args[0].value.capitalize()
        if year:
            return "{} {}".format(year, month)
        return month

    def monthday_date_easter(self, args):
        if len(args) == 1:  # "easter"
            return "easter"
        elif len(args) == 2:
            if isinstance(args[0], _Token):  # "easter +2 days"
                return "easter " + args[1]
            elif isinstance(args[1], _Token):  # "2020 easter"
                return args[0] + " easter"
        else:  # "2020 easter +2 days"
            return args[0] + " easter " + args[2]

    def day_offset(self, args):
        offset_sign = args[0].value
        days = int(args[1].value)
        if days == 1:
            return offset_sign + str(days) + " day"
        else:
            return offset_sign + str(days) + " days"

    # Nth entries
    def wday_nth_sequence(self, args):
        return "[{}]".format(','.join(args))

    def nth_entry(self, args):
        if len(args) == 1:
            return self.check_nth_value(args[0].value)
        else:
            return (
                self.check_nth_value(args[0].value) + '-' +
                self.check_nth_value(args[1].value)
            )

    def negative_nth_entry(self, args):
        return '-' + self.check_nth_value(args[0].value)

    def check_nth_value(self, value):
        if 0 < int(value) < 6:
            return value
        raise InconsistentField(
            "The nth-weekday {} is invalid (must be '1 <= n <= 5').".format(value)
        )

    # Holidays
    def holiday_sequence(self, args):
        return ','.join(args)

    def holiday(self, args):
        return args[0].value.upper()

    # weekday_selector
    def weekday_or_holiday_sequence_selector(self, args):
        return ','.join(args)

    def holiday_and_weekday_sequence_selector(self, args):
        return ','.join(args)

    def holiday_in_weekday_sequence_selector(self, args):
        holidays = [h.upper() for h in args if h.lower() in ('sh', 'ph')]
        days = [d for d in args if d not in holidays]
        return ','.join(holidays) + ' ' + args[-1]

    # Weekdays
    def weekday_sequence(self, args):
        return ','.join(args)

    def weekday_range(self, args):
        if len(args) == 3:
            return args[0] + '-' + args[2]
        return ''.join(args)

    def wday(self, args):
        DAYS = {
            'WDAY_MO': 'Mo',
            'WDAY_TU': 'Tu',
            'WDAY_WE': 'We',
            'WDAY_TH': 'Th',
            'WDAY_FR': 'Fr',
            'WDAY_SA': 'Sa',
            'WDAY_SU': 'Su',
        }
        return DAYS[args[0].type]

    # Year
    def year(self, args):
        return args[0]

    def year_range(self, args):
        if len(args) == 1:
            return args[0]
        elif len(args) == 2:
            return args[0] + '-' + args[1]
        else:
            return args[0] + '-' + args[1] + '/' + args[2]

    def year_selector(self, args):
        return ','.join(args)

    # Week
    def week_selector(self, args):
        return "week " + ','.join(args[1:])

    def week(self, args):
        if len(args) == 1:
            return args[0]
        elif len(args) == 2:
            return args[0] + '-' + args[1]
        else:
            step = int(args[2].value)
            if step > 53:  # Not in specifications, it's just logic.
                raise InconsistentField(
                    "The step {} between weeks is invalid.".format(step)
                )
            return "{}-{}/{}".format(args[0], args[1], step)

    def weeknum(self, args):
        num = int(args[0].value)
        if 1 <= num <= 53:
            return str(num)
        raise InconsistentField(
            "The week number {} is invalid (must be '1 <= n <= 53').".format(num)
        )

    # Time
    def time_selector(self, args):
        return ','.join(args)

    def timespan(self, args):
        if len(args) == 1:
            return args[0] # Ready-to-use full_timespan string
        if len(args) < 3:
            span = args[0]
        else:
            span = args[0] + '-' + args[2]
        if args[-1] == '+':
            span = span + "+"
        return span

    def time(self, args):
        return args[0]

    def hms(self, args):
        combined = int(args[0])
        h = combined // 100
        m = combined % 100
        if len(args) > 1 and args[1].type == 'PM':
            h = h + 12
        return str(h).zfill(2) + ':' + str(m).zfill(2)

    def hour_minutes(self, args):
        if len(args) == 1 and ':' in args[0]:
            return args[0] # Ready-to-use hour_am_pm_minutes string
        h = int(args.pop(0))
        m = 0
        for arg in args:
            if arg.type == 'MINUTE':
                m = int(arg)
            elif arg.type == 'PM':
                h = h + 12
        return str(h).zfill(2) + ':' + str(m).zfill(2)

    def variable_time(self, args):
        event = args[0].value.lower()
        if len(args) == 1:
            return event
        offset_sign = args[1].value
        time = args[2]
        return "({event}{sign}{time})".format(
            event=event, sign=offset_sign, time=time
        )

    def rule_modifier_open(self, args):
        if len(args) == 2:
            return "open " + args[1].value
        return "open"

    def rule_modifier_closed(self, args):
        if len(args) == 2:
            return "closed " + args[1].value
        return "closed"

    def rule_modifier_off(self, args):
        if len(args) == 2:
            return "off " + args[1].value
        return "off"

    def rule_modifier_comment(self, args):
        return args[0].value


def sanitize_field(field):
    """An autocorrector for the 'opening_hours' fields from OpenStreetMap.

    This function tries to fix the most current errors in the given field (str).

    It can raise the following exceptions:

    - TypeError : If the given field is not a string.
    - SanitizeError : The generic exception of 'oh_sanitizer',
        raised when the field can't be parsed (if it is too complex, or invalid).
    - InconsistentField : Inheriting from SanitizeError,
        raised when the field contains an invalid pattern which can't
        be corrected automatically.

    Example:
    >>> import oh_sanitizer
    >>> print(oh_sanitizer.sanitize_field("mo-fr 10h - 7:00 pm"))
    "Mo-Fr 10:00-19:00"
    """
    # The exceptions catching should be modified when the next version
    # 'lark-parser' will be released (it introduce a better exception handling).
    if not isinstance(field, str) and not isinstance(field, unicode):
        raise TypeError("The field must be a string.")
    if _re.match("[0-9]{4} [0-9].+", field):
        raise SanitizeError("This field can not be parsed properly.")
    if field.count('"') % 2 != 0:
        raise InconsistentField("This field contains inconsistent quotes.")
    try:
        field = field.replace('"""', '"').replace('""', '"')
        tree = PARSER.parse(field)
        new_field = SanitizerTransformer().transform(tree)
    except _lark.exceptions.LarkError as e:
        raise SanitizeError(
            "The field could not be parsed. It is probably invalid, "
            "or just too complex for the parser."
        )
    return new_field


# Unit tests


class TestSanitize(_unittest.TestCase):
    maxDiff = None

    def test_valid_fields(self):
        self.assertEqual(sanitize_field("24/7"), "24/7")
        self.assertEqual(sanitize_field("24/7; Jan 1 off"), "24/7; Jan 1 off")
        self.assertEqual(sanitize_field("Mo 10:00"), "Mo 10:00")
        self.assertEqual(sanitize_field("Mo 11:00+"), "Mo 11:00+")
        self.assertEqual(sanitize_field("Mo 10:00-20:00"), "Mo 10:00-20:00")
        self.assertEqual(sanitize_field("Mo 11:00-21:00+"), "Mo 11:00-21:00+")

        self.assertEqual(sanitize_field("Mo-Fr 10:00-20:00"), "Mo-Fr 10:00-20:00")
        self.assertEqual(sanitize_field("Mo,We 10:00-20:00"), "Mo,We 10:00-20:00")
        self.assertEqual(sanitize_field("SH,Mo-Fr 10:00-20:00"), "SH,Mo-Fr 10:00-20:00")
        self.assertEqual(sanitize_field("PH,Mo-Fr 10:00-20:00"), "PH,Mo-Fr 10:00-20:00")
        self.assertEqual(sanitize_field("Mo-Fr,SH 10:00-20:00"), "Mo-Fr,SH 10:00-20:00")
        self.assertEqual(sanitize_field("Mo-Fr,PH 10:00-20:00"), "Mo-Fr,PH 10:00-20:00")
        self.assertEqual(sanitize_field("Mo-Fr 10:00-12:00,13:00-20:00"), "Mo-Fr 10:00-12:00,13:00-20:00")
        self.assertEqual(sanitize_field("Mo 10:00-12:00,14:00-18:00; Tu 11:00-13:00,15:00-19:00"), "Mo 10:00-12:00,14:00-18:00; Tu 11:00-13:00,15:00-19:00")
        # Ideally we would want a space after the comma rule separator in
        # "off, Mar" and after no other comma. But the space is optional,
        # getting the parser to correctly identify this case is hard /
        # impossible, and it's a very rare case anyway.
        self.assertEqual(sanitize_field("08:00-17:45; Su 08:00-09:00 off, Mar 17:45-19:00"), "08:00-17:45; Su 08:00-09:00 off,Mar 17:45-19:00")

        self.assertEqual(sanitize_field("PH 10:00-20:00"), "PH 10:00-20:00")
        self.assertEqual(sanitize_field("SH 10:00-20:00"), "SH 10:00-20:00")
        self.assertEqual(sanitize_field("SH,PH 10:00-20:00"), "SH,PH 10:00-20:00")

        self.assertEqual(sanitize_field("10:00-12:00,13:00-20:00"), "10:00-12:00,13:00-20:00")
        self.assertEqual(sanitize_field("10:00-20:00"), "10:00-20:00")

        self.assertEqual(sanitize_field("sunrise-sunset"), "sunrise-sunset")
        self.assertEqual(sanitize_field("(sunrise-01:00)-(sunset+01:00)"), "(sunrise-01:00)-(sunset+01:00)")

        self.assertEqual(sanitize_field("Jan-Feb 10:00-20:00"), "Jan-Feb 10:00-20:00")
        self.assertEqual(sanitize_field("Jan 10:00-20:00"), "Jan 10:00-20:00")
        self.assertEqual(sanitize_field("Jan,Aug 10:00-20:00"), "Jan,Aug 10:00-20:00")
        self.assertEqual(sanitize_field("Mo-Su 08:00-18:00; Apr 10-15 off; Jun 08:00-14:00; Aug off; Dec 25 off"), "Mo-Su 08:00-18:00; Apr 10-15 off; Jun 08:00-14:00; Aug off; Dec 25 off")

        # Raises a SanitizeError, cause "<year> <time>" confuses with "<time>" without colon.
        # self.assertEqual(sanitize_field("2010 10:00-20:00"), "2010 10:00-20:00")
        self.assertEqual(sanitize_field("2010-2020 10:00-20:00"), "2010-2020 10:00-20:00")
        self.assertEqual(sanitize_field("2010-2020/2 10:00-20:00"), "2010-2020/2 10:00-20:00")
        self.assertEqual(sanitize_field("2010-2020/2 Mo-Fr 10:00-20:00"), "2010-2020/2 Mo-Fr 10:00-20:00")

        self.assertEqual(sanitize_field("week 1 10:00-20:00"), "week 1 10:00-20:00")
        self.assertEqual(sanitize_field("week 1-10 10:00-20:00"), "week 1-10 10:00-20:00")
        self.assertEqual(sanitize_field("week 1-20/2 10:00-20:00"), "week 1-20/2 10:00-20:00")
        self.assertEqual(sanitize_field("week 1-20/2 Mo-Fr 10:00-20:00"), "week 1-20/2 Mo-Fr 10:00-20:00")

        self.assertEqual(sanitize_field("2010-2020/2 week 1-12/2 Mo-Fr 10:00-12:00,13:00-20:00"), "2010-2020/2 week 1-12/2 Mo-Fr 10:00-12:00,13:00-20:00")

        self.assertEqual(sanitize_field("Mo-Fr off"), "Mo-Fr off")
        self.assertEqual(sanitize_field("10:00-20:00 off"), "10:00-20:00 off")
        self.assertEqual(sanitize_field("PH off"), "PH off")
        self.assertEqual(sanitize_field("off"), "off")
        self.assertEqual(sanitize_field("closed"), "closed")

        self.assertEqual(sanitize_field("Dec 25: 09:00-12:00"), "Dec 25: 09:00-12:00")
        self.assertEqual(sanitize_field("Dec 25: closed"), "Dec 25: closed")
        self.assertEqual(sanitize_field('Dec 25: closed "except if there is snow"'), 'Dec 25: closed "except if there is snow"')

        self.assertEqual(sanitize_field('"on appointement"'), '"on appointement"')
        self.assertEqual(sanitize_field('Mo-Fr "on appointement"'), 'Mo-Fr "on appointement"')
        self.assertEqual(sanitize_field('Mo-Fr 10:00-20:00 "on appointement"'), 'Mo-Fr 10:00-20:00 "on appointement"')

        self.assertEqual(sanitize_field("Mo[1] 10:00-20:00"), "Mo[1] 10:00-20:00")
        self.assertEqual(sanitize_field("Mo[-1] 10:00-20:00"), "Mo[-1] 10:00-20:00")
        self.assertEqual(sanitize_field("Mo[1,3] 10:00-20:00"), "Mo[1,3] 10:00-20:00")

    def test_invalid_fields(self):
        self.assertEqual(sanitize_field(" 24/7 "), "24/7")

        # Case correction
        self.assertEqual(sanitize_field("mo-fr 10:00-20:00"), "Mo-Fr 10:00-20:00")
        self.assertEqual(sanitize_field("jan-feb 10:00-20:00"), "Jan-Feb 10:00-20:00")
        self.assertEqual(sanitize_field("jan-feb,aug 10:00-20:00"), "Jan-Feb,Aug 10:00-20:00")
        self.assertEqual(sanitize_field("SUNRISE-SUNSET"), "sunrise-sunset")
        self.assertEqual(sanitize_field("(SUNrISE-01:00)-(SUnsET+01:00)"), "(sunrise-01:00)-(sunset+01:00)")
        self.assertEqual(sanitize_field("su,sh off"), "Su,SH off")
        self.assertEqual(sanitize_field("mo-fr CLOSED"), "Mo-Fr closed")

        # Weekday correction
        self.assertEqual(sanitize_field("Mon-fri 10:00-20:00"), "Mo-Fr 10:00-20:00")
        self.assertEqual(sanitize_field("Mo-Fr : 10:00-20:00"), "Mo-Fr 10:00-20:00")
        self.assertEqual(sanitize_field("Lundi - Vendredi: 10:00-20:00"), "Mo-Fr 10:00-20:00")

        # Time correction
        self.assertEqual(sanitize_field("8:00"), "08:00")
        self.assertEqual(sanitize_field("8 pm"), "20:00")
        self.assertEqual(sanitize_field("9:00-12:00"), "09:00-12:00")
        self.assertEqual(sanitize_field("9h-12h5"), "09:00-12:05")
        self.assertEqual(sanitize_field("8h45 am - 11.45 a.m."), "08:45-11:45")
        self.assertEqual(sanitize_field("9h p.m. 6 - 10 pm 15"), "21:06-22:15")
        self.assertEqual(sanitize_field("9 am - 12+"), "09:00-12:00+")

        # Timespan correction
        self.assertEqual(sanitize_field("09:00-12:00/13:00-19:00"), "09:00-12:00,13:00-19:00")
        self.assertEqual(sanitize_field("09 : 00 - 12 : 00 , 13 : 00 - 19 : 00"), "09:00-12:00,13:00-19:00")
        self.assertEqual(sanitize_field("09:00-12:00 /13:00-19:00"), "09:00-12:00,13:00-19:00")
        self.assertEqual(sanitize_field(u"Mo 09:00-12:00 14:00-18:00"), "Mo 09:00-12:00,14:00-18:00")
        self.assertEqual(sanitize_field(u"Mo 09:00-12:00 18:00"), "Mo 09:00-12:00,18:00")
        self.assertEqual(sanitize_field(u"Mo 09h:12h"), "Mo 09:00-12:00")
        self.assertEqual(sanitize_field(u"Mo 09:00:12:00"), "Mo 09:00-12:00")
        self.assertEqual(sanitize_field(u"Mo–Fr 09:00–12:00"), "Mo-Fr 09:00-12:00")

        # Global
        self.assertEqual(sanitize_field("2010-2020/2 WEEK 1-12/2 mo-fr 10h- 12h am, 1:00 pm - 20:00"), "2010-2020/2 week 1-12/2 Mo-Fr 10:00-12:00,13:00-20:00")
        self.assertEqual(sanitize_field("2020 mo-fr 1000 - 2000 / 22:20-23:00"), "2020 Mo-Fr 10:00-20:00,22:20-23:00")
        self.assertEqual(sanitize_field("Monday-friday 10h am - 12h / 13h-20h"), "Mo-Fr 10:00-12:00,13:00-20:00")
        self.assertEqual(sanitize_field(u"lundi-vendredi 10h am - 12h / 13h-20h; dimanche fermé"), "Mo-Fr 10:00-12:00,13:00-20:00; Su off")
        self.assertEqual(sanitize_field("lu - je 10h am - 12h / 13h-20h"), "Mo-Th 10:00-12:00,13:00-20:00")
        # FIXME Slashes are used as rule separators too but recognizing those
        # clashes with their use as timespan separators
        #self.assertEqual(sanitize_field("Mo-Fr 06:00-18:00 / Sa 06:00-12:30"), "Mo-Fr 06:00-18:00; Sa 06:00-12:30")
        self.assertEqual(sanitize_field("mo-fr 10h am - 2:00 PM ||Sa-Su 1000-2000"), "Mo-Fr 10:00-14:00 || Sa-Su 10:00-20:00")
        self.assertEqual(sanitize_field('mo-fr 10h-20h open "on appointement"'), 'Mo-Fr 10:00-20:00 open "on appointement"')
        self.assertEqual(sanitize_field("sunrise-( sunset+ 01h10)"), "sunrise-(sunset+01:10)")
        self.assertEqual(sanitize_field("dec 25: 09h-12h"), "Dec 25: 09:00-12:00")
        self.assertEqual(sanitize_field("Dec 25 : OFF"), "Dec 25: off")

        self.assertEqual(sanitize_field('""on appointement""'), '"on appointement"')
        self.assertEqual(sanitize_field('"""on appointement"""'), '"on appointement"')

    def test_exception_raising(self):
        with self.assertRaises(SanitizeError) as context:
            sanitize_field('Mo 9 12')

        with self.assertRaises(SanitizeError) as context:
            sanitize_field('Mo 09:00+-12:00')

        with self.assertRaises(SanitizeError) as context:
            sanitize_field('on appointement')

        with self.assertRaises(SanitizeError) as context:
            sanitize_field("week 1337 10:00-20:00 Mo-Fr")

        with self.assertRaises(InconsistentField) as context:
            sanitize_field("week 10-20/54 off")

        with self.assertRaises(InconsistentField) as context:
            sanitize_field("week 56 off")

        with self.assertRaises(InconsistentField) as context:
            sanitize_field('"on appointement')

        with self.assertRaises(InconsistentField) as context:
            sanitize_field('on appointement"')


if __name__ == '__main__':
    _unittest.main()
