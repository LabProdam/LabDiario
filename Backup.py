import re
import os
import shutil
import datetime

def Backup():
    """Backup last execution pickles"""
    bkpFolder = "bkp"
    bkpName = os.path.join(bkpFolder, 
			   datetime.datetime.now().isoformat().replace("-", "").replace(":", "").replace(".", ""))
    if not os.path.exists(bkpFolder):
	os.mkdir(bkpFolder)
    os.mkdir(bkpName)
    files = os.listdir(".")
    for file in files:
	if re.search("\.pk", file):
	    shutil.copy(file, bkpName)
