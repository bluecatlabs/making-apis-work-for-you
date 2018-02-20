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

from zeep import Client
import getpass

#Parameters
BAMAddress="10.244.137.5"
url="http://"+BAMAddress+"/Services/API?wsdl"
account="api"
account_password=getpass.getpass("Enter Password: ")

searchTerm="appsrv"

#api session
client = Client(url)

#login to api session
client.service.login(account,account_password)

#APi calls
searchresults = client.service.searchByObjectTypes(searchTerm,"HostRecord", \
                                                    0, 100)

print(searchresults)
"""for items in searchresults:
    if "GATEWAY" in items.properties:
        print items"""

searchresults = client.service.searchByCategory("F*1","RESOURCE_RECORD",0,50)
for items in searchresults:
    print(items.name + " " +items.type)


# logout of api session
client.service.logout()
