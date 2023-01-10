from helperMethods import fileToList, listToFile

def deDupFile(fileName):
    """Given a file name, will remove all duplicates directly from that file."""
    # get list of file contents
    fileList = fileToList(fileName)
    print(f"Started with {len(fileList)} lines.")

    # de-dup file contents by turning into a set & back into a list
    result = list(set(fileList))
    print(f"Ended with {len(result)} lines.")
    print(f"(Removed {len(fileList) - len(result)})")

    # write de-dup listed back to file
    writeFile = open(fileName, "w")
    for ele in result:
        writeFile.write(ele+"\n")
    writeFile.close()


def removeComparisons(fileName1, fileName2):
    """Given file1 & file 2, will directly remove a line from file1 if already in file2."""
    # get contents of both files
    changingList = fileToList(fileName1)
    print(f"Original file started with {len(changingList)} lines.")

    comparisionList = fileToList(fileName2)
    result = []
    runoff = []

    # append lines from file1 that do NOT appear in file2 to result[]
    for ele in changingList:
        if ele not in comparisionList:
            result.append(ele)
        else:
            runoff.append(ele) # else, append to runoff[]

    # write result[] to file1 to overwrite previous contents
    listToFile(fileName1, result, "w")
    
    # print progress report
    print(f"Original file ended with {len(result)} lines.")
    print(f"Removed {len(changingList) - len(result)}:")


def cycle():
    numList = fileToList("workspace/allNums3.txt")
    result = []
    for num in numList:
        result.append("https://archiveofourown.org/works/" + num)

    listToFile("workspace/urls.txt", result, "w")

cycle()
#deDupFile("workspace/allNums3.txt")
#removeComparisons("workspace/allNums3.txt","workspace/recordedNums3.txt")
