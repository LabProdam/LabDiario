#!/usr/bin/python
#coding: utf-8
from Prodam.Prodam import *
import datetime
import sys

def HandleNomeacao(configInstance):
    searcher = SearchProdam(configInstance, True)
    parser = ParseProdam()
    processor = ProcessorProdam(configInstance, searcher, parser, configInstance.logName, "Prodam")    
    return processor.Process()

config = Configuration("config.xml", sys.argv) 
Log.Log("Searching Nomeacoes")
messages = HandleNomeacao(config)

exit(0)

try:
    config = Configuration("config.xml", sys.argv) 
    Log.Log("Searching Prodam")
    messages = HandleNomeacao(config)
    
    if (config.mode == "alert mode"):
	messages = "Relatório de " + datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S") + "\r\n\r\n" + messages
	Log.Log("Enviando E-Mail")
	mailer = GMailerWrappper(config)    
	mailer.Send(messages)
except Exception as e:
    Log.Warning("Problemas encontrados durante a execução do script")
    Log.Warning(str(e))


