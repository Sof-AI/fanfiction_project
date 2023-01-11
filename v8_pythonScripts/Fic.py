""" Description: Fic object
    Author(s): Sofia Kobayashi
    Date: 03/06/2022
    Table of Contents: 
        Fic Object
        Testing
"""
from GreaterMethods import *
from helperMethods import *


# ***    FIC OBJECT    *** #
class ArchiveFic:
    """Object that represents a single fanfiction from AO3"""
    def __init__(self, ficNum, dtbNum):
        """Constructor for Fic object."""
        self.url = "https://archiveofourown.org/works/"+ficNum
        self.dtbNum = dtbNum
        self.ficNum = ficNum
        self.addDate = "TBD"
        self.soup = getSoup(self.url)

        # 
        self.myData = {}

        # title, authors, summary, associations, frontNotes, endNotes, worksInspired, site
        self.metaInfo = getMetaInfo(self.soup) 

        # rating, warnings, romanticCats, fandoms, relationships, characters, moreTags, language, series, collections
        self.tags = getTags(self.soup)

        # publishDate, completeDate, numWords, numCharacters, totalChapters, numComments, numKudos, numBookmarks, numHits
        self.stats = getStats(self.soup)
        

    def __str__(self):
        """toString() method for Fic object."""
        results = ""
        bigBar = "------------------\n"
        bar = "\n------\n"

        results += bigBar + f"Fic#{self.dtbNum} added on {self.addDate}\n" + bigBar + "\n"

        # Add metaInfo{} section
        results += "metaInfo{}" + bar
        for info in self.metaInfo:
            results +=(f"- {info}: {self.metaInfo[info]}\n")

        # Add tags{} section
        results += "\n\ntags{}" + bar
        for info in self.tags:
            results +=(f"- {info}: {self.tags[info]}\n")

        # Add stats{} section
        results += "\n\nstats{}" + bar
        for info in self.stats:
            results +=(f"- {info}: {self.stats[info]}\n")

        # Add stats{} section
        results += "\n\nmyData{}" + bar
        for info in self.myData:
            results +=(f"- {info}: {self.myData[info]}\n")

        return results + bigBar

    def intro(self):
        """Returns a (string) small header of the fic."""
        return(f"dtb#{self.dtbNum}: {self.metaInfo['title']} by {doubleListToString(self.metaInfo['authors'])}" + 
            f" ({self.stats['numWords']:,} words)")
        # print(f"Fandom(s): {doubleListToString(self.tags['fandoms'])}")
    
    def isComplete(self):
        """Determines is fic is complete. Returns boolean value."""
        return(self.stats["completeDate"] != "")

    def isCrossover(self):
        """Determines is fic is a crossover. Returns boolean value."""
        return(len(self.tags["fandoms"]) > 1)


# # # ***    TESTING    *** #
# f1 = ArchiveFic("32361358", 1)
# print(f1)