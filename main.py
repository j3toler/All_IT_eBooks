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


def worker(q):
    while not q.empty():
        entry = q.get()
        return_dict = processEntry(entry)
        q.task_done()


@log_and_time
def processEntry(entry_contents):
    """
       Takes a dictionary as input, and returns a dictionary as output.
       
       Honestly, the input/output shit is probably going to change soon.
        I've got an idea about making a database of the results, but that's for
        a later iteration. For now, I'm just going to move on from here...
       
       [X] FUNCITONAL
       [_] UNDER CONSTRUCTION
       [*] COMPLETED TESTING

       * Manual testing completed. No Unit Testing has been done for this function.
    """
    return_dict = {"title": None, "small description": None, "save result": None}
    title, small_description, next_link = entry_contents['title'], entry_contents["small description"], entry_contents["next link"]
    next_page = requests.get(next_link).text
    next_soup = bs(next_page, 'lxml')
    next_entry = next_soup.find('article')
    found = None
    for potential_link in next_entry.find_all('a', href=True):
        if re.match(pattern_PDF, potential_link['href']):
            found = potential_link['href']
            break
    if not found:
        return_dict["save result"] = False
        if SUMMARY:
            ERRORS.append(title)
        if VERBOSE:
            print(colorRED("[!] FILE NOT FOUND: " + title))
            print(small_break)
        logger.error("File Not Found: {}".format(title))
        return return_dict
    if VERBOSE:
        print(colorGREEN("File: " + found))
        print(small_break)
    fName = "{}.{}".format(slugify(title), 'pdf')
    pathDir = BASEPATH + fName
    if path.isfile(pathDir):
        if VERBOSE:
            print(colorYELLOW("[!] PDF already exists!"))
        logger.warning("File already exists: {}".format(title))
        return return_dict
    else:
        if VERBOSE:
            print(colorYELLOW("[_] Writing file to directory..."))
        try:
            r = requests.get(found, stream=True)
            if r.status_code == 404:
                ERRORS.append(title)
                if VERBOSE:
                    print(colorRED("File returned a 404: {}".format(title)))
                return_dict["save result"] = False
                logger.error("File returned a 404: {}".format(title))
                return return_dict
            with open(pathDir, 'wb') as fd:
                for chunk in r.iter_content(2048):
                    fd.write(chunk)
            return_dict['save result'] = True
            if VERBOSE:
                print(colorGREEN("[+] Wrote File to Directory"))
        except:
            if SUMMARY:
                ERRORS.append(title)
            if VERBOSE:
                print(colorRED("[!] Something went wrong..."))
            logger.error("Could not write to file: {}".format(title))
            return_dict['result'] = False
        finally:
            if VERBOSE:
                print_title = unicodedata.normalize("NFKD", title).encode('ascii', 'ignore')
                print("Title: {}".format(print_title))
                print("Small Description: {}".format(small_description))
                print(big_break)
            return return_dict


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
       
       [X] FUNCITONAL
       [_] UNDER CONSTRUCTION
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


@log_and_time
def main():
    """
       MISSING DESCRIPTION
       
       [X] FUNCITONAL
       [/] UNDER CONSTRUCTION
       [*] COMPLETED TESTING

       * Some manual testing has been done. No Unit tests have been made.
    """
    global VERBOSE
    global SUMMARY
    global ERRORS
    ERRORS = []
    MAX_THREADS = 20
    
    choices, VERBOSE, SUMMARY = getChoices()
    
    for category in choices:
        global BASEPATH
        BASEPATH = "C:\\tmp\\" + category + "\\"
        category_queue = Queue()

        try:
            makedirs(BASEPATH)
        except:
            logger.warning("Failed to create directories.")
            pass

        base_URL = "http://www.allitebooks.com/{}/page/".format(category.lower())
        max_page = categories[category]
        for page_number in range(1,max_page):
            target_page = base_URL + str(page_number) + "/"
            print "Target:", target_page
            processEntirePage(target_page, category_queue)
        
        for _ in range(MAX_THREADS):
            t = Thread(target=worker, args=(category_queue,))
            t.start()

        category_queue.join()

    if SUMMARY:
        system('pause')
        logger.info("Starting Summary")
        print("Now displaying errors...")
        for title in ERRORS:
            print(small_break)
            print(title)
        print(big_break)
        logger.info("Finished Summary")
    print("Finished!\nExiting...")
    return True


if __name__ == "__main__":
    main()