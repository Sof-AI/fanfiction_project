import time # uses perf_counter
from Fic import ArchiveFic
from bs4 import BeautifulSoup
from GreaterMethods import getMetaInfo, getTags, getStats
from helperMethods import fileToList, listToFile, getSoup, fileToString, getSoupFromFile
import csv

# ------ Archive-Involved Helper Methods ------#
def getAo3Tag(url, type):
    """Returns the 'ending part' of url given a type: /users/, /collections/, or /tags/"""
    start = url.find(type) + len(type)
    return url[start:]

def getAo3TagEnd(url, type):
    """Returns the 'ending part' of url given a type: /users/, /collections/, or /tags/"""
    start = url.find(type) + len(type)
    end = url[start:].find("/")
    return url[start:][:end]

def getAo3Num(url, type):
    """Returns  AO3 id/fic number from the given url, given type: /works/ or /series/"""
    start = url.find(type) + len(type)
    if "/" in url[start:]:
        end = url.find("/", start)
        return url[start:end]
    return url[start:]

def getAo3NumFromFile(fileName):
    htmlText = fileToString(fileName)
    soup = BeautifulSoup(htmlText, "lxml")
    url = soup.find("p", class_="message").find_all("a")
    url = url[1].text
    start = url.find("/works/") + len("/works/")
    if "/" in url[start:]:
        end = url.find("/", start)
        return url[start:end]
    return url[start:]

def makeFicFromNum(archiveFicNum):
    """Returns a dict representation of the fic."""
    url = "https://archiveofourown.org/works/"+archiveFicNum
    soup = getSoup(url)

    # title, authors, summary, associations, frontNotes, endNotes, worksInspired, site
    metaInfo = getMetaInfo(soup) 
    # rating, warnings, romanticCats, fandoms, relationships, characters, moreTags, language, series, collections
    tags = getTags(soup)
    # publishDate, completeDate, numWords, numCharacters, totalChapters, numComments, numKudos, numBookmarks, numHits
    stats = getStats(soup)
    
    return {"metaInfo": metaInfo,
            "tags": tags,
            "stats": stats}




# ------ Archive URL Methods ------#
def sortUrlBySite(inputUrlList, runoff):
    """Given a list of URLs, returns list of AO3-links, appends other links to runoff."""
    results = []
    
    # sorts URLS into AO3 or other
    for url in inputUrlList:
        if "archiveofourown.org" in url:
            results.append(url)
        else:
            runoff.append(url)

    return results


def getFicNumList(inputUrlList, runoff):
    """Given a list of URLs, returns list of AO3 ficNums, appends other URLs to runoff."""
    results = []
    
    # sorts URLS into AO3 or other
    for url in inputUrlList:
        if "https://archiveofourown.org/works/" in url:
            results.append(getAo3Num(url, "/works/"))
        else:
            runoff.append(url)

    return results


def sortAo3Urls(inputArchiveUrlList):
    """Returns dict of sorted AO3 URLS"""
    ao3Types = {"works": [], # will be a number
            "users": [], # will be "name/pseuds/..."
            "series": [], # will be a number
            "collections": [], # will be "collection_name"
            "tags": [], #will be "certain%20tag"
            "other": [] # will be a URL
            }
        
    # sorts URLS into correct AO3 type
    for url in inputArchiveUrlList:
        if "/works/" in url:
            ao3Types["works"].append(getAo3Num(url, "/works/"))
        elif "/series/" in url:
            ao3Types["series"].append(getAo3Num(url, "/series/"))
        elif "/users/" in url:
            ao3Types["users"].append(getAo3Tag(url, "/users/"))
        elif "/collections/" in url:
            ao3Types["collections"].append(getAo3Tag(url, "/collections/"))
        elif "/tags/" in url:
            ao3Types["tags"].append(getAo3Tag(url, "/tags/"))
        else:
            ao3Types["other"].append(url)

    return ao3Types



# ------ Archive File Methods ------#
def csvToFicDict(csvFileName):
    """Returns a fic-dict populated from given fic-csvFile."""
    resultDict = {}
    
    with open(csvFileName, "r") as csvFile: # open file
        reader = csv.reader(csvFile) # initiate reader
        header = next(reader) # get fieldnames
        
        # read each row so it is in form: {ele1: {ele2: "", ele3: "", ...}, ele1: {ele2: "", ele3: "", ...}, ...}
        for row in reader:
            resultDict[row[0]] = {}
            for i, key in enumerate(header):
                resultDict[row[0]].update({key: row[i]})


def updateStorage(fileToBeAdded):
    """Update other & archive txt files with given file of URLs."""
    # get all urls from a file to a list
    allUrls = fileToList(fileToBeAdded)

    # sort urls into archiveUrls and otherUrls
    otherUrls = []
    archiveUrls = sortUrlBySite(allUrls, otherUrls)

    # write all other urls into a file
    listToFile(otherUrls, "STORAGE/otherUrls.txt")

    # write all archive urls into a file
    listToFile(archiveUrls, "STORAGE/archiveUrls.txt")



# ------ archiveFic Object Methods ------#
def isArchive404(ao3FicNum):
    """Returns boolean - checks if ficNum is an Error 404"""
    # gets HTML text of URL
    soup = getSoup("https://archiveofourown.org/works/"+ao3FicNum)
    
    # checks if there's a Error 404
    error = soup.find("h2", class_="heading")
    if error != None:
        if error.text == "Error 404":
            return True
    
    return False

def makeAo3FicArray(ao3FicNumList, saveListArchiveObjs):
    """Makes all ficNums in given list into ArchiveFic objects and saves them to saveToList. 
    Returns a list[] of all the ficNums that gave an error."""
    count = 0
    runoff = []

    # try to make all ficNums into ArchiveFic objects
    for index, ficNum in enumerate(ao3FicNumList):
        print(f"{index}: adding {ficNum}")
        try: 
            # start of runtime timer
            tic = time.perf_counter()

            # make ficNum into ArchiveObject and save it to list
            saveListArchiveObjs.append(ArchiveFic(ficNum, count))
            print(f"    {saveListArchiveObjs[count].intro()}")
            count +=1

            # end of runtime timer
            toc = time.perf_counter()
            print(f"    [RUNTIME] Fic Creation in {toc - tic:0.4f} seconds")
        
        # if there's an error, add URL to runoff list
        except:
            print(f"ERROR_Undetermined")
            runoff.append(ficNum)

    return runoff
