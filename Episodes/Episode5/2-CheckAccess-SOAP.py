#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Author: vivek Mistry @[Vivek M.]​
Date: 2017-10-11T20:28:17.096Z

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
from getpass import getpass

input = raw_input

BAMAddress="bam.lab.corp"
url="http://"+BAMAddress+"/Services/API?wsdl"
account=input("Enter Your User ID: ")
account_password=getpass("Enter Password: ")
username = "blue"
hostrecordname = "oldtest.lab.corp"

def getuser(bam_url,login_user,login_password,user_name):
    """Get the User details
    """
    # api session
    client = Client(bam_url)
    # login
    client.service.login(login_user,login_password)
    # get User
    user = client.service.getEntityByName(0,user_name,"User")
    # logout
    client.service.logout()

    return user

def gethostrecordwithhint(bam_url, login_user, login_password, host_record_name):
    """get the host record FQDN and return the entity details
    """
    # api session
    client = Client(bam_url)
    # login
    client.service.login(login_user,login_password)
    # get the host record details
    records = client.service.getHostRecordsByHint(0,10,"hint="+host_record_name+"|")
    # logout of BAM
    client.service.logout()
    # return the records from function
    return records

def getAccessRightbyuseronentity(bam_url, login_user, login_password, user_id, entity_id):
    """get the access rights for a user from getAccessRights api call
    """
    # api session
    client = Client(bam_url)

    # login
    client.service.login(login_user,login_password)
    # get the host record details
    accessrights = client.service.getAccessRight(entity_id,user_id)
    # logout of BAM
    client.service.logout()
    # return the records from function
    return accessrights


userinfo = getuser(url,account,account_password,username)
entityinfo = gethostrecordwithhint(url,account,account_password,hostrecordname)
accessrights = getAccessRightbyuseronentity(url,account,account_password,userinfo['id'],entityinfo[0]['id'])
print(accessrights)
