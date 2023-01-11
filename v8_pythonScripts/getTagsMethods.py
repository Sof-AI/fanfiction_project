""" Description: All the getTags{} methods
    Author(s): Sofia Kobayashi
    Date: 03/05/2022
    https://beautiful-soup-4.readthedocs.io/en/latest/
    Table of Contents: 
        Helper Methods
        Methods to get tags{}
        Testing
"""
from helperMethods import *
from bs4 import BeautifulSoup
import requests

# ***    HELPER METHODS    *** #
def splitCharacters(splitter, relationship):
    """Helper method for getRelationships(), splits characters & determines type 
        of relationship. Returns a python array of strings 
        [relationshipType, char1, char2, char3, etc.]."""
    results = []
    
    if splitter == "/":
        results.append("romantic")
    elif splitter == "&":
        results.append("platonic")
    
    characters = relationship.split(splitter)
    for character in characters:
        results.append(cleanEdges(character))

    return results


# ***    METHODS TO GET TAGS{}    *** #
def getRating(wrapper):
    """Gets fic's rating. Returns a string."""
    rating = wrapper.find("dd", class_="rating tags").find("a").text
    return rating

def getWarnings(wrapper):
    """Gets fic's warnings. Returns a python list."""
    results = []
    tagsList = wrapper.find("dd", class_="warning tags")

    if tagsList != None:
        tagsList = tagsList.find_all("a")
        for tag in tagsList:
            results.append(tag.text)

    return results

def getRomanticCats(wrapper):
    """Gets fic's romantic categories. Returns a python list."""
    results = []
    tagsList = wrapper.find("dd", class_="category tags")

    if tagsList != None:
        tagsList = tagsList.find_all("a")
        for tag in tagsList:
            results.append(tag.text)

    return results

def getFandoms(wrapper):
    """Gets fic's fandom(s). Returns a python list."""
    results = []
    tagsList = wrapper.find("dd", class_="fandom tags")

    if tagsList != None:
        tagsList = tagsList.find_all("a")
        for tag in tagsList:
            results.append([tag.text, tag["href"]])

    return results

def getRelationships(wrapper):
    """Gets fic's relationship(s). Returns a python list of strings."""
    results = []
    tagsList = wrapper.find("dd", class_="relationship tags")

    if tagsList != None:
        tagsList = tagsList.find_all("a")
        for tag in tagsList:
            if "/" in tag.text:
                results.append(splitCharacters("/", tag.text))
            elif "&" in tag.text:
                results.append(splitCharacters("&", tag.text))
            else:
                results.append([f"{taggingError1}: {tag.text}", tag["href"]])

    return results

def getCharacters(wrapper):
    """Gets fic's characters. Returns a python list."""
    results = []
    tagsList = wrapper.find("dd", class_="character tags")

    if tagsList != None:
        tagsList = tagsList.find_all("a")
        for tag in tagsList:
            results.append([tag.text, tag["href"]])

    return results

def getMoreTags(wrapper):
    """Gets fic's additional tags. Returns a python list."""
    results = []
    tagsList = wrapper.find("dd", class_="freeform tags")

    if tagsList != None:
        tagsList = tagsList.find_all("a")
        for tag in tagsList:
            results.append(tag.text)

    return results

def getLanguage(wrapper):
    """Gets fic's language. Returns a string."""
    lang = wrapper.find("dd", class_="language").text.replace("  ", "").replace("\n", "")
    return lang

def getSeries(wrapper):
    """Gets fic's series. Returns a python list of strings [[partNum, seriesName]]."""
    results = []
    tagsList = wrapper.find("dd", class_="series")

    if tagsList != None:
        
        tagsList = tagsList.find_all("span", class_="position")
        for tag in tagsList:
            # split entire "Part 29 of the 100 Prompts Challenge series", get [1] of it
            part = tag.text.split()
            results.append([part[1], tag.a.text])

    return results

def getCollections(wrapper):
    """Gets fic's collections. Returns a python list."""
    results = []
    tagsList = wrapper.find("dd", class_="collections")

    if tagsList != None:
        tagsList = tagsList.find_all("a")
        for tag in tagsList:
            results.append(tag.text)

    return results


# ***    TESTING    *** #
# print()
# print("------------")

# # Get HTML text from AO3 fic
# htmlText = requests.get("https://archiveofourown.org/works/13273611/chapters/30371190").text
# soup = BeautifulSoup(htmlText, "lxml")
# wrapper = soup.find("div", class_="wrapper")

# # Declare tags dict
# tags = {}

# # TESTING AREA (uncomment some)
# tags["rating"] = getRating(wrapper)
# tags["warnings"] = getWarnings(wrapper)
# tags["romanticCats"] = getRomanticCats(wrapper)
# tags["fandoms"] = getFandoms(wrapper)
# tags["relationships"] = getRelationships(wrapper)
# tags["characters"] = getCharacters(wrapper)
# tags["moreTags"] = getMoreTags(wrapper)
# tags["language"] = getLanguage(wrapper)
# tags["series"] = getSeries(wrapper)
# tags["collections"] = getCollections(wrapper)

# # print results
# for data in tags:
#     print(f"-{data.upper()}: {tags[data]}")

# print("------------")
# print()