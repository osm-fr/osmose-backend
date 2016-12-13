#!/usr/bin/ruby

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2016                                      ##
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

# http://www.unicode.org/Public/UNIDATA/Scripts.txt
@scripts = File.open('Scripts.txt').each_line.select{ |line|
  line[0] != '#' && line != "\n"
}.collect{ |line|
  range, script = line.split(/[;#]/).collect(&:strip)
  range = range.split('..').collect(&:hex)
  [range, script]
}.sort_by{ |r| r[0][0] }.reduce(nil){ |sum, n|
  if sum == nil
    sum = [n]
  elsif sum[-1][0][-1] == n[0][0] && sum[-1][1] == n[1]
    sum[-1][0][-1] = n[0][-1]
  else
    sum << n
  end
}

def get_script(point_code)
  i = (0..@scripts.size).bsearch{ |i| @scripts[i][0][0] >= point_code }
  if @scripts[i][0][0] > point_code
    i -= 1
  end
  if i >= 0 && @scripts[i][0][0] <= point_code && point_code <= @scripts[i][0][-1]
    @scripts[i][1]
  end
end


# http://www.unicode.org/Public/security/latest/confusables.txt
confusables = File.open('confusables.txt').each_line.select{ |line|
  line[0] != '#' && line != "\n"
}.collect{ |line|
  line.split(';').collect(&:strip)[0..1].collect{ |o| o.split(' ').collect(&:hex) }
}.select{ |a, b|
  a.size == 1 && b.size == 1
}.collect{ |a, b|
  [a.pack('U'), b.pack('U')]
}.group_by(&:last).collect{ |g, v|
  [g, [g] + v.collect(&:first)]
}

usable_confusables = confusables.collect{ |g, v|
  [g, v.collect{ |vv| [vv, get_script(vv.unpack('U')[0])] }.select{ |vv, script| script && script != 'Common' }]
}.select{ |g, v|
  v.size > 0
}.collect{ |g, v|
  [g, v.group_by(&:last).select{ |script, y| y.size == 1 }.collect{ |script, y| [y[0][0], script] }]
}.select{ |g, v|
  v.size > 0 && !(v.size == 1 && g == v[0][0])
}


def quote(s)
  s = s == "'" ? "\\'" : s
  "u'#{s}'"
end

puts "#! /usr/bin/python"
puts "# -*- coding: UTF-8"

puts "confusables_fix = {"
puts usable_confusables.collect{ |k, v|
  "  #{quote(k)}:{" + v.collect{ |vv, script| "'#{script}':#{quote(vv)}" }.join(',') + "}"
}.join(",\n")
puts "}"

usable_confusables_key = usable_confusables.collect(&:first)
puts "confusables = {"
puts confusables.select{ |g, v|
  usable_confusables_key.include?(g)
}.collect{ |g, v|
  v.collect{ |vv|
    "  #{quote(vv)}:#{quote(g)}"
  }
}.flatten.join(",\n")
puts "}"
