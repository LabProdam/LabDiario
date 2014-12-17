#!/usr/bin/python
#coding: utf-8

import sys
class Log(object):
	"""Basic logging"""
	@staticmethod
	def Log(msg):
		print msg
	@staticmethod
	def Warning(msg):
		sys.stderr.write("WARNING: " + msg + "\n")
		
