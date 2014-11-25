#!/usr/bin/python
#coding: utf-8
from DiarioTools.Log import *
from DiarioTools.Retriever import *
from DiarioTools.Parser import *
from Tkinter import *


class DlSearch(object):
	def __init__(self, jsonFormat = False):
		self.baseUrl = "http://devcolab.each.usp.br"
		self.options = {}
		
		self.queryAddr = "/do/?"
		if jsonFormat:
			self.queryAddr = "/do/catalog.json?"		
		
	def SetOptions(self):
		pass
	
	def Search(self, query=None):
		self.SetOptions()
		i = 0;
		while True:			
			i += 1
			self.options["page"] = i
			if query is not None:
				self.options["q"] = query
			retriever = Retriever(self.baseUrl, self.queryAddr, self.options)
			contents = retriever.Retrieve()
			if contents is not None:
				yield contents
				
	
	
	
			
	
			
