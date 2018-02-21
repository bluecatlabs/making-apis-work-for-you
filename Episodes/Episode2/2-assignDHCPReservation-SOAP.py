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

from zeep import Client
from requests import Session
from zeep.transports import Transport
from getpass import getpass

#Parameters
BAMAddress="bam.lab.corp"
url="https://"+BAMAddress+"/Services/API?wsdl"
account="api"
account_password=getpass("Enter Password: ")

# get the HTTPS session verified
websession = Session()
# refer to certificate file path
websession.verify = "bam.crt"
webtransport=Transport(session=websession)
client = Client(url, transport=webtransport)

#login to api session
client.service.login(account,account_password)

# Add DHCP reservation for client
mac_address="BB:CC:AA:AA:AA:AA"
networkcidr="192.168.3.0/24"
hostname="appsrv22"
zonename="lab.corp"
viewname="default"
config_name="main"

# assignNextAvailableIP4Address
# get configuration information
configinfo = client.service.getEntityByName(0,config_name,"Configuration")
configurationId = configinfo.id

# get network information
networkinfo = client.service.getIPRangedByIP(configinfo.id,"IP4Network","192.168.3.1")
parentId = networkinfo.id

#macAddress information
macAddress=mac_address

#viewid information
viewinfo = client.service.getEntityByName(configinfo.id,viewname,"View")
#hostinfo
hostInfo = hostname+"."+zonename+","+str(viewinfo.id)+",true,false"

action = "MAKE_DHCP_RESERVED"
properties = "name="+hostname+"|locationCode=US DAL|"

assignaddress = client.service.assignNextAvailableIP4Address(configurationId,
                                                                parentId,
                                                                macAddress,
                                                                hostInfo,
                                                                action,
                                                                properties)
# logout of api session
client.service.logout()

print("ID: "+str(assignaddress.id))
print("Name: "+assignaddress.name)
print("Type: "+assignaddress.type)
print("Properties:")
for item in (assignaddress.properties).split("|"):
    print(item)
