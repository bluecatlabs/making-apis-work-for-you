#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Author: vivek Mistry @[Vivek M.]​
Date: 26-04-2018 07:01

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
import pandas as pd
import numpy as np
from jinja2 import Environment, FileSystemLoader
import datetime as dt
from weasyprint import HTML

reportName = "Printer List for Head Office"
reportfilename = reportName.replace(" ","_")+"_"+str(dt.datetime.now().strftime("%Y%m%d-%H%M%S"))

df = pd.read_csv("PrinterList.csv")
#print(df.head())
#print(df)
printer_report = pd.pivot_table(df,
                                index=["SubNet","PrinterModel"],
                                values=["PrinterName"],
                                aggfunc=[np.count_nonzero],
                                margins=True)

#print(printer_report)


# Import HTML Template using jinja2
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("report_template.html")

# Assign values to variables in report
template_vars = {"title" : reportName,
                "data_table": printer_report.to_html(),
                "currentdate":dt.datetime.now().strftime('%Y-%m-%d %H:%M')}

# get the html output from the template with the data
html_out = template.render(template_vars)
#print(html_out)
# create html report
with open(reportfilename+".html","w") as f:
    f.write(html_out)


# Generate pdf using weasyprint
HTML(string=html_out).write_pdf(reportfilename+".pdf")

#HTML(string=html_out).write_pdf(args.outfile.name, stylesheets=["style.css"])
