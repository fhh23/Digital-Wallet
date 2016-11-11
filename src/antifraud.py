import csv
from collections import defaultdict
import sys
from datetime import datetime, timedelta
import re
import ntpath
from queue import deque

def pathFilename(path):
    '''Function to return just filename from any path
        Ex: /x/y/z.txt returns z.txt '''
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
    
def setRowVals(row, headers):
    '''Function to set variables based on each field in a row '''
    #Set date as datetime variable of month, day, year
    recentDate = row[headers[0]].strip()
    recentDate = str.join(' ', recentDate.split(' ')[0:1])
    #If date has letters in it, it is invalid and initialize to a default date
    if re.search('[a-zA-Z]', recentDate):
        recentDate = '11/2/2016'
    #Deal with date format in year-month-day
    if '-' in recentDate:
        recentDate = datetime.strptime(recentDate, '%Y-%m-%d')
    #Deal with date format in month/day/year
    else:
        recentDate = datetime.strptime(recentDate, '%m/%d/%Y')
    recentDate = recentDate.date()
    #Set id1
    id1 = row[headers[1]].strip()
    #If id1 has letters in it, it is invalid and initialize to a default id
    if re.search('[a-zA-Z]', id1):
        id1 = '0'
    #Set id2
    id2 = row[headers[2]].strip()
    if re.search('[a-zA-Z]', id2):
        id2 = '0'
    #Set transaction amount
    maxAmt = row[headers[3]].strip()
    #If transaction amount has letters in it, it is invalid and initialize to a default amount
    if re.search('[a-zA-Z]', maxAmt):
        maxAmt = '0'
    maxAmt = float(maxAmt)
    return recentDate, id1, id2, maxAmt
    
def updatehashMaxs(id1, id2, maxAmt, recentDate, hashMaxs):
    '''This function updates the max transaction amount between 2 ids if it is bigger than the previous max amount
        and updates most recent transaction date between 2 ids if it is more recent than the previous recent date '''
    #Update max transaction amount between 2 Ids
    if maxAmt > hashMaxs[id1][id2]['amount']:
        hashMaxs[id1][id2]['amount'] = maxAmt
        hashMaxs[id2][id1]['amount'] = maxAmt
    #Update most recent transaction date between 2 Ids
    if recentDate > hashMaxs[id1][id2]['date']:
        hashMaxs[id1][id2]['date'] = recentDate
        hashMaxs[id2][id1]['date'] = recentDate
    return hashMaxs

def updateAdjListTrans(id1, id2, adjListTrans):
    '''If an Id is not in a key's adjacency list, append it '''
    if (id2 not in adjListTrans[id1]):
        adjListTrans[id1].append(id2)
    if (id1 not in adjListTrans[id2]):
        adjListTrans[id2].append(id1)
    return adjListTrans

