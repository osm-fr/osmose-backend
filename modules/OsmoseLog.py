#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
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

from __future__ import print_function

import time, sys, subprocess

class logger:
    
    def __init__(self, out = sys.stdout, showall = True):
        self._incpt   = False
        self._out     = out
        self._showall = showall

        self.log_av_r = u'\033[0;31m'
        self.log_av_b = u'\033[0;34m'
        self.log_av_v = u'\033[0;32m'
        self.log_ap   = u'\033[0m'

        
    def _log(self, txt, level):
        if self._incpt:
            self._out.write(u"\r".encode("utf-8"))
            self._out.write(u" "*len(self._lastcpt.encode("utf-8")))
            self._out.write(u"\r".encode("utf-8"))
            self._out.flush()
            self._incpt = False
        pre  = u""
        pre += time.strftime("%Y-%m-%d %H:%M:%S ")
        pre += u"  "*level
        suf  = u""
        print(pre.encode("utf8") + txt.encode("utf8") + suf.encode("utf8"), file=self._out)
        self._out.flush()
        
    def _cpt(self, txt, level):
        if not self._showall:
            return
        if self._incpt:
            self._out.write(u"\r".encode("utf-8"))
            self._out.write(" "*len(self._lastcpt.encode("utf-8")))
            self._out.write(u"\r".encode("utf-8"))
        self._incpt = True
        pre  = u""
        pre += time.strftime("%Y-%m-%d %H:%M:%S ").decode("utf8")
        pre += "  "*level
        suf  = u""
        self._lastcpt = pre + txt + suf
        self._out.write(self._lastcpt.encode("utf-8"))
        self._out.flush()
        
    def log(self, txt):
        self._log(txt, 0)

    def cpt(self, txt):
        self._cpt(txt, 0)

    def sub(self):
        return sublog(self, 1)
        
    def execute_err(self, cmd):
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        newline = True
        while True:
            cerr = proc.stderr.read(1)
            if cerr == '' and proc.poll() != None:
                break
            if newline:
                if self._showall:
                    self._out.write(time.strftime("%Y-%m-%d %H:%M:%S ").decode("utf8")+"  ")
                newline = False
            if cerr in "\r\n":
                newline = True
            if self._showall:
                self._out.write(cerr)
                self._out.flush()
        proc.wait()
        if proc.returncode:
            raise RuntimeError("'%s' exited with status %s"%(' '.join(cmd), repr(proc.returncode)))
        #self.log(str(proc.returncode))
        
    def execute_out(self, cmd):
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        newline = True
        while True:
            cerr = proc.stdout.read(1)
            if cerr == '' and proc.poll() != None:
                break
            if newline:
                if self._showall:
                    self._out.write(time.strftime("%Y-%m-%d %H:%M:%S ").decode("utf8")+"  ")
                newline = False
            if cerr in "\r\n":
                newline = True
            if self._showall:
                self._out.write(cerr)
                self._out.flush()
        proc.wait()
        if proc.returncode:
            raise RuntimeError("'%s' exited with status %s :\n%s"%(' '.join(cmd), repr(proc.returncode), proc.stderr.read()))
        #self.log(str(proc.returncode))
    
class sublog:
    
    def __init__(self, root, level):
        self._root  = root
        self._level = level

    def log(self, txt):
        self._root._log(txt, self._level)

    def cpt(self, txt):
        self._root._cpt(txt, self._level)

    def sub(self):
        return sublog(self._root, self._level + 1)

if __name__=="__main__":
    a = logger()
    a.log("coucou")
    a.sub().log("test")
    a.sub().sub().log("test")
    a.sub().log("test")
