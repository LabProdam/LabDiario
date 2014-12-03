#!/usr/bin/python
#coding: utf-8
from ChefeDeGabinete import *

try:
    searcher = SearchChefeDeGabinete(True)
    parser = ParseChefeDeGabinete()
    processor = ProcessorChefeDeGabinete(searcher, parser, "registros.log", "ChefeDeGabinete")
    processor.Process()
except Exception as e:
    Log.Warning("Problemas encontrados durante a execução do script")
    Log.Warning(e)

