from helperMethods import fileToList, listToFile, listToCsv, csvToList, getSoupFromFile, fileToString
from archiveMethods import sortAo3Urls, makeFicFromNum, getAo3Num, getAo3TagEnd
# from GreaterMethods import getMetaInfo, getTags, getStats
# import requests
# import csv
# from bs4 import BeautifulSoup

# fileToList(fileName, stopCase = "stopCase3stopCase2stopCase1")
# listToFile(fileName, listToBeAdded, writeType = "a", wantHeader = False)
# listToCsv(fileName, listToBeAdded, writeType = "a", seperator = ",")
# csvToList(fileName, getIndex = -1)

# get list of URLs from a file
fileName = "workspace/urlFiles/readinglist4.txt"
urlList = fileToList(fileName)
result = set()

print(f"{len(urlList)} urls!")
for url in urlList:
    # if it's not an AO3 URL
    if ("archiveofourown.org" in url) and ("/collections/" not in url) and ("/works/" in url):
        ficNum = getAo3Num(url, "/works/")
        result.add(ficNum)

listToFile(fileName, list(result), "w")

print()
print("----")




# result = set()
# runoff = []

# # get allFicNums
# urlList = fileToList("workspace/allFutureFicUrls.txt")
# for url in urlList:
#     test = getAo3Num(url, "/works/")
#     print(f"TEST: {test}")
#     result.add(test)
#     # print(getAo3Num(url, "/works/"))
#         # runoff.append(url)

# listToFile("workspace/allFutureFicNums.txt", list(result), "a")

# for ele in runoff:
#     print(ele)