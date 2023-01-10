#   Description: Scraping AO3, FIRST TEST kept for *****REFERENCE******
#   Author(s): Sofia Kobayashi
#   Date: 03/05/2022
#   https://beautiful-soup-4.readthedocs.io/en/latest/

from bs4 import BeautifulSoup
import requests

print()
print("------------")

# Getting HTML of the AO3 page
html_text = requests.get("https://archiveofourown.org/works/13273611/chapters/30371190").text
soup = BeautifulSoup(html_text, "lxml")

# Declaring FFN variables
title = soup.find("h2", class_="title heading").text.replace("  ", "").replace("\n", "")
author = soup.find("h3", class_="byline heading").a.text.replace("  ", "").replace("\n", "")
summary = soup.find("blockquote", class_="userstuff").text
rating = ""
warnings = []
romanticCats = []
fandoms = []
relationships = []
characters = []
tags = []
lang = ""
collections = []
stats = {"publishDate": "", 
        "completedDate": "",
        "wordCount": -1,
        "currentChapters": -1,
        "totalChapters": -1,
        "comments": -1,
        "kudos": -1,
        "bookmarks": -1,
        "hits": -1,
        }


print(f"{title} by {author}\n{summary}\n")

# *** GETTING TAGS ***
# Getting HTML of preface
preface = soup.find("dl", class_="work meta group")
tagNames = preface.find_all("dt")
tagData = preface.find_all("dd")

# for name in tagNames:
#     print(name.text.replace("  ", "").replace("\n", ""))
#     count +=1

# for tag in tagData:
#     print(tag.text.replace("  ", "").replace("\n", ""))
#     count +=1


# Assigning tag variables
for i in range(10):
    # FIND Rating
    if i == 0:
        # Get (uppercase) name of tag
        name = tagNames[i].text.replace("  ", "").replace("\n", "").upper()
        
        # Get Rating (string)
        rating = tagData[i].text.replace("  ", "").replace("\n", "")
        
        # Print representation of tag
        print(f"{name} {rating}")
    
    # FIND Warning(s)
    elif i == 1:
        # Get (uppercase) name of tag
        name = tagNames[i].text.replace("  ", "").replace("\n", "").upper()
        
        # Get a list of all warnings, then append them to warnings[]
        listWarnings = tagData[i].find_all("a")
        for element in listWarnings:
            warnings.append(element.text)

        # Print representation of tag
        print(f"{name} {warnings}")
        
    # FIND Romantic Categories
    elif i == 2:
        # Get (uppercase) name of tag
        name = tagNames[i].text.replace("  ", "").replace("\n", "").upper()
        
        # Get a list of all warnings, then append them to warnings[]
        listRoms = tagData[i].find_all("a")
        for element in listRoms:
            romanticCats.append(element.text)

        # Print representation of tag
        print(f"{name} {romanticCats}")

    # FIND Fandom(s)
    elif i == 3:
        # Get (uppercase) name of tag
        name = tagNames[i].text.replace("  ", "").replace("\n", "").upper()
        
        # Get a list of all warnings, then append them to warnings[]
        listOf = tagData[i].find_all("a")
        for element in listOf:
            fandoms.append(element.text)

        # Print representation of tag
        print(f"{name} {fandoms}")

    # FIND Relationship(s)
    elif i == 4:
        # Get (uppercase) name of tag
        name = tagNames[i].text.replace("  ", "").replace("\n", "").upper()
        
        # Get a list of all warnings, then append them to warnings[]
        listOf = tagData[i].find_all("a")
        for element in listOf:
            relationships.append(element.text)

        # Print representation of tag
        print(f"{name} {relationships}")
    
    # FIND Character(s)
    elif i == 5:
        # Get (uppercase) name of tag
        name = tagNames[i].text.replace("  ", "").replace("\n", "").upper()
        
        # Get a list of all warnings, then append them to warnings[]
        listOf = tagData[i].find_all("a")
        for element in listOf:
            characters.append(element.text)

        # Print representation of tag
        print(f"{name} {characters}")

    # FIND Tag(s)
    elif i == 6:
        # Get (uppercase) name of tag
        name = tagNames[i].text.replace("  ", "").replace("\n", "").upper()
        
        # Get a list of all warnings, then append them to warnings[]
        listOf = tagData[i].find_all("a")
        for element in listOf:
            tags.append(element.text)

        # Print representation of tag
        print(f"{name} {tags}")
    
    # FIND Language
    elif i == 7:
        # Get (uppercase) name of tag
        name = tagNames[i].text.replace("  ", "").replace("\n", "").upper()
        
        # Get Rating (string)
        lang = tagData[i].text.replace("  ", "").replace("\n", "")
        
        # Print representation of tag
        print(f"{name} {lang}")
    
    # FIND Collection(s)
    elif i == 8:
        # Get (uppercase) name of tag
        name = tagNames[i].text.replace("  ", "").replace("\n", "").upper()
        
        # Get a list of all warnings, then append them to warnings[]
        listOf = tagData[i].find_all("a")
        for element in listOf:
            collections.append(element.text)

        # Print representation of tag
        print(f"{name} {collections}")

    # FIND Stats
    elif i == 9:
        # Get names and data of stats
        # statNames = tagNames[i].find_all("dt")
        statData = tagData[i].find_all("dd")
        
        # Assign the uncomplicated data
        stats["publishDate"] = statData[0].text
        stats["wordCount"] = int(statData[2].text)
        stats["comments"] = int(statData[4].text)
        stats["kudos"] = int(statData[5].text)
        stats["bookmarks"] = int(statData[6].text)
        stats["hits"] = int(statData[7].text)

        # stats["completedDate"] = statData[1].text
        # stats["ChapterCount"] = int(statData[3].text)
        
        # Print representation of stats
        print(f"STATS: {stats}")


print("------------")
print()