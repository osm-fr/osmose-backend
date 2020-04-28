#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo <@free.fr> 2009                           ##
##            Etienne Chové <chove@crans.org> 2009                       ##
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

from .Analyser_Osmosis import Analyser_Osmosis
from modules import languages

sql01_fr = u"""
-- http://www-lium.univ-lemans.fr/~carlier/recherche/soundex.html
--

DROP FUNCTION IF EXISTS FN_SOUNDEX2(name VARCHAR (1024));

CREATE FUNCTION FN_SOUNDEX2 (name_in VARCHAR (1024))
RETURNS VARCHAR AS $$
DECLARE
    name VARCHAR(1024) := name_in;
    prefixe VARCHAR(1024);
    suffixe VARCHAR(1024);
    i INT;
    last_ VARCHAR(1024);
BEGIN
    IF name IS NULL THEN
        RETURN NULL;
    END IF;

-- Eliminer les blancs  droite et  gauche du nom

-- Convertir le nom en majuscule
    name := UPPER(name);

-- Convertir les lettres accentues et le c cedille en lettres non accentues
    name := TRANSLATE(name, 'ÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ', 'AAAEEEEIIOOUUUC');

-- Eliminer les blancs et les tirets
    name := REPLACE(name, ' ', '');
    name := REPLACE(name, '-', '');

    name := REPLACE(name, '''', '');
    name := REPLACE(name, '/', '');

-- Remplacer les groupes de lettres suivantes par leur correspondance
    name := REPLACE(name, 'GUI','KI');
    name := REPLACE(name, 'GUE','KE');
    name := REPLACE(name, 'GA',    'KA');
    name := REPLACE(name, 'GO',    'KO');
    name := REPLACE(name, 'GU',    'K');
    name := REPLACE(name, 'CA',    'KA');
    name := REPLACE(name, 'CO',    'KO');
    name := REPLACE(name, 'CU',    'KU');
    name := REPLACE(name, 'Q',    'K');
    name := REPLACE(name, 'CC',    'K');
    name := REPLACE(name, 'CK',    'K');

-- Remplacer toutes les voyelles sauf le Y par A excepte s'il y a un A en tete
    name := SUBSTRING(name, 1, 1) || REPLACE(SUBSTRING(name, 2, LENGTH(name)), 'E',    'A');
    name := SUBSTRING(name, 1, 1) || REPLACE(SUBSTRING(name, 2, LENGTH(name)), 'I',    'A');
    name := SUBSTRING(name, 1, 1) || REPLACE(SUBSTRING(name, 2, LENGTH(name)), 'O',    'A');
    name := SUBSTRING(name, 1, 1) || REPLACE(SUBSTRING(name, 2, LENGTH(name)), 'U',    'A');

-- Remplacer les prefixes suivants par leur correspondance
    prefixe := SUBSTRING(name, 1, 3);
    suffixe := SUBSTRING(name, 4, LENGTH(name));
    IF prefixe = 'MAC' THEN
        name := 'MCC' || suffixe;
    ELSEIF prefixe = 'ASA' THEN
        name := 'AZA' || suffixe;
    ELSEIF prefixe = 'SCH' THEN
        name := 'SSS' || suffixe;
    ELSE
        prefixe := SUBSTRING(name, 1, 2);
        suffixe := SUBSTRING(name, 3, LENGTH(name));
        IF prefixe = 'KN' THEN
            name := 'NN' || suffixe;
        ELSEIF prefixe = 'PH' THEN
            name := 'FF' || suffixe;
        END IF;
    END IF;

-- Supprimer les H sauf s'ils sont precedes par C ou S
    i := 1;
    WHILE i <= LENGTH(name)-1 LOOP
        IF SUBSTRING(name, i, 1) != 'C' AND SUBSTRING(name, i, 1) != 'S' AND SUBSTRING(name, i+1, 1) = 'H' THEN
            name := SUBSTRING(name, 1, i) || SUBSTRING(name, i+2, LENGTH(name));
        END IF;
        i := i + 1;
    END LOOP;

-- Supprimer les Y sauf s'il est precede d'un A
    i := 1;
    WHILE i <= LENGTH(name)-1 LOOP
        IF SUBSTRING(name, i, 1) != 'A' AND SUBSTRING(name, i+1, 1) = 'Y' THEN
            name := SUBSTRING(name, 1, i) || SUBSTRING(name, i+2, LENGTH(name));
        END IF;
        i := i + 1;
    END LOOP;

-- Supprimer les terminaisons suivantes A, T, D et S
    last_ := SUBSTRING(name, LENGTH(name), 1);
    IF last_ = 'A' OR last_ = 'T' OR last_ = 'D' OR last_ = 'S' THEN
        name := SUBSTRING(name, 1, LENGTH(name)-1);
    END IF;

-- Enlever tous les A sauf le A de tete s'il y en a un
    name := SUBSTRING(name, 1, 1) || REPLACE(SUBSTRING(name, 2, LENGTH(name)), 'A', '');

-- Enlever toutes les sous chaines de lettre repetitives
    i := 1;
    last_ := SUBSTRING(name, i, 1);
    WHILE i <= LENGTH(name) LOOP
        IF SUBSTRING(name, i+1, 1) = last_ THEN
            name := SUBSTRING(name, 1, i) || SUBSTRING(name, i+2, LENGTH(name));
        ELSE
            i := i + 1;
            last_ := SUBSTRING(name, i, 1);
        END IF;
    END LOOP;

-- Conserver les 4 premiers caractres du mot et si besoin le complter avec des blancs pour obtenir 4 caractres
--    name := RPAD(name, 4, ' ');

    RETURN name;
END
$$ LANGUAGE plpgsql;
"""

