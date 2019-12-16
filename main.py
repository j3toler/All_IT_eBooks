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
@log_and_time
def slugify(string):
    """
       Normalizes string, converts to lowercase, removes non-alpha characters,
        and converts spaces to hyphens.
    """
    value = string[:]
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    value = unicode(re.sub('[-\s]+', '-', value))
    return value


@log_and_time
def getChoices():
    """
       Function takes no input, and returns a tuple of length 3.
       
       return_tuple[0] = <list>     # final choices of categories
       return_tuple[1] = <bool>     # verbose output
       return_tuple[2] = <bool>     # summary at end
       
       This function displays the list of available categories still left to be chosen,
        and prompts the user to either finish choosing or keep choosing categories.
       
       Additionally, asks the user if they would like to enable Verbose and/or Summary mode.
       
       [X] FUNCITONAL
       [_] UNDER CONSTRUCTION
       [*] COMPLETED TESTING
       
       * Manual testing completed. No Unit Testing has been done for this function.
    """
    all_choices = categories.keys()
    choices_deque = deque(all_choices)
    choices_final = []
    while len(choices_deque) != 2:
        system('cls')
        print "Please choose a category for download from the list"
        for i, category in enumerate(choices_deque):
            line = "{1: >{2}}.\t{0}".format(category, i, 2)
            print line

        try:
            choice = int(raw_input("Choice: "))
        except:
            choice = 0
        finally:
            valids = range(len(choices_deque))
            if choice not in valids:
                choice = 0

        if choice == 0:
            break

        selection = choices_deque[choice]
        if selection == "All":
            choices_final = all_choices[2:]
            break
        else:
            choices_final.append(selection)
            choices_deque.remove(selection)

    system('cls')

    verbose = raw_input("Would you like to make things more Verbose? (Y/n) ").strip()
    if len(verbose) == 0:
        verbose = True
    elif verbose[0].lower() == 'y':
        verbose = True
    else:
        verbose = False

    summary = raw_input("\nHow about a brief summary of the entries that did't work? (Y/n) ").strip()
    if len(summary) == 0:
        summary = True
    elif summary[0].lower() == 'y':
        summary = True
    else:
        summary = False

    return choices_final, verbose, summary


@log_and_time
def processEntry(entry):
    """
       MISSING DESCRIPTION
       
       [_] FUNCITONAL
       [_] UNDER CONSTRUCTION
       [_] COMPLETED TESTING
    """
    pass


@log_and_time
def processEntirePage(page, q):
    """
       Function takes a URL and a Queue as input, and returns True always.
       
       This function uses the requests library to get the HTML back from the 
        given URL and parses the information. Once properly parsed, it finds
        all of the <article> tags. This is where the information for the ebooks
        are held. Next up, it grabs a few items from the article and puts it in
        a dictionary:
         1. title
         2. small description
         3. next link
        
        Once it has these things, it appends it to a final list and passes 
        the list of dicts into a queue for later processing.

       page = <string>
       q = Queue()
       
       [/] FUNCITONAL
       [/] UNDER CONSTRUCTION
       [*] COMPLETED TESTING
       
       * Some manual testing has been done. No Unit tests have been made.
    """
    passed_values = []

    source = requests.get(page).text
    soup = bs(source, 'lxml')
    entries = soup.find_all('article')
    for entry in entries:
        contents = {"title": None, "small description": None, "next link": None}
        title = entry.h2.text
        contents['title'] = title
        small_description = unicodedata.normalize("NFKD", entry.p.text).encode('ascii', 'ignore')
        contents['small description'] = small_description
        next_link = entry.find('a', href=True)['href']
        contents['next link'] = next_link
        passed_values.append(contents)
    map(q.put, passed_values)
    return True


def main():
    """
       MISSING DESCRIPTION
       
       [_] FUNCITONAL
       [_] UNDER CONSTRUCTION
       [_] COMPLETED TESTING
    """
    pass


if __name__ == "__main__":
    pass