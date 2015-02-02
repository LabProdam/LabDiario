#!/usr/bin/python
#coding: utf-8
import json
import pickle
import re
from Log import *
from ProdamMailer import *

def IsNewer(id, other):
    newer = False

    if id is not None:
	pId = ProcessId(id)
    else:
	pId = 0

    if other is not None:
	other = ProcessId(other)	
    else:
	other = 0


    if (pId > other):
	newer = True

    return newer

def ProcessId(id):
    idRe = re.search("^(\d{4}).(\d{2}).(\d{2})", id)
    if idRe is not None:
	id = int(idRe.group(1) + idRe.group(2) + idRe.group(3)) 
    else:
	raise Exception("Invalid Id: " + id)
    return id

class LastSearch(object):
	"""To be persisted indicating where last search terminated"""
	def __init__(self):
	    self.latest = None
	    self.candidate = None

	def SetCandidate(self, id):	   
	    if IsNewer(id, self.candidate):
		self.candidate = id

	def SetLatestFromCandidate(self):
	    if IsNewer(self.candidate, self.latest):
		self.latest = self.candidate
		self.candidate = None

	def IsNewer(self, id):
	    return IsNewer(id, self.latest)
	    	
class ResponseProcessor(object):
	"""Process received response"""
	def __init__(self, configInstance, searchObject, parseObject, sessionName):
		self.configuration = configInstance
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
			if self.configuration.mode == "local search":#Meaning start/end dates were not passed
			    for response in self.parseObject.Parse(doc['texto']):
				    self.Persist(response)
			    self.Iterate()
			elif (self.lastSearch is not None and
			    self.lastSearch.IsNewer(doc['id']) and 
			    IsNewer(doc['id'], self.configuration.baseDate)):

			    self.lastSearch.SetCandidate(doc['id'])
			    for response in self.parseObject.Parse(doc['texto']):
				    self.Persist(response)
			    self.Iterate()
			else:			   
			    Log.Log("Iteration Over")
			    return
			

	def ProcessEnd(self):
	    """To be implemented by subs"""
	    pass

	def Process(self):
	    pickleFileName = self.sessionName + ".pk"
	    self._LoadPersistedFile(pickleFileName)

	    self._ProcessIterate()
	    self.lastSearch.SetLatestFromCandidate()
	    retVal = self.ProcessEnd()

	    self._SavePersistedFile(pickleFileName)
	    return retVal

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
			
    	def GetDateFromId(self):
		idRe = re.search("^(\d{4}).(\d{2}).(\d{2})", self.doc["id"])
		if idRe is not None:
		    dateFromId = idRe.group(3) + "/" + idRe.group(2) + "/" + idRe.group(1)
		else:
		    dateFromId = self.doc["id"]
		return dateFromId
		
	def GetSecretary(self):
		return self.doc["secretaria"]

	def GetOrgan(self):
		return self.doc["orgao"]

	def GetType(self):
		return self.doc["tipo_conteudo"]

	def Persist(self, data):
		"""To be implemented on child"""
		pass

	def Iterate(self):
		"""To be implemented on child"""
		pass
