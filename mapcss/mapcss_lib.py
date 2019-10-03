#-*- coding: utf-8 -*-
import requests.utils
import re

try:
    unicode # Python 2
except:
    unicode = str
    long = int


# Utils

def memoize(f):
    class memodict(dict):
        __slots__ = ()
        def __missing__(self, key):
            self[key] = ret = f(key)
            return ret
    return memodict().__getitem__

def memoizeN(f):
    memo = {}
    def wrapper(*args):
        try:
            return memo[args]
        except KeyError:
            rv = f(*args)
            memo[args] = rv
            return rv
    return wrapper

@memoize
def str_value(string):
    return str_value_(string)

class str_value_(unicode):
    def __new__(cls, string):
        if string.__class__ == str_value_:
            return string
        else: # Keep None string value
            s = super(str_value_, cls).__new__(cls, string)
            s.none = string == None
            return s

    def __radd__(self, o):
        if self.none:
            return None_value
        if o.__class__ in (int, long):
            return str_value(o + self.to_n())
        else:
            return str_value(o) + self

    def __add__(self, o):
        if self.none:
            return None_value
        elif o.__class__ in (int, long):
            return str_value(self.to_n() + o)
        else:
            return str_value(super(str_value_, self).__add__(o))

    def __rsub__(self, o):
        if self.none:
            return None_value
        elif o.__class__ in (int, long):
            return str_value(o - self.to_n())
        else:
            raise NotImplementedError

    def __sub__(self, o):
        if self.none:
            return None_value
        elif o.__class__ in (int, long):
            return str_value(self.to_n() - o)
        else:
            raise NotImplementedError

    def __rmul__(self, o):
        if self.none:
            return None_value
        elif o.__class__ in (int, long):
            return str_value(o * self.to_n())
        else:
            raise NotImplementedError

    def __mul__(self, o):
        if self.none:
            return None_value
        elif o.__class__ in (int, long):
            return str_value(self.to_n() * o)
        else:
            raise NotImplementedError

    def __rdiv__(self, o):
        if self.none:
            return None_value
        elif o.__class__ in (int, long):
            return str_value(float(o) / self.to_n())
        else:
            raise NotImplementedError

    def __truediv__(self, o):
        if self.none:
            return None_value
        elif o.__class__ in (int, long):
            return str_value(float(self.to_n()) / o)
        else:
            raise NotImplementedError

    __div__ = __truediv__  # Python 2 compatibility

    def __lt__(self, o):
        if self.none:
            return False
        elif o.__class__ in (int, long):
            return self.to_n() < o
        else:
            return super(str_value_, self).__lt__(o)

    def __le__(self, o):
        if self.none:
            return False
        elif o.__class__ in (int, long):
            return self.to_n() <= o
        else:
            return super(str_value_, self).__le__(o)

    def __eq__(self, o):
        if self.none:
            return False
        elif o.__class__ in (int, long):
            return self.to_n() == o
        else:
            return super(str_value_, self).__eq__(o)

    def __ne__(self, o):
        if self.none:
            return True
        elif o.__class__ in (int, long):
            return self.to_n() != o
        else:
            return super(str_value_, self).__ne__(o)

    def __gt__(self, o):
        if self.none:
            return False
        elif o.__class__ in (int, long):
            return self.to_n() > o
        else:
            return super(str_value_, self).__gt__(o)

    def __ge__(self, o):
        if self.none:
            return False
        elif o.__class__ in (int, long):
            return self.to_n() >= o
        else:
            return super(str_value_, self).__ge__(o)

    def __bool__(self):
        if self.none:
            return False
        else:
            return len(self) > 0

    __nonzero__ = __bool__  # Python 2 compatibility

    def to_n(self):
        try:
            if '.' in self:
                return float(self)
            else:
                return int(self)
        except:
            raise RuleAbort()

    # Required in Pyhton 3 the make the class hashable
    def __hash__(self):
        return unicode.__hash__(self)

None_value = str_value(None)

