#!/usr/bin/python
#coding: utf-8
from Log import *
from xml.etree.ElementTree import *
import os
import re
import getopt

manualTypes = ["Timeout",
	       "Retries",
	       "TimeBetweenRetries",
	       "LogMode",
	       "To",
	       "Modules"]

validConfig = False
def IfValidConfig(func):
    def decorated(*args, **kwargs):	
	if validConfig:
	    return func(*args, **kwargs)
    return decorated

class Configuration(object):
    """ Basic configuration. Read from xml and make available in config instance"""
    def __init__(self,configFileName, args):
	self.destination = []
	self.modules = []
	self._ProcessConfigFile(configFileName)
	self._ProcessArgs(args)
	
    def AppendConfigurationFile(self, configfileName):
	self._ProcessConfigFile(configfileName)

    def _ProcessArgs(self, args):
	self.startDate = None
	self.endDate = None
	opts = getopt.getopt(args[1:], "s:e:h")
	for opt, value in opts[0]:
	    if opt == "-s":
		date = self._ParseDate(value)
		if date is not None:
		    self.startDate = date
	    if opt == "-e":
		date = self._ParseDate(value)
		if date is not None:
		    self.endDate = date
	    if opt == "-h":
		Log.Log("""Uso: """ + args[0] + """ [-s data -e data]

Argumentos:
-s	Data inicial
-e	Data final""")
		exit(0)

	if self.startDate == None and self.endDate != None:
	    Log.Warning("Data final especificada sem data initial")
	    exit(1)

	if self.startDate != None and self.endDate == None:
	    Log.Warning("Data inicial especificada sem data final")
	    exit(1)

	if self.startDate is not None:
	    self.mode = "local search"
	else:
	    self.mode = "alert mode"

    def _ParseDate(self, date):
	retDate = None
	dateRe = re.search("(\d{2})/(\d{2})/(\d{4})", date)
	if dateRe is not None:
	    retDate = dateRe.group(3) + "-" + dateRe.group(2) + "-" + dateRe.group(1) + "T00:00:00.000Z"
	return retDate

    def _ProcessConfigFile(self, configFileName):
	global validConfig 
	if os.path.exists(configFileName):
	    try:
		tree = parse(configFileName)
		types = tree.findall("./*")

		#automatically transform xml elements into attributes (lowering
		#first letter ex LogName becomes logName
		for configType in types:		    
		    if configType.tag not in manualTypes:			
			configName = configType.tag[0].lower() + configType.tag[1:]
			setattr(self, configName, configType.text)		

		#manual types
		if tree.find("./Timeout") is not None:
		    self.timeout = float(tree.find("./Timeout").text)
		if tree.find("./Retries") is not None:
		    self.retries = int(tree.find("./Retries").text)
		if tree.find("./TimeBetweenRetries") is not None:
		    self.timeBetweenRetries = float(tree.find("./TimeBetweenRetries").text)
		if tree.find("./LogMode") is not None:
		    self._ProcessCleanLogs(tree.find("./LogMode").text, self.logName)		
		
		emails = tree.findall("./To/Email")
		for email in emails:
		    self.AddDestination(email.text)

		modules = tree.findall("./Modules/Name")
		for module in modules:
		    self.AddModule(module.text)
		
		validConfig = True
	    except Exception as ex:
		Log.Warning("Erro de processamento do arquivo de configuração: " + str(ex))
		exit(1)
	else:
	    Log.Warning("Arquivo de configuração não encontrado")
	    exit(1)

    def _ProcessCleanLogs(self, logMode, logName):
	if re.search("Overwrite", logMode, re.I) is not None:
	    if os.path.exists(logName):
		os.remove(logName)

    def AddDestination(self, email):
	self.destination.append(email)

    def AddModule(self, modulesName):
	self.modules.append(modulesName)
