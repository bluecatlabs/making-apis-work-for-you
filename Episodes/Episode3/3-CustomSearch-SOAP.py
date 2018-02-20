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
from zeep import Client
from zeep import xsd
import getpass, os

#Parameters
BAMAddress="bam.lab.corp"
url="http://"+BAMAddress+"/Services/API?wsdl"
account="api"
account_password=getpass.getpass("Enter Password: ")

#api session
client = Client(url)

#login to api session
client.service.login(account,account_password)

"""SearchTerm: XEROX
UDF: printerModel"""
"""
Before starting to make the api call we first to define String array
in for the filters and options.
Since Options will be left blank we will just put 2 doublequotes.
For filters we need to first with zeep identify the type of entity,
which in this case is a stringArray. After inspecting the WSDL using
the command
python -m zeep http://bam.lab.corp/Services/API?wsdl

I found the value for customSearch to be
customSearch(filters: ns0:stringArray, type: xsd:string,
options: ns0:stringArray, start: xsd:int, count: xsd:int
) -> return: ns1:APIEntityArray

using get_type function on zeep client library we define it as below
"""
stringArrayType = client.get_type('ns0:stringArray')

#assign the variable filters the stringArrayType
filters = stringArrayType()
# append value list of the dictory for the key item
filters['item'].append("printerModel=XEROX")

# enter the parameters for customSearch and search
searchresults = client.service.customSearch(
                                            filters,
                                            "MACAddress",
                                            "",
                                            0,
                                            100)
for items in searchresults:
    print(items['properties'])

"""printer Serial# MHB8923049
UDF: serialNumber"""
# create filter for printer serial number result stringArrayType
printer_Serial = stringArrayType()

# assign value same as prior example
printer_Serial['item'].append("serialNumber=MHB8923049")

searchresults = client.service.customSearch(
                                            printer_Serial,
                                            "MACAddress",
                                            "",
                                            0,
                                            100)
print(searchresults)

#logout of API session
client.service.logout()
