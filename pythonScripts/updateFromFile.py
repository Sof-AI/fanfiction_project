import csv
import os
from helperMethods import fileToList, listToFile, clearDuplicates
from archiveMethods import makeFicFromNum, getFicNumList

# fileToList(fileName, stopCase = "stopCase3stopCase2stopCase1")
# listToFile(fileName, listToBeAdded, writeType = "a", wantHeader = False)
# listToCsv(fileName, listToBeAdded, writeType = "a", seperator = ",")
# csvToList(fileName, getIndex = -1)

print()
print("------------")


##### For each fic:
for filename in os.scandir("update/htmlFiles"):
    # get ficNum
    

###### Get list of all FicNums, get rid of duplicates, and delete duplicate files
# Get list of ficNums from HTML files
# Write runoff1.txt, clear runoff list
# Get rid off any duplicates that have already been added to v8 & delete duplicate files

###### Make all archive ficNums into ficDicts, return a dict of ficDicts and write any URLs that gave errors to runoff2.txt
# for all ficNums, make into ficDict & appends to allFics{}
# Write runoff2.txt, clear runoff list

###### Add all ficDicts into output.csv, add ficNum to 1STORAGE/v8FicNums.txt, write any errors to runoff3.txt
# prepare csv file & csv writer
# Write runoff3.txt
# Add all successfully added ficNums to the file that stores all ficNums in v8



print("------------")
print()