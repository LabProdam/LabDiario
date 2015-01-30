#!/usr/bin/python
#coding: utf-8
from DiarioTools.Parser import *
from DiarioTools.Process import *
from DiarioTools.Search import *
import re

wordsOfInterest = ["Prodam",
		   "Empresa de Tecnologia da Informação e Comunicação",
		   "CNPJ 43.076.702/0001-61",
		   "CNPJ 43076702/0001-61"
		 ]

class ParseProdam(GenericParser):
	def Initialize(self):
		self.AddExpression(".+", [0], re.I|re.S)
		
class SearchProdam(DlSearch):
	global wordsOfInterest
	def SetOptions(self):		
		self.options["sort"] = u"data desc"
		
		query = ""
		for word in wordsOfInterest:
		    query += "\"" + word + "\" "
		self.query = query

class ProcessorProdam(ResponseProcessor):
	def __init__(self, configInstance, searchObject, parseObject, fileName, sessionName):
		super(ProcessorProdam, self).__init__(configInstance, searchObject, parseObject, sessionName)
		self.fileName = fileName
		self.records = []
		self.dlProcessor = DlTagsProcessor()

		with open(self.fileName, "a") as fd:
			 fd.write("*** Prodam ***\r\n")
	print """
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
		
	def Persist(self, data):
	    print "<div class=\"item-entry\">"
	    print """	    
	    <div class="item-contents">
		<div class="item-hide" onclick="parentNode.style.display ='none';">[Esconder]</div>
		<table class="item-header">
		<tr><td class="element-name">DATA</td><td><span class="header-value">""" + self.GetDateFromId().encode("utf-8") + """</span></td></tr>
		<tr><td class="element-name">CONTEÚDO</td><td><span class="header-value">""" + self.GetType().encode("utf-8") + """</span></td></tr>
		<tr><td class="element-name">SECRETARIA</td><td><span class="header-value">""" + self.GetSecretary().encode("utf-8") + """</span></td></tr>
		<tr><td class="element-name">ÓRGÃO</td><td><span class="header-value">""" + self.GetOrgan().encode("utf-8") + """</span></td></tr>
		</table>
	    """ + self.dlProcessor.Process(data[0].encode("utf-8")) + """</div>\n\n"""
	    print "</div><br/>"

	def ProcessEnd(self):
	    print "</html>"

class Tag(object):
    def __init__(self, startExpr, startReplace, endExpr, endReplace):
	self.se = "\(\(" + startExpr + "\)\)"
	self.sr = startReplace
	self.ee = "\(\(" + endExpr + "\)\)"
	self.er = endReplace
    
    def Apply(self, text):
	newText = text	
	expressions = re.findall(self.se + ".*?" + self.ee, newText, re.I| re.S)
	for expression in expressions:	    
	    newExpression = expression
	    newExpression = re.sub(self.se, self.sr, newExpression, 1, re.I|re.S)
	    newExpression = re.sub(self.ee, self.er, newExpression, 1, re.I|re.S)
	    newText = newText.replace(expression, newExpression)
	return newText

class DlTagsProcessor(object):
    def __init__(self):
	bold = Tag("NG", "<b>", "CL", "</b>")

	self.tags = [bold]

    def Process(self, text):
	global wordsOfInterest

	parsedText = text
	for tag in self.tags:
	    parsedText = tag.Apply(parsedText)
	parsedText = re.sub("\(\(T.TULO\)\)","", parsedText)
	parsedText = re.sub("\(\(TÍTULO\)\)","", parsedText)
	parsedText = re.sub("\(\(TEXTO\)\)","", parsedText)
	parsedText = re.sub("\(\(NG\)\)","", parsedText)
	parsedText = re.sub("\(\(CL\)\)","", parsedText)
	parsedText = re.sub("^\s*","", parsedText)
	parsedText = re.sub("^(.*)","<h2>\\1</h2>", parsedText)

	for word in wordsOfInterest:  
	    parsedText = re.sub("([^\>\n\r]*" + word + "[^\<\n\r]*)", "<span style='background-color: #ffff00'>\\1</span>", parsedText, 0, re.I)
	    break;
	return parsedText
