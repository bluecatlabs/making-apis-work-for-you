#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Author: vivek Mistry @[Vivek M.]​
Date: 24-01-2018 09:17

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
import requests, json, getpass, csv, os

#main variables
user = "api"
password = getpass.getpass("Enter Password: ")
bamurl = "bam.lab.corp"
mainurl = "https://"+bamurl+"/Services/REST/v1/"
bamcert = "bam.crt"
s = requests.Session()
s.verify = bamcert
# methods url
# Login method
# http://bam.lab.corp/Services/REST/v1/login?username=api&password=pass
loginurl = mainurl+"login?"
param = {"username":user,"password":password}

# getsysinfo method
getsysinfourl = mainurl+"getSystemInfo?"

# logout method
logouturl = mainurl+"logout?"

#config Parameters for getEntityByName
getentitybynameurl = mainurl+"getEntityByName?"
getEntityByNameParams = {
                            "parentid":"",
                            "name":"main",
                            "type":"Configuration"
                            }

# getIPRangedByIP Parameters
getIPRangedByIPURL = mainurl+"getIPRangedByIP?"
getIPRangedByIPparams = {
                            "containerId":0,
                            "type":"IP4Network",
                            "address":"192.168.2.1"
                            }

# getEntities Parameters
getEntitiesurl = mainurl+"getEntities?"
getEntitiesparams = {
                        "parentId":0,
                        "type":"IP4Address",
                        "start":0,
                        "count":250
                        }

# login to BAM
response = requests.get(loginurl, params=param)

# get the Token and put it into a variable
token = str(response.json())
token = token.split()[2]+" "+token.split()[3]
#print token
# set header value for the next methods
header={'Authorization':token,'Content-Type':'application/json'}

# you api calls

response = requests.get(getentitybynameurl,
                        params=getEntityByNameParams,
                        headers=header)
config = response.json()
getIPRangedByIPparams['containerId'] = config['id']

response = requests.get(getIPRangedByIPURL,
                        params=getIPRangedByIPparams,
                        headers=header)
londonnetwork = response.json()
getEntitiesparams['parentId'] = londonnetwork['id']

response = requests.get(getEntitiesurl,
                        params=getEntitiesparams,
                        headers=header)
iplist = response.json()
print(iplist)
# Logout of BAM
response=requests.get(logouturl,headers=header)
print(response.json())

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


def searchReserved(listofips):
    """Search for iplist and return only DHCP_RESERVED addresses
    """
    searchlist=[]
    for address in listofips:
        if address["name"] == None:
            address["name"]  = ""

        ipitem = [address['id'],address['type'],address['name']]

        addressprops=""
        for aprop in address['properties'].split("|"):
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
    csvfile = "londoniplist.csv"
    header = ["ID","Type","Name","IP4Address","IPState","MACAddress"]
    IP4Addresslist.insert(0,header)
    with open(csvfile,'wb') as outfile:
        wr = csv.writer(outfile, delimiter=',',quoting=csv.QUOTE_ALL)
        wr.writerows(IP4Addresslist)
    print("see file londoniplist.csv in "+os.getcwd())

def printlist(IP4Addresslist):
    '''
    print the list of ip address
    '''
    print("ID,Type,Name,IP4Address,IPState,MACAddress")
    for item in IP4Addresslist:
        print(item)

filterediplist = searchReserved(iplist)
exportToCSV(filterediplist)
printlist(filterediplist)
