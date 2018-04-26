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
import requests, logging
from getpass import getpass
import sys

logging.basicConfig(filename="warning-rest.log",
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


def get(bam_url, api_call, call_parameters, header):
    """requests get call that returns the json data"""

    call_url = "http://"+bam_url+"/Services/REST/v1/"+api_call+"?"
    try:
        if call_parameters == "":
            response = requests.get(call_url, headers=header)
        else:
            response = requests.get(call_url, params=call_parameters, headers=header)

        #print(response.text)
        if response.status_code != 200:
            raise requests.ConnectionError("Code "+str(response.status_code)+" "+response.json())

    except requests.exceptions.RequestException as e:
        print(e)
        logging.exception(e)
        sys.exit(1)

    return response.json()

def deletecall(bam_url,api_call,call_parameters,delete_entity,header):
    """API request to delete and return values"""
    call_url = "http://"+bam_url+"/Services/REST/v1/"+api_call+"?"
    print("You are requesting to delete:")
    print(delete_entity)
    answer = input("Do you want to proceed (y (yes) or n (no))? ")
    try:
        if answer.lower() == "y":
            response = requests.delete(call_url,params=call_parameters, headers=header)
            return response.json()
        elif answer.lower() == "n":
            return "You aborted deletion"
        else:
            return "You entered an invalid character"
    except requests.exceptions.RequestException as e:
        print(e)


def update_header(login_response, call_header):
    """Function to process and update the header after login"""

    token = str(login_response).split()[2] + " " + str(login_response).split()[3]
    call_header['Authorization'] = token
    return call_header

#input = raw_input

user = input("Enter Your User ID: ")
password = getpass("Enter Password: ")
bamurl = "bam.lab.corp"
header = {'Content-Type': 'application/json'}

# Login parameters
login_param = {"username": user, "password": password}

# login to BAM
login = get(bamurl, "login", login_param, header)

# update header with login token
header = update_header(login, header)

# get BAM System info
"""sys_info = get(bamurl, "getSystemInfo", "", header)
for item in sys_info.split("|"):
    print(item)"""

# get servers
configid = 100957
getserverparams = {
                    'parentId': configid,
                    'type':'Server',
                    'start':0,
                    'count':100
                    }
serverslist = get(bamurl,"getEntities", getserverparams, header)
# need to transform all properties to a new list that can be used for reporting
reformattedlist = []

# get every server from list
for server in serverslist:
    # get properties for each server
    propertieslist = list(server['properties'].split("|"))
    # create empty dictionary for server properties
    propertiesdic = {}
    for item in propertieslist:
        if item is not '':
            # only show none blank properties
            # create a temp blank list
            shortlist=[]
            # take the propertie is split it into the temp list
            shortlist = list(item.split("="))
            # append the property dictionary with property from temp list
            propertiesdic[shortlist[0]] = shortlist[1]
        else:
            break
    # update the server dictionary with new properties
    server.update(propertiesdic)
    #print(server)

    # remove the properties key
    del server['properties']
    #print(server)

    # append the reformatted list with the updated dictionary
    reformattedlist.append(server)

# print the reformatted list that show properties of every entity as dictionary
print(reformattedlist)

# logout
logout = get(bamurl, "logout", "", header)
print(logout)
