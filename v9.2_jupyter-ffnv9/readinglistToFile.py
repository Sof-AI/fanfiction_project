#!/usr/bin/env python
"""
Author: original by alexwlchan, modified by Sofia Kobayashi
    see https://alexwlchan.net/2015/11/export-urls-from-safari-reading-list/
Date: 01/16/2022
Description: This script gets a list of all the URLs in Safari Reading List, 
    and writes them all to a file. Requires Python 3.
    Modified by Sofia Kobayashi to include date_added & date_last_viewed.
"""

import os
import plistlib
import json

from datetime import datetime
now = datetime.now()
current_date = now.strftime("%m-%d-%y")

INPUT_FILE  = os.path.join(os.environ['HOME'], 'Library/Safari/Bookmarks.plist')
OUTPUT_FILE = f"readinglist_{current_date}.json"

# Load and parse the Bookmarks file
with open(INPUT_FILE, 'rb') as plist_file:
    plist = plistlib.load(plist_file)

# Look for the child node which contains the Reading List data.
# There should only be one Reading List item
children = plist['Children']
for child in children:
    if child.get('Title', None) == 'com.apple.ReadingList':
        reading_list = child

# Extract the bookmarks
bookmarks = reading_list['Children']

# For each bookmark in the bookmark list, grab the URL, dateAdded & dateLastViewed
urls = []

for bookmark in bookmarks:
    temp = {}
    temp["url"] = bookmark["URLString"]
    temp["dateAdded"] = bookmark["ReadingList"]["DateAdded"].strftime("%m-%d-%y %H:%M:%S")
    temp["dateLastViewed"] = bookmark["ReadingList"].get("DateLastViewed")
    if temp["dateLastViewed"] != None: temp["dateLastViewed"] = temp["dateLastViewed"].strftime("%m-%d-%y %H:%M:%S")
    urls.append(temp)

# Write the URLs to a file
with open(OUTPUT_FILE, "w") as outfile:
    json.dump(urls, outfile)
