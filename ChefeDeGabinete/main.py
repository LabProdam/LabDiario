#!/usr/bin/python
#coding: utf-8
from Nomeacao import *
from Exoneracao import *
from Substituicao import *
from DiarioTools.Config import Configuration
from DiarioTools.GMailer import *
from DiarioTools.Log import *
import datetime
import sys
import os

logName = "Default.log"

def HandleNomeacao(configInstance):
    searcher = SearchNomeacaoChefeDeGabinete(configInstance, True)
    parser = ParseNomeacaoChefeDeGabinete()
    processor = ProcessorNomeacaoChefeDeGabinete(configInstance, searcher, parser, logName, "NomeacaoChefeDeGabinete")
    return processor.Process()

def HandleExoneracao(configInstance):
    searcher = SearchExoneracaoChefeDeGabinete(configInstance, True)
    parser = ParseExoneracaoChefeDeGabinete()
    processor = ProcessorExoneracaoChefeDeGabinete(configInstance, searcher, parser, logName, "ExoneracaoChefeDeGabinete")
    return processor.Process()

def HandleSubstituicao(configInstance):
    searcher = SearchSubstituicaoChefeDeGabinete(configInstance, True)
    parser = ParseSubstituicaoChefeDeGabinete()
    processor = ProcessorSubstituicaoChefeDeGabinete(configInstance, searcher, parser, logName, "SubstituicaoChefeDeGabinete")
    return processor.Process()

def Run(localLogName = "Default.log"):
    global logName
    logName = localLogName

    try:
	config = Configuration(os.path.join("Config","config.xml"), sys.argv, logName) 
	config.AppendConfigurationFile(os.path.join("Config","chefesdegabinete.xml"))
	Log.Log("Searching Nomeacoes")
	messages = HandleNomeacao(config)
	Log.Log("Searching Exoneracoes")
	messages += HandleExoneracao(config)
	Log.Log("Searching Substituicoes")
	messages += HandleSubstituicao(config)

	if (config.mode == "alert mode"):
	    messages = "Relatório de " + datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S") + "\r\n\r\n" + messages
	    Log.Log("Enviando E-Mail")
	    mailer = GMailerWrappper(config)    
	    mailer.Send(messages)
    except Exception as e:
	Log.Warning("Problemas encontrados durante a execução do script")
	Log.Warning(str(e))
