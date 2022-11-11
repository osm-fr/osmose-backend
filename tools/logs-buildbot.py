#!/usr/bin/env python3

import argparse
import collections
import datetime
import json
import os
import re
import sys
import requests

from typing import List, Dict, Any, Union, Optional
from termcolor import colored

def analyse_log(filename):
  re_timestamp = re.compile("^[0-9]{4}-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]")

  log_with_color = False

  first_timestamp = None
  cur_timestamp = None

  cur_task = None

  tasks = collections.OrderedDict()

  f = open(filename, "r")
  for line in f:
    if not re_timestamp.match(line):
      continue

    if "[0" in line:
      log_with_color = True
    elif log_with_color:
      continue

    # hack for lines with multiple timestamps
    while re_timestamp.match(line[22:]):
      line = line[22:]

    cur_timestamp = datetime.datetime.strptime(line[:19], "%Y-%m-%d %H:%M:%S")
    new_task = cur_task

    if first_timestamp is None:
      first_timestamp = cur_timestamp

    if line[20:27] == "[0;31m":
      new_task = line[27:].strip()

    elif line[19] == " " and line[20] != " " and line[20] != "":
      new_task = line[20:].strip()

    if new_task != cur_task:
      if cur_task and not "iteration=" in cur_task:
        tasks[cur_task] = cur_timestamp - first_task_timestamp # noqa
      cur_task = new_task
      first_task_timestamp = cur_timestamp # noqa

  if first_timestamp is None:
    return None

  return {"total": cur_timestamp - first_timestamp, "tasks": tasks}

def str_timedelta(t, print_day=False):
  mm, ss = divmod(t.seconds, 60)
  hh, mm = divmod(mm, 60)
  s = "%2d:%02d:%02d" % (hh, mm, ss)
  if t.days:
    s = ("%d days, " % t.days) + s
  elif print_day or t.days:
    s = "        " + s
  if t.microseconds:
    s = s + ".%06d" % t.microseconds
  return s

def str_timedelta_empty(print_day=False):
  return "    -   "

