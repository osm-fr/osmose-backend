from unittest import mock
from plugins.Plugin import TestPluginCommon
from plugins.modules import wikiReader
from plugins.modules.wikiReader import read_wiki_table, read_wiki_templates, wikitag2text, urlwikiread

class Test(TestPluginCommon):
    def test_wikitag2text(self):
        for k in ["{{tag|abc|def}}", "{{Tag|abc|def}}", "{{ Tag | abc | def }}", "{{Key|abc|def}}", "{{Tag|abc||def}}", "{{Tag|abc|def|kl=de|vl=de}}", "{{Tag|abc|def|lang=de|nocat=yes}}", ]:
            assert wikitag2text(k) == "abc=def"

        for k in ["{{Tag|abc|}}", "{{tag|abc}}", "{{Key|abc}}"]:
            assert wikitag2text(k) == "abc=*"
            assert wikitag2text(k, star_value=False) == "abc"

        assert wikitag2text("{{tag|abc|def}} and {{tag|ghi|jkl}}", quote=True) == "`abc=def` and `ghi=jkl`"

        for k in ["{{Tag|abc:def:ghi|jkl}}", "{{Tag|abc|subkey=def|subkey2=ghi|jkl}}", "{{Tag|abc|:=def|::=ghi|jkl}}", "{{Tag|abc|:=def|::=ghi|jkl|kl::=fr}}", ]:
            assert wikitag2text(k) == "abc:def:ghi=jkl"

        for k in ["{{Tag|abc||def;ghi}}", "{{Tag|abc|def|;=ghi}}", "{{Tag|abc|def|;=ghi|vl1=nl}}", ]:
            assert wikitag2text(k) == "abc=def;ghi"



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

    def test_wikitable_celltemplate(self):
        t = """
{| class="wikitable sortable"
| ABC || DEF {{Taginfo entry|amenity}} || GHI
|-
| ABC || DEF
{{Taginfo entry|amenity}}
| {{Key|GHI}}
|-
| ABC ||
{{Taginfo entry|amenity}} ||
|}
"""
        assert read_wiki_table(t) == [
            ["ABC", "DEF", "{{Taginfo entry|amenity}}", "GHI"],
            ["ABC", "DEF", "{{Taginfo entry|amenity}}", "{{Key|GHI}}"],
            ["ABC", "", "{{Taginfo entry|amenity}}", ""]]

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

    def test_urlwikiread_no_redirect(self):
        with mock.patch.object(wikiReader, "urlread", return_value="some wikitext") as m:
            assert urlwikiread("https://wiki.openstreetmap.org/w/index.php?title=Foo&action=raw", 7) == "some wikitext"
            m.assert_called_once_with("https://wiki.openstreetmap.org/w/index.php?title=Foo&action=raw", 7)

    def test_urlwikiread_redirect_indexphp(self):
        def fake(url, delay):
            return "#REDIRECT [[Bar]]" if "title=Foo" in url else "{| table |}"
        with mock.patch.object(wikiReader, "urlread", side_effect=fake) as m:
            assert urlwikiread("https://wiki.openstreetmap.org/w/index.php?title=Foo&action=raw", 7) == "{| table |}"
        m.assert_has_calls([
            mock.call("https://wiki.openstreetmap.org/w/index.php?title=Foo&action=raw", 7),
            mock.call("https://wiki.openstreetmap.org/w/index.php?title=Bar&action=raw", 7)])

    def test_urlwikiread_redirect_wiki_path(self):
        calls = []
        def fake(url, delay):
            calls.append((url, delay))
            return "#REDIRECT [[List of postal codes]]" if len(calls) == 1 else "final"
        with mock.patch.object(wikiReader, "urlread", side_effect=fake):
            assert urlwikiread("https://en.wikipedia.org/wiki/Postal_codes?action=raw", 1) == "final"
        assert calls == [
            ("https://en.wikipedia.org/wiki/Postal_codes?action=raw", 1),
            ("https://en.wikipedia.org/wiki/List_of_postal_codes?action=raw", 1)]

    def test_urlwikiread_max_redirects(self):
        with mock.patch.object(wikiReader, "urlread", return_value="#REDIRECT [[X]]"):
            with self.assertRaises(Exception):
                urlwikiread("https://wiki.openstreetmap.org/w/index.php?title=A&action=raw", 1, maxRedirects=2)
