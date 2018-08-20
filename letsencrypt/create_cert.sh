#!/usr/bin/bash

set -e

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

die() { echo "$*" 1>&2 ; exit 1; }

source "${SCRIPT_DIR}/../config"

export PLESK_URL
export PLESK_USER
export PLESK_PASSWORD
export BASE_DOMAIN

test -n "$ACME_SH" || die "'ACME_SH' not set"
test -x "${ACME_SH}/acme.sh" || die "'ACME_SH' doesn't point to a directory containing an executuable 'acme.sh' script"

mkdir -p "$ACME_SH/dnsapi"
cp "${SCRIPT_DIR}/../plesk-dns/acme_sh_dns_plesk.sh" "$ACME_SH/dnsapi/dns_plesk.sh"
cp -r "${SCRIPT_DIR}"/../plesk-dns/*.py "$ACME_SH/"

DOMAINS=

for i in $(seq -w 0 50); do
	DOMAINS="$DOMAINS -d cluster${i}.${SUB_DOMAIN_PART}.${BASE_DOMAIN}"
	DOMAINS="$DOMAINS -d *.cluster${i}.${SUB_DOMAIN_PART}.${BASE_DOMAIN}"
done

"$ACME_SH/acme.sh" $ACME_OPTS --issue $DOMAINS --dns dns_plesk
