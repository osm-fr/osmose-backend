#!/bin/bash

# @(#) requirements.sh, v1.1.0, 2022/10/30, run pip -r requirements.txt if needed
# ##############################################################################
# v1.1.0, 2022/10/30, Marc_marc:
# - less hardcore path, use pushd/popd in stead of cd, more error code
# ##############################################################################
# v1.0.0, 2022/10/27, Marc_marc:
# - initial release
################################################################################
## Copyrights Marc_marc <marcmarcmarcmarc@protonmail.com> 2018                ##
## License : GNU General Public License as published by                       ##
## the Free Software Foundation, either version 3 of the License,             ##
## or (at your option) any later version.                                     ##
## http://www.gnu.org/licenses/                                               ##
################################################################################
# exit code :
# 0 : ok
# 1 : error when pushd/popd
# 2 : error with pip
# 3 : requirements.txt not found

echo "$(date --rfc-3339=s) INFO: ${0} start..."
Semaphore=/tmp/requirements.txt.$USER.done
pushd $(dirname $(dirname ${0})) >/dev/null || { echo "$(date --rfc-3339=s) ERROR: pushd" >&2 ; exit 1 ; }
if [ -f ${Semaphore} ]; then
  echo "$(date --rfc-3339=s) DEBUG: at least one requirements run"
  if [ ! -z "$(find . -type f -name requirements.txt -cnewer ${Semaphore} -prune 2>/dev/null)" ]; then
    echo "$(date --rfc-3339=s) WARNING: requirements.txt is newer than our semaphore. updating"
    pip3 install --upgrade pip
    [ -f requirements.txt ] || { echo "$(date --rfc-3339=s) ERROR: requirements.txt not found in $PWD" >&2 ; exit 3 ; }
    rm -rf ~/.local/lib/python*/site-packages/PyKOpeningHours*
    pip3 install -r requirements.txt || exit 2
    touch -r requirements.txt ${Semaphore}
    echo "$(date --rfc-3339=s) INFO: pip -r requirements.txt done"
  else
    echo "$(date --rfc-3339=s) DEBUG: requirements.txt not newer than our semaphore. nothing todo"
  fi
else
  echo "$(date --rfc-3339=s) WARNING: requirements semaphore doesn't exist. updating"
  pip3 install --upgrade pip
  [ -f requirements.txt ] || { echo "$(date --rfc-3339=s) ERROR: requirements.txt not found in $PWD" >&2 ; exit 3 ; }
  rm -rf ~/.local/lib/python*/site-packages/PyKOpeningHours*
  pip3 install -r requirements.txt || exit 2
  touch -r requirements.txt ${Semaphore}
  echo "$(date --rfc-3339=s) INFO: pip -r requirements.txt done"
fi
popd >/dev/null || { echo "$(date --rfc-3339=s) ERROR: popd" >&2 ; exit 1 ; }
echo "$(date --rfc-3339=s) INFO: ${0} end."
