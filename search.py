from DiarioTools.Log import *
from DiarioTools.Retriever import *
from Tkinter import *

class DlSearch(object):
	def __init__(self, jsonFormat = False):
		self.baseUrl = "http://devcolab.each.usp.br"
		self.options = {}
		
		self.queryAddr = "/do/?"
		if jsonFormat:
			self.queryAddr = "/do/catalog.json?"		
		
	def Search(self, query):
		i = 0;
		while True:			
			i += 1
			self.options["page"] = i
			self.options["q"] = query
			retriever = Retriever(self.baseUrl, self.queryAddr, self.options)
			contents = retriever.Retrieve()
			if contents is not None:
				yield contents
				
import json
mySearch = DlSearch(True)
for val in mySearch.Search("\"Paulo de Negreiros Spinelli\""):
	Log.Log("Iterating")
	try:
		parsedVal = json.loads(val)
		if len(parsedVal["response"]["docs"]) == 0:
			break
	except:
		Log.Log("Invalid data retrieved")
		break
	
	
	
			
	
			
