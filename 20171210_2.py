#!/usr/bin/env python
# coding: utf-8

#UNDO RECOVERING
#20171210
#Akhil Singh
import sys
def readfile(f):
    global startCkptPos,endCkptPos
    data = f.readlines()
    dbElements = data[0].strip().split(' ')
    Vars,Vals = dbElements[::2],dbElements[1::2]

    for i in range(len(Vars)):
        VarDisk[Vars[i]] = Vals[i]

    lineNumber = -1
    for line in data[1:]:
        if line.strip():
            logs.append(line[1:-2])
            if 'START CKPT' in line:
                startCkptPos = lineNumber
            if 'END CKPT' in line:
                endCkptPos = lineNumber
        lineNumber += 1


def UndoAll():
    global logs

    commited = []
    for line in logs[::-1]:
        if line[0] == 'T':
            tr,var,val = line.split(",")
            tr = tr.strip()
            var = var.strip()
            val = val.strip()
            if tr not in commited:
                VarDisk[var] = int(val)

        if 'COMMIT' in line:
            line = line.split(" ")
            commited.append(line[1])

def UndoOnlyStart():
    global logs
    commited = []

    Line = logs[startCkptPos]
    Line = Line.replace(" ","").split("(")[1]
    Line = Line.split(")")[0]

    ActiveTransactions = Line.split(",")


    for Line in logs[::-1]:
        if(len(ActiveTransactions)) == 0:
            break
        if Line[0] == 'T':
            tr,var,val = Line.split(",")
            tr = tr.strip()
            var = var.strip()
            val = val.strip()
            if tr not in commited:
                VarDisk[var] = int(val)
        elif 'COMMIT' in Line:
            Line = Line.split(" ")
            commited.append(Line[1])
        elif 'START' in Line and 'CKPT' not in Line:
            Line = Line.split(" ")
            if Line[1] in ActiveTransactions:
                ActiveTransactions.remove(Line[1])

def UndoEndPresent():
    global logs
    commited = []
    Logs = logs[startCkptPos+1:]

    for line in Logs[::-1]:
        if line[0] == 'T':
                tr,var,val = line.split(",")
                tr = tr.strip()
                var = var.strip()
                val = val.strip()
                if tr not in commited:
                    VarDisk[var] = int(val)

        if 'COMMIT' in line:
            line = line.split(" ")
            commited.append(line[1])


def recovery():
    global startCkptPos,endCkptPos
    start,end = startCkptPos,endCkptPos

    if startCkptPos > endCkptPos:
        endCkptPos = -1

    if startCkptPos!=-1 and endCkptPos == -1:
        #ONLY START CHECKPOINT IS PRESENT NO END
        UndoOnlyStart()
    elif startCkptPos!=-1 and endCkptPos!=-1:
        #BOTH START CHECKPOINT AND END CHECKPOINT PRESENT
        UndoEndPresent()

    if startCkptPos == -1 and endCkptPos == -1:
        #NO CheckPoint
        UndoAll()
    elif startCkptPos == -1 and endCkptPos!= -1:
        print("END CHECKPOINT FOUND BUT NO START CHECKPOINT")
def writeOutput():
    finalValues = ""
    #print(VarDisk)
    for i in sorted(VarDisk):
        finalValues+= i + " " + str(VarDisk[i]) + " "
    # print(finalValues)
    outputFile.write(finalValues[:-1]+"\n")
logs = []
VarDisk = {}
inputfile = sys.argv[1]
startCkptPos  = -1
endCkptPos = -1
inputfile = open(inputfile,'r')
readfile(inputfile)

outputFile = open("20171210_2.txt","w")
recovery()
writeOutput()
inputfile.close()
outputFile.close()
