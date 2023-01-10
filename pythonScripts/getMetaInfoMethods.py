""" Description: All the getMetaInfo{} methods
    Author(s): Sofia Kobayashi
    Date: 03/05/2022
    https://beautiful-soup-4.readthedocs.io/en/latest/
    Table of Contents: 
        Methods to get metaInfo{}
        Testing
"""
from helperMethods import cleanEdges, getSoup
from bs4 import BeautifulSoup
import requests


# ***    METHODS TO GET METAINFO{}    *** #
def getTitle(preface):
    """Finds and returns fic's title. Returns a string."""
    title = preface.find("h2", "title heading").text.replace("  ", "").replace("\n", "")
    return title


def getAuthors(preface):
    """Finds and returns fic's author(s). Returns a python list of strings [author, link]."""
    results = []
    authors = preface.find("h3", class_="byline heading").find_all("a")

    for author in authors:
        oneAuthor = author.text.replace("  ", "").replace("\n", "")
        oneLink = author["href"]
        results.append([oneAuthor, oneLink])

    return results


def getSummary(preface):
    """Finds and returns fic's summary. Returns a string w/ formatting tags."""
    results = ""
    summary = preface.find("div", class_="summary module")

    if summary != None:
        summary = summary.find("blockquote", "userstuff")
        for p in summary:
            results += str(p)

    return cleanEdges(results)


def getAssociations(preface):
    """Finds and returns fic's association(s). Returns a python list of strings [associationText, [ficName, link], [author, link]]."""
    results = []
    associations = preface.find("ul", class_="associations")

    if associations != None:
        associations = associations.find_all("li")

        for li in associations:
            asso = li.text.replace("  ", ""). replace("\n", "")
            oneAsso = [cleanEdges(asso)]

            assoList = li.find_all("a")
            for a in assoList:
                oneAsso.append([a.text, a["href"]])
            
            results.append(oneAsso)

    return results


def getFrontNotes(soup):
    """Finds and returns fic's front notes. Returns a string w/ formatting tags."""
    results = ""
    fNotes = soup.find("div", class_="notes module")
    if fNotes != None:
        fNotes = fNotes.find("blockquote", "userstuff")
        if fNotes != None:
            for p in fNotes:
                results += str(p)
    
    return cleanEdges(results)
        

def getEndNotes(soup):
    """Finds and returns fic's end notes. Returns a string w/ formatting tags."""
    results = ""
    eNotes = soup.find("div", class_="end notes module")
    if eNotes != None:
        eNotes = eNotes.find("blockquote", class_="userstuff")
        for p in eNotes:
            results += str(p)

    return cleanEdges(results)


def getWorksInspired(preface):
    """Finds and returns fic's work(s) inspired. Returns a python list of strings [[[inspiredFic, ficLink], [author, authorLink]]]."""
    results = []
    links = preface.find("p", class_="jump")

    if links != None:
        links = links.find_all("a")

        if len(links) > 1:
            inspiredLink = "https://archiveofourown.org"+links[1]["href"]

            endText = requests.get(inspiredLink).text
            soupEnd = BeautifulSoup(endText, "lxml")

            works = soupEnd.find("div", class_="children module")
            
            if works != None:
                works = works.find_all("li") # get list of all work/author pairs
                for work in works:
                    links = work.find_all("a") # get the work/author links for each pair
                    if len(links) == 2:
                        # if both work/author links are present, append
                        results.append([[links[0].text, links[0]["href"]], [links[1].text, links[1]["href"]]])
                    elif work.find("[Restricted Work]") != -1:
                        # if it's a restricted work, change and append
                        results.append([["Restricted Work", None], [links[0].text, links[0]["href"]]])

    return results



# # # # # ***    TESTING    *** #
# print()
# print("------------")

# # Get HTML text from AO3 fic
# htmlText = requests.get("https://archiveofourown.org/works/11284494").text
# soup = BeautifulSoup(htmlText, "lxml")
# preface = soup.find("div", class_="preface group")

# test = getWorksInspired(preface)
# print(test)

# # # Declare metaInfo dict
# # metaInfo = {}

# # # TESTING AREA (uncomment some)
# # metaInfo["title"] = getTitle(preface)
# # metaInfo["authors"] = getAuthors(preface)
# # metaInfo["summary"] = getSummary(preface)
# # metaInfo["associations"] = getAssociations(preface)
# # metaInfo["frontNotes"] = getFrontNotes(soup)
# # metaInfo["endNotes"] = getEndNotes(soup)
# # metaInfo["worksInspired"] = getWorksInspired(soup)

# # # print results
# # for data in metaInfo:
# #     print(f"-{data.upper()}: {metaInfo[data]}")

# print("------------")
# print()