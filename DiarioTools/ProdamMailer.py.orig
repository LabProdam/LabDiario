#!/usr/bin/python
#coding: utf-8
from smtplib import *
from Log import *
from Config import Configuration, IfValidConfig

import re
import socket
class ProxyException(Exception):
    def __repr__(self):
	return
    def __str__(self):
	return "Proxy Connection Error"

class ProxiedSMTP(SMTP):
	""" Implement proxy layer above SMTP """
	def __init__(self, proxy = None, host='', port=0, local_hostname=None,
                 timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
	    super(ProxiedSMTP, self).__init__(host, port, local_hostname, timeout)
	    self.ProcessProxy(proxy)

	def ProcessProxy(self, proxy):
	    self.proxyHost = None
	    self.proxyPort = 0

	    proxyRe = re.search("://([^:]*):(\d*))", proxy)
	    if proxyRe is not None:
		self.proxyHost = proxyRe.group(1)
		self.proxyPort = int(proxyRe.group(2))

        def _get_socket(self, port, host, timeout):
	    # This makes it simpler for SMTP_SSL to use the SMTP connect code
	    # and just alter the socket connection bit.
	    if self.proxyHost is None or len(self.proxyHost) <= 0:
		if self.debuglevel > 0:
		    print>>stderr, 'connect:', (host, port)
		return socket.create_connection((port, host), timeout)
	    else: #If proxy set
		try:
		    connSock = socket.create_connection((self.proxyPort, self.proxyHost), timeout)
		    connSock.sendall("CONNECT %s:%d HTTP/1.1\r\n\r\n" %(host,  port))
		    connSock.recv(2048) #parse it
		    connSock.recv(2048) #parse it
		    return connSock
		except:
		    raise ProxyException()


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
	    server = ProxiedSMTP(self.config.proxy, self.config.serverAddr, self.config.serverPort)
	    server.starttls()
	    server.login(self.config.username, self.config.password)
	    server.sendmail(self.config.frommail, ";".join(self.config.destination),message)
	    server.quit()
	    Log.Log("E-mail enviado")
	except:
	    Log.Warning("Não foi possível enviar e-mails")
	
