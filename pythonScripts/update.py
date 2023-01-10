import csv
from helperMethods import fileToList, listToFile, clearDuplicates
from archiveMethods import makeFicFromNum, getFicNumList

# fileToList(fileName, stopCase = "stopCase3stopCase2stopCase1")
# listToFile(fileName, listToBeAdded, writeType = "a", wantHeader = False)
# listToCsv(fileName, listToBeAdded, writeType = "a", seperator = ",")
# csvToList(fileName, getIndex = -1)

print()
print("------------")

###### Get URLs from input.txt, return a list of archive ficNums and write any other URLs to runoff1.txt
# Setup
allFics = {} #dict in which all ficDicts will be stored, using ficNum as key, ficDict as value
runoff = [] #for various non-AO3-works 
v8FicNums = fileToList("update/2STORAGE/v8FicNums.txt") #all ficNums that have ever been successfully added to v8
dg = {} #for printing reasons
######

# get URLs from input.txt & seperate AO3 works from everything else
inputList = fileToList("update/input.txt") # inputList = all URLs from input.txt
if "archiveofourown.org" in inputList[0]:
    archiveList = getFicNumList(inputList, runoff) # archiveList = all AO3 ficNums, runoff = all URLs that are NOT AO3 works
else:
    archiveList = inputList


# Write runoff1.txt, clear runoff list
listToFile("update/runoff1.txt", runoff)
dg["run1"] = len(runoff)
runoff = []

# Get rid off any duplicates that have already been added to v8
ficNumList = clearDuplicates(archiveList, v8FicNums) #workingList = AO3 ficNums not already in v8
dg["totNonDup"] = len(ficNumList)



###### Make all archive ficNums into ficDicts, return a dict of ficDicts and write any URLs that gave errors to runoff2.txt
# Setup
total = len(ficNumList) #for printing reasons
print(f"{total} fics to be written")
######

# for all ficNums, make into ficDict & appends to allFics{}
for i, num in enumerate(ficNumList):
    try: 
        fic = makeFicFromNum(num)
        allFics.update({num: fic})
        print(f"({'{0:.1%}'.format((i+1)/total)}) {num} has been list-ified ")
    # if error, add to runoff, runoff = all ficNums that threw an error
    except:
            print(f"ERROR_Undetermined {num}")
            runoff.append(num)

# Write runoff2.txt, clear runoff list
listToFile("update/runoff2.txt", runoff)
runoff = []
dg["run2"] = len(runoff)



###### Add all ficDicts into output.csv, add ficNum to 1STORAGE/v8FicNums.txt, write any errors to runoff3.txt
# Setup
print("\n--- List-ifying done!! ---\n")
total = len(allFics) #for printing reasons
completedList = [] #for ficNums that have been successfully added
######

# prepare csv file & csv writer
with open("update/output.csv", "a") as newFile:
    # define the keys for the csv file
    keysField = ['idNum', 'title', 'authors', 'summary', 'associations', 'frontNotes', 'endNotes', 'worksInspired', 'frontNotes', 'endNotes', 'site', 
            'rating', 'warnings', 'romanticCats', 'fandoms', 'relationships', 'characters', 'moreTags', 'language', 'series', 'collections',
            'publishDate', 'completeDate', 'numWords', 'numChapters', 'totalChapters', 'numComments', 'numKudos', 'numBookmarks', 'numHits']
    
    # create csv writer & write key names at top
    rawWriter = csv.DictWriter(newFile, fieldnames = keysField)
    #rawWriter.writeheader()

    # for ficDict in allFics{}, write info in ficDict to output.txt
    for i, fic in enumerate(allFics):
        try: 
            # define all relevent dicts
            headerDict = {"idNum": fic}
            metaDict = allFics[fic]["metaInfo"]
            statsDict = allFics[fic]["stats"]
            tagsDict = allFics[fic]["tags"]

            # combine all relevent dicts
            headerDict.update(metaDict)
            headerDict.update(statsDict)
            headerDict.update(tagsDict)

            # write combined dict to csv file
            rawWriter.writerow(headerDict)
            completedList.append(fic)
            print(f"({'{0:.1%}'.format((i+1)/total)}) {fic} has been written!")
        # if error, flag and append to runoff
        except:
            print(f"ERROR_Undetermined2 {fic}")
            runoff.append(fic)
    
# Write runoff3.txt
listToFile("update/runoff3.txt", runoff)
dg["run3"] = len(runoff)

# Add all successfully added ficNums to the file that stores all ficNums in v8
listToFile("update/2STORAGE/v8FicNums.txt", completedList)
dg["totCom"] = len(completedList)


# after-action report
print("\n--- Writing done!! ---\n")
print("\n--- Action Summary ---")
print(f"{len(inputList)} total URLs from input.txt: {len(archiveList)} AO3 works, {dg['run1']} other")
print(f"{len(archiveList)} total AO3 ficNums: {dg['totNonDup']} original AO3 ficNums, {len(archiveList)-dg['totNonDup']} duplicate(s)")
print(f"{dg['totNonDup']} total original AO3 ficNums: {dg['totNonDup'] - dg['run2']} successfully list-ified, {dg['run2']} list error(s)")
print(f"{dg['totNonDup'] - dg['run2']} total successfully list-ified: {dg['totCom']} successfully written, {dg['run3']} writing error(s)")
print(f"Of the {dg['totNonDup']} original AO3 ficNUms, {dg['totCom']} were successfully written! ({'{0:.1%}'.format((dg['totNonDup'])/(dg['totCom']+.00001))} successful)")

# following steps to take
print("\n--- Steps to fully update v8 ---")
print("1) Import output.csv into v8 in Google Sheets")
print("2) Copy/paste appropriate info")
print("3) Deal with runoffs 1-3 (can just copy/paste to otherUrls.txt in 2STORAGE)")
print("4) Clear contents of: input.txt, output.csv, and runoffs 1-3")
print("\n*wrote to output.csv, runoff1.txt, runoff2.txt, runoff2.txt, v8FicNums.txt")

print("------------")
print()