#!/usr/bin/python
#coding: utf-8
from Log import *
from xml.etree.ElementTree import *
import os

validConfig = False
def IfValidConfig(func):
    def decorated(*args, **kwargs):	
	if validConfig:
	    return func(*args, **kwargs)
    return decorated

class Configuration(object):
    """ Basic configuration. Read from xml and make available in config instance"""
    def __init__(self,configFileName):
	self.destination = []
	self._ProcessConfigFile(configFileName)

    def _ProcessConfigFile(self, configFileName):
	global validConfig 
	if os.path.exists(configFileName):
	    try:
		tree = parse(configFileName)
		self.username = tree.find("./User").text
		self.password = tree.find("./Password").text
		self.frommail = tree.find("./From").text
		self.serverAddr = tree.find("./ServerAddress").text	
		self.serverPort = int(tree.find("./ServerPort").text)
		self.subject = tree.find("./Subject").text
		self.header = tree.find("./Header").text
		self.footer = tree.find("./Footer").text
		self.baseDate = tree.find("./BaseDate").text
		
		emails = tree.findall("./To/Email")
		for email in emails:
		    self.AddDestination(email.text)
		
		validConfig = True
	    except:
		Log.Warning("Erro de processamento do arquivo de configuração")
	else:
	    Log.Warning("Arquivo de configuração não encontrado")

    def AddDestination(self, email):
	self.destination.append(email)
