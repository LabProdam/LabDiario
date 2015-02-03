#!/usr/bin/python
#coding: utf-8
from DiarioTools.Parser import *
from DiarioTools.Process import *
from DiarioTools.Search import *
import re

class ParseExoneracaoChefeDeGabinete(GenericParser):
	def Initialize(self):
		self.AddExpression("^\s*Exonerar.{0,1000}?(senhora|senhor)([^,]+).{0,400}?Chefe de Gabinete.(.+)", [2,3], re.I|re.M)

class SearchExoneracaoChefeDeGabinete(DlSearch):
	def SetOptions(self):		
		self.options["sort"] = u"data desc"
		self.query = "exonerar \"chefe de gabinete\""

class ProcessorExoneracaoChefeDeGabinete(ResponseProcessor):
	def __init__(self, configInstance, searchObject, parseObject, fileName, sessionName):
		super(ProcessorExoneracaoChefeDeGabinete, self).__init__(configInstance, searchObject, parseObject, sessionName)
		self.fileName = fileName
		self.records = []

		with open(self.fileName, "a") as fd:
			 fd.write("*** Exonerações ***\r\n")
		
	def Persist(self, data):
	    if len(data) > 0:
		strOut = """Em """ + self.GetDateFromId() + """,  """ + self.ProcessName(data) + """ foi exonerado do cargo Chefe de Gabinete """ + self.ProcessGabinete(data) + "\n"
		self.records.append(strOut.encode("utf-8"))
		with open(self.fileName, "a") as fd:
			 fd.write(strOut.encode("utf-8"))

	def ProcessEnd(self):
		message = "*** Exonerações ***\r\n"
		if (len(self.records) == 0):    
		    message += """Nenhum Chefe de Gabinete exonerado neste período\r\n\r\n"""
		    Log.Log("Sem Alterações")
		else:
		    message += "\r\n".join(self.records)
		    message += "\r\n"
		return message

	def ProcessName(self, data):
		return data[0]
    
	def ProcessGabinete(self, data):
		gabineteRe = re.search("(Funda..o|Controladoria|Secretaria|Subprefeitura|Superintend.ncia)\s*,?\s*(([^\.](?! constante))*)", data[1], re.I)
		if gabineteRe is not None:
		    gabineteFromData = gabineteRe.group(0)
		    gabineteFromData = "da " + gabineteFromData
		else:
		    gabineteRe = re.search("(Instituto|Servi.o)\s*,?\s*([^,]*)", data[1], re.I)
		    if gabineteRe is not None:
			gabineteFromData = gabineteRe.group(0)
			gabineteFromData = "do " + gabineteFromData
		    else:
			gabineteRe = re.search("^([^,]*).\s*s.mbolo", data[1], re.I)
			if gabineteRe is not None:
			    gabineteFromData = gabineteRe.group(1)			
			else:
			    gabineteFromData = data[1]
			    gabineteFromData = re.sub("s.mbolo \w*,", "", gabineteFromData, re.I)			    
			    gabineteFromData = re.sub(",?\s*da Chefia de Gabinete[^,]*x", "", gabineteFromData, re.I)
		gabineteFromData = re.sub(",?\s*constante.*$", "", gabineteFromData, re.I)
		return gabineteFromData
