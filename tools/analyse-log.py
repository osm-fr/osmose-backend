#! /usr/bin/python

import fileinput
import datetime
import re

re_timestamp = re.compile("^[0-9]{4}-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]")

def convert_time(string):
  return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

def end_file():
  end_task()
  diff = convert_time(cur_timestamp) - convert_time(first_timestamp)
  print diff, cur_filename
  print

def end_task():
  diff = convert_time(cur_timestamp) - convert_time(first_task_timestamp)
  print "--", diff, cur_task

cur_filename = None

cur_task = None

first_timestamp = None
cur_timestamp = None

for line in fileinput.input():
  if not re_timestamp.match(line):
    continue

  if cur_filename is None:
    cur_filename = fileinput.filename()
    first_timestamp = line[:19]

  if fileinput.filename() != cur_filename:
    end_file()
    cur_filename = fileinput.filename()
    first_timestamp = line[:19]
    cur_task = None

  cur_timestamp = line[:19]

  if line[20:27] == "[0;31m":
    if cur_task != None:
      end_task()
    cur_task = line[27:].strip()
    first_task_timestamp = line[:19]

  elif line[19] == " " and line[20] != " " and line[20] != "":
    if cur_task != None:
      end_task()
    cur_task = line[20:].strip()
    first_task_timestamp = line[:19]

end_file()
