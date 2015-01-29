#!/usr/bin/python
#coding: utf-8
from Log import *
import urllib
import socket
import re
import time

class Retriever(object):
	""" Retrieves html contents from URL"""
	def __init__(self, baseUrl, queryAddr, options, configuration):
		self.baseUrl = baseUrl
		self.queryAddr = queryAddr
		self.options = options

		timeout = configuration.timeout
		socket.setdefaulttimeout(timeout)

		self.retries = configuration.retries
		self.timeBetweenRetries = configuration.timeBetweenRetries

		proxy = configuration.proxy
		if proxy is not None and len(proxy) > 0:
		    self.proxy = {"http" : proxy}
		else:
		    self.proxy = {}
				
	def Retrieve(self, retries = None, timeBetweenRetries = None):
		"""Tries to fetch information from provided url
		    retries is the number of attempts to acquire contents if timeout occurs
		    timeBetweenRetries is the number of seconds to wait for the next attempt if a request times out
		"""
		if retries is None:
		    retries = self.retries
		if timeBetweenRetries is None:
		    timeBetweenRetries = self.timeBetweenRetries

		contents = None
		url = self.baseUrl + self.queryAddr + urllib.urlencode(self.options)
		Log.Log("Searching: " + url)
		sd = None
		try:
		    sd = urllib.urlopen(url, proxies = self.proxy)
		    contents = sd.read()
		except IOError:
		    retries -= 1
		    if retries > 0:
			Log.Warning("TimedOut. Retrying more " + str(retries) + " times in " + str(timeBetweenRetries) + "s")			
			time.sleep(timeBetweenRetries)
			self.Retrieve(retries)
		    else:
			raise
		finally:
		    if sd:
			sd.close()		
		return contents;
		
		

		
