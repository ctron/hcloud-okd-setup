#!/usr/bin/env sh

#
# acme.sh DNS API script
#
# Copy this file to ~/.acme.sh/dnsapi as 'dns_plesk.sh'
#

#
# PLESK_URL = Plesk server URL
# PLESK_USER = user name
# PLESK_PASSWORD = password
# BASE_DOMAIN = domain name
#

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

dns_plesk_add() {
	fulldomain=$1
	txtvalue=$2

	"$SCRIPT_DIR/add.py" "$BASE_DOMAIN" "TXT" "$fulldomain" "$txtvalue"
}

dns_plesk_rm() {
	fulldomain=$1
	txtvalue=$2

	"$SCRIPT_DIR/rm.py" "$BASE_DOMAIN" "TXT" "$fulldomain" "$txtvalue"
}