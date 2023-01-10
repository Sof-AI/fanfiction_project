""" Description: All the getStats{} methods
    Author(s): Sofia Kobayashi
    Date: 03/06/2022
    https://beautiful-soup-4.readthedocs.io/en/latest/
    Table of Contents: 
        Methods to get tags{}
        Testing
"""
from helperMethods import *
from bs4 import BeautifulSoup
import requests


# ***    METHODS TO GET TAGS{}    *** #
def getPublishDate(statSection):
    """Gets fic's published date. Returns a string."""
    date = statSection.find("dd", class_="published").text
    return date

def getCompleteDate(statSection):
    """Gets fic's TAG. Returns a SOMETHING."""
    # get total number of chapters
    totalChapters = statSection.find("dd", class_="chapters").text.split("/")
    if int(totalChapters[0]) == 1:
        return (statSection.find("dd", class_="published").text) #publish date
    else:
        results = ""
        date = statSection.find("dd", class_="status")
        if date != None:
            results = date.text
        
        return results

def getNumWords(statSection):
    """Gets fic's word count. Returns an int."""
    result = 0
    num = statSection.find("dd", class_="words")
    if num != None:
        result = int(num.text)

    return result

def getNumChapters(statSection):
    """Gets fic's current number of chapters. Returns an int."""
    num = statSection.find("dd", class_="chapters").text.split("/")
    return int(num[0])

def getTotalChapters(statSection):
    """Gets fic's total chapters. Returns a string."""
    num = statSection.find("dd", class_="chapters").text.split("/")
    return num[1]

def getNumComments(statSection):
    """Gets fic's comment count. Returns an int."""
    result = 0
    num = statSection.find("dd", class_="comments")
    if num != None:
        result = int(num.text)

    return result

def getNumKudos(statSection):
    """Gets fic's kudos count. Returns an int."""
    result = 0
    num = statSection.find("dd", class_="kudos")
    if num != None:
        result = int(num.text)

    return result

def getNumBookmarks(statSection):
    """Gets fic's bookmark count. Returns an int."""
    result = 0
    num = statSection.find("dd", class_="bookmarks")
    if num != None:
        result = int(num.text)

    return result

def getNumHits(statSection):
    """Gets fic's hits count. Returns an int."""
    result = 0
    num = statSection.find("dd", class_="hits")
    if num != None:
        result = int(num.text)

    return result



# ***    TESTING    *** #
# print()
# print("------------")

# # Get HTML text from AO3 fic
# htmlText = requests.get("https://archiveofourown.org/works/11802984").text
# soup = BeautifulSoup(htmlText, "lxml")
# statSection = soup.find("dl", class_="stats")

# # Declare tags dict
# stats = {}

# # TESTING AREA (uncomment some)
# stats["publishDate"] = getPublishDate(statSection)
# stats["completeDate"] = getCompleteDate(statSection)
# stats["numWords"] = getNumWords(statSection)
# stats["numChapters"] = getNumChapters(statSection)
# stats["totalChapters"] = getTotalChapters(statSection)
# stats["numComments"] = getNumComments(statSection)
# stats["numKudos"] = getNumKudos(statSection)
# stats["numBookmarks"] = getNumBookmarks(statSection)
# stats["numHits"] = getNumHits(statSection)

# # print results
# for data in stats:
#     print(f"-{data.upper()}: {stats[data]}")

# print("------------")
# print()