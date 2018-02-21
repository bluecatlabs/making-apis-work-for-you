#!/usr/bin/python2
# -*- coding: utf-8 -*-
'''
Author: vivek Mistry @[Vivek M.]​
Date: 2017-10-24T16:18:27.003Z

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
import csv, sys
from suds.client import Client
from suds import WebFault

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
#api session
client = Client(url)

def getRecords(csvfile):
    '''
    read a file with a list of ids
    '''
    with open(csvfile, 'rb') as f:
        reader = f.readlines()

    your_list = [x.strip() for x in reader]
    return tuple(your_list)

def check_arguments():
    '''
    returns the numnber of arguments
    '''
    return len(sys.argv)

def deletion(entityid, delete_options):
    '''
    run the api call to delete the entity with options below
    noServerUpdate=[true/false]
    deleteOrphanedIPAddresses=[true/false]
    '''
    delete = client.service.deleteWithOptions(entityid,delete_options)
    return delete

def main():
    '''
    main method that executes
    '''
    idlist=getRecords(sys.argv[1])
    print idlist

    #login to api session
    client.service.login(account,account_password)

    #deletion tracking list
    deletedList=[]
    #deletion
    for id_num in idlist:
        deleteOptions='deleteOrphanedIPAddresses=true|'
        if id_num != "" or id_num != None:
            try:
                deleted=""
                deleted = deletion(id_num,deleteOptions)
            except WebFault as errormessage:
                print errormessage.fault.faultstring
            except UnboundLocalError as arguments:
                print("--")
        else:
            print("skipped blank")
        deletedList.append(deleted)

    # logout of api session
    client.service.logout()
    for items in deletedList:
        print items


if __name__ == "__main__":
    if check_arguments() == 2:
        main()
    else:
        print('''Please Enter parameter with the csvfile
        bulk-delete.py "filename.csv"''')
