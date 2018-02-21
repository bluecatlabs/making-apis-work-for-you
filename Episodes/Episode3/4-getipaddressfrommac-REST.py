#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Author: vivek Mistry @[Vivek M.]​
Date: 2017-11-06T22:21:31.880Z

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

# getLinkedEntities method
getLinkedEntitiesURL = mainurl+"getLinkedEntities?"
getLinkedEntitiesparam = {
                            "entityId":"",
                            "type":"",
                            "start":0,
                            "count":100
                            }


# login to BAM
response = requests.get(loginurl, params=param)

# get the Token and put it into a variable
token = str(response.json())
token = token.split()[2]+" "+token.split()[3]
#print token
# set header value for the next methods
header={'Authorization':token,'Content-Type':'application/json'}

# get information for macid=105739
macid=105739
getLinkedEntitiesparam["entityId"] = macid
getLinkedEntitiesparam["type"] = "IP4Address"

response=requests.get(
                        getLinkedEntitiesURL,
                        params=getLinkedEntitiesparam,
                        headers=header
                        )

print(response.json())

# Logout of BAM
response=requests.get(logouturl,headers=header)
print(response.json())
