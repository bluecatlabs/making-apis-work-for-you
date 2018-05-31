#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Author: vivek Mistry @[Vivek M.]​
Date: 31-05-2018 10:25

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
import zeep
from getpass import getpass
import sys
from time import sleep

# remove this if your are using python 3.x
# input = raw_input

# Parameters
BAMAddress = "bam.lab.corp"
url = "http://"+BAMAddress+"/Services/API?wsdl"
account = "api"
account_password = getpass("Enter Password: ")
hostrecordname = {"fqdn":"test.lab.corp", "newip":"192.168.0.11"}

client = Client(url)
client.service.login(account, account_password)

record = client.service.getEntityByName(105021, "test", "HostRecord")
print(record)

record["properties"] = "absoluteName=test.lab.corp|addresses={}|reverseRecord=true|".format(hostrecordname['newip'])
print(record)

client.service.update(record)

longArrayType = client.get_type('ns0:longArray')
records = longArrayType()
# print(records)

records['item'].append(record["id"])
# print(records)

deploymenttoken = client.service.selectiveDeploy(records, "scope=related")

print(deploymenttoken)

count = range(5)
for i in count:
    status = client.service.getDeploymentTaskStatus(deploymenttoken)
    print(status)
    sleep(1)

client.service.logout()
