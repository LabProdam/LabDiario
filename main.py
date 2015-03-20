#!/usr/bin/python
#coding: utf-8
from DiarioTools import Config
from DiarioTools.Log import Log
from DlSanity import *
import sys

import Backup
Backup.Backup()

def HandleSanity(configInstance):
    searcher = SearchSanity(configInstance, True)
    parser = ParseSanity()
    processor = ProcessorSanity(configInstance, searcher, parser, "SanityCheck.log", "SanityCheck")
    return processor.Process()

cfg = Config.Configuration("Config/config.xml", sys.argv)

if len(sys.argv) > 1 or HandleSanity(cfg):
	#Load and run modules present in config.xml
	for moduleName in cfg.modules:
	    Log.Log("Importing :" + moduleName)
	    module = __import__(moduleName, fromlist = ["main"])
	    module.main.Run(moduleName + ".log")
else:
	Log.Warning("Sanity Failed. Aborting")

