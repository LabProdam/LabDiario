#!/usr/bin/python
#coding: utf-8
from DiarioTools.Parser import *
from DiarioTools.Process import *
from DiarioTools.Search import *
import re

class ParseChefeDeGabinete(GenericParser):
	def Initialize(self):
		self.AddExpression("^\s*Nomear.*?(senhora|senhor)\s*([^,]*).*?Chefe de Gabinete.(.*)", [2,3], re.I|re.M)

class SearchChefeDeGabinete(DlSearch):
	def SetOptions(self):		
		self.options["f[orgao_facet][]"] = u"TITULOS DE NOMEA\u00C7\u00C3O".encode("utf-8")		
		self.options["sort"] = u"data desc"		

class ProcessorChefeDeGabinete(ResponseProcessor):
	def __init__(self, searchObject, parseObject, fileName, sessionName):
		super(ProcessorChefeDeGabinete, self).__init__(searchObject, parseObject, sessionName)
		self.fileName = fileName
		self.records = []
		
	def Persist(self, data):
		strOut = """Em """ + self.ProcessId(data) + """,  """ + self.ProcessName(data) + """ foi nomeado Chefe de Gabinete """ + self.ProcessGabinete(data) + "\n\n"
		self.records.append(strOut.encode("utf-8"))
		with open(self.fileName, "a") as fd:
			 fd.write(strOut.encode("utf-8"))		 

	def ProcessEnd(self):
		mailer = ProdamMailer("mailer_config.xml")
		mailer.AddDestination("pnspin@gmail.com")
		mailer.SetSubject("Nomeação de Chefes de Gabinete")
		if (len(self.records) == 0):    
		    message = """Nenhum Chefe de Gabinete nomeado neste período"""
		else:
		    message = "\r\n".join(self.records)
		mailer.Send(message)

	def ProcessId(self, data):
		idRe = re.search("^(\d{4}).(\d{2}).(\d{2})", self.doc["id"])
		if idRe is not None:
		    dateFromId = idRe.group(3) + "/" + idRe.group(2) + "/" + idRe.group(1)
		else:
		    dateFromId = self.doc["id"]
		return dateFromId

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
