#coding: UTF-8
import mechanize
import cookielib
import traceback
import re
import sys
from Log import *

class GMailerWrappper(object):
	"""Simplifies GMailer class usage, taking parameters within configuration object"""
	def __init__(self, configInstance = None):	
		if configInstance == None:
			Log.Warning("Configuração inválida. Não será possível mandar e-mails")
		else:
			self.config = configInstance
		self.attach = []
		
	def AttachFile(self, fileName):
	    self.attach.append(fileName)

	def Send(self, message):
		mailer = GMailer()
		sendMessage = self.config.header + "\r\n\r\n" + message + "\r\n\r\n" + self.config.footer
		
		if self.config.proxy is not None and len(self.config.proxy) > 0:
			proxies = {"http": self.config.proxy, "https": self.config.proxy}
			mailer.SetProxies(proxies)			
		for file in self.attach:
		    mailer.AttachFile(file)
		mailer.SetLoginInfo(self.config.username, self.config.password)
		mailer.SendEmail(self.config.destination, self.config.subject.encode("utf-8"), sendMessage)

class GMailer:
	"""Sends e-mail through gmail. Set login info, proxy if necessary and 
	just send the e-mail"""
	def __init__(self):
		self.email = None
		self.password = None
		self.proxies = None
		self.attach = []
		
	def SetLoginInfo(self, email, password):
		self.email = email
		self.password = password
		
	def SetProxies(self, proxies):
		self.proxies = proxies
		
	def SendEmail(self, to, subject, body):
		connection = self._InitComm()
		self._Authenticate(connection)
		self._SendEmail(connection, to, subject, body)
		
	def AttachFile(self, filePath):
		self.attach.append(filePath)

	def _InitComm(self):
		try:
			# Browser
			br = mechanize.Browser()
			if self.proxies is not None:
				br.set_proxies(self.proxies)
				
			# Cookie Jar
			cj = cookielib.LWPCookieJar()
			br.set_cookiejar(cj)

			# Browser options
			br.set_handle_equiv(True)
			br.set_handle_redirect(True)
			br.set_handle_referer(True)
			br.set_handle_robots(False)

			# Follows refresh 0 but not hangs on refresh > 0
			br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

			# User-Agent (this is cheating, ok?)
			br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

			# The site we will navigate into, handling it's session
			br.open('http://gmail.com')
		except:
			traceback.print_stack()
			Log.Warning("Excepted while initializing connection")
			exit(1)
		
		return br
		
	def _Authenticate(self, connection):	
		try:
			br = connection
			# Select the first (index zero) form
			br.select_form(nr=0)

			# User credentials
			br.form['Email'] = self.email
			br.form['Passwd'] = self.password

			# Login
			br.submit()
		except:
			traceback.print_stack()
			Log.Warning("Excepted while authenticating connection")
			exit(1)
		
	def _SendEmail(self, connection, to, subject, body):
		try:
			br = connection
			#Enter without js enabled
			response = br.response().read()
			jsForm = None		
			forms = re.findall("\<form.*?\</form\>", response, re.I|re.M)
			for form in forms:
				if re.search("javascript", form, re.I) is not None:		
					jsForm = form
					break
					
			if jsForm:
				response = br.response()
				response.set_data(jsForm)
				br.set_response(response)
				br.select_form(nr=0)
				br.submit()
				
			#Select Write E-Mail
			link = br.links(text_regex="Escrever.*?e-mail").next()
			br.follow_link(link)
				
			#Attach files
			if len(self.attach) > 0:
			    br.select_form(predicate=lambda form: form.method == "POST")
			    br.submit(name="nvp_bu_amf")

			    br.select_form(predicate=lambda form: form.method == "POST")
			    for num, fileName in enumerate(self.attach):
				fieldName = 'file' + str(num + 1)
				br.form.add_file(open(fileName), "text/plain", fileName, fieldName)
			    br.submit()
			
			#Write Contents
			br.select_form(predicate=lambda form: form.method == "POST")
			br.form['bcc'] = ";".join(to)
			br.form['subject'] = subject
			br.form['body'] = body
			br.submit()
		except Exception as e:			
			traceback.print_stack()
			Log.Warning("Excepted while sending e-mail:" + str(e))
			raise
