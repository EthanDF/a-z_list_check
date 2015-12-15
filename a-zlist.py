import csv
import urllib
import os
from urllib import request

import tkinter

root = tkinter.Tk()
root.withdraw()

baseURL = 'http://hx8vv5bf7j.search.serialssolutions.com/?V=1.0&L=HX8VV5BF7J&S=I_M&C='

def checkISSN(vendorName, issn):

    # issn = '1544-0737'
    # vendorName = 'Sage'

    doUrl = baseURL+issn
    r = urllib.request.urlopen(doUrl)
    httpList = r.readlines()

    vendorFound = False

    for l in httpList:
        if vendorName.upper() in l.decode().upper():
            vendorFound = True

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
    print('thanks! got it!\nrunning...')

    from tkinter import filedialog
    csvPath = tkinter.filedialog.askopenfile()
    fileName = csvPath.name


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







