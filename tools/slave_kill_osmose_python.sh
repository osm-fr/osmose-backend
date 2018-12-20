#!/bin/bash

# @(#) slave_kill_osmose_python.sh, v1.0.0, 2018/11/22, kill python process run by osmose user
# ##############################################################################
# v1.0.0.debug, 2018/11/22, Marc_marc:
# - initial release
################################################################################
## Copyrights Marc_marc <marcmarcmarcmarc@protonmail.com> 2018                ##
## License : GNU General Public License as published by                       ##
## the Free Software Foundation, either version 3 of the License,             ##
## or (at your option) any later version.                                     ##
## http://www.gnu.org/licenses/                                               ##
################################################################################
# exit code :
# 0 : nothing todo
# 1 : successful use of kill
# 2 : successful use kill -9
# 3 : process still there after kill -9
# TODO : kill parent if kill -9 fails

# check arguments ...
[ "${#}" -eq 1 ] || { echo "$(date --rfc-3339=s) ERROR: usage: ${0} country" ; echo "$(date --rfc-3339=s) ERROR: usage: ${0} country" >&2 ; exit 1 ; }

echo "$(date --rfc-3339=s) INFO: ${0} start..."

if [ $(pgrep -u osmose -a python | grep " --country ${1}" | wc -l) -eq 0 ]; then
 echo "$(date --rfc-3339=s) INFO: no match. nothing todo"
 exit 0
fi
echo "$(date --rfc-3339=s) WARNING: match found. i'll make a kill"
#echo "$(date --rfc-3339=s) DEBUG: pgrep output : $(pgrep -u osmose -a python -o | grep " --country ${1}")"
#echo "$(date --rfc-3339=s) DEBUG: I 'll do : kill $(pgrep -u osmose -a python -o | grep " --country ${1}" | awk '{ print $1 }')"
kill $(pgrep -u osmose -a python -o | grep " --country ${1}" | awk '{ print $1 }')
sleep 5
if [ $(pgrep -u osmose -a python | grep " --country ${1}" | wc -l) -eq 0 ]; then
 echo "$(date --rfc-3339=s) INFO: no more match. kill win :-)"
 exit 1
fi
echo "$(date --rfc-3339=s) WARNING: match still found. i'll make a kill -9"
#echo "$(date --rfc-3339=s) DEBUG: I 'll do : kill -9 $(pgrep -u osmose -a python -o | grep " --country ${1}" | awk '{ print $1 }')"
kill -9 $(pgrep -u osmose -a python -o | grep " --country ${1}" | awk '{ print $1 }')
sleep 5
if [ $(pgrep -u osmose -a python | grep " --country ${1}" | wc -l) -eq 0 ]; then
 echo "$(date --rfc-3339=s) INFO: no more match. kill -9 win :-)"
 exit 2
fi
echo "$(date --rfc-3339=s) WARNING: match still found. request a sysadmin to improve the script :-)"
#echo "$(date --rfc-3339=s) DEBUG: ps waxuf | grep [o]smose_run.py"
ps waxuf | grep [o]smose_run.py
exit 3
echo "$(date --rfc-3339=s) INFO: ${0} end."
