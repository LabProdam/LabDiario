#!/usr/bin/python
#coding: utf-8
from smtplib import *
from Log import *
from Config import Configuration, IfValidConfig
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

import re
import socket
class ProxyException(Exception):
    def __repr__(self):
	return
    def __str__(self):
	return "Proxy Connection Error"

class ProxiedSMTP(SMTP, object):
	""" Implement proxy layer above SMTP """
	def __init__(self, proxy = None, host="", port=0, local_hostname=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
	    self.ProcessProxy(proxy)
	    super(ProxiedSMTP, self).__init__(host, port, local_hostname, timeout)

	def ProcessProxy(self, proxy):
	    self.proxyHost = None
	    self.proxyPort = 0

	    if proxy is not None:
		proxyRe = re.search("://([^:]*):(\d*)", proxy)
		if proxyRe is not None:
		    self.proxyHost = socket.gethostbyname(proxyRe.group(1))		
		    self.proxyPort = int(proxyRe.group(2))

	def _get_socket(self, port, host, timeout):
	    # This makes it simpler for SMTP_SSL to use the SMTP connect code
	    # and just alter the socket connection bit.
	    if self.proxyHost is None or len(self.proxyHost) <= 0:
		if self.debuglevel > 0:
		    print>>stderr, 'connect:', (host, port)
		return socket.create_connection((port, host), timeout)
	    else: #If proxy set
#		try:
		connSock = socket.create_connection((self.proxyHost, self.proxyPort), timeout)
		print "Connline: " + "CONNECT %s:%s HTTP/1.1\r\n\r\n" %(port,  host)
		connSock.sendall("CONNECT %s:%s HTTP/1.1\r\n\r\n" %(port,  host))
		rcv = connSock.recv(2048)
		print rcv
		result = re.search("\s(\d+)", rcv)
		if result:	
			code = int(result.group(1))
			if code == 200:
				print "Connection successfull"
				return connSock
			else:
				raise ProxyException()			
#		except:
#			raise ProxyException()


class ProdamMailer(object):
    """ Sends e-mail through google server (only if valid configuration is found)"""
    def __init__(self, configInstance = None):	
	if configInstance == None:
	    Log.Warning("Configuração inválida. Não será possível mandar e-mails")
	else:
	    self.config = configInstance
  
    @IfValidConfig
    def _PrepareMessage(self, messageText):
	multipart = MIMEMultipart('alternative')
    	#multipart["From"] = Header(self.config.frommail.encode("utf-8"), "UTF-8").encode()
    	#multipart["To"] = Header("; ".join(self.config.destination).encode("utf-8"), "UTF-8").encode()
    	multipart["Subject"] = Header(self.config.subject.encode("utf-8"), "UTF-8").encode()

	body = self.config.header + "\r\n\r\n"
	body += messageText.decode("utf-8")
	body += "\r\n\r\n" + self.config.footer
	multipart.attach(MIMEText(body.encode("utf-8"), 'plain', 'UTF-8'))
	return multipart.as_string()

    @IfValidConfig    
    def Send(self, messageText):    
	message = self._PrepareMessage(messageText)	
	try:
	    server = ProxiedSMTP(self.config.proxy, self.config.serverAddr, self.config.serverPort)
	    server.starttls()
	    server.login(self.config.username, self.config.password)
	    server.sendmail(self.config.frommail, self.config.destination, message)
	    server.quit()
	    Log.Log("E-mail enviado")
	except:
	    Log.Warning("Não foi possível enviar e-mails")
	