def flatten(z):
    return [x for y in z for x in y]

uncapture_param_re = re.compile('\{([0-9]+\.[a-z]+)\}')
def _uncapture_param(capture, a):
    i, ty = a.split('.', 1)
    k, v = capture.get(int(i), [None, None])
    k, v = k or '{' + i + '.key}', v or '{' + i + '.value}'
    if ty == 'key':
        return k
    elif ty == 'value':
        return v
    else: # tag
        return k + '=' + v

def _tag_uncapture(capture, string):
    if string != None:
        return uncapture_param_re.sub(lambda a: _uncapture_param(capture, a.group(1)), string)

class RuleAbort(Exception):
    pass


# MapCSS Private function, operator replacement


def startswith(subject, string):
    if subject != None and string != None:
        return subject.startswith(string)

def endswith(subject, string):
    if subject != None and string != None:
        return subject.endswith(string)

def string_contains(subject, string):
    if subject != None and string != None:
        return string in subject

def list_contains(subject, string):
    if subject != None and string != None:
        return string in subject

def at(asset_lat, asset_lon, lat, lon):
    return asset_lat == lat and asset_lon == lon


# MapCSS Public function


#+, -, *, /
#    arithmetic operations 

#||, &&, !
#    boolean operations 

#<, >, <=, >=, ==
#    comparison operators 

#asin, atan, atan2, ceil, cos, cosh, exp, floor, log, max, min, random, round, signum, sin, sinh, sqrt, tan, tanh
#    the usual meaning, details 
import math
import random
asin = math.asin
atan = math.atan
atan2 = math.atan2
ceil = math.ceil
cos = math.cos
cosh = math.cosh
exp = math.exp
floor = math.floor
log = math.log
#max = max
#min = min
random = random.random
round = lambda f: f.round
signum = lambda x: (x > 0) - (x < 0)
sin = math.sin
sinh = math.sinh
sqrt = math.sqrt
tan = math.tan
tanh = math.tanh

#cond(b, fst, snd)
#b ? fst : snd
#    if (b) then fst else snd 
def cond(b, fst, snd):
    if b:
        return fst
    else:
        return snd

#list(a, b, ...)
#    create list of values, e.g. for the dashes property 
def list_(*args):
   return list(args)

#get(lst, n)
#    get the nth element of the list lst (counting starts at 0) [since 5699] 
def get(lst, n):
    try:
        return lst[n]
    except:
        return None

#split(sep, str)
#    splits string str at occurrences of the separator string sep, returns a list [since 5699] 
def split(sep, string):
    if sep != None and string != None:
        return list(map(str_value, string.split(sep)))

#prop(p_name)
#    value of the property p_name of the current layer, e.g. prop("width") 
#prop(p_name, layer_name)
#    property from the layer layer_name 
#is_prop_set(p_name)
#    true, if property p_name is set for the current layer 
#is_prop_set(p_name, layer_name)
#    true, if property p_name is set for the layer layer_name 

#tag(key_name)
#    get the value of the key key_name from the object in question 

@memoizeN
def _re_search(r, s):
    return r.search(s)

def tag(tags, key_name):
    if tags != None and key_name != None:
        if key_name.__class__ in (str, unicode, str_value_):
            return str_value(tags.get(key_name))
        else: # regex
            for k in tags.keys():
                if _re_search(key_name, k):
                    return str_value(tags[k])
    return None_value

def _tag_capture(stock, index, tags, key_name):
    if tags != None and key_name != None:
        if index >= len(stock):
            stock[index] = [None, None]

        if key_name.__class__ in (str, unicode, str_value_):
            stock[index][0] = key_name
            if not stock[index][1]:
                stock[index][1] = tags.get(key_name)
            return str_value(tags.get(key_name))
        else: # regex
            for k in tags.keys():
                if _re_search(key_name, k):
                    stock[index][0] = k
                    if not stock[index][1]:
                        stock[index][1] = tags[k]
                    return str_value(tags[k])
            # No match found, store the regex
            stock[index][0] = key_name.pattern
    return None_value

