#!/bin/bash

# @(#) sentry.sh, v1.0.0, 2022/10/24, echo debug for sentry
# ##############################################################################
# v1.0.0, 2022/10/24, Marc_marc:
# - initial release
################################################################################
## Copyrights Marc_marc <marcmarcmarcmarc@protonmail.com> 2022                ##
## License : GNU General Public License as published by                       ##
## the Free Software Foundation, either version 3 of the License,             ##
## or (at your option) any later version.                                     ##
## http://www.gnu.org/licenses/                                               ##
################################################################################
# exit code :
# 0 : nothing todo

echo "$(date --rfc-3339=s) INFO: ${0} start..."
if [ -z "$SENTRY_DSN" ]; then
  echo "$(date --rfc-3339=s) WARNING: SENTRY_DSN not set or empty"
else
  echo "$(date --rfc-3339=s) INFO: SENTRY_DSN is $SENTRY_DSN"
fi
echo "$(date --rfc-3339=s) INFO: ${0} end."