sql03 = """
CREATE TEMP TABLE way_tags_name_phonic AS
SELECT
    id AS way_id,
    {0}(ways.tags -> 'name') AS phonic_all,
    substring(ways.tags -> 'name' for position(' ' in ways.tags -> 'name')-1) AS name_1,
    {0}(substring(ways.tags -> 'name' for position(' ' in ways.tags -> 'name')-1)) AS phonic_1,
    substring(ways.tags -> 'name' from position(' ' in ways.tags -> 'name')+1) AS name_2oo,
    {0}(substring(ways.tags -> 'name' from position(' ' in ways.tags -> 'name')+1)) AS phonic_2oo
FROM
    ways
WHERE
    tags != ''::hstore AND
    tags?'name' AND
    tags->'name' NOT LIKE '%;%' AND
    tags->'name' LIKE '% %' AND
    LENGTH(substring(tags->'name' for position(' ' in tags -> 'name')-1) ) >= 3 AND
    LENGTH(substring(tags->'name' from position(' ' in tags -> 'name')+1) ) >= 7 AND
    regexp_replace(substring(tags->'name' from position(' ' in tags->'name')+1), '^[- 0-9_/]+$', '' ) != ''
"""

sql03i = """
CREATE INDEX way_tags_name_phonic_phonic_2oo ON way_tags_name_phonic(phonic_2oo)
"""

sql04 = """
CREATE OR REPLACE VIEW phonic AS
SELECT
    phonic_2oo,
    COUNT(phonic_2oo) AS count
FROM
    way_tags_name_phonic
GROUP BY
    phonic_2oo
"""

sql05 = """
CREATE TEMP TABLE phonic_usage AS
SELECT
    phonic.phonic_2oo,
    name_2oo,
    count(*) * 100 / phonic.count AS percent
FROM
    way_tags_name_phonic
    JOIN phonic ON
        way_tags_name_phonic.phonic_2oo = phonic.phonic_2oo AND
        phonic.count > 20
GROUP BY
    phonic.phonic_2oo,
    phonic.count,
    name_2oo
"""

sql05i = """
CREATE INDEX phonic_usage_phonic_2oo_80 ON phonic_usage(phonic_2oo) WHERE percent >= 80
"""

sql06 = """
SELECT
    way_tags_name_phonic.way_id,
    ST_AsText(way_locate(ways.linestring)),
    ways.tags->'name',
    way_tags_name_phonic.name_1 || ' ' || phonic_faible.name_2oo AS faible,
    way_tags_name_phonic.name_1 || ' ' || phonic_fort.name_2oo AS fort
FROM
    way_tags_name_phonic
    JOIN ways ON
        way_tags_name_phonic.way_id = ways.id
    JOIN phonic_usage AS phonic_faible ON
        phonic_faible.percent < 20 AND
        way_tags_name_phonic.name_2oo = phonic_faible.name_2oo
    JOIN phonic_usage AS phonic_fort ON
        phonic_fort.percent >= 80 AND
        phonic_fort.phonic_2oo = phonic_faible.phonic_2oo
WHERE
    levenshtein(upper(unaccent(phonic_fort.name_2oo)), upper(unaccent(phonic_faible.name_2oo))) <= 1 AND
    replace(upper(phonic_fort.name_2oo), '-', ' ') <> replace(upper(phonic_faible.name_2oo), '-', ' ')
"""


class Analyser_Osmosis_Soundex(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)

        # Check langues for country are writen with alphabets
        self.scripts = 'language' in config.options and languages.scripts(config.options['language'])
        if self.scripts and len(self.scripts) == 1 and (self.scripts[0] == 'Latin' or self.scripts[0].startswith('[A-Za-z')):
            self.classs[1] = self.def_class(item = 5050, level = 2, tags = ['name', 'fix:survey'],
                title = T_('Soundex test'),
                detail = T_(
'''A street name "sounds" like a other street name already known but is
not spelled on the same way.'''),
                fix = T_(
'''After you have checked that it is a mistake, change the name.'''),
                trap = T_(
'''* The "Rue Desjardins" can be called like that, even though offers
"Rue des Jardins",
* Beware of homonyms, a local glorious man can be called "Jean Monet",
his name not need be transformed into "Jean Monnet",
* The "Rond-Point des Allées" is perhaps not the "Rond-Point des Alliés",
* The "Rue de Ballevue" may be the right name for this street.'''),
                example = T_(
'''* Rue Piere Curie ==> Rue Pierre Curie
* Rue du Général de Gaules ==> Rue du Général de Gaulle
* Mac Donald ==> McDonald's'''))


        else:
            self.scripts = None

    def analyser_osmosis_common(self):
        if not self.scripts:
            return

        if "language" in self.config.options and self.config.options["language"].startswith("fr"):
            self.run(sql01_fr)
            self.run(sql03.format("fn_soundex2"))
        else:
            self.run(sql03.format("dmetaphone"))
        self.run(sql03i)
        self.run(sql04)
        self.run(sql05)
        self.run(sql05i)
        self.run(sql06, lambda res: {
            "class":1,
            "data":[self.way_full, self.positionAsText],
            "fix":{"name":res[2].replace(res[3], res[4])}
        } )
