#!/usr/bin/python2
# -*- coding: utf-8 -*-
'''
Author: vivek Mistry @[Vivek M.]​
Date: 2017-10-23T17:31:56.063Z

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

from suds.client import Client

# login parameters
BAMAddress="bam.lab.corp"
url="http://"+BAMAddress+"/Services/API?wsdl"
account="api"
account_password="pass"

# Server information
ipaddress='192.168.0.15'
hostname='FINRPT01'
alias='reporting'
zone='lab.corp'

# additional info known
config_name='main'
view_name='default'



# api session
client = Client(url)

# login to api session
client.service.login(account,account_password)

# api calls
# configuration information
config_info = client.service.getEntityByName(0,config_name,'Configuration')
#print(config_info)

# view information
view_info = client.service.getEntityByName(config_info.id,view_name,'View')
#print(view_info)

# addhost record
hostrecordname = hostname +"."+ zone
record = client.service.addHostRecord(view_info.id,hostrecordname,ipaddress, \
                                        -1,"reverseRecord=true|")
print("Record ID Created:"+str(record))
print("--------")
showrecord = client.service.getEntityById(record)
print(showrecord)

# add alias record link to the record created on line 49
aliasrecordname = alias+"."+zone
aliasrecord = client.service.addAliasRecord(view_info.id,aliasrecordname, \
                                               hostrecordname,-1,"" )
print("--------")
print("Record ID Created:"+str(aliasrecord))
print("--------")
showrecord = client.service.getEntityById(aliasrecord)
print(showrecord)

#logout of api session
client.service.logout()
