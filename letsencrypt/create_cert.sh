#!/usr/bin/bash

#
# Create a LE cert with a set of wildcard names.
#
# This script makes used of the "lexicon" DNS API. If you cannot use this API,
# then you need to figure it out on your own. Sorry.
#

#
# This script expects number of hostnames as input, only the host part!
#
#  ./create_cert.sh cluster00 cluster01 cluster02
#
# or
#
#  ./create_cert.sh $(seq -f cluster%02g 25 50)

set -e

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

die() { echo "$*" 1>&2 ; exit 1; }

set -a
source "${SCRIPT_DIR}/../config"
set +a

if [ -z "$ACME_SH" ]; then
	which acme.sh &>/dev/null && ACME_SH=acme.sh || die "'ACME_SH' not set and 'acme.sh' is not in the PATH"
else
	ACME_SH="${ACME_SH}/acme.sh"
	test -x "${ACME_SH}" || die "'ACME_SH' doesn't point to a directory containing the 'acme.sh' script"
fi

DOMAINS=

for i in "$@"; do
	DOMAINS="$DOMAINS -d ${i}.${SUB_DOMAIN_PART}.${BASE_DOMAIN}"
	DOMAINS="$DOMAINS -d *.${i}.${SUB_DOMAIN_PART}.${BASE_DOMAIN}"
done

test -n "$DOMAINS" || die "No domains provided"

"$ACME_SH" $ACME_OPTS --issue $DOMAINS --dns dns_lexicon

