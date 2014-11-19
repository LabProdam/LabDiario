from Log import *
import urllib
import re

class Retriever(object):
	def __init__(self, baseUrl, queryAddr, options):
		self.baseUrl = baseUrl
		self.queryAddr = queryAddr
		self.options = options	
				
	def Retrieve(self):
		contents = None
		url = self.baseUrl + self.queryAddr + urllib.urlencode(self.options)
		Log.Log("Searching: " + url)
		sd = urllib.urlopen(url)
		contents = sd.read()
		sd.close()
		return contents;
		
		

		
