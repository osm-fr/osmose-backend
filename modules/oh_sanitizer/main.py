# coding: utf-8

import os as _os
import re as _re

import unittest as _unittest

import lark as _lark
from lark.lexer import Token as _Token


# TODO: Fix 'Mo,SH'


def get_parser():
    """
        Returns a Lark parser able to parse a valid field.
    """
    base_dir = _os.path.dirname(_os.path.realpath(__file__))
    with open(_os.path.join(base_dir, "field.ebnf"), 'rb') as f:
        grammar = f.read().decode("UTF-8")
    return _lark.Lark(grammar, start="time_domain", parser="earley")


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
    def time_domain(self, args):
        parts = []
        for arg in args:
            if isinstance(arg, _Token):
                parts.append(
                    {';': '; ', ',': ', ', '||': ' || '}.get(arg.value.strip())
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
        if len(args) == 1:  # "time_selector"
            return args[0]
        else:  # "range_selectors time_selector"
            return (args[0] + ' ' + args[1])
    
    def range_selectors(self, args):
        return ' '.join(args).replace(' :', ':')
    
    # Dates
    def monthday_selector(self, args):
        return ','.join(args)
    
    def monthday_range(self, args):
        return '-'.join(args)
    
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
        holidays = args[1:]
        return ','.join(holidays) + ' ' + args[-1]
    
    # Weekdays
    def weekday_sequence(self, args):
        return ','.join(args)
    
    def weekday_range(self, args):
        return '-'.join(args)
    
    def wday(self, args):
        day = args[0]
        DAYS = {
            "Mo": ["mo", "monday", "lundi", "lunes"],
            "Tu": ["tu", "tuesday", "mardi", "martes"],
            "We": ["we", "wednesday", "mercredi", "miercoles", u"miércoles"],
            "Th": ["th", "thursday", "jeudi", "jueves"],
            "Fr": ["fr", "friday", "vendredi", "viernes"],
            "Sa": ["sa", "saturday", "samedi", "sabado", u"sábado"],
            "Su": ["su", "sunday", "dimanche", "domingo"]
        }
        for normalized_day, localized_days in DAYS.items():
            if day.lower() in localized_days:
                return normalized_day
        # Should not come here.
    
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
        return args[0] + '-' + args[1]
    
    def time(self, args):
        return args[0]
    
    def hour_minutes(self, args):
        if len(args) == 3:  # "10" "h" "30"
            h, _, m = args
        elif len(args) == 2:
            if args[1].type == "HOUR_MINUTES_H":  # "10" "h"
                h = args[0]
                m = '00'
            else:
                h, m = args[0].value, args[1].value
        else:
            h, m = args[0].value[:2], args[0].value[2:]
        return h.zfill(2) + ':' + m.zfill(2)
    
    def hour_minutes_am_pm(self, args):
        if len(args) == 3:  # "10:00 am" / "10h am"
            h = args[0].value
            am_pm = args[2].value.upper()
            if args[1].type == "HOUR_MINUTES_H":
                m = '00'
            else:
                m = args[1].value
        else:  # "10h00 am"
            h, m, am_pm = args[0].value, args[2].value, args[3].value.upper()
        if am_pm == "AM":
            return h.zfill(2) + ':' + m.zfill(2)
        else:
            return str(int(h)+12).zfill(2) + ':' + m.zfill(2)
    
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
        self.assertEqual(sanitize_field("Mo-Fr 10:00-20:00"), "Mo-Fr 10:00-20:00")
        self.assertEqual(sanitize_field("Mo 10:00-20:00"), "Mo 10:00-20:00")
        self.assertEqual(sanitize_field("Mo,We 10:00-20:00"), "Mo,We 10:00-20:00")
        self.assertEqual(sanitize_field("SH,Mo-Fr 10:00-20:00"), "SH,Mo-Fr 10:00-20:00")
        self.assertEqual(sanitize_field("PH,Mo-Fr 10:00-20:00"), "PH,Mo-Fr 10:00-20:00")
        self.assertEqual(sanitize_field("Mo-Fr,SH 10:00-20:00"), "Mo-Fr,SH 10:00-20:00")
        self.assertEqual(sanitize_field("Mo-Fr,PH 10:00-20:00"), "Mo-Fr,PH 10:00-20:00")
        self.assertEqual(sanitize_field("Mo-Fr 10:00-12:00,13:00-20:00"), "Mo-Fr 10:00-12:00,13:00-20:00")
        
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
    
    def test_invalid_fields(self):
        # Case correction
        self.assertEqual(sanitize_field("mo-fr 10:00-20:00"), "Mo-Fr 10:00-20:00")
        self.assertEqual(sanitize_field("jan-feb 10:00-20:00"), "Jan-Feb 10:00-20:00")
        self.assertEqual(sanitize_field("jan-feb,aug 10:00-20:00"), "Jan-Feb,Aug 10:00-20:00")
        self.assertEqual(sanitize_field("SUNRISE-SUNSET"), "sunrise-sunset")
        self.assertEqual(sanitize_field("(SUNrISE-01:00)-(SUnsET+01:00)"), "(sunrise-01:00)-(sunset+01:00)")
        self.assertEqual(sanitize_field("su,sh off"), "Su,SH off")
        self.assertEqual(sanitize_field("mo-fr CLOSED"), "Mo-Fr closed")
        
        # Time correction
        self.assertEqual(sanitize_field("9:00-12:00"), "09:00-12:00")
        self.assertEqual(sanitize_field("9h-12h"), "09:00-12:00")
        self.assertEqual(sanitize_field("9:00 am - 12:00 am"), "09:00-12:00")
        # TODO
        #self.assertEqual(sanitize_field("9 am - 12 am"), "09:00-12:00")
        
        # Timespan correction
        self.assertEqual(sanitize_field("09:00-12:00/13:00-19:00"), "09:00-12:00,13:00-19:00")
        self.assertEqual(sanitize_field("09 : 00 - 12 : 00 , 13 : 00 - 19 : 00"), "09:00-12:00,13:00-19:00")
        self.assertEqual(sanitize_field("09:00-12:00 /13:00-19:00"), "09:00-12:00,13:00-19:00")
        
        # Global
        self.assertEqual(sanitize_field("2010-2020/2 WEEK 1-12/2 mo-fr 10h- 12h am, 1:00 pm - 20:00"), "2010-2020/2 week 1-12/2 Mo-Fr 10:00-12:00,13:00-20:00")
        self.assertEqual(sanitize_field("2020 mo-fr 1000 - 2000 / 22:20-23:00"), "2020 Mo-Fr 10:00-20:00,22:20-23:00")
        self.assertEqual(sanitize_field("lundi-vendredi 10h am - 12h / 13h-20h"), "Mo-Fr 10:00-12:00,13:00-20:00")
        self.assertEqual(sanitize_field("mo-fr 10h am - 2:00 PM ||Sa-Su 1000-2000"), "Mo-Fr 10:00-14:00 || Sa-Su 10:00-20:00")
        self.assertEqual(sanitize_field('mo-fr 10h-20h open "on appointement"'), 'Mo-Fr 10:00-20:00 open "on appointement"')
        self.assertEqual(sanitize_field("sunrise-( sunset+ 01h10)"), "sunrise-(sunset+01:10)")
        self.assertEqual(sanitize_field("dec 25: 09h-12h"), "Dec 25: 09:00-12:00")
        self.assertEqual(sanitize_field("Dec 25 : OFF"), "Dec 25: off")
        
        self.assertEqual(sanitize_field('""on appointement""'), '"on appointement"')
        self.assertEqual(sanitize_field('"""on appointement"""'), '"on appointement"')
    
    def test_exception_raising(self):
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
