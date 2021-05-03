#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2017                                      ##
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

# http://www.regular-expressions.info/unicode.html#script
# https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
language2scripts = {
  'ar': ['Arabic', '[\u064B-\u0655\u0670]'], # 'Arabic', 'Script_Extensions=Arabic,Syriac' Arabic,Syriac frequent at least in Iraq,
  'az': ['Arabic', 'Cyrillic', 'Latin'],
  'be': ['Cyrillic'],
  'ber': ['Tifinagh'],
  'bg': ['Cyrillic'],
  'bn': ['Bengali'],
  'bs': ['Latin'],
  'ca': ['Latin'],
  'cs': ['Latin'],
  'cy': ['Latin'],
  'da': ['Latin'],
  'de': ['Latin'],
  'dv': None, # Divehi
  'dz': None, # Dzongkha
  'el': ['Greek'],
  'en': ['Latin'],
  'es': ['Latin'],
  'et': ['Latin'],
  'eu': ['Latin'],
  'fa': ['Arabic', '[\u064B-\u0655\u0670]'], # 'Arabic', 'Script_Extensions=Arabic,Syriac'
  'fi': ['Latin'],
  'fo': ['Latin'],
  'fr': [u'[A-Za-zÉÀÈÙÂÊÎÔÛËÏÜŸÇŒÆéàèùâêîôûëïüÿçœæ]'],
  'fr_GF': [u'[A-Za-zÉÀÈÙÂÊÎÔÛËÏÜŸÇŒÆÃĨÕŨÖƗéàèùâêîôûëïüÿçœæãĩõũöɨ]'],
  'fr_LU': [u'[A-Za-zÉÀÈÙÂÊÎÔÛÄËÏÜŸÇŒÆéàèùâêîôûäëïüÿçœæ]'],
  'fr_PF': [u'[A-Za-zÉÀÈÙÂÊÎÔÛËÏÖÜŸÇŒÆĀĒĪŌŪÚéàèùâêîôûëïöüÿçœæāēīōū]'],
  'fy': ['Latin'],
  'ga': ['Latin'],
  'gl': ['Latin'],
  'he': ['Hebrew'],
  'hi': ['Devanagari'],
  'hr': ['Latin'],
  'hu': ['Latin'],
  'hy': ['Armenian'],
  'id': ['Latin'],
  'is': ['Latin'],
  'it': ['Latin'],
  'ja': None, # 'Hiragana', 'Katakana' and Kanji
  'ka': ['Georgian'],
  'kl': ['Latin'],
  'km': ['Khmer'],
  'ko': ['Hangul'],
  'kw': ['Latin'],
  'ky': ['Cyrillic'],
  'lo': ['Lao'],
  'lt': ['Latin'],
  'lv': ['Latin'],
  'mg': ['Latin'],
  'mn': ['Cyrillic'],
  'ms': ['Latin'],
  'my': None, # Birman
  'ne': ['Devanagari'],
  'nl': [u'[A-Za-zÁÉÍÓÚÀÈÌÒÙÄËÏÖÜÇÑáéíóúàèìòùäëïöüçñ]'],
  'no': ['Latin'],
  'pl': ['Latin'],
  'pt': ['Latin'],
  'rm': ['Latin'],
  'ro': ['Latin'],
  'ru': ['Cyrillic'],
  'si': ['Sinhala'],
  'sk': ['Latin'],
  'sl': ['Latin'],
  'so': ['Latin'],
  'sq': [u'[A-Za-zÇËçë]'],
  'sr': ['Cyrillic'],
  'sr-Latn': [u'[A-Za-zČĆĐŠŽčćđšž]'],
  'sv': ['Latin'],
  'ta': ['Tamil'],
  'tg': ['Arabic', 'Cyrillic'],
  'th': ['Thai'],
  'tk': ['Cyrillic', 'Latin'],
  'tr': ['Latin'],
  'uk': ['Cyrillic', '[\u0301]'],
  'ur': ['Arabic', '[\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]'],
  'vi': ['Latin'],
  'zgh': ['Tifinagh'],
  'zh': None, # Bopomofo and other
  'zh_TW': None, # Bopomofo and other
}

def script_is_alphabet(script):
    return script in ['Arabic', 'Armenian', 'Bengali', 'Birman', 'Cyrillic', 'Divehi', 'Devanagari', 'Georgian', 'Greek', 'Hebrew', 'Khmer', 'Latin', 'Lao', 'Manchu', 'Sinhala', 'Tamil', 'Thai', 'Tifinagh']

def scripts(languages):
    if not languages:
        return
    if not isinstance(languages, list):
        languages = [languages]
    all_scripts = []
    for language in languages:
        if language in language2scripts:
            scripts = language2scripts[language]
        elif '_' in language:
            l = language.split('_')[0]
            scripts = language2scripts[l]
        if not scripts:
            return
        all_scripts += scripts
    return list(set(all_scripts))

def languages_are_alphabets(languages):
    scripts_ = scripts(languages)
    if not scripts_:
        return False
    for script in scripts_:
        if script[0] != '[' and not script_is_alphabet(script):
            return False
    return True

def gen_regex(scripts):
    if scripts:
        ret = r""
        for s in scripts:
            if s[0] == r"[":
                ret += s
            else:
                ret += r"\p{" + s + "}"
        return ret

###########################################################################
import unittest

class Test(unittest.TestCase):

    def test(self):
        assert languages_are_alphabets('fr')
        assert languages_are_alphabets(['fr', 'it'])

        assert not languages_are_alphabets('my')
        assert not languages_are_alphabets(['it', 'my'])
