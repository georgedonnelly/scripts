#!/usr/bin/env python

# Simple script to download images and other attachments from your AirTable table
# using the AirTable API and the pyairtable library.

import os
from pyairtable import Table
# enable below if want to use formulas to search (match)
#from pyairtable.formulas import match
import urllib.request
import time

# set variables
os.environ.setdefault('AIRTABLE_API_KEY', 'xxxxxxxxxx')
os.environ.setdefault('ONBOARDING_BASE', 'yyyyyyyyyy')
os.environ.setdefault('PEOPLE_TABLE', 'zzzzzzzzzzz')

# get variables
api_key = os.environ['AIRTABLE_API_KEY']
base = os.environ['ONBOARDING_BASE']
people_table = os.environ['PEOPLE_TABLE']

# table object
table = Table(api_key, base, people_table)

# use formula if you want to search, then add 'formula=formula' as an argument to table.iterate()
#formula = match({"Identifier": "215"})
# records is a list
for records in table.iterate():
    # iterating over the list to get the fields element
    for object in records:
        # fields is a dict
        fields = object.get('fields')
        # wallet_photo is a list
        # change 'Wallet Photo' to the name of your AirTable field
        wallet_photo = fields['Wallet Photo']
        for file in wallet_photo:
            url = file.get('url')
            file_name = file.get('filename')
            # download the file and save as filename
            # maybe use requests library instead of urllib (which is deprecated in python3)
            file = urllib.request.FancyURLopener()
            file.retrieve(url, 'img/' + file_name)
            # don't overload the API
            time.sleep(1)
