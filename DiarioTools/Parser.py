#!/usr/bin/python
#coding: utf-8
import re
class GenericParser(object):
	""" Given a set of regular expressions, evaluate them and convert groups
	of interest into array"""
	def __init__(self):
		self.expressions = []
		self.Initialize()
	
	def Initialize(self):
		"""Override this method"""
		pass
	
	def AddExpression(self, reExpression, groupsOfInterest, flags = None):
		self.expressions.append((reExpression, groupsOfInterest, flags))
				
	def Parse(self, content):		
		for expression, groupsOfInterest, flags in self.expressions:
			if flags is not None:
				matches = re.finditer(expression, content, flags) 
			else:
				matches = re.finditer(expression, content)			
			for match in matches:				
				matchGroups = []
				for group in groupsOfInterest:
					matchGroups.append(match.group(group))
				yield matchGroups
				
