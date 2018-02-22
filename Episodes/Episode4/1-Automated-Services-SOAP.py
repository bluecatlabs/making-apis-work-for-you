#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Automate Services using API
Author: vivek Mistry @[Vivek M.]​
Date: 15-02-2018 09:32


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
"""

from zeep import Client
from getpass import getpass

#Parameters
BAMAddress="bam.lab.corp"
url="http://"+BAMAddress+"/Services/API?wsdl"
account="api"
account_password=getpass("Enter Password: ")

"""Steps to create on Parent block 10.0.0.0/8
1. Create the next available /22 Block
2. Create the 2 next available /24 Networks
3. Create the 2 next available /25 Networks
4. Add 2 BDDS 20
5. Add DNS and DHCP roles to the network with the 2 BDDS
"""
configname="main"
viewname="default"
mainblock="10.0.0.0/8"
# process parameters customer will give
blockname = "ChrylerBuilding"
locationcode = "US MNH"
locationname = locationcode.replace(" ","")
bdds1name = "BDDS"+locationname+"1"
bdds2name = "BDDS"+locationname+"2"


#api session
client = Client(url)
#login to api session
client.service.login(account,account_password)
# Your api calls
# test connection with BAM
#sysinfo = client.service.getSystemInfo()
#print(sysinfo)
# get configuration information
configinfo = client.service.getEntityByName(0,configname,"Configuration")
# get main block information
mainblockinfo = client.service.getEntityByCIDR(configinfo.id,mainblock,"IP4Block")
# Get the first available /22 block and create it
block_22 = client.service.getNextAvailableIPRanges(
                        mainblockinfo.id,
                        1024,
                        "IP4Block",
                        1,
                        "reuseExsting=False|isLargerAllowed=False|autoCreate=False"
                            )
block_22 = client.service.getEntityById(block_22[0].id)
# Update the name and location code for block
block_22.name = blockname
block_22.properties = "locationInherited=false|locationCode="+locationcode+"|"
# send update to BAM
client.service.update(block_22)
# check if updated was completed
block_22 = client.service.getEntityById(block_22.id)

print(block_22)
# Get first 2 available /24 networks for wired and wireless devices
network_24 = client.service.getNextAvailableIPRanges(
                        block_22.id,
                        256,
                        "IP4Network",
                        2,
                        "reuseExsting=False|isLargerAllowed=False|autoCreate=False|"
                            )

print(network_24)
# update the names of the
network_24[0].name = locationname+"_Wired"
network_24[1].name = locationname+"_Wireless"

# send update to BAM
for network in network_24:
    client.service.update(network)


# verify the networks have the correct details
for network in network_24:
    print(client.service.getEntityById(network.id))
# Get first 2 available /25 networks for servers and IOT devices
network_25 = client.service.getNextAvailableIPRanges(
                        block_22.id,
                        128,
                        "IP4Network",
                        2,
                        "reuseExsting=False|isLargerAllowed=False|autoCreate=False|"
                            )
# update names
network_25[0].name = locationname+"_Servers"
network_25[1].name = locationname+"_IOT"

# send updates to BAM
for network in network_25:
    client.service.update(network)
# verify the changes
for network in network_25:
    print(client.service.getEntityById(network.id))


def getippart(ipentity):
    """
    Get the CIDR from network entity and return the first 3 octates
    """
    cidr = ""
    for prop in ipentity.properties.split("|"):
        if prop.startswith("CIDR"):
            cidr=prop.split("=")[1]
    iphead = cidr[:-4]
    return iphead

bdds1ip = getippart(network_25[0])+"11"
bdds2ip = getippart(network_25[0])+"12"
bddsprofile = "DNS_DHCP_SERVER_20"
bddsnetmask = "255.255.255.128"

# add servers
bdds1 = client.service.addServer(
                                    configinfo.id,
                                    bdds1name,
                                    bdds1ip,
                                    bdds1name+"lab.corp",
                                    bddsprofile,
                                    "connected=false|servicesIPv4Address="+bdds1ip+"|servicesIPv4Netmask="+bddsnetmask+"|locationCode="+locationcode+"|"
                                    )
bdds1 = client.service.getEntityById(bdds1)

bdds2 = client.service.addServer(
                                    configinfo.id,
                                    bdds2name,
                                    bdds2ip,
                                    bdds2name+"lab.corp",
                                    bddsprofile,
                                    "connected=false|servicesIPv4Address="+bdds2ip+"|servicesIPv4Netmask="+bddsnetmask+"|locationCode="+locationcode+"|"
                                    )
bdds2 = client.service.getEntityById(bdds2)

bdds1ipassign = client.service.assignIP4Address(
                                                configinfo.id,
                                                bdds1ip,
                                                "",
                                                "",
                                                "MAKE_STATIC",
                                                "name="+bdds1name+"|"
                                                )

bdds2ipassign = client.service.assignIP4Address(
                                                configinfo.id,
                                                bdds2ip,
                                                "",
                                                "",
                                                "MAKE_STATIC",
                                                "name="+bdds2name+"|"
                                                )

bdds1interface = client.service.getEntities(bdds1.id,
                                            "NetworkServerInterface",
                                            0,10)
bdds1interface = bdds1interface[0]

bdds2interface = client.service.getEntities(bdds2.id,
                                            "NetworkServerInterface",
                                            0,10)
bdds2interface = bdds2interface[0]

dhcprole = client.service.addDHCPDeploymentRole(
                                                block_22.id,
                                                bdds1interface.id,
                                                "MASTER",
                                                "secondaryServerInterfaceId="+str(bdds2interface.id)+"|"
                                                )
print(dhcprole)
#logout
client.service.logout()
