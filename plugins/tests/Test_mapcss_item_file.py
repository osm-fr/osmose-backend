#-*- coding: utf-8 -*-
import importlib
import inspect
from plugins.Plugin import TestPluginCommon
from mapcss.item_map import item_map

class Test(TestPluginCommon):
  def test(self):
    for file_id, file_props in item_map.items():
      classname = file_props["prefix"] + file_id.replace("-", "_")
      n = getattr(importlib.import_module("plugins." + classname), classname)
      mapcssObj = n(None)
      mapcssObj.init(None)

      if "class" in file_props:
        known_classes = file_props["class"].values()
        # Check if hardcoded classes still exist
        for classNo in known_classes:
          if classNo != 0:
            assert classNo in mapcssObj.errors, "item_map.py: class " + str(classNo) + " doesn't exist anymore in " + file_id

        # Check if classes are missing in hardcoded list
        for err in mapcssObj.errors:
          pass
          # assert err in known_classes, "item_map.py: class " + str(err) + " doesn't exist yet in " + file_id

      # Existing blacklisted subclasses should be present as comments in the source file
      if "subclass_blacklist" in file_props:
        code_source = inspect.getsourcefile(n)
        code = open(code_source, "r").read()
        for blacklist_id in file_props["subclass_blacklist"]:
          assert str(blacklist_id) in code, "item_map.py: blacklist " + str(blacklist_id) + " doesn't exist anymore in " + file_id
