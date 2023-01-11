""" Description: All the higher-level methods to be used
    Author(s): Sofia Kobayashi
    Date: 03/06/2022
    https://beautiful-soup-4.readthedocs.io/en/latest/
    Table of Contents: 
        Helper Methods
        Greater Methods
        Testing
"""
from getMetaInfoMethods import *
from getTagsMethods import *
from getStatsMethods import *
from helperMethods import *
from bs4 import BeautifulSoup
import requests

# ***    HELPER METHODS    *** #
def addCharacterFromRelationship(charaPairs, relationships):
    """If a character is in a relationship, but not the characters list, add character to list [charater, "-1"]."""
    characters = []
    for pair in charaPairs:
        characters.append(pair[0])
    
    # print(f"INITIAL: {characters}")
    for relationship in relationships:
        if taggingError1 not in relationship:
            for i in range(1,len(relationship)):
                if relationship[i] not in characters:
                    characters.append([f"{taggingError2} {relationship[i]}","-1"])
                    # print(f"Added {relationship[i]}")

    # print(f"FINAL: {characters}")



# ***    GREATER METHODS    *** #
def getMetaInfo(soup):
    """Calls all get methods for metaInfo{} on given URL. Returns a python dict{}."""
    preface = soup.find("div", class_="preface group")
    metaInfo = {}

    metaInfo["title"] = getTitle(preface)
    metaInfo["authors"] = getAuthors(preface)
    metaInfo["summary"] = getSummary(preface)
    metaInfo["associations"] = getAssociations(preface)
    metaInfo["frontNotes"] = getFrontNotes(soup)
    metaInfo["endNotes"] = getEndNotes(soup)
    metaInfo["worksInspired"] = getWorksInspired(soup)
    metaInfo["site"] = "ao3"
    
    return metaInfo


def getTags(soup):
    """Calls all get methods for metaInfo{} on given URL. Returns a python dict{}."""
    wrapper = soup.find("div", class_="wrapper")
    tags = {}

    tags["rating"] = getRating(wrapper)
    tags["warnings"] = getWarnings(wrapper)
    tags["romanticCats"] = getRomanticCats(wrapper)
    tags["fandoms"] = getFandoms(wrapper)
    tags["relationships"] = getRelationships(wrapper)
    tags["characters"] = getCharacters(wrapper)
    tags["moreTags"] = getMoreTags(wrapper)
    tags["language"] = getLanguage(wrapper)
    tags["series"] = getSeries(wrapper)
    tags["collections"] = getCollections(wrapper)
    addCharacterFromRelationship(tags["characters"], tags["relationships"])

    return tags


def getStats(soup):
    """Calls all get methods for metaInfo{} on given URL. Returns a python dict{}."""
    statSection = soup.find("dl", class_="stats")
    stats = {}

    stats["publishDate"] = getPublishDate(statSection)
    stats["completeDate"] = getCompleteDate(statSection)
    stats["numWords"] = getNumWords(statSection)
    stats["numChapters"] = getNumChapters(statSection)
    stats["totalChapters"] = getTotalChapters(statSection)
    stats["numComments"] = getNumComments(statSection)
    stats["numKudos"] = getNumKudos(statSection)
    stats["numBookmarks"] = getNumBookmarks(statSection)
    stats["numHits"] = getNumHits(statSection)

    return stats

    
# # ***    TESING    *** #
# print()
# print("------")
# soup = getSoup("https://archiveofourown.org/works/10453449")
# stats = getStats(soup)
# print(f"-{stats['completeDate']}-")

# htmlText = requests.get("https://archiveofourown.org/works/32361358/chapters/80227150").text
# soup = BeautifulSoup(htmlText, "lxml")
# getTags(soup)

# # for data in test:
# #     print(f"{data.upper()}: {test[data]}")

# print("------")
# print()