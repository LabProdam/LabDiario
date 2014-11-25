#!/usr/bin/python
#coding: utf-8
from DiarioTools.Parser import *
from DiarioTools.Process import *
from DiarioTools.Search import *
	
class ParseChefeDeGabinete(GenericParser):
	def Initialize(self):
		self.AddExpression("^\s*Nomear.*?(senhora|senhor)\s*([^,]*).*?Chefe de Gabinete.(.*)", [2,3], re.I|re.M)

class SearchChefeDeGabinete(DlSearch):
	def SetOptions(self):		
		self.options["f[orgao_facet][]"] = u"TITULOS DE NOMEA\u00C7\u00C3O".encode("utf-8")		

		
class ProcessorChefeDeGabinete(ResponseProcessor):
	def __init__(self, searchObject, parseObject, fileName):
		super(ProcessorChefeDeGabinete, self).__init__(searchObject, parseObject)
		self.fileName = fileName
		
	def Persist(self, data):
		with open(self.fileName, "a") as fd:
			 fd.write(self.doc["id"] + " - ")
			 fd.write(data[0].encode("utf-8") + "\n\t" + data[1].encode("utf-8") + "\n\n")
