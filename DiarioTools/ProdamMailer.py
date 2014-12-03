#!/usr/bin/python
#coding: utf-8
import os
import smtplib
from Log import *
from xml.etree.ElementTree import *

_mailerValidConfig = False
def IfValidConfig(func):
    def decorated(*args, **kwargs):	
	if _mailerValidConfig:
	    return func(*args, **kwargs)
    return decorated

class ProdamMailer(object):
    def __init__(self, configFileName):	
	self.destination = []
	self._ProcessConfigFile(configFileName)
    
    def _ProcessConfigFile(self, configFileName):
	global _mailerValidConfig

	if os.path.exists(configFileName):
	    try:
		tree = parse(configFileName)
		self.username = tree.find("./User").text
		self.password = tree.find("./Password").text
		self.frommail = tree.find("./From").text
		self.serverAddr = tree.find("./ServerAddress").text	
		self.serverPort = int(tree.find("./ServerPort").text)
		self.subject = tree.find("./SubjectPrefix").text
		self.header = tree.find("./Header").text
		self.footer = tree.find("./Footer").text
		
		emails = tree.findall("./To/Email")
		for email in emails:
		    self.AddDestination(email.text)
		
		_mailerValidConfig = True
	    except:
		Log.Warning("Erro de processamento do arquivo de configuração")
	    
	if not _mailerValidConfig:
	    Log.Warning("Configuração inválida. Não será possível mandar e-mails")
	    Log.Warning("Por favor verifique: " + configFileName)

    @IfValidConfig
    def SetSubject(self, subject):
	self.subject += subject

    @IfValidConfig
    def AddDestination(self, email):
	self.destination.append(email)
    
    @IfValidConfig
    def _PrepareMessage(self, messageText):
    	message = "from: " + self.frommail + "\r\n"
	message += "to: " + ";".join(self.destination) + "\r\n"
	message += "subject: " + self.subject + "\r\n"
	message += "mime-version: 1.0\r\n"
	message += "content-tupe: text/plain\r\n\r\n"
	message += self.header + "\r\n\r\n"
	message += messageText
	message += "\r\n\r\n" + self.footer	
	return message

    @IfValidConfig    
    def Send(self, messageText):    
	message = self._PrepareMessage(messageText)
    
	try:
	    server = smtplib.SMTP(self.serverAddr, self.serverPort)
	    server.starttls()
	    server.login(self.username, self.password)
	    server.sendmail(self.frommail, ";".join(self.destination),message)
	    server.quit()
	    Log.Log("E-mail enviado")
	except:
	    Log.Warning("Não foi possível enviar e-mails")
	
