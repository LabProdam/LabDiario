#!/usr/bin/python
#coding: utf-8
from ChefeDeGabinete import *

searcher = SearchChefeDeGabinete("Gabinete")
parser = ParseChefeDeGabinete()
processor = ProcessorChefeDeGabinete(searcher, parser, "registros.log", "ChefeDeGabinete")
processor.Process()