def readInput(inputFile):
    '''Function to read in batch input file 
        and create adjacency list for transaction ids
        and create hash tables for max transaction amount and most recent transaction date '''
    with open(inputFile, "r", encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        #Initialize adjacency list
        adjListTrans = defaultdict(list)
        #Initialize hash table
        hashMaxs = defaultdict((lambda : defaultdict(dict)))
        headers = reader.fieldnames   
        for row in reader:
            #Only run if rows have something in every field
            if row[headers[0]] and row[headers[1]] and row[headers[2]] and row[headers[3]]:
                #Set variables for each field
                recentDate, id1, id2, maxAmt = setRowVals(row, headers)
                #Update adjacency list
                adjListTrans = updateAdjListTrans(id1, id2, adjListTrans)
                #Update hash table
                if (hashMaxs[id1].get(id2) == None):
                    hashMaxs[id1][id2]['amount'] = maxAmt
                    hashMaxs[id2][id1]['amount'] = maxAmt
                    hashMaxs[id1][id2]['date'] = recentDate 
                    hashMaxs[id2][id1]['date'] = recentDate
                hashMaxs = updatehashMaxs(id1, id2, maxAmt, recentDate, hashMaxs)
    return adjListTrans, hashMaxs

def readStreaming(streamingFile, outputFile, adjListTrans, hashMaxs):
    '''Function to read in streaming file and output verified/unverified
        to each output file for each feature '''
    reader = csv.DictReader(open(streamingFile, encoding='utf8'))
    headers = reader.fieldnames  
    #Dictionary of filenames to allow variable number of features to be tested
    files = {filename: open(filename, 'w') for filename in outputFile}
    for row in reader:
        #Only run if rows have something in every field
        if row[headers[0]] and row[headers[1]] and row[headers[2]] and row[headers[3]]:
            #Set variables for each field
            recentDate, id1, id2, maxAmt = setRowVals(row, headers)
            #Find degree seperation between 2 Ids using BFS
            degrees = BFS(adjListTrans, id1, id2)
            for file in files:
                #Feature 1: Trusted if 2 Ids only have 1 degree seperation
                if pathFilename(file) == 'output1.txt':
                    if (degrees <= 1):
                        files[file].write("trusted\n")
                    else:
                        files[file].write("unverified\n")
                #Feature 2: Trusted if 2 Ids have at most 2 degree seperation       
                elif pathFilename(file) == 'output2.txt':    
                    if (degrees <= 2):
                        files[file].write("trusted\n")
                    else:
                        files[file].write("unverified\n")
                #Feature 3: Trusted if 2 Ids have at most 4 degree seperation  
                elif pathFilename(file) == 'output3.txt':
                    if (degrees <= 4):
                        files[file].write("trusted\n")
                    else:
                        files[file].write("unverified\n")
                #Feature 4: Trusted if transaction amount is less than 2x the previous maximum transaction amount       
                elif pathFilename(file) == 'output4.txt':
                    if (hashMaxs[id1].get(id2) == None):
                        #Values set to ensure 'unverified' will be written to file
                        hashMaxs[id1][id2]['amount'] = maxAmt/2-1
                        hashMaxs[id2][id1]['amount'] = maxAmt/2-1
                        hashMaxs[id1][id2]['date'] = recentDate - timedelta(days=90)
                        hashMaxs[id2][id1]['date'] = recentDate - timedelta(days=90)
                    if maxAmt > (2*hashMaxs[id1][id2]['amount']):
                        files[file].write("unverified\n")
                    else:
                        files[file].write("trusted\n")
                #Feature 5: Trusted if transaction date is within 60 days of last transaction
                elif pathFilename(file) == 'output5.txt':
                    if (hashMaxs[id1].get(id2) == None):
                        #Values set to ensure 'unverified' will be written to file
                        hashMaxs[id1][id2]['amount'] = maxAmt/2-1
                        hashMaxs[id2][id1]['amount'] = maxAmt/2-1
                        hashMaxs[id1][id2]['date'] = recentDate - timedelta(days=90)
                        hashMaxs[id2][id1]['date'] = recentDate - timedelta(days=90)
                        #Calculate difference in days
                    daysDiff = (recentDate-hashMaxs[id1][id2]['date']).days
                    if daysDiff > 60:
                        files[file].write("unverified\n")
                    else:
                        files[file].write("trusted\n")
            #Update adjacency list and hash table
            adjListTrans = updateAdjListTrans(id1, id2, adjListTrans)
            hashMaxs = updatehashMaxs(id1, id2, maxAmt, recentDate, hashMaxs)
    #Close all files
    for file in files:
        files[file].close()

    
def BFS(adj_list, start, end):
    #Initialize Queue to first Id
    queue = deque()
    queue.appendleft([start])
    visited = set()
    while len(queue) > 0:
        #Get first path in queue
        path = queue.pop()
        #Get last node in the path
        node = path[-1]
        #Check if second Id last in path, if so return degrees seperation
        if node == end:
            return (len(path)-1)
        #Check if already visited Id
        elif node not in visited:
            #Go through all adjacent nodes in list, make a new path and push into the queue
            for adjNode in adj_list.get(node, []):
                nextPath = list(path)
                nextPath.append(adjNode)
                #If path has <= 4 nodes push to queue (since max degrees sep allowed is 4)
                if ((len(nextPath)-1) <= 4):
                    queue.appendleft(nextPath)
            # Mark the Id as visited
            visited.add(node)
    #Return 5 if no path with <= 4 nodes found
    return 5

if __name__ == '__main__':
    #Batch input file first arg in run.sh
    batchFile = sys.argv[1]
    #Streaming input file second arg in run.sh
    streamingFile = sys.argv[2]
    outputFiles = []
    #Rest of args in run.sh are output files
    for x in range(3,len(sys.argv)):
        outputFiles.append(sys.argv[x])
    #Create adj list and hash table
    adjListTrans, hashMaxs = readInput(batchFile)
    #Read streaming file and output verified/unverified to output.txt files
    readStreaming(streamingFile, outputFiles, adjListTrans, hashMaxs)

    
