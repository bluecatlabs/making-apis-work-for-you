#!/usr/bin/python2
# -*- coding: utf-8 -*-
'''
Author: vivek Mistry @[Vivek M.]​
Date: 2017-10-23T18:44:38.677Z

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

# Parameters
account="api"
account_password="pass"
bamurl = "bam.lab.corp"
mainurl = "http://"+bamurl+"/Services/REST/v1/"

# Server information
ipaddress='192.168.0.16'
hostname='FINRPT02'
alias='reporting2'
zone='lab.corp'

# additional info known
config_name='main'
view_name='default'

# Login method
loginurl = mainurl+"login?username="+account+"&password="+account_password
# getsysinfo method
getsysinfourl = mainurl+"getSystemInfo?"
# logout method
logouturl = mainurl+"logout?"
# getEntityByName method
e_parentId=0
e_name=""
e_type=""
getEntityByName = mainurl+"getEntityByName?parentId="+ str(e_parentId) \
                        +"&name="+e_name+"&type="+e_type
# getEntityById
e_id=0
getEntityById = mainurl+"getEntityById?id="+str(e_id)
# addHostRecord
r_viewId = 0
r_absoluteName=""
r_addresses = ""
r_ttl=""
r_properties=""
addHostRecord = mainurl+"addHostRecord?viewId="+str(r_viewId)+"&absoluteName=" \
                +r_absoluteName+"&addresses="+r_addresses+ \
                "&ttl="+r_ttl+"&properties="+r_properties
# addAliasRecord
r_linkedRecordName=""
addAliasRecord = mainurl+"addAliasRecord?viewId="+str(r_viewId)+"&absoluteName=" \
                    +r_absoluteName+"&linkedRecordName="+r_linkedRecordName+ \
                    "&ttl="+r_ttl+"&properties="+r_properties

# login to BAM
response = requests.get(loginurl)
# get the Token and put it into a variable
token = str(response.json())
token = token.split()[2]+" "+token.split()[3]
# set header value for the next methods
header={'Authorization':token,'Content-Type':'application/json'}

# api calls
# configuration information
#config_info = client.service.getEntityByName(0,config_name,'Configuration')
#print(config_info)
# set Parametere to get configuration
e_name='main'
e_type="Configuration"
getEntityByName = mainurl+"getEntityByName?parentId="+ str(e_parentId) \
                        +"&name="+e_name+"&type="+e_type
# run the api call
response = requests.get(getEntityByName,headers=header)
config_info = response.json()
print("-------config------")
print(config_info)
print("------config['id']-------")
print(config_info['id'])
print("-------------")
# view information
e_name='default'
e_type='View'
e_parentId = config_info['id']
getEntityByName = mainurl+"getEntityByName?parentId="+ str(e_parentId) \
                        +"&name="+e_name+"&type="+e_type

# run the api call
response = requests.get(getEntityByName,headers=header)
view_info = response.json()
print("------view-------")
print(view_info)
print("-------------")
# addhost record
r_viewId = view_info['id']
r_absoluteName= hostname+"."+zone
r_addresses = ipaddress
r_ttl="-1"
r_properties="reverseRecord=true"
addHostRecord = mainurl+"addHostRecord?viewId="+str(r_viewId)+"&absoluteName=" \
                +r_absoluteName+"&addresses="+r_addresses+ \
                "&ttl="+r_ttl+"&properties="+r_properties

# run the api call to addhostrecord
response = requests.post(addHostRecord,headers=header)
hostinfo = response.text
print("-------------")
print("Record ID Created:"+str(hostinfo))
print("-------------")
# get hostinformation
e_id=hostinfo
getEntityById = mainurl+"getEntityById?id="+str(e_id)

# api call
response = requests.get(getEntityById,headers=header)
hostinfo = response.json()
print("------full host info-------")
print(hostinfo)
print("-------------")

# add alias record link to the record created
r_absoluteName=alias+"."+zone
r_properties=""
r_linkedRecordName=hostname+"."+zone
addAliasRecord = mainurl+"addAliasRecord?viewId="+str(r_viewId)+"&absoluteName=" \
                    +r_absoluteName+"&linkedRecordName="+r_linkedRecordName+ \
                    "&ttl="+r_ttl+"&properties="+r_properties

# run the api call to addaliasrecord
response = requests.post(addAliasRecord,headers=header)
aliasinfo = response.text
print("-------------")
print("Record ID Created:"+str(aliasinfo))
print("-------------")

# get alias record information
e_id=aliasinfo
getEntityById = mainurl+"getEntityById?id="+str(e_id)
response = requests.get(getEntityById,headers=header)
aliasinfo = response.text
print("------alias record-------")
print(aliasinfo)
print("-------------")


# logout from BAM
response=requests.get(logouturl,headers=header)
print(response.json())
