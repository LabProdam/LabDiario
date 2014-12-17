#!/usr/bin/python
#coding: utf-8
from NomeacaoChefeDeGabinete import *
from ExoneracaoChefeDeGabinete import *
from SubstituicaoChefeDeGabinete import *
from DiarioTools.Config import Configuration
from DiarioTools.ProdamMailer import *

def HandleNomeacao(configInstance):
    searcher = SearchNomeacaoChefeDeGabinete(True)
    parser = ParseNomeacaoChefeDeGabinete()
    processor = ProcessorNomeacaoChefeDeGabinete(configInstance, searcher, parser, "registroNomeacoes.log", "NomeacaoChefeDeGabinete")
    return processor.Process()

def HandleExoneracao(configInstance):
    searcher = SearchExoneracaoChefeDeGabinete(True)
    parser = ParseExoneracaoChefeDeGabinete()
    processor = ProcessorExoneracaoChefeDeGabinete(configInstance, searcher, parser, "registroExoneracoes.log", "ExoneracaoChefeDeGabinete")
    return processor.Process()

def HandleSubstituicao(configInstance):
    searcher = SearchSubstituicaoChefeDeGabinete(True)
    parser = ParseSubstituicaoChefeDeGabinete()
    processor = ProcessorSubstituicaoChefeDeGabinete(configInstance, searcher, parser, "registroSubstituicao.log", "SubstituicaoChefeDeGabinete")
    return processor.Process()

import os
try:
    config = Configuration("config.xml")
    messages = HandleNomeacao(config)
    messages += HandleExoneracao(config)
    messages += HandleSubstituicao(config)

    mailer = ProdamMailer(config)    
    mailer.Send(messages)

except Exception as e:
    Log.Warning("Problemas encontrados durante a execução do script")
    Log.Warning(str(e))


