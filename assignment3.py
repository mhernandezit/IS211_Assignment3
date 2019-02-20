#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Assignment 3 - Using RegEx to parse a CSV file """
from __future__ import division # I don't want to do integer division for the % later on
from urllib2 import Request, urlopen, URLError, HTTPError
import csv
import re
import argparse
import sys
import logging
from datetime import datetime

TESTURL = 'http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv'

def main():
    """Main method - using a default --url argument """
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='URL to lookup', default=TESTURL)
    args = parser.parse_args()
    if args:
        csvdata = downloadData(args.url)
    else:
        LOGGER.error("No URL entered, please use the --url argument")
        sys.exit()
    weblog = processData(csvdata) # turn the csv into a dictionary
    imageSearch(weblog) # search the dictionary for images
    browserSearch(weblog) # search the dictionary for browsers
    timeSearch(weblog) # search the dictionary for entries by hour

def downloadData(url):
    """Download the CSV at the url provided, return a URLlib response object"""
    try:
        req = Request(url)
        response = urlopen(req)
    except HTTPError as error:
        LOGGER.error(error)
        sys.exit()
    except URLError:
        LOGGER.error('Unable to retrieve CSV file')
        sys.exit()
    return response

def processData(csvdata):
    """Build out a list of dictionaries from the csv object """
    fieldnames = ("filepath", "datetime", "browser", "status", "request_size")
    datafile = csv.DictReader(csvdata, fieldnames=fieldnames)
    dictList = []
    for line in datafile:
        dictList.append(line)
    return dictList

def imageSearch(datafile):
    """Searches values for extensions ending in jpg, png and gif, ignoring case """
    images = 0
    for row in datafile:
        for key, value in row.items():
            if key == 'filepath':
                if re.search('.(jpg|png|gif|jpeg)', value, re.IGNORECASE):
                    images += 1
    print("Image requests account for {}% of all requests").format(images/len(datafile)*100)

def browserSearch(datafile):
    """Searches datafile for Browsers in the text fields """
    browsers = {'Firefox': 0, 'Chrome': 0, 'Internet Explorer': 0, 'Safari': 0}
    for row in datafile:
        for key, value in row.items():
            if key == 'browser':
                if re.search('firefox', value, re.IGNORECASE):
                    browsers['Firefox'] += 1
                if re.search('chrome', value, re.IGNORECASE):
                    browsers['Chrome'] += 1
                if re.search('ie', value, re.IGNORECASE):
                    browsers['Internet Explorer'] += 1
                if re.search('safari', value, re.IGNORECASE):
                    browsers['Safari'] += 1
    print("The most popular browser of the day is {}.").format(max(browsers, key=browsers.get))

def timeSearch(datafile):
    """Builds a time dictionary that tracks hits based off of hours """
    activehours = {}
    for row in datafile:
        for key, value in row.items():
            if key == 'datetime':
                dFormat = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                if dFormat.hour in activehours:
                    activehours[dFormat.hour] += 1
                else:
                    activehours[dFormat.hour] = 1
    #Loop through 24 hours of the day, for any hours that return None, report 0
    for hour in xrange(0, 24):
        print("Hour {} has {} hits").format(hour, activehours.get(hour, 0))

if __name__ == '__main__':
    LOGGER = logging.getLogger('assignment3')
    LOGGER.setLevel(logging.ERROR)
    try:
        LOGFILE = logging.FileHandler('errors.log')
    except IOError:
        print "Unable to open log file"
    LOGFILE.setLevel(logging.DEBUG)
    FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    LOGFILE.setFormatter(FORMATTER)
    LOGGER.addHandler(LOGFILE)
    main()
