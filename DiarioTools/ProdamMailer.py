#!/usr/bin/python
#coding: utf-8
import smtplib
from Log import *
from Config import Configuration, IfValidConfig

class ProdamMailer(object):
    """ Sends e-mail through google server (only if valid configuration is found)"""
    def __init__(self, configInstance = None):	
	if configInstance == None:
	    Log.Warning("Configuração inválida. Não será possível mandar e-mails")
	else:
	    self.config = configInstance
  
    @IfValidConfig
    def _PrepareMessage(self, messageText):
    	message = "from: " + self.config.frommail + "\r\n"
	message += "to: " + ";".join(self.config.destination) + "\r\n"
	message += "subject: " + self.config.subject + "\r\n"
	message += "mime-version: 1.0\r\n"
	message += "content-tupe: text/plain\r\n\r\n"
	message += self.config.header + "\r\n\r\n"
	message += messageText.decode("utf-8")
	message += "\r\n\r\n" + self.config.footer	
	return message.encode("utf-8")

    @IfValidConfig    
    def Send(self, messageText):    
	message = self._PrepareMessage(messageText)
    
	try:
	    server = smtplib.SMTP(self.config.serverAddr, self.config.serverPort)
	    server.starttls()
	    server.login(self.config.username, self.config.password)
	    server.sendmail(self.config.frommail, ";".join(self.config.destination),message)
	    server.quit()
	    Log.Log("E-mail enviado")
	except:
	    Log.Warning("Não foi possível enviar e-mails")
	
