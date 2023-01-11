""" Description: GENERAL helper methods
    Author(s): Sofia Kobayashi
    Date: 03/06/2022
"""


import requests
import datetime
from bs4 import BeautifulSoup
import csv

# ***    ERRORS    *** #
taggingError1 = "RELATIONSHIP_TAGGING_ERROR" # relationship without a / or &
taggingError2 = "CROSS_TAGGING_ERROR" # character in relationship not in character list
loadingError1 = "ERROR_404_Page_Not_Found"


# ***    HELPER METHODS FOR VARIOUS FILES    *** #
def cleanEdges(textBlock):
    """ Removes all linebreak and space characters from the very front and very
        back of given string. Returns a string.
        @param textBlock - string input to be cleaned
    """
    try:
        while (textBlock[0] == "\n" or textBlock[0] == " "):
            textBlock = textBlock[1:]
        while (textBlock[-1] == "\n" or textBlock[-1] == " "):
            textBlock = textBlock[:-1]
    except:
        pass
    return textBlock


def getSoupFromFile(htmlFileName):
    """Returns a BeautifulSoup instance from the given url."""
    htmlText = fileToString(htmlFileName)
    return BeautifulSoup(htmlText, "lxml")

def getSoup(url):
    """Returns a BeautifulSoup instance from the given url."""
    htmlText = requests.get(url).text
    return BeautifulSoup(htmlText, "lxml")


def doubleListToString(list):
    """Given a list  of [name, link], results a string of "name, name, name, etc."""
    results = ""
    count = 0
    for ele in list:
        results += ele[0] + ", "
        count +=len(ele[0])+2

        if count > 70:
            results += "\n"
            count = 0

    if results != "":
        results = results[:-2]

    return results



# ------ File Helper Methods ------ #
def fileToList(fileName, stopCase = "stopCase3stopCase2stopCase1"):
    """Gets all urls from given file & saves them to a list[] saveToList."""
    results = []
    fileUrls = open(fileName, "r")

    for url in fileUrls:
        if stopCase not in url:
            results.append(cleanEdges(url))
    fileUrls.close()

    return results


def listToFile(fileName, listToBeAdded, writeType = "a", wantHeader = False):
    """Appends (or creates a file) all elements from given list to given file."""
    # open file, get current date, and write header if wanted (Added: date)
    file = open(fileName, writeType)
    date = datetime.datetime.now()

    if wantHeader == True:
        file.write("------ Added: "+str(date)+" ------\n")

    # Appends list to file, each element gets its own line
    for line in listToBeAdded:
        file.write(line + "\n")
    file.close()

def csvToList(fileName, getIndex = -1):
    """Returns a list from the contents of a csv file."""
    results = []
    
    # opening a csv file reader
    with open(fileName, "r") as csvFile:
        listReader = csv.reader(csvFile)
        
        # reads & appends line in csv file to the list to be returned
        for line in listReader:
            if getIndex is not -1:
                line = line[getIndex]
            results.append(line)
    
    return results

def listToCsv(fileName, listToBeAdded, writeType = "a", seperator = ","):
    """Appends a list (probably of lists) to a CSV file."""
    # opening a csv writer
    with open(fileName, writeType) as newFile:
        csvWriter = csv.writer(newFile, delimiter=seperator)

        # appending/writing elements to csv file
        for element in listToBeAdded:
            csvWriter.writerow(element)

def getNewFile(inputFile, outputFile):
    fileInfo = fileToList(inputFile)
    results = []

    # for info in fileInfo:
    #     # sorting lines
    #     results.append(sortedInfo)

    listToCsv(outputFile, results)

def fileToString(fileName):
    html_text = ""
    file = open(fileName, "r")

    for line in file:
        html_text += line

    file.close()
    return html_text


def clearDuplicates(inputList, concreteList):
    """Returns a list (originally inputList) with all duplicates already in concreteList
    weeded out."""
    results = []
    for element in inputList:
        if element not in concreteList and element not in results:
            results.append(element)
        elif element in results:
            print(f"{element} was in the input list twice (maybe even 3 times).")
        elif element in concreteList:
            print(f"{element} is already in the concrete list!")
    
    return results