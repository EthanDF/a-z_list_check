import csv
import urllib
import os
import codecs
import unicodedata
from urllib import request

import tkinter

root = tkinter.Tk()
root.withdraw()

baseURL = 'http://hx8vv5bf7j.search.serialssolutions.com/?V=1.0&L=HX8VV5BF7J&S=I_M&C='
nothingFound = 'Sorry, this search returned no results'

def checkISSN(vendorName, issn, startDate, endDate):
    """
    if the input has None, we default to assuming we've found the file, if we return a 0 result, we'll return no results
    we check the vendor name - it must be equal to "None" (cap-sensitive) in order to trigger the no vendor check
    otherwise, it will search for a match for the provided vendor name
    """

    # issn = '1544-0737'
    # vendorName = 'Sage'

    if len(issn) == 9:
        doUrl = baseURL+str(issn)
    else:
        doUrl = str(issn)

    # for debugging
    # print(doUrl)

    r = urllib.request.urlopen(doUrl)
    httpList = r.readlines()

    vendorFound = False

    if vendorName != "None":
        # print('vendorName is not None')
        for l in httpList:
            if vendorName.upper() in l.decode().upper():
                vendorFound = True

    if vendorName == 'None' or vendorName == '' or vendorName == 'xxxx':
        # print('vendorName is None')
        vendorFound = True
        for l in httpList:
            if nothingFound.upper() in l.decode().upper():
                vendorFound = False

    startDatesMatch = False
    if startDate is not None:
        for l in httpList:
            if startDate in l.decode():
                startDatesMatch = True

    endDatesMatch = False
    if endDate is not None:
        for l in httpList:
            if endDate in l.decode():
                endDatesMatch = True


    return [vendorFound, startDatesMatch, endDatesMatch]

def writeResults(resultString):
    resultsLog = 'Results.txt'
    with codecs.open(resultsLog, 'a', encoding='utf-8') as x:
        x.write(resultString+'\n')

def readFile():
    """
    Create a csv file with:
    alephbib, title, vendor, issn, any other columns are fine but won't be read
    """
    input('press any key to choose the input csv file...')

    from tkinter import filedialog
    csvPath = tkinter.filedialog.askopenfile()
    fileName = csvPath.name

    print('thanks! got it!\nrunning...')


    checkList = []
    with open(fileName, 'r', encoding='utf-8') as c:
        reader = csv.reader(c)
        for row in reader:
            # for debugging
            # print(row)
            checkList.append(row)

    return checkList

def runCheck():


    print('running check...')
    checkList = readFile()

    for title in checkList:
        sys = title[0]
        journalTitle = title[1]
        vendorName = title[2]
        issn = str(title[3]).rstrip()

        try:
            startdate = title[4]
            enddate = title[5]
        except IndexError:
            startdate = None
            enddate = None


        result = checkISSN(vendorName, str(issn), startdate, enddate)
        vendorFound = result[0]

        if startdate is not None:
            startdateFound = result[1]
            enddateFound = result[2]
        else:
            startdateFound = "None"
            enddateFound = "None"

        resultURL = ''

        # for printing purposes only, set the result URL. If provided an ISSN, print full URL+ISSN
        # , otherwise, just provided URL

        if len(issn) == 9:
            # for debugging
            # print('using ISSN, '+str(issn))
            resultURL = baseURL + str(issn)
        else:
            # for debugging
            # print('using full URL provided, '+str(issn))
            resultURL = str(issn)

        vendorFound = result[0]

        resultString = str(sys) + '\t' + str(journalTitle) + '\t' + str(vendorName) + '\t' + str(issn) + '\t' +str(startdate)+ '\t' +str(enddate)+ '\t' + resultURL + '\t' + str(vendorFound)+ '\t' + str(startdateFound)+ '\t' + str(enddateFound)
        # print(resultString)
        writeResults(resultString)

    print('...done')
    input('press any key to launch the log file')
    os.system("start "+'Results.txt')

runCheck()







