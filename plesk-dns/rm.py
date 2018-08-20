#!/usr/bin/python3

###############################################################################
# Copyright (c) 2018 Red Hat Inc
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
###############################################################################

import PleskApiClient

import sys
import os

SITE_NAME = sys.argv[1]
TYPE = sys.argv[2]
HOST = sys.argv[3]+"."
VALUE = sys.argv[4] if len(sys.argv) >= 5 else None

REMOTE_URL=os.environ["PLESK_URL"]
REMOTE_USER=os.environ["PLESK_USER"]
REMOTE_PASSWORD=os.environ["PLESK_PASSWORD"]

client = PleskApiClient.PleskApiClient(REMOTE_URL, REMOTE_USER, REMOTE_PASSWORD, SITE_NAME)

print ( "Site: %s" % client.site_id )
print ( "Deleting: %s/%s = %s" % (TYPE, HOST, VALUE))

entries = client.dns_remove(TYPE, HOST, VALUE)
print ( "Deleted: %s" % entries )