def _value_capture(stock, index, value):
    if index >= len(stock):
        stock[index] = [None, None]
    if value.__class__ in (str, unicode, str_value_):
        # If not a string, let the tag capture fill the value part
        stock[index][1] = value
    elif value.__class__ in (int, float):
        # If not a number, let the tag capture fill the value part
        stock[index][1] = str(value)
    return value

def _value_const_capture(stock, index, value, const):
    _value_capture(stock, index, const)
    return value

#parent_tag(key_name)
#    get the value of the key key_name from the object's parent 
#parent_tags(key_name)
#    returns all parent's values for the key key_name as a list ordered by a natural ordering [since 8775] 

#has_tag_key(key_name)
#    true, if the object has a tag with the given key 

#rgb(r, g, b)
#    create color value (arguments from 0.0 to 1.0) 
#hsb_color(h, s, b)
#    create color from hue, saturation and brightness (arguments from 0.0 to 1.0) [since 6899] 
#red(clr), green(clr), blue(clr)
#    get value of color channels in rgb color model 
#alpha(clr)
#    get the alpha value of the given color [since 6749] 

#length(str)
#    length of a string 
def length(string):
    if string != None:
        return len(string)

#count(lst)
#    length of a list, i.e., counts its elements [since 7162] 
def count(lst):
    if lst != None:
        return len(lst)

#length(lst)
#    length of a list [since 5699] – deprecated since 7162 

#any(obj1, obj2, ...)
#    returns the first object which is not null (formerly coalesce, [since 7164]) 
def any_(*args):
    if args != None:
        return next(item for item in args if item is not None)

#concat(str1, str2, ...)
#    assemble the strings to one 
def concat(*args):
    if args != None:
        return str_value(''.join(args))

#join(sep, str1, str2, ...)
#    join strings, whith sep as separator [since 6737] 
def join(sep, *args):
    if sep != None and args != None:
        return str_value(sep.join(args))

#join_list(sep, list_name)
#    joins the elements of the list list_name to one string separated by the separator sep [since 8775] 
def join_list(sep, list_name):
    if sep != None and list_name != None:
        return str_value(sep.join(list_name))

#upper(str)
#    converts string to upper case [since 11756] 
def upper(string):
    if string != None:
        return str_value(string.upper())

#lower(str)
#    converts string to lower case [since 11756] 
def lower(string):
    if string != None:
        return str_value(string.lower())

#trim(str)
#    remove leading and trailing whitespace from string [since 11756] 
def trim(string):
    if string != None:
        return str_value(string.strip())

#JOSM_search("...")
#    true, if JOSM search applies to the object 
def JOSM_search(string):
    raise NotImplementedError

#tr(str, arg0, arg1, ...)
#    translate from English to the current language (only for strings in the JOSM user interface) [since 6506] 
def tr(string, *args):
    if string != None:
        return T_f(string, *args)

#regexp_test(regexp, string)
#    test if string matches pattern regexp [since 5699] 
def regexp_test(regexp, string):
    if regexp == None or string == None:
        return False
    else:
        return regexp.search(string)

#regexp_test(regexp, string, flags)
#    test if string matches pattern regexp; flags is a string that may contain "i" (case insensitive), "m" (multiline) and "s" ("dot all") [since 5699] 
#regexp_match(regexp, string)
#    Tries to match string against pattern regexp. Returns a list of capture groups in case of success. The first element (index 0) is the complete match (i.e. string). Further elements correspond to the bracketed parts of the regular expression. [since 5701] 
def regexp_match(regexp, string):
    if regexp == None or string == None:
        return False
    else:
        a = regexp.findall(string)
        if a:
            a = [string] + flatten(a)
        return list(map(str_value, a))

#regexp_match(regexp, string, flags)
#    Tries to match string against pattern regexp. Returns a list of capture groups in case of success. The first element (index 0) is the complete match (i.e. string). Further elements correspond to the bracketed parts of the regular expression. Flags is a string that may contain "i" (case insensitive), "m" (multiline) and "s" ("dot all") [since 5701] 

#substring(str, idx)
#    return the substring of str, starting at index idx (0-indexed) [since 6534]
#substring(str, start, end)
#    return the substring of str, starting at index start (inclusive) up to end (exclusive) (0-indexed) [since 6534]
def substring(string, start, end=None):
    if string is not None and start is not None:
        return str_value(string[start:end])

#replace(string, old, new)
#    Replaces any occurrence of the substring old within the string string with the text new 
def replace(string, old, new):
    if string != None and old != None and new != None:
        return str_value(string.replace(old, new))

#osm_id()
#    returns the OSM id of the current object [since 5699] 

#parent_osm_id()
#    returns the OSM id of the object's parent (matched by child selector) [since 13094] 

#URL_encode(str)
#    percent-encode a string. May be useful for data URLs [since 6805] 
#URL_decode(str)
#    percent-decode a string. [since 11756] 
def URL_decode(string):
    if string != None:
        # An URL is an ASCII String
        try:
            return requests.utils.unquote_unreserved(string)
        except UnicodeDecodeError:
            pass

#XML_encode(str)
#    escape special characters in xml. E.g. < becomes &lt;, other special characters: >, ", ', &, \n, \t and \r [since 6809] 
#CRC32_checksum(str)
#    calculate the CRC32 checksum of a string (result is an integer from 0 to 232-1) [since 6908] 

#is_right_hand_traffic()
#    Check if there is left-hand or right-hand traffic at the current location. [since 7193] 

#number_of_tags()
#    returns the number of tags for the current OSM object [since 7237] 

#print(o)
#    prints a string representation of o to the command line (for debugging) [since 7237] 
##def print(o):
##    print(o, end='')

#println(o)
#    prints a string representation of o to the command line, followed by a new line (for debugging) [since 7237] 
def println(o):
    print(o)

#JOSM_pref(key, default)
#    Get value from the JOSM advanced preferences. This way you can offer certain options to the user and make the style customizable. It works with strings, numbers, colors and boolean values.
#    [This function exists since version 3856, but with some restrictions. JOSM_pref always returns a string, but in version 7237 and earlier, the automatic conversion of string to boolean and color was not working. You can use the following workarounds for boolean values and color in version 7237 and earlier: cond(JOSM_pref("myprefkey", "true")="true", "X", "O") and html2color(JOSM_pref("mycolor", "#FF345611")). These explicit conversions should be no longer necessary in version 7238 and later. Automatic conversion to a number works in any version.] 
def JOSM_pref(key, default):
    raise NotImplementedError

#setting()
#    to use a style setting [since 7450] 
def setting(options, key):
    return options.get(key)

#degree_to_radians()
#    returns a in degree given direction in radians [since 8260] 
#cardinal_to_radians()
#    returns a cardinal direction in radians [since 8260] 

#waylength()
#    returns the length of the way in metres [since 8253] 
def waylength():
    raise NotImplementedError

#areasize()
#    returns the area of a closed way in square meters [since 8253] 
def areasize():
    raise NotImplementedError

#at(lat,lon)
#    returns true if the object centroid lies at given lat/lon coordinates, e.g. to check for nodes at "null island" node[at(0.0,0.0)] [since 12514] 


# Other functions

def inside(options, areas):
    country = options.get("country")
    return country and any(map(lambda c: country.startswith(c), areas.split(','))) or False

def outside(options, areas):
    country = options.get("country")
    return country and all(map(lambda c: not country.startswith(c), areas.split(','))) or False


# Osmose extention MapCSS function

# only_for lang
def language(options, locales):
    language = options.get("language")
    return language and not isinstance(language, list) and any(map(lambda c: language.startswith(c), locales.split(','))) or False

# not_for lang
def no_language(options, locales):
    language = options.get("language")
    return language and not isinstance(language, list) and all(map(lambda c: not language.startswith(c), locales.split(','))) or False
