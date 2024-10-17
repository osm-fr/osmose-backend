#-*- coding: utf-8 -*-
from plugins.Plugin import TestPluginCommon
from plugins.modules.wikiReader import read_wiki_table, read_wiki_templates, wikitag2text

class Test(TestPluginCommon):
    def test_wikitag2text(self):
        for k in ["{{tag|abc|def}}", "{{Tag|abc|def}}", "{{ Tag | abc | def }}", "{{Key|abc|def}}", "{{Tag|abc||def}}", ]:
            assert wikitag2text(k) == "abc=def"

        for k in ["{{Tag|abc|}}", "{{tag|abc}}", "{{Key|abc}}"]:
            assert wikitag2text(k) == "abc=*"
            assert wikitag2text(k, star_value=False) == "abc"

        assert wikitag2text("{{tag|abc|def}} and {{tag|ghi|jkl}}", quote=True) == "`abc=def` and `ghi=jkl`"


    def test_wikitable(self):
        t = """
{| class="wikitable"
! species || species:wikidata || {{key|leaf_cycle}} || {{key|leaf_type}}
|-
| Abies alba || [[:d:Q146992|Q146992]] || evergreen     || '''needleleaved'''
|-
|Abies pinsapo
|[[:d:Q849381|Q849381]]
|evergreen
|needleleaved
|-
| Ziziphus jujuba || [[:d:Q11181633|Q11181633]] || deciduous
|}"""
        # Basic table reading + missing cell
        assert read_wiki_table(t) == [
            ["Abies alba", "Q146992", "evergreen", "needleleaved"],
            ["Abies pinsapo", "Q849381", "evergreen", "needleleaved"],
            ["Ziziphus jujuba", "Q11181633", "deciduous", None]]

        # Header retention and ensuring templates like {{key|*}} are retained
        assert read_wiki_table(t, skip_headers=False) == [
            ["species", "species:wikidata", "{{key|leaf_cycle}}", "{{key|leaf_type}}"],
            ["Abies alba", "Q146992", "evergreen", "needleleaved"],
            ["Abies pinsapo", "Q849381", "evergreen", "needleleaved"],
            ["Ziziphus jujuba", "Q11181633", "deciduous", None]]

        # Ensure we can use markup if needed
        assert read_wiki_table(t, keep_markup=True) == [
            ["Abies alba", "[[:d:Q146992|Q146992]]", "evergreen", "'''needleleaved'''"],
            ["Abies pinsapo", "[[:d:Q849381|Q849381]]", "evergreen", "needleleaved"],
            ["Ziziphus jujuba", "[[:d:Q11181633|Q11181633]]", "deciduous", None]]


    def test_wikitemplate(self):
        t = """
{{Deprecated features/item|lang={{{lang|}}}
|suggestion={{Tag|leaf_type}} '''or''' {{Tag|leaf_cycle}}
|  22  }}
"""
        assert read_wiki_templates(t, "Deprecated features/item")[0] == [
            "{{Deprecated features/item|lang=\n|suggestion={{Tag|leaf_type}} or {{Tag|leaf_cycle}}\n|  22  }}",
            "Deprecated features/item",
            "lang=",
            "suggestion={{Tag|leaf_type}} or {{Tag|leaf_cycle}}",
            "22"]
        assert read_wiki_templates(t, "Deprecated features/item", keep_markup = True)[0] == [
            t.strip(),
            "Deprecated features/item",
            "lang={{{lang|}}}",
            "suggestion={{Tag|leaf_type}} '''or''' {{Tag|leaf_cycle}}",
            "22"]
