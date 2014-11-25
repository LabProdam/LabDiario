#!/usr/bin/python
#coding: utf-8
import json
from Log import *

class ResponseProcessor(object):
	def __init__(self, searchObject, parseObject):
		self.searchObject = searchObject
		self.parseObject = parseObject
		self.doc = None
	
	def Process(self):
		for val in self.searchObject.Search():
			Log.Log("Iterating")

			parsedVal = json.loads(val)
			docs = parsedVal["response"]["docs"]
			if len(parsedVal["response"]["docs"]) == 0:
				break
			
			for doc in docs:
				self.doc = doc		
				for response in self.parseObject.Parse(doc['texto']):
					self.Persist(response)
					
	def Persist(self, data):
		"""To be implemented on child"""
		pass