if __name__ == "__main__":

  parser = argparse.ArgumentParser(description="Download logs from buildbot")
  parser.add_argument("country", nargs="+", help="Country to download (can be repeated, can end with *)")
  parser.add_argument("--task", dest="tasks", action="append", help="Task to check (can be repeated)")
  parser.add_argument("--force", action="store_true", help="Force re-downloading previous logs")
  parser.add_argument("--no-buildbot-check", action="store_true", help="Don't check if Buildbot server has more recent builds ")
  parser.add_argument("--num-builds", action="store", type=int, help="Number of builds to fetch")
  parser.add_argument("--past-build", action="store", metavar="BUILD", type=int, default=0, help="Check build before %(metavar)s")

  group = parser.add_argument_group('various statistics')
  group.add_argument("--country-stats", dest="stats_country", action="store_true", help="Statistics per country")
  group.add_argument("--global-stats", dest="stats_global", action="store_true", help="Global statistics")

  args = parser.parse_args()

  if not args.num_builds:
    if args.stats_global:
      args.num_builds = 1
    else:
      args.num_builds = 5

  buildbot_root = u"https://buildbot.osmose.openstreetmap.fr"
  buildbot_api = buildbot_root + "/api/v2/"

  builders_json: Dict[str, Any] = json.loads(requests.get(buildbot_api + "builders").text)
  builders = {}
  for b in builders_json["builders"]:
    builders[b["name"]] = b["builderid"]

  all_country: List[str] = []
  list_country = set()
  for country in args.country:
    found = False
    if country in builders:
      list_country.add(country)
      found = True
    elif country.endswith("*"):
      if not all_country:
        all_country = list(builders.keys())
        if "osmose-frontend" in all_country:
          all_country.remove("osmose-frontend")
        if "osmose-backend" in all_country:
          all_country.remove("osmose-backend")
      for c in all_country:
        if c.startswith(country[:-1]):
          list_country.add(c)
          found = True

    if not found:
      print("%s not found" % country)
      if args.no_buildbot_check and os.listdir(os.path.join("logs", country)):
        list_country.add(country)
      else:
        sys.exit(1)

  timedelta_zero = datetime.timedelta(0)

  if args.stats_global:
    global_tasks_longest: Dict[Any, Any] = {}
    global_countries_longest = {}
    global_total_time = timedelta_zero

  for country in list_country:
    if args.stats_country or not args.no_buildbot_check or len(list_country) < 15:
      print(colored(country, attrs=["bold"]))
    c_dir = os.path.join("logs", country)
    if not os.path.exists(c_dir):
      os.makedirs(c_dir)

    if args.no_buildbot_check and os.listdir(c_dir):
      nums = sorted([int(i) for i in os.listdir(c_dir)], reverse=True)
      list_builds = nums[:]
    else:
      builds = json.loads(requests.get(buildbot_api + "builders/%d/builds?complete__eq=true&order=-complete_at&limit=%d" % (builders[country], args.num_builds + args.past_build)).text)
      list_builds = [int(i["buildid"]) for i in builds["builds"]]
      if len(list_builds) == 0:
        continue

    if args.past_build > 0:
      orig_list_builds = list_builds[args.past_build:]
    else:
      orig_list_builds = list_builds[:]

    list_builds = orig_list_builds[:]
    for i in orig_list_builds:
      log_name = os.path.join(c_dir, "%03d" % i)
      if not args.force and os.path.isfile(log_name):
        if os.path.getsize(log_name) == 0:
          list_builds.remove(i)
        continue

      print("  downloading %d" % i)
      try:
        u = buildbot_api + "builds/%d/steps/2/logs/stdio/contents" % i
        log: Dict[str, List[Dict[str, str]]] = json.loads(requests.get(u).text)
        with open(log_name, 'w') as f:
          for cc in log["logchunks"]:
            for line in cc["content"].split("\n"):
              # need to remove first character, encoding stdio/stderr
              f.write(line[1:] + "\n")

      except:
        if os.path.isfile(log_name):
          os.unlink(log_name)
        print("    skipping (log missing)")
        list_builds.remove(i)

    if len(list_builds) == 0:
      continue

    if args.stats_country:
      stats = {}
      longer_than_day = False
      timedelta_long = datetime.timedelta(days=100)
      tasks_longest: Dict[Any, Any] = {}
      tasks_shortest: Dict[Any, Any] = {}
      tasks_increase: Dict[Any, Any] = {}
      tasks_decrease: Dict[Any, Any] = {}
      prev_i = None

      orig_list_builds = list_builds[:]
      for i in orig_list_builds:
        log_name = os.path.join(c_dir, "%03d" % i)
        stats[i] = analyse_log(log_name)
        if stats[i] is None:
          print("    skipping %s" % log_name)
          list_builds.remove(i)
          continue
        if stats[i]["total"].days:
          longer_than_day = True
        for (t, tt) in stats[i]["tasks"].items():
          if tasks_longest.get(t, (timedelta_zero, 0))[0] < tt:
            tasks_longest[t] = (tt, i)
          if tasks_shortest.get(t, (timedelta_long, 0))[0] > tt:
            tasks_shortest[t] = (tt, i)
          if prev_i is not None and t in stats[prev_i]["tasks"]:
            delta = tt - stats[prev_i]["tasks"][t]
            if delta > tasks_increase.get(t, (timedelta_zero, 0))[0]:
              tasks_increase[t] = (delta, i)
            if -delta > tasks_decrease.get(t, (timedelta_zero, 0))[0]:
              tasks_decrease[t] = (-delta, i)
        prev_i = i

      big_tasks = []
      if args.tasks:
        for i in args.tasks:
          for j in tasks_longest:
            if i in j:
              big_tasks.append(j)
        print("tasks:")
      else:
        for (k, v) in sorted(tasks_longest.items(), key=lambda x: x[1][0], reverse=True):
          big_tasks.append(k)
        print("longest tasks:")
      num_big_tasks = min(len(big_tasks), 5)
      for i in range(num_big_tasks):
        print("  ", str_timedelta(tasks_longest[big_tasks[i]][0], print_day=longer_than_day), " ", big_tasks[i].split(":")[-1].strip())
      print()

      for i in list_builds:
        print(i, end=' ')
        print("  ", end=' ')
        print(str_timedelta(stats[i]["total"], print_day=longer_than_day), end=' ')
        for t in range(num_big_tasks):
          taskname = big_tasks[t]
          print(" - ", end=' ')
          color: Optional[str] = None
          attrs: Optional[Union[str, List[str]]] = None
          if tasks_longest[taskname][1] == i:
            color = "red"
            attrs = ["bold"]
          elif tasks_shortest[taskname][1] == i:
            color = "green"
            attrs = ["bold"]
          elif taskname in tasks_increase and tasks_increase[taskname][1] == i:
            color = "yellow"
            attrs = None
          elif taskname in tasks_decrease and tasks_decrease[taskname][1] == i:
            color = "green"
            attrs = None
          else:
            color = None
            attrs = None
          try:
            val = str_timedelta(stats[i]["tasks"][taskname], print_day=tasks_longest[taskname][0].days)
          except:
            val = str_timedelta_empty()
          print(colored(val, color, attrs=attrs), end=' ')
        print()

      if not args.tasks:
        print()
        big_tasks = []
        for (k, v) in sorted(tasks_increase.items(), key=lambda x: x[1][0], reverse=True):
          big_tasks.append(k)
        print("largest increase in time:")
        for i in range(min(5,len(big_tasks))):
          print("  ", str_timedelta(tasks_increase[big_tasks[i]][0]), " ", tasks_increase[big_tasks[i]][1], " ", big_tasks[i].split(":")[-1].strip())
        print()

    if args.stats_global:
      last_num = list_builds[0]
      try:
        last_stat = stats[last_num]
      except NameError:
        log_name = os.path.join(c_dir, "%03d" % last_num)
        last_stat = analyse_log(log_name)
      global_total_time += last_stat["total"]
      for (t, tt) in last_stat["tasks"].items():
        a = t.split(":")[-1].strip()
        global_tasks_longest[a] = global_tasks_longest.get(a, timedelta_zero) + tt

      if args.tasks:
        for t in last_stat["tasks"]:
          if args.tasks[0] in t:
            global_countries_longest[country] = last_stat["tasks"][t]
      else:
        global_countries_longest[country] = last_stat["total"]

  if args.stats_global:
    print()
    print(colored("GLOBAL STATISTICS", attrs=["bold"]))
    print("total time:", global_total_time)
    big_tasks = []
    if args.tasks:
      for i in args.tasks:
        for j in global_tasks_longest:
          if i in j:
            big_tasks.append(j)
      print("tasks:")
    else:
      for (k, v) in sorted(global_tasks_longest.items(), key=lambda x: x[1], reverse=True):
        big_tasks.append(k)
      print("longest tasks:")
    for i in range(min(10,len(big_tasks))):
      print("  ", str_timedelta(global_tasks_longest[big_tasks[i]]), " ", big_tasks[i])
    print()

    print("longest countries:")
    big_countries = []
    for (k, v) in sorted(global_countries_longest.items(), key=lambda x: x[1], reverse=True):
      big_countries.append(k)
    for i in range(min(10,len(big_countries))):
      print("  ", str_timedelta(global_countries_longest[big_countries[i]]), " ", big_countries[i])
    print()
