# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 15:38:10 2019

@author: Jay
"""


#################### Do some Imports ####################
try:
    from os import path, makedirs, system
    from bs4 import BeautifulSoup as bs
    from clint.textui import colored
    from collections import deque
    from threading import Thread
    from Queue import Queue
    import unicodedata
    import functools
    import requests
    import logging
    import time
    import re
except ImportError, e:
    print "Could not import all modules: %s" % str(e)
    exit(0)


#################### Set some Values ####################
pattern_PDF = "^http://file.allitebooks.com/.*\.pdf"
categories = {"Quit": None,
    "Web-Development": 190,
    "Programming": 173,
    "Datebases": 91,
    "Graphics-Design": 32,
    "Operating-Systems": 76,
    "Networking-Cloud-Computing": 73,
    "Administration": 24,
    "Certification": 18,
    "Computers-Technology": 26,
    "Enterprise": 18,
    "Game-Programming": 33,
    "Hardware": 35,
    "Marketing-SEO": 7,
    "Security": 19,
    "Software": 40,
    "All": None}
small_break = "-----------------------------------"
big_break = "==================================="
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = ".\\run.log",
                    level = logging.DEBUG,
                    format = LOG_FORMAT,
                    filemode = 'w')
logger = logging.getLogger()


#################### Define some Colors ####################
def colorRED(text):
    """
       returns the string of text in the color RED

       input <string>
       output <string>
    """
    return colored.red(text)


def colorGREEN(text):
    """
       returns the string of text in the color GREEN

       input <string>
       output <string>
    """
    return colored.green(text)


def colorYELLOW(text):
    """
       returns the string of text in the color YELLOW

       input <string>
       output <string>
    """
    return colored.yellow(text)


#################### Define Logging Decorator #################
def log_and_time(func):
    """
       This decorator is used to log the arguments passed to the function, 
        as well as the time it takes to complete.
    """
    @functools.wraps(func)
    def wrapper_timing(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = ["{}={}".format(k,v) for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logger.info("Started the function {}({}).".format(func.__name__, signature))
        start_time = time.time()
        vals = func(*args, **kwargs)
        end_time = time.time()
        run_time = end_time - start_time
        logger.info("Finished the function '{}' in {:.4f} secs".format(func.__name__, run_time))
        return vals
    return wrapper_timing


#################### Define some Functions ####################
def main():
    """
       MISSING DESCRIPTION
    """
    pass


if __name__ == "__main__":
    pass