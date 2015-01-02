#!/usr/bin/python
#coding: utf-8
from DiarioTools.Parser import *
from DiarioTools.Process import *
from DiarioTools.Search import *
import re

class ParseSubstituicaoChefeDeGabinete(GenericParser):
	def Initialize(self):
		self.AddExpression("^.*?(senhora|senhor)([^,]+).{0,100}?Per.odo de ([^,]*).{0,100}?Substituir.{0,300}?(senhora|senhor)([^,]+).{0,300}?(chefe de gabinete.*)", [2,5,6,3], re.I|re.M)

class SearchSubstituicaoChefeDeGabinete(DlSearch):
	def SetOptions(self):		
		self.options["sort"] = u"data desc"
		self.query = "substituir chefe de gabinete"		

class ProcessorSubstituicaoChefeDeGabinete(ResponseProcessor):
	def __init__(self, configInstance, searchObject, parseObject, fileName, sessionName):
		super(ProcessorSubstituicaoChefeDeGabinete, self).__init__(configInstance, searchObject, parseObject, sessionName)
		self.fileName = fileName
		self.records = []

		with open(self.fileName, "a") as fd:
			 fd.write("*** Substituições ***\r\n")
		
	def Persist(self, data):
		strOut = """Em """ + self.GetDateFromId() + """,  """ + self.ProcessName1(data) + """ substitui """ + self.ProcessName2(data) + """, chefe de gabinete """ + self.ProcessGabinete(data) + """ de """ + self.ProcessPeriod(data)+ "\n\n"
		self.records.append(strOut.encode("utf-8"))
		with open(self.fileName, "a") as fd:
			 fd.write(strOut.encode("utf-8"))

	def ProcessEnd(self):
		message = "*** Substituições ***\r\n"
		if (len(self.records) == 0):    
		    message += """Nenhum Chefe de Gabinete substituído neste período\r\n\r\n"""
		    Log.Log("Sem Alterações")
		else:
		    message += "\r\n".join(self.records)
		return message

	def ProcessName1(self, data):
		return data[0]
	
	def ProcessName2(self, data):
		return data[1]

	def ProcessPeriod(self, data):		
		return data[3]
    
	def ProcessGabinete(self, data):		
		gabineteRe = re.search("(Controladoria|Secretaria|Subprefeitura|Superintend.ncia)\s*,?\s*([^,]*)", data[2], re.I)
		if gabineteRe is not None:
		    gabineteFromData = gabineteRe.group(0)
		    gabineteFromData = "da " + gabineteFromData
		else:
		    gabineteRe = re.search("(Instituto|Servi.o)\s*,?\s*([^,]*)", data[2], re.I)
		    if gabineteRe is not None:
			gabineteFromData = gabineteRe.group(0)
			gabineteFromData = "do " + gabineteFromData
		    else:
			gabineteRe = re.search("^([^,]*).\s*s.mbolo", data[2], re.I)
			if gabineteRe is not None:
			    gabineteFromData = gabineteRe.group(1)			
			else:
			    gabineteFromData = data[2]
			    gabineteFromData = re.sub("s.mbolo \w*,", "", gabineteFromData, re.I)
			    gabineteFromData = re.sub(",?\s*constante.*$", "", gabineteFromData, re.I)
			    gabineteFromData = re.sub(",?\s*da Chefia de Gabinete[^,]*x", "", gabineteFromData, re.I)
		return gabineteFromData
