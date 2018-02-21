#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Author: vivek Mistry @[Vivek M.]​
Date: 2017-11-06T10:06:52.002-05:00

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
from getpass import getpass
from requests import Session
from zeep.transports import Transport
from zeep import Client
import csv, os

#Parameters
BAMAddress="bam.lab.corp"
url="https://"+BAMAddress+"/Services/API?wsdl"
account="api"
account_password=getpass("Enter Password: ")

def printEntity(apientity):
    '''
    takes a entity got by prints it easy to read with properties
    '''
    for key in apientity:
        if key == 'properties':
            if apientity['properties'] != None:
                print(key)
                for props in apientity[key].split("|"):
                    print(props)
            else:
                print(key+": None")

        else:
            print(key+"="+str(apientity[key]))


# get the HTTPS session verified
websession = Session()
# refer to certificate file path
websession.verify = "bam.crt"
webtransport=Transport(session=websession)
client = Client(url, transport=webtransport)

#login to api session
client.service.login(account,account_password)

#APi calls
# The networks we are looking at is 192.168.0.0/24
# let get the details of that network first.
config = client.service.getEntityByName(0,"main","Configuration")
torontoNetwork = client.service.getIPRangedByIP(config.id, "IP4Network", \
                                                "192.168.0.1")

listofIP = client.service.getEntities(torontoNetwork.id, "IP4Address",0,250)

# logout of api session
client.service.logout()

'''for address in listofIP:
    print("--------------------")
    printEntity(address)
    print("--------------------")'''

def searchReserved(listofips):
    searchlist=[]
    for address in listofips:
        if address.name == None:
            address.name = ""

        ipitem = [address.id,address.type,address.name]

        addressprops=""
        for aprop in address.properties.split("|"):
            proplist = aprop.split("=")
            if len(proplist) > 1:
                ipitem.append(proplist[1])

        del ipitem[5]

        if "DHCP_RESERVED" in ipitem:
            searchlist.append(ipitem)
    return searchlist

def exportToCSV(IP4Addresslist):
    '''
    Export list of ip addresses to CSV file named iplist.CSV
    '''
    csvfile = "iplist.csv"
    header = ["ID","Type","Name","IP4Address","IPState","MACAddress"]
    IP4Addresslist.insert(0,header)
    with open(csvfile,'wb') as outfile:
        wr = csv.writer(outfile, delimiter=',',quoting=csv.QUOTE_ALL)
        wr.writerows(IP4Addresslist)
    print("see file iplist.csv in "+os.getcwd())

def printlist(IP4Addresslist):
    '''
    print the list of ip address
    '''
    print("ID,Type,Name,IP4Address,IPState,MACAddress")
    for item in searchReserved(listofIP):
        print(item)

printlist(listofIP)
exportToCSV(searchReserved(listofIP))
