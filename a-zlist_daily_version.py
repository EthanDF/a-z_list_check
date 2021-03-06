import csv
import urllib
import os
import codecs
from urllib import request
import datetime

# import tkinter

# root = tkinter.Tk()
# root.withdraw()

baseURL = 'http://hx8vv5bf7j.search.serialssolutions.com/?V=1.0&L=HX8VV5BF7J&S=I_M&C='
nothingFound = 'Sorry, this search returned no results'
fileName = 'z:\\FenichelE\\a-zList\\a-z_list_daily_check.csv'
resultsLog = 'Z:\\FenichelE\\A-ZList\\Results.txt'
emailFile = 'Z:\\FenichelE\\A-ZList\\emailConfig.txt'

# userLogin = 'fenichele@fau.edu'

def checkISSN(vendorName, issn):
    """
    if the input has None, we default to assuming we've found the file, if we return a 0 result, we'll return no results
    we check the vendor name - it must be equal to "None" (cap-sensitive) in order to trigger the no vendor check
    otherwise, it will search for a match for the provided vendor name
    """

    # issn = '1544-0737'
    # vendorName = 'Sage'

    if len(issn) == 9:
        # for debugging
        # print('using ISSN, '+str(issn))
        doUrl = baseURL+str(issn)
    else:
        # for debugging
        # print('using full URL provided, '+str(issn))
        doUrl = str(issn)

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

    return vendorFound

def wipeResults():
    with open(resultsLog, 'w') as x:
        x.write('')

def writeResults(resultString):
    with codecs.open(resultsLog, 'a', encoding='utf-8') as x:
        x.write(resultString+'\n')

def getEmails():

    toaddr = []
    with open(emailFile, 'r') as l:
        for line in l:
            toaddr.append(line.strip('\n'))
    return toaddr


def sendEmail(hasResults):
    emailList = getEmails()

    import smtplib
    server = smtplib.SMTP('smtp.fau.edu')

    server.ehlo()
    # server.starttls()
    # server.ehlo()

    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    fromaddr = "fenichele@fau.edu"
    toaddr = emailList
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = ", ".join(toaddr)
    msg['Subject'] = str(datetime.date.today().isoformat()).replace('-', '')+" A-Z List Update"

    body = ''
    if hasResults is True:
        body = "A-Z results finished today\nInput File (ISSNs) may be found at: \n" + fileName + "\n\nResults may be found at: \n"+resultsLog
    elif hasResults is False:
        body = "A-Z results finished today.\nInput File (ISSNs) may be found at \n" + fileName + "\n\nThere were no results.\n\nHave a great day!!!"
    msg.attach(MIMEText(body, 'plain'))

    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, msg.as_string())

def readFile():
    """
    Create a csv file with:
    alephbib, title, vendor, issn, any other columns are fine but won't be read
    """
    # input('press any key to choose the input csv file...')

    from tkinter import filedialog
    # csvPath = tkinter.filedialog.askopenfile()
    # fileName = csvPath.name

    # print('thanks! got it!\nrunning...')


    checkList = []
    with open(fileName, 'r') as c:
        reader = csv.reader(c)
        for row in reader:
            checkList.append(row)

    return checkList

def runCheck():


    # print('running check...')
    checkList = readFile()

    trueResult = False

    for title in checkList:
        sys = title[0]
        journalTitle = title[1]
        vendorName = title[2]
        issn = str(title[3]).rstrip()

        result = checkISSN(vendorName, str(issn))
        if result is True:
            trueResult = True

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

        resultString = str(sys)+'\t'+str(journalTitle)+'\t'+str(vendorName)+'\t'+str(issn)+'\t'+resultURL+'\t'+str(result)
        # print(resultString)
        writeResults(resultString)

    print('...done')
    if trueResult is False:
        sendEmail(trueResult)
        wipeResults()
        # wipeIt = input('there were no "True" results... press "y" to wipe the log, otherwise, press any other key to open the log\n')
        # if wipeIt == 'y':
        #     wipeResults()
        # else:
            # os.system("start " + 'Results.txt')
    else:
        sendEmail(trueResult)
        # input('There was at least 1 "True" result, press any key to launch the log file\n')
        # os.system("start "+resultsLog)

runCheck()







