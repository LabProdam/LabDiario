#!/usr/bin/python
#coding: utf-8
from ChefeDeGabinete.Nomeacao import *
from ChefeDeGabinete.Exoneracao import *
from ChefeDeGabinete.Substituicao import *
from DiarioTools.Config import Configuration
from DiarioTools.GMailer import *
from DiarioTools.Log import *
import datetime
import sys

def HandleNomeacao(configInstance):
    searcher = SearchNomeacaoChefeDeGabinete(configInstance, True)
    parser = ParseNomeacaoChefeDeGabinete()
    processor = ProcessorNomeacaoChefeDeGabinete(configInstance, searcher, parser, "registroNomeacoes.log", "NomeacaoChefeDeGabinete")
    return processor.Process()

def HandleExoneracao(configInstance):
    searcher = SearchExoneracaoChefeDeGabinete(configInstance, True)
    parser = ParseExoneracaoChefeDeGabinete()
    processor = ProcessorExoneracaoChefeDeGabinete(configInstance, searcher, parser, "registroExoneracoes.log", "ExoneracaoChefeDeGabinete")
    return processor.Process()

def HandleSubstituicao(configInstance):
    searcher = SearchSubstituicaoChefeDeGabinete(configInstance, True)
    parser = ParseSubstituicaoChefeDeGabinete()
    processor = ProcessorSubstituicaoChefeDeGabinete(configInstance, searcher, parser, "registroSubstituicao.log", "SubstituicaoChefeDeGabinete")
    return processor.Process()

try:
    config = Configuration("config.xml", sys.argv) 
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


