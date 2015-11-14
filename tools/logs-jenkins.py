#! /usr/bin/python

import argparse
import collections
import datetime
import jenkinsapi
import operator
import os
import pprint
import re
import sys
import termcolor

from jenkinsapi.jenkins import Jenkins
from termcolor import colored

def analyse_log(filename):
  re_timestamp = re.compile("^[0-9]{4}-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]")

  first_timestamp = None
  cur_timestamp = None

  cur_task = None

  tasks = collections.OrderedDict()

  f = open(filename, "r")
  for line in f:
    if not re_timestamp.match(line):
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
        tasks[cur_task] = cur_timestamp - first_task_timestamp
      cur_task = new_task
      first_task_timestamp = cur_timestamp

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


if __name__ == "__main__":

  parser = argparse.ArgumentParser(description="Download logs from Jenkins")
  parser.add_argument("country", nargs="+", help="Country to download (can be repeated, can end with *)")
  parser.add_argument("--force", action="store_true", help="Force re-downloading previous logs")
  parser.add_argument("--no-jenkins-check", action="store_true", help="Don't check if Jenkins server has more recent builds ")
  parser.add_argument("--num-builds", action="store", type=int, help="Number of builds to fetch")

  group = parser.add_argument_group('various statistics')
  group.add_argument("--country-stats", dest="stats_country", action="store_true", help="Statistics per country")
  group.add_argument("--global-stats", dest="stats_global", action="store_true", help="Global statistics")

  args = parser.parse_args()

  if not args.num_builds:
    if args.stats_global:
      args.num_builds = 0
    else:
      args.num_builds = 5

  J = Jenkins('http://jenkins.osmose.openstreetmap.fr')

  all_country = []
  list_country = set()
  for country in args.country:
    found = False
    if country in J:
      list_country.add(country)
      found = True
    elif country.endswith("*"):
      if not all_country:
        all_country = J.keys()
        all_country.remove("osmose-frontend")
        all_country.remove("osmose-backend")
      for c in all_country:
        if c.startswith(country[:-1]):
          list_country.add(c)
          found = True

    if not found:
      print "%s not found" % country
      sys.exit(1)

  timedelta_zero = datetime.timedelta(0)

  if args.stats_global:
    global_tasks_longest = {}
    global_total_time = timedelta_zero

  for country in list_country:
    if args.stats_country or not args.no_jenkins_check or len(list_country) < 15:
      print colored(country, attrs=["bold"])
    c_dir = os.path.join("logs", country)
    if not os.path.exists(c_dir):
      os.makedirs(c_dir)

    if args.no_jenkins_check and os.listdir(c_dir):
      nums = sorted([int(i) for i in os.listdir(c_dir)])
      last_num = int(nums[-1])
      first_num = max(nums[0],last_num-args.num_builds)
      orig_list_builds = sorted(set(nums).intersection(range(first_num, last_num + 1)))
    else:
      #last_num = J[country].get_last_completed_buildnumber()
      last_num = J[country].get_last_good_buildnumber()
      first_num = max(1,last_num-args.num_builds)
      orig_list_builds = range(first_num, last_num + 1)

    list_builds = orig_list_builds[:]
    for i in orig_list_builds:
      log_name = os.path.join(c_dir, "%03d" % i)
      if not args.force and os.path.isfile(log_name):
        if os.path.getsize(log_name) == 0:
          list_builds.remove(i)
        continue

      print "  downloading %d" % i
      try:
        b = J[country].get_build(i)
        with open(log_name, "w") as f:
          if b.get_status() == "SUCCESS":
            f.write(b.get_console())
          else:
            f.write("")
            print "    skipping (status=%s)" % b.get_status()
            list_builds.remove(i)

      except KeyError:
        print "    skipping (log missing)"
        list_builds.remove(i)

    if args.stats_country:
      stats = {}
      longer_than_day = False
      timedelta_long = datetime.timedelta(days=100)
      tasks_longest = {}
      tasks_shortest = {}
      tasks_increase = {}
      tasks_decrease = {}
      prev_i = None

      for i in list_builds:
        log_name = os.path.join(c_dir, "%03d" % i)
        stats[i] = analyse_log(log_name)
        if stats[i]["total"].days:
          longer_than_day = True
        for (t, tt) in stats[i]["tasks"].iteritems():
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
      for (k, v) in sorted(tasks_longest.items(), key=lambda x: x[1][0], reverse=True):
        big_tasks.append(k)
      print "longest tasks:"
      for i in xrange(5):
        print "  ", str_timedelta(tasks_longest[big_tasks[i]][0], print_day=longer_than_day), " ", big_tasks[i].split(":")[-1].strip()
      print

      for i in list_builds:
        print i,
        print "  ",
        print str_timedelta(stats[i]["total"], print_day=longer_than_day),
        for t in xrange(5):
          taskname = big_tasks[t]
          print " - ",
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
          print colored(str_timedelta(stats[i]["tasks"][taskname], print_day=tasks_longest[taskname][0].days), color, attrs=attrs),
        print

      print
      big_tasks = []
      for (k, v) in sorted(tasks_increase.items(), key=lambda x: x[1][0], reverse=True):
        big_tasks.append(k)
      print "largest increase in time:"
      for i in xrange(5):
        print "  ", str_timedelta(tasks_increase[big_tasks[i]][0]), " ", tasks_increase[big_tasks[i]][1], " ", big_tasks[i].split(":")[-1].strip()
      print

    if args.stats_global:
      try:
        last_stat = stats[last_num]
      except NameError:
        log_name = os.path.join(c_dir, "%03d" % last_num)
        last_stat = analyse_log(log_name)
      global_total_time += last_stat["total"]
      for (t, tt) in last_stat["tasks"].iteritems():
        a = t.split(":")[-1].strip()
        global_tasks_longest[a] = global_tasks_longest.get(a, timedelta_zero) + tt

  if args.stats_global:
    print
    print colored("GLOBAL STATISTICS", attrs=["bold"])
    print "total time:", global_total_time
    big_tasks = []
    for (k, v) in sorted(global_tasks_longest.items(), key=lambda x: x[1], reverse=True):
      big_tasks.append(k)
    print "longest tasks:"
    for i in xrange(10):
      print "  ", str_timedelta(global_tasks_longest[big_tasks[i]]), " ", big_tasks[i]
    print
