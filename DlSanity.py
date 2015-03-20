#!/usr/bin/python
#coding: utf-8
from DiarioTools.Parser import *
from DiarioTools.Process import *
from DiarioTools.Search import *
import re

class ParseSanity(GenericParser):
	def Initialize(self):
		self.AddExpression(".*", [0], re.I|re.M)

class SearchSanity(DlSearch):
	def SetOptions(self):		
		self.options["sort"] = u"data desc"
		self.options["f[data][]"] = u"week_1"

class ProcessorSanity(ResponseProcessor):
	def __init__(self, configInstance, searchObject, parseObject, fileName, sessionName):
		super(ProcessorSanity, self).__init__(configInstance, searchObject, parseObject, sessionName)
		self.newData = False

	def _ProcessIterate(self):
		for val in self.searchObject.Search():
		    Log.Log("Iterating")

		    parsedVal = json.loads(val)
		    docs = parsedVal["response"]["docs"]
		    if len(parsedVal["response"]["docs"]) == 0:
			    break
		    
		    for doc in docs:			
			self.doc = doc
			if self.configuration.mode == "local search":#Meaning start/end dates were not passed
			    for response in self.parseObject.Parse(doc['texto']):
				    self.Persist(response)
				    return
			    
			elif (self.lastSearch is not None and
			    self.lastSearch.IsNewer(doc['id']) and 
			    IsNewer(doc['id'], self.configuration.baseDate)):

			    self.lastSearch.SetCandidate(doc['id'])
			    for response in self.parseObject.Parse(doc['texto']):
				    self.Persist(response)
				    return
			    
			else:			   
			    Log.Log("Iteration Over")
			    return		

	def Persist(self, data):
  	    """We just want to know if there is new data"""
	    self.newData = True

	def ProcessEnd(self):
	    return self.newData
