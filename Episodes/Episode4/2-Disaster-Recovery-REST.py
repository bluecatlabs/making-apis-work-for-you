#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Author: vivek Mistry @[Vivek M.]​
Date: 15-02-2018 09:32

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
import requests, json

#main variables
user = "api"
password = "pass"
bamurl = "bam.lab.corp"
mainurl = "http://"+bamurl+"/Services/REST/v1/"

configname = "main"
servername = "bdds1"
bdds1newip = "10.244.137.8"
bdds1netmask = "255.255.255.0"

"""
Actions that are needed to restore services
1. Disable Server
2. Replace Server
3. Deploy Service to Server
4. Verify
"""

# methods url
# Login method
# http://bam.lab.corp/Services/REST/v1/login?username=api&password=pass
loginurl = mainurl+"login?"
param = {"username":user,"password":password}

# getsysinfo method
getsysinfourl = mainurl+"getSystemInfo?"

# logout method
logouturl = mainurl+"logout?"

# replace server
replaceurl = mainurl+"replaceServer?"
replaceparams={
                "serverId":0,
                "name":servername,
                "defaultInterface":"",
                "hostName":servername+".lab.corp",
                "password":"bluecat",
                "upgrade":False,
                "properties":"resetServices=true"}
# update server
updateurl = mainurl+"update?"

# deploy method
deployurl = mainurl+"deployServer?"
deployparams = {"serverId":0}



# getEntityByName
getEntityByNameurl = mainurl+"getEntityByName?"
getEntityByNameparams = {
                            "parentId":0,
                            "name":configname,
                            "type":"Configuration"
                            }

# getEntities
getEntitiesurl = mainurl+"getEntities?"
getEntitiesparams = {
                        "parentId":0,
                        "type":"",
                        "start":0,
                        "count":10
                        }

# login to BAM
response = requests.get(loginurl, params=param)

# print login
#print(response)
#print(response.text)
#print(response.status_code)
#print(response.json())

# get the Token and put it into a variable
token = str(response.json())
token = token.split()[2]+" "+token.split()[3]
#print token
# set header value for the next methods
header={'Authorization':token,'Content-Type':'application/json'}

# get configuration
response = requests.get(
                        getEntityByNameurl,
                        params=getEntityByNameparams,
                        headers=header
                        )
configinfo = response.json()
print(configinfo)

serverparams = {
                    "parentId":configinfo['id'],
                    "name":servername,
                    "type":"Server"
                    }
# get Server bdds1
response = requests.get(
                        getEntityByNameurl,
                        params=serverparams,
                        headers=header
                        )
serverinfo = response.json()
print(serverinfo)
serverinfo['properties'] = serverinfo['properties'] + "connected=false|"

# disable bdds1
response = requests.put(
                        updateurl,
                        json=serverinfo,
                        headers=header
                        )
print(response.status_code)

getEntitiesparams['parentId'] = serverinfo['id']
getEntitiesparams['type'] = "NetworkServerInterface"
response = requests.get(
                        getEntitiesurl,
                        params=getEntitiesparams,
                        headers=header
                        )

# get default network interface of bdds1
getEntitiesparams['parentId'] = serverinfo['id']
getEntitiesparams['type'] = "NetworkServerInterface"
response = requests.get(
                        getEntitiesurl,
                        params=getEntitiesparams,
                        headers=header
                        )

bdds1interface = response.json()[0]

# replace server Parameters
replaceparams['serverId'] = serverinfo['id']
replaceparams['defaultInterface'] = bdds1interface['id']
servicesIPv4Address = "servicesIPv4Address="+bdds1newip+"|"
servicesIPv4Netmask = "servicesIPv4Netmask="+bdds1netmask+"|"
replaceparams['properties'] = replaceparams['properties']+servicesIPv4Address+servicesIPv4Netmask

response = requests.put(
                        replaceurl,
                        json=replaceparams,
                        headers=header
                        )
print(response.text)
deployparams['serverId'] = serverinfo['id']
reponse = requests.post(
                        deployurl,
                        params=deployparams,
                        headers=header
                        )
print(response.json())
import time
time.sleep(5)
# logout from BAM
response=requests.get(logouturl,headers=header)
print(response.json())
