#!/usr/bin/python
#coding: utf-8
from ChefeDeGabinete.Nomeacao import *
from ChefeDeGabinete.Exoneracao import *
from ChefeDeGabinete.Substituicao import *
from DiarioTools.Config import Configuration
from DiarioTools.ProdamMailer import *
import sys

def HandleNomeacao(configInstance):
    searcher = SearchNomeacaoChefeDeGabinete(configInstance, True)
    parser = ParseNomeacaoChefeDeGabinete()
    processor = ProcessorNomeacaoChefeDeGabinete(configInstance, searcher, parser, configInstance.logName, "NomeacaoChefeDeGabinete")
    return processor.Process()

def HandleExoneracao(configInstance):
    searcher = SearchExoneracaoChefeDeGabinete(configInstance, True)
    parser = ParseExoneracaoChefeDeGabinete()
    processor = ProcessorExoneracaoChefeDeGabinete(configInstance, searcher, parser, configInstance.logName, "ExoneracaoChefeDeGabinete")
    return processor.Process()

def HandleSubstituicao(configInstance):
    searcher = SearchSubstituicaoChefeDeGabinete(configInstance, True)
    parser = ParseSubstituicaoChefeDeGabinete()
    processor = ProcessorSubstituicaoChefeDeGabinete(configInstance, searcher, parser, configInstance.logName, "SubstituicaoChefeDeGabinete")
    return processor.Process()

import os
try:
    config = Configuration("config.xml", sys.argv)    
    Log.Log("Procurando Nomeacoes")
    messages = HandleNomeacao(config)
    Log.Log("Procurando Exoneracoes")
    messages += HandleExoneracao(config)
    Log.Log("Procurando Substituicoes")
    messages += HandleSubstituicao(config)

    if (config.mail and config.mode == "alert mode"):
	Log.Log("Enviando E-Mail")
	mailer = ProdamMailer(config)
	mailer.Send(messages)
except Exception as e:
    Log.Warning("Problemas encontrados durante a execução do script")
    Log.Warning(str(e))


