#!/usr/bin/python
#coding: utf-8
from Common import *
from DiarioTools.Parser import *
from DiarioTools.Process import *
from DiarioTools.Search import *
import re

wordsOfInterest = []

reOfInterest = ["GabPrefeito",
		   "Pro-dam",
		   "EMPRESA DE TECNOLOGIA DA INFORMA..O E COMUNICA..O",		   
		   "Emp. Tec. da Informa..o e Comunica..o",
		   "CNPJ 43.076.702/0001-61",
		   "CNPJ 43076702/0001-61"
		 ]

class ParseGabPrefeito(GenericParser):
	def Initialize(self):
		self.AddExpression(".+", [0], re.I|re.S)
		
class SearchGabPrefeito(DlSearch):
	global wordsOfInterest
	
	def __init__(self, organ, *args):
	    super(SearchGabPrefeito, self).__init__(*args)
	    self.organ = organ
	
	def SetOptions(self):		
		self.options["sort"] = u"data desc"
		self.options["f[orgao_facet][]"] = self.organ
		self.options["f[secretaria_facet][]"] = u"GABINETE DO PREFEITO"
		
		query = ""
		for word in wordsOfInterest:
		    query += "\"" + word + "\" "
		self.query = query
		
class ProcessorGabPrefeitoPartial(ResponseProcessor):
	def __init__(self, configInstance, searchObject, parseObject, fileName, sessionName):
		super(ProcessorGabPrefeitoPartial, self).__init__(configInstance, searchObject, parseObject, sessionName)
		self.fileName = fileName
		self.data = ""
		self.atLeadOneFound = False
		self.dlProcessor = DlTagsProcessor(reOfInterest)

		with open(self.fileName, "a") as fd:
			 fd.write("*** GabPrefeito (" + sessionName + ") ***\r\n")
		self.data += ""
		
	def Persist(self, data):
	    self.atLeadOneFound = True
	    contents = data[0].encode("utf-8")
	    with open(self.fileName, "a") as fd:
		 fd.write(contents)

	    self.data += "<div class=\"item-entry\">"
	    self.data += """	    
	    <div class="item-contents">
		<div class="item-hide" onclick="parentNode.style.display ='none';">[Esconder]</div>
		<table class="item-header">
		<tr><td class="element-name">DATA</td><td><span class="header-value">""" + self.GetDateFromId().encode("utf-8") + """</span></td></tr>
		<tr><td class="element-name">CONTEÚDO</td><td><span class="header-value">""" + self.GetType().encode("utf-8") + """</span></td></tr>
		<tr><td class="element-name">SECRETARIA</td><td><span class="header-value">""" + self.GetSecretary().encode("utf-8") + """</span></td></tr>
		<tr><td class="element-name">ÓRGÃO</td><td><span class="header-value">""" + self.GetOrgan().encode("utf-8") + """</span></td></tr>
		</table>
	    """ + self.dlProcessor.Process(contents) + """</div>\n\n"""
	    self.data += "</div><br/>"

	def ProcessEnd(self):
	    return self.data


class ProcessorGabPrefeito(object):
	def __init__(self, configInstance, searchObjects, parseObject, fileName, sessionName):
		self.configInstance = configInstance
		self.parseObject = parseObject
		self.searchObjects = searchObjects
		self.fileName = fileName
		self.sessionName = sessionName
		self.data = ""

		with open(self.fileName, "a") as fd:
			 fd.write("*** GabPrefeito ***\r\n")
		self.header = """
		<!DOCTYPE HTML>
		<html>
		    <head>
			<meta charset="utf-8"/>
		    </head>
		    <style>
			body {
			    font-size: 14px;
			    text-align: center;
			    background-color: #eee;
			}
			b, h2{
			    background-color: inherit;
			}
			h2 {
			    margin: 0;
			}

			.item-entry {
			    display: inline-block; 
			    width: 800px;
			    background-color: #fff;
			    box-shadow: 2px 2px 10px #aaa;
			    margin-bottom:2em;
			}
			.item-contents {
			    white-space: pre-line; 
			    text-align: justify;
			    padding: 1em 2em;	
			    font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
			    line-height: 1.5em;
			}
			.item-hide {
			    font-size: 0.7em; 
			    text-decoration: underline;
			    cursor: pointer;
			}
			.item-header {
			    border: 1px solid black;
			    background-color: #eee;
			    font-size: 0.8em;
			    font-family: arial;
			    font-weight: 700;
			    line-height: 1em;
			}
			.header-value {
			    font-size: 0.8em;
			    font-weight: 300;
			}
			.element-name {
			    text-align: right;
			}
		    </style>
		"""

	def Process(self):
	    for searchObject in self.searchObjects:
		    processor = ProcessorGabPrefeitoPartial(self.configInstance, searchObject, self.parseObject, self.fileName, self.sessionName + "_" + searchObject.organ)
		    self.data += processor.Process()
	    if len(self.data) <= 0:
		    return None
	    else:
		self.data = self.header + self.data + "</html>"
		return self.data
	

