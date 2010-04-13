# -*- coding:utf-8 -*-

import logging
from django.conf import settings

def getlogger():
    logger = logging.getLogger()
    hdlr = logging.FileHandler(settings.LOG_FILE)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s') 
    
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    return logger

try:
    logger
except NameError:
    logger = getlogger()
