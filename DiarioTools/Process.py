#!/usr/bin/python
#coding: utf-8
import json
import pickle
import re
from Log import *
from ProdamMailer import *

class LastSearch(object):
	"""To be persisted indicating where last search terminated"""
	def __init__(self):
	    self.latest = 0
	    self.candidate = 0

	def SetCandidate(self, id):
	    processedId = self._ProcessId(id)	    
	    if (processedId > self.candidate):
		self.candidate = processedId

	def SetLatestFromCandidate(self):
	    if self.candidate > self.latest:
		self.latest = self.candidate
		self.candidate = 0

	def IsNewer(self, id):
	    newer = False
	    pId = self._ProcessId(id)	    
	    if (pId > self.latest):
		newer = True

	    return newer

	def _ProcessId(self, id):
	    idRe = re.search("^(\d{4}).(\d{2}).(\d{2})", id)
	    if idRe is not None:
		id = int(idRe.group(1) + idRe.group(2) + idRe.group(3)) 
	    else:
		raise "Invalid Id"
	    return id

class ResponseProcessor(object):
	"""Process received response"""
	def __init__(self, searchObject, parseObject, sessionName):
		self.searchObject = searchObject
		self.parseObject = parseObject
		self.sessionName = sessionName
		self.lastSearch = None	
		self.doc = None
	
	def _ProcessIterate(self):
		for val in self.searchObject.Search():
		    Log.Log("Iterating")

		    parsedVal = json.loads(val)
		    docs = parsedVal["response"]["docs"]
		    if len(parsedVal["response"]["docs"]) == 0:
			    break
		    
		    for doc in docs:
			self.doc = doc
			if (self.lastSearch is not None and self.lastSearch.IsNewer(doc['id'])):
			    self.lastSearch.SetCandidate(doc['id'])
			    for response in self.parseObject.Parse(doc['texto']):
				    self.Persist(response)
			else:
			    return

	def ProcessEnd(self):
	    """To be implemented by subs"""
	    pass

	def Process(self):
	    pickleFileName = self.sessionName + ".pk"
	    self._LoadPersistedFile(pickleFileName)

	    self._ProcessIterate()
	    self.lastSearch.SetLatestFromCandidate()
	    self.ProcessEnd()

	    self._SavePersistedFile(pickleFileName)

	def _LoadPersistedFile(self, pickleFileName):	    
	    try:
		fd = open(pickleFileName)
		self.lastSearch = pickle.load(fd)
		fd.close()
		Log.Log("Reloading Last Session");
	    except:
		self.lastSearch = LastSearch()
    
	def _SavePersistedFile(self, pickleFileName):
	    with open(pickleFileName, "w") as fd:
		pickle.dump(self.lastSearch, fd)		
					
	def Persist(self, data):
		"""To be implemented on child"""
		pass
