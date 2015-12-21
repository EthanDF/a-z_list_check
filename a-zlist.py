import csv
import urllib
import os
from urllib import request

import tkinter

root = tkinter.Tk()
root.withdraw()

baseURL = 'http://hx8vv5bf7j.search.serialssolutions.com/?V=1.0&L=HX8VV5BF7J&S=I_M&C='
nothingFound = '0 RECORDS RETRIEVED FOR THE SEARCH'

def checkISSN(vendorName, issn):
    """
    if the input has None, we default to assuming we've found the file, if we return a 0 result, we'll return no results
    we check the vendor name - it must be equal to "None" (cap-sensitive) in order to trigger the no vendor check
    otherwise, it will search for a match for the provided vendor name
    """

    # issn = '1544-0737'
    # vendorName = 'Sage'

    doUrl = baseURL+issn
    r = urllib.request.urlopen(doUrl)
    httpList = r.readlines()

    vendorFound = False

    if vendorName != "None":
        for l in httpList:
            if vendorName.upper() in l.decode().upper():
                vendorFound = True

    if vendorName == 'None':
        vendorFound = True
        for l in httpList:
            if nothingFound in l.decode().upper():
                vendorFound = False

    return vendorFound

def writeResults(resultString):
    resultsLog = 'Results.txt'
    with open(resultsLog, 'a') as x:
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
    with open(fileName, 'r') as c:
        reader = csv.reader(c)
        for row in reader:
            checkList.append(row)

    return checkList

def runCheck():


    print('running check...')
    checkList = readFile()

    for title in checkList:
        sys = title[0]
        journalTitle = title[1]
        vendorName = title[2]
        issn = title[3]

        result = checkISSN(vendorName, issn)
        resultString = str(sys)+'\t'+str(journalTitle)+'\t'+str(issn)+'\t'+str(vendorName)+'\t'+str(baseURL)+str(issn)+'\t'+str(result)
        writeResults(resultString)

    print('...done')
    input('press any key to launch the log file')
    os.system("start "+'Results.txt')

runCheck()







