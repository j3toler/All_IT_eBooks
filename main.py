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
    import requests
    import logging
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


def main():
    """
       MISSING DESCRIPTION
    """
    pass

if __name__ == "__main__":
    pass