#!/usr/bin/python
#coding: utf-8
from DiarioTools import Config
from DiarioTools.Log import Log
import sys


cfg = Config.Configuration("Config/config.xml", sys.argv)
#Load and run modules present in config.xml
for moduleName in cfg.modules:
    Log.Log("Importing :" + moduleName)
    module = __import__(moduleName, fromlist = ["main"])
    module.main.Run()
