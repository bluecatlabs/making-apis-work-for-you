#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Author: vivek Mistry @[Vivek M.]​
Date: 26-04-2018 07:02

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
import logging, sys


# turn on logging
logging.basicConfig(filename="debug-soap.log",
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

# remove this if your are using python 3.x
#input = raw_input

# Parameters
BAMAddress="bam.lab.corp"
url="http://"+BAMAddress+"/Services/API?wsdl"
account = ""
try:
    account=input("Enter User Name: ")
    if account == "":
        raise ValueError("Error: No User Name was provided")
except Exception as e:
    print(e)
    logging.exception(e)
    sys.exit(1)
account_password=getpass("Enter Password: ")
hostrecordname = "test.lab.corp"

def gethostrecordwithhint(bam_url, login_user, login_password, host_record_name):
    """get the host record FQDN and return the entity details
    """
    records=""
    try:
        # api session
        client = Client(bam_url)
        # login
        client.service.login(login_user,login_password)
        # get the host record details
        records = client.service.getHostRecordsByHint(0,10,"hint="+host_record_name+"|")
        # logout of BAM
        client.service.logout()
    except zeep.exceptions.Fault as e:
        print(e.message)
        logging.exception(e)
        sys.exit(1)
    # return the records from function
    return records


def deletehostrecord(bam_url, login_user, login_password, host_record):
    """Delete host record
    """
    # api session
    client = Client(bam_url)

    # login
    client.service.login(login_user,login_password)
    # get the host record details
    print("You are requesting to delete:")
    print(host_record)
    answer = input("Do you want to proceed (y (yes) or n (no))? ")
    if answer.lower() == "y":
        deletion = client.service.deleteWithOptions(host_record['id'],
                                                "deleteOrphanedIPAddresses=true|")
    elif answer.lower() == "n":
        print("You requested deletion to be stopped")
    else:
        print("Invalid Entry")
    # logout of BAM
    client.service.logout()
    # return the records from function

hostrecords = gethostrecordwithhint(bam_url=url,
                                    login_user=account,
                                    login_password=account_password,
                                    host_record_name=hostrecordname)

print(hostrecords)
#deletehostrecord(url,account,account_password,hostrecords[0])
