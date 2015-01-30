#!/usr/bin/python
#coding: utf-8
from Log import *
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
	
	def AddExpression(self, reExpression, groupsOfInterest, flags = None, count = -1):
		self.expressions.append((reExpression, groupsOfInterest, flags, count))
				
	
	def Parse(self, content):		
		for expression, groupsOfInterest, flags, count in self.expressions:			
			if flags is not None:
				matches = re.finditer(expression, content, flags) 
			else:
				matches = re.finditer(expression, content)			
			
			yieldResult = False
			for num, match in enumerate(matches):				
				if count >= 0 and num >= count:
				    break
				matchGroups = []
				for group in groupsOfInterest:
					matchGroups.append(match.group(group))
				yield matchGroups
				yieldResult = True

			if not yieldResult:
			    #yield empty response for keeping control when group is over 
			    yield []
			
