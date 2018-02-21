#!/usr/bin/python
# -*- coding: utf-8 -*-
'''2-assignDHCPReservation-SOAP
Author: vivek Mistry @[Vivek M.]​
Date: 2017-11-22T16:25:09.525Z

Disclaimer:
All information, documentation, and code is provided to you AS-IS and should
only be used in an internal, non-production laboratory environment.

License:
Copyright 2017 BlueCat Networks, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import requests, json, getpass

#main variables
user = "api"
password = getpass.getpass("Enter password: ")
bamurl = "bam.lab.corp"
mainurl = "https://"+bamurl+"/Services/REST/v1/"
bamcert = "bam.crt"

# Add DHCP reservation for client
mac_address="BB:CC:DD:AA:AA:AA"
networkcidr="192.168.3.0/24"
hostname="appsrv23"
zonename="lab.corp"
viewname="default"
config_name="main"

# Login
loginurl = mainurl+"login?"
loginparam = {"username":account,"password":account_password}

# logout method
logouturl = mainurl+"logout?"

# getEntityByName
getEntityByNameurl = mainurl+"getEntityByName?"
getEntityByNameparams = {
                            "parentId":"0",
                            "name":config_name,
                            "type":"Configuration"
                        }

# getIPRangedByIP
getIPRangedByIPurl = mainurl+"getIPRangedByIP?"
getIPRangedByIPparams = {
                            "containerId":"0",
                            "type":"IP4Network",
                            "address":"192.168.3.1"
                        }

# assignNextAvailableIP4Address
assignNextAvailableIP4Addressurl = mainurl+"assignNextAvailableIP4Address?"
assignNextAvailableIP4Addressparams = {
                                        "configurationId":"0",
                                        "parentId":"0",
                                        "macAddress":mac_address,
                                        "hostInfo":"",
                                        "action":"MAKE_DHCP_RESERVED",
                                        "properties":"name="+hostname+"|locationCode=US DAL|"
                                        }

# login to BAM
response = requests.get(loginurl, params=loginparam, verify=bamcert)
# process the token
token = str(response.json())
token = token.split()[2]+" "+token.split()[3]
# set header value for the next methods
header={'Authorization':token,'Content-Type':'application/json'}
# configuration information
response = requests.get(
                            getEntityByNameurl,
                            params=getEntityByNameparams,
                            headers=header,
                            verify=bamcert
                            )
configinfo = response.json()
# set the valie of containerId for getIPRangedByIPparams to config id
getIPRangedByIPparams["containerId"] = configinfo['id']
# IPv4 Network information
response = requests.get(
                            getIPRangedByIPurl,
                            params=getIPRangedByIPparams,
                            headers=header,
                            verify=bamcert
                            )
networkinfo = response.json()

# view information
getEntityByNameparams["parentId"] = configinfo['id']
getEntityByNameparams["name"] = viewname
getEntityByNameparams["type"] = "View"

response = requests.get(
                        getEntityByNameurl,
                        params=getEntityByNameparams,
                        headers=header,
                        verify=bamcert
                        )
viewinfo = response.json()

# assignNextAvailableIP4Address
hostInfo = hostname+"."+zonename+","+str(viewinfo['id'])+",true,false"
assignNextAvailableIP4Addressparams['hostInfo'] = hostInfo
assignNextAvailableIP4Addressparams['parentId'] = networkinfo['id']
assignNextAvailableIP4Addressparams['configurationId'] = configinfo['id']

response = requests.post(
                            assignNextAvailableIP4Addressurl,
                            params=assignNextAvailableIP4Addressparams,
                            headers=header,
                            verify=bamcert
                            )
print(response.json())

# logout of api session
response = requests.get(logouturl,headers=header,verify=bamcert)
print(response.json())
