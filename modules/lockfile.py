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

import os, fcntl


def get_pstree(pid=os.getpid()):
    tree = []
    while os.path.isdir("/proc/%d"%pid):
        tree.append((pid, open("/proc/%d/cmdline"%pid).read().replace('\x00', ' ').strip()))
        pid = int(open("/proc/%d/stat"%pid).read().split(" ")[3])
    tree.reverse()
    return tree

class lockfile:
    def __init__(self, filename):
        #return
        self.fn = filename
        try:
            olddata = open(self.fn, "r").read()
        except:
            olddata = ""
        try:
            self.fd = None
            self.fd = open(self.fn, "w")
            for l in get_pstree():
                self.fd.write("%6d %s\n"%l)
            self.fd.flush()
            fcntl.flock(self.fd, fcntl.LOCK_NB|fcntl.LOCK_EX)
        except:
            #restore old data
            if self.fd:
                self.fd.close()
            open(self.fn, "w").write(olddata)
            raise
        self.ok = True
    def __del__(self):
        #return
        if "fd" in dir(self):
            try:
                fcntl.flock(self.fd, fcntl.LOCK_NB|fcntl.LOCK_UN)
                self.fd.close()
            except:
                pass
        if "fn" in dir(self) and "ok" in dir(self):
            try:
                os.remove(self.fn)
            except:
                pass


###########################################################################
import unittest

class Test(unittest.TestCase):
    from modules import config

    dir_tmp_tests = os.path.join(config.dir_tmp, "tests")
    f1 = os.path.join(dir_tmp_tests, "lockfile1")
    f2 = os.path.join(dir_tmp_tests, "lockfile2")

    def setup(self):
        import os
        if not os.path.exists(self.dir_tmp_tests):
            os.makedirs(self.dir_tmp_tests)
        if os.path.isfile(self.f1):
            os.remove(self.f1)
        if os.path.isfile(self.f2):
            os.remove(self.f2)

    def test_two_locks(self):
        l1 = lockfile(self.f1)
        l2 = lockfile(self.f2)
        del l2
        del l1
        assert not os.path.isfile(self.f1)
        assert not os.path.isfile(self.f2)

    def test_twice_lock(self):
        l1 = lockfile(self.f1)
        with self.assertRaises(IOError):
            l1bis = lockfile(self.f1)

        del l1
        assert not os.path.isfile(self.f1)
