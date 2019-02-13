#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
""" Assignment 3 - Using RegEx to parse a CSV file """
import csv
import re
import argparse
import sys
from pprint import pprint as pp

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--url', help='URL to lookup', required=no, default='http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv')
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

def processData(datafile):
	logDict = {}
	return logDict

def imageSearch(datafile):
	pp("imageSearch placeholder")

def browserSearch(datafile):
	pp("browserSearch placeholder")

def timeSearch(datafile):
	pp("timeSearch placeholder")

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
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