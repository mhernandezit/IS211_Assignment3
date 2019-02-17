#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
""" Assignment 3 - Using RegEx to parse a CSV file """
from __future__ import division
from urllib2 import Request, urlopen, URLError, HTTPError
import csv
import re
import argparse
import sys
import logging
from pprint import pprint as pp

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='URL to lookup', default='http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv')
    args = parser.parse_args()
    try:
        csvdata = downloadData(args.url)
    except HTTPError as h:
        logger.error(h)
        sys.exit()
    except URLError:
        logger.error('Unable to retrieve CSV file')
        sys.exit()
    weblog = processData(csvdata)
    imageSearch(weblog)
    browserSearch(weblog)
    timeSearch(weblog)

def downloadData(url):
    """Download the CSV at the url provided, return a CSV reader object"""
    req = Request(url)
    response = urlopen(req)
    return csv.DictReader(response, fieldnames = ("filepath","datetime","browser","status","request_size"))

def processData(datafile):
    dict_list = []
    for line in datafile:
        dict_list.append(line)
    return dict_list

def imageSearch(datafile):
    images = 0
    for row in datafile:
        for k,v in row.items():
            if k == 'filepath':
                if re.search('\.(jpg|png|gif|jpeg)', v, re.IGNORECASE):
                    images += 1
    print('Image requests account for {}% of all requests').format(images/len(datafile)*100)

def browserSearch(datafile):
    browsers = {'firefox': 0, 'chrome': 0, 'ie': 0, 'safari': 0}
    for row in datafile:
        for k, v in row.items():
            if k == 'browser':
                if re.search('firefox', v , re.IGNORECASE):
                    browsers['firefox'] += 1
                if re.search('chrome', v, re.IGNORECASE):
                    browsers['chrome'] += 1
                if re.search('ie', v, re.IGNORECASE):
                    browsers['ie'] += 1
                if re.search('safari', v, re.IGNORECASE):
                    browsers['safari'] += 1
    print max(browsers, key=browsers.get)

def timeSearch(datafile):
    print "timesearch"

if __name__ == '__main__':
    logger = logging.getLogger('assignment3')
    logger.setLevel(logging.ERROR)
    try:
        logFile = logging.FileHandler('errors.log')
    except IOError:
        print "Unable to open log file"
    logFile.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logFile.setFormatter(formatter)
    logger.addHandler(logFile)
    main()