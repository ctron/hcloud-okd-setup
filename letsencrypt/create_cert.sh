#!/usr/bin/bash

#
# Create a LE cert with a set of wildcard names.
#
# This script makes used of the "lexicon" DNS API. If you cannot use this API,
# then you need to figure it out on your own. Sorry.
#

set -e

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

die() { echo "$*" 1>&2 ; exit 1; }

source "${SCRIPT_DIR}/../config"

export PROVIDER
export LEXICON_OPTS

if [ -z "$ACME_SH" ]; then
	which acme.sh &>/dev/null && ACME_SH=acme.sh || die "'ACME_SH' not set and 'acme.sh' is not in the PATH"
else
	ACME_SH="${ACME_SH}/acme.sh"
	test -x "${ACME_SH}" || die "'ACME_SH' doesn't point to a directory containing the 'acme.sh' script"
fi

DOMAINS=

for i in $(seq -w 0 25); do
	DOMAINS="$DOMAINS -d cluster${i}.${SUB_DOMAIN_PART}.${BASE_DOMAIN}"
	DOMAINS="$DOMAINS -d *.cluster${i}.${SUB_DOMAIN_PART}.${BASE_DOMAIN}"
done

"$ACME_SH" $ACME_OPTS --issue $DOMAINS --dns dns_lexicon
