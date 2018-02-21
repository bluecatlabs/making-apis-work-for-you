#!/usr/bin/python2
# -*- coding: utf-8 -*-
'''
Author: vivek Mistry @[Vivek M.]​
Date: 2017-10-24T15:58:20.851Z

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
import csv
from suds.client import Client

#Parameters
BAMAddress="bam.lab.corp"
# we are using unsecure http example, for secure https connection with BAM see
# episode 2 on how to verify SSL connection.
# see link
url="http://"+BAMAddress+"/Services/API?wsdl"
account="api"
# saving passwords in scripts is unsecure see episode 2 on how to secure your
# passwords. see link
account_password="pass"

# known info
printerList="PrinterList.csv"
config_name='main'
view_name='default'
zone_name='lab.corp'

def getRecords(csvfile):
    '''
    Get a csv file and convert it to a list in python
    Format of the file would follows
    ip,hostname
    '''
    with open(csvfile, 'rb') as f:
        reader = csv.reader(f)
        your_list = map(tuple, reader)

    return tuple(your_list)

printertuple = getRecords(csvfile=printerList)

#api session
client = Client(url)

#login to api session
client.service.login(account,account_password)

#APi calls
#set a list to track added hostrecords in a list
addedlist = []
# get the config information to get the view information
configinfo = client.service.getEntityByName(0,'main','Configuration')

# get the view information to
viewinfo = client.service.getEntityByName(configinfo.id,'default','View')

# add the records in BAM now
for item in printertuple:
    # get item on the 2nd column in csv file
    # with the hostname and append with zone
    absoluteName=item[1]+"."+zone_name
    # get ip from the 1st column from the csv file
    addresses=str(item[0])
    # set ttl to default ttl
    ttl=-1
    # allow PTR record to be created for the records in the properties
    properties="reverseRecord=true|"
    # send the api call the BAM
    addedrecord = client.service.addHostRecord(viewinfo.id, absoluteName, \
                                                addresses, ttl, properties)

    # append the list with added record information
    addedlist.append(addedrecord)

for a in addedlist:
    print a

# logout of api session
client.service.logout()
