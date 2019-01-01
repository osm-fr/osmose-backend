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
        self._out     = out
        self._showall = showall

        self.log_av_r     = u'\033[0;31m'  # red
        self.log_av_b     = u'\033[0;34m'  # blue
        self.log_av_green = u'\033[0;32m'  # green
        self.log_ap       = u'\033[0m'     # reset color


    def _log(self, txt, level):
        pre  = u""
        pre += time.strftime("%Y-%m-%d %H:%M:%S ")
        pre += u"  "*level
        suf  = u""
        print(pre.encode("utf8") + txt.encode("utf8") + suf.encode("utf8"), file=self._out)
        self._out.flush()

    def log(self, txt):
        self._log(txt, 0)


    def _err(self, txt, level):
        self._log(self.log_av_r + "error: " + txt + self.log_ap, level)

    def err(self, txt):
        self._err(txt, 0)


    def sub(self):
        return sublog(self, 1)

    def execute_err(self, cmd):
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            cerr = proc.stderr.readline().decode('utf-8').strip()
            if cerr == '' and proc.poll() != None:
                break
            if cerr == '':
                continue
            if self._showall:
                self._out.write(u'{0}   {1}\n'.format(time.strftime("%Y-%m-%d %H:%M:%S"), cerr))
                self._out.flush()
        proc.wait()
        if proc.returncode:
            raise RuntimeError("'%s' exited with status %s"%(' '.join(cmd), repr(proc.returncode)))
        #self.log(str(proc.returncode))

    def execute_out(self, cmd, cwd=None):
        proc = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            cerr = proc.stdout.readline().decode('utf-8').strip()
            if cerr == '' and proc.poll() != None:
                break
            if cerr == '':
                continue
            if self._showall:
                self._out.write(u'{0}   {1}\n'.format(time.strftime("%Y-%m-%d %H:%M:%S "), cerr))
                self._out.flush()
        proc.wait()
        if proc.returncode:
            raise RuntimeError("'%s' exited with status %s :\n%s"%(' '.join(cmd), repr(proc.returncode), proc.stderr.read()))
        #self.log(str(proc.returncode))

    def send_alert_email(self, email_to, err_msg):
        if not email_to:
            return

        import smtplib, socket
        from email.mime.text import MIMEText

        hostname = socket.getfqdn()
        email_from = "osmose@%s" % hostname

        msg = MIMEText(err_msg)
        msg['Subject'] = '%s - osmose failure - %s' % (hostname, err_msg)
        msg['From'] = email_from
        msg['To'] = ", ".join(email_to)

        s = smtplib.SMTP('127.0.0.1')
        s.sendmail(email_from, email_to, msg.as_string())
        s.quit()


class sublog:

    def __init__(self, root, level):
        self._root  = root
        self._level = level

    def log(self, txt):
        self._root._log(txt, self._level)

    def err(self, txt):
        self._root._err(txt, self._level)

    def sub(self):
        return sublog(self._root, self._level + 1)

if __name__=="__main__":
    a = logger()
    a.log("coucou")
    a.sub().log("test")
    a.sub().sub().log("test")
    a.sub().log("test")
    a.log(a.log_av_r     + "red" + a.log_ap)
    a.log(a.log_av_green + "green" + a.log_ap)
    a.log(a.log_av_b     + "blue" + a.log_ap)
    a.err("test 1")
    a.sub().err("test 2")
    a.sub().sub().err("test 3")
