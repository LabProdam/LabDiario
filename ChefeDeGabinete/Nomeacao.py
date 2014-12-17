#!/usr/bin/python
#coding: utf-8
from DiarioTools.Parser import *
from DiarioTools.Process import *
from DiarioTools.Search import *
import re

class ParseNomeacaoChefeDeGabinete(GenericParser):
	def Initialize(self):
		self.AddExpression("^\s*Nomear.*?(senhora|senhor)\s*([^,]*).*?Chefe de Gabinete.(.*)", [2,3], re.I|re.M)

class SearchNomeacaoChefeDeGabinete(DlSearch):
	def SetOptions(self):		
		self.options["f[orgao_facet][]"] = u"TITULOS DE NOMEA\u00C7\u00C3O".encode("utf-8")		
		self.options["sort"] = u"data desc"		

class ProcessorNomeacaoChefeDeGabinete(ResponseProcessor):
	def __init__(self, configInstance, searchObject, parseObject, fileName, sessionName):
		super(ProcessorNomeacaoChefeDeGabinete, self).__init__(configInstance, searchObject, parseObject, sessionName)
		self.fileName = fileName
		self.records = []
		
	def Persist(self, data):
		strOut = """Em """ + self.GetDateFromId() + """,  """ + self.ProcessName(data) + """ foi nomeado Chefe de Gabinete """ + self.ProcessGabinete(data) + "\n\n"
		self.records.append(strOut.encode("utf-8"))
		with open(self.fileName, "a") as fd:
			 fd.write(strOut.encode("utf-8"))		 

	def ProcessEnd(self):
		if (len(self.records) == 0):    
		    message = """Nenhum Chefe de Gabinete nomeado neste período\r\n\r\n"""
		    Log.Log("Sem Alterações")
		else:
		    message = "\r\n".join(self.records)
		return message

	def ProcessName(self, data):
		return data[0]
    
	def ProcessGabinete(self, data):
		gabineteRe = re.search("(Secretaria|Subprefeitura)\s*,?\s*([^,]*)", data[1], re.I)
		if gabineteRe is not None:
		    gabineteFromData = gabineteRe.group(0)
		    gabineteFromData = "da " + gabineteFromData
		else:
		    gabineteRe = re.search("^([^,]*).\s*s.mbolo", data[1], re.I)
		    if gabineteRe is not None:
			gabineteFromData = gabineteRe.group(1)			
		    else:
			gabineteFromData = data[1]
			gabineteFromData = re.sub("s.mbolo \w*,", "", gabineteFromData, re.I)
			gabineteFromData = re.sub(",?\s*constante.*$", "", gabineteFromData, re.I)
			gabineteFromData = re.sub(",?\s*da Chefia de Gabinete[^,]*x", "", gabineteFromData, re.I)
		return gabineteFromData
