#!/bin/bash
# Author: vivek Mistry @[Vivek M.]​
# Date: 2017-10-11T20:28:17.096Z
#
# Disclaimer:
# All information, documentation, and code is provided to you AS-IS and should
# only be used in an internal, non-production laboratory environment.
#
# License:
# Copyright 2017 BlueCat Networks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
curl -request GET \
  --url 'http://bam.lab.corp/Services/REST/v1/getSystemInfo?' \
  --header 'Authorization : "BAMAuthToken: 9g4fEMTUwODMzMTc5MzE0NTphcGk="' \
  --header 'content-type:  application/json'
