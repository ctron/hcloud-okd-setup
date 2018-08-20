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

import http.client

import requests
import logging

import ssl
import xmltodict
from collections import OrderedDict

logger = logging.getLogger("PleskApiClient")

class PleskApiClient:

    """A Plesk API Client"""

    host = ""
    port = 0
    user = ""
    password = ""
    site_name = ""
    site_id = ""

    def __init__(self, url, user, password, site_name):
        self.url = url
        self.user = user
        self.password = password
        self.site_name = site_name
        
        self.site_id = self.__find_site(self.site_name)

    def __fqdn(self, name):
        if name.endswith("."):
            return name
        else:
            return name + "." + self.site_name + "."

    def __localdn(self, name):
        suffix = "." + self.site_name + "."
        if name.endswith(suffix):
            return name[:-len(suffix)]
        else:
            return name

    def simple_request(self, type, operation, req):
        response = self.plesk_request({
            type: {
                operation: req
            }
        })[type][operation]
        
        result = response["result"]
        
        if isinstance(result, list):
            for r in result:
                if r["status"] == "error":
                    raise Exception("API returned at least one error: %s" % r["errtext"] )
        elif response["result"]["status"] == "error":
            raise Exception("API returned error: %s" % response["result"]["errtext"] )
        
        return response

    def plesk_request(self, request):

        headers = {}
        headers["Content-type"] = "text/xml"
        headers["HTTP_PRETTY_PRINT"] = "TRUE"
        headers["HTTP_AUTH_LOGIN"] = self.user
        headers["HTTP_AUTH_PASSWD"] = self.password

        xml = xmltodict.unparse({
                "packet": request
            }, pretty=True)
        # print ( "Request: %s" % xml )
        logger.debug ( "Request: %s", xml)

        r = requests.post(self.url + "/enterprise/control/agent.php", headers=headers, data=xml,  auth=(self.user, self.password))

        data = r.text

        logger.debug ( "Response: %s", data )
        result = xmltodict.parse(data )
        # print ( "Result: %s" % result )
        return result["packet"]
    
    def set_dns_record(self, type, host, value):
        self.dns_remove(type, host)
        self.dns_add(type, host, value)

    def dns_remove(self, type, host, value = None):
        entries = self.find_dns_entries ( type, self.__fqdn(host), value )
        self.delete_dns_records(entries)
        return entries

    def dns_add(self, type, host, value):
        
        entries = self.find_dns_entries(type, self.__fqdn(host), value)
        
        if entries:
            return True # already exists

        self.simple_request('dns','add_rec',OrderedDict([
            ('site-id', self.site_id),
            ('type', type),
            ('host', self.__localdn(host)),
            ('value', value)
        ]))
        
        return True

    def dns_list(self):
        
        result = self.simple_request('dns', 'get_rec', {
           'filter': {
                'site-id': self.site_id
            }
        })
        
        entries = []
        for r in result["result"]:

            entries.append(OrderedDict([
                ("type", r["data"]["type"]),
                ("host", r["data"]["host"]),
                ("value", r["data"]["value"]),
            ]))

        return entries

    def delete_dns_records(self, entries):
        if not entries:
            return

        req = []
        for i in entries:
            req.append({
                'del_rec': {
                    'filter': {
                        'id': i
                    }
                }
            })

        self.plesk_request({
            'dns': req
        })

    def __find_site(self, domain):
        return self.simple_request('site', 'get', OrderedDict([
            ('filter', {'name': domain}),
            ('dataset', {})
        ]))["result"]["id"]

    def find_dns_entries(self, type, host, value = None):
        logger.info("Searching for: %s, %s, %s" % (type, host, value) )
        result = self.simple_request('dns', 'get_rec', {
           'filter': {
                'site-id': self.site_id
            }
        })
        
        ids = []
        # print("Result: %s" % json.dumps(result, indent=4) )
        for r in result["result"]:
            #print ( "Value: " + str(value) )
            if r["data"]["type"] != type:
                continue
            
            if r["data"]["host"] != self.__fqdn(host):
                continue
            
            if value != None and r["data"]["value"] != value:
                continue
            
            ids.append(r["id"])
        
        return ids
