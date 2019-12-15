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

def main():
    """
       MISSING DESCRIPTION
    """
    pass

if __name__ == "__main__":
    pass