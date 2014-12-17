#!/usr/bin/python
#coding: utf-8
from Log import *
import urllib
import re

class Retriever(object):
	""" Retrieves html contents from URL"""
	def __init__(self, baseUrl, queryAddr, options, configuration):		
		self.baseUrl = baseUrl
		self.queryAddr = queryAddr
		self.options = options

		proxy = configuration.proxy
		if proxy is not None and len(proxy) > 0:
		    self.proxy = {"http" : proxy}
		else:
		    self.proxy = {}
				
	def Retrieve(self):
		contents = None
		url = self.baseUrl + self.queryAddr + urllib.urlencode(self.options)
		Log.Log("Searching: " + url)
		sd = urllib.urlopen(url, proxies = self.proxy)
		contents = sd.read()
		sd.close()
		return contents;
		
		

		
