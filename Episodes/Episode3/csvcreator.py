#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Author: vivek Mistry @[Vivek M.]​
Date: 15-01-2018 09:49

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

import csv, os

def csvwriter(filename, datalist):
    """csvwriter function to take a list and write it to CSV
    Parameters
    filename : Name of the file it you will create for CSV
    datalist : Python list that has the data for the CSV file
    """
    with open (filename, 'wb') as f:
        wr = csv.writer(f, delimiter=",", quoting=csv.QUOTE_ALL)
        wr.writerow(datalist)
        print("see file "+filename+" in "+os.getcwd())

def appendheader (datalist, header):
    """appendheader function to add a header to datalist python list for CSV
    Parameters
    datalist : Python list that has data for the CSV file
    header : Python list with the header for the datalist entities
    """
    datalist.insert(0,header)
    return datalist
