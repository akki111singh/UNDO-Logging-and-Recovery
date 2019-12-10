#!/usr/bin/env python
# coding: utf-8

#UNDO LOOGGING
#AKHIL SINGH
#20171210
import sys
import os
def PrinttoDiskandMem():
    s = ""
    for i in sorted(VarMemory):
        s = s + i + " "+ str(VarMemory[i]) + " "
    outputfile.write(s[:-1]+"\n")
    s = ""
    for i in sorted(VarDisk):
        s = s + i + " "+ str(VarDisk[i]) + " "
    outputfile.write(s[:-1]+"\n")

def operate(inp1,inp2,op):

    if op=='+':
        return inp1+inp2
    elif op=='-':
        return inp1-inp2
    elif op=='*':
        return inp1*inp2
    elif op=='/':
        if inp2 == '0':
            print("Divide by zero")
            sys.exit(0)
        else:
            return float(inp1)/float(inp2)


def PerformLog(CurrTransaction,x,startFrom):
    if startFrom == 0:
        outputfile.write("<START " + CurrTransaction + ">" + "\n")
        PrinttoDiskandMem()

    if startFrom >= TransactionLength[CurrTransaction]:
        TransactionsDone[CurrTransaction] = True
        return

    instructions = Transactions[CurrTransaction][startFrom:startFrom+x]

    for line in instructions:
        line = line.strip()
        if line.split("(")[0] == 'READ':
            line = line.split('(')[1]
            line = line.split(")")[0].strip()

            if ',' in line:
                line = line.split(',')

            var,val = line[0],line[1]

            if var in LocalVar.keys():
                LocalVar[var] = val
                LocalValues[val] = VarMemory[var]
            else:
                LocalVar[var] = val
                LocalValues[val] = VarDisk[var]
                VarMemory[var] = VarDisk[var]


        elif line.split("(")[0] == 'WRITE':
            line = line.split('(')[1]
            line = line.split(")")[0].strip()

            if ',' in line:
                line = line.split(',')
            var,val = line[0],line[1]
            towrite = "<"+CurrTransaction+", " + var + ", " + str(VarMemory[var]) + ">" + "\n"
            outputfile.write(towrite)
            VarMemory[var] = int(LocalValues[val])
            PrinttoDiskandMem()
        elif line.split("(")[0] == 'OUTPUT':
            line = line.split('(')[1]
            line = line.split(")")[0].strip()

            if ',' in line:
                line = line.split(',')
            var = line[0]

            VarDisk[var] = VarMemory[var]
        else:
            operators = ['+' , '-' , '*' , '/']
            line = line.strip().split(":=")
            var = line[0].strip()

            for op in operators:
                if op in line[1]:
                    inp1, inp2 = line[1].strip().split(op)
                    LocalValues[var] = operate(int(LocalValues[inp1]),int(inp2),op)

    if startFrom + x >= TransactionLength[CurrTransaction]:
        writecommit = "<COMMIT "+CurrTransaction+">"+"\n"
        outputfile.write(writecommit)
        PrinttoDiskandMem()
def ReadFile(f):
    data = f.readlines()
    dbElements = data[0].strip().split(' ')
    Vars,Vals = dbElements[::2],dbElements[1::2]

    for i in range(len(Vars)):
        VarDisk[Vars[i]] = Vals[i]

    for line in data[1:]:
        T = line.split(" ")
        if T[0][0] == 'T':
            TransactionNumber = T[0]
            TransactionsOrder.append(TransactionNumber)
            TransactionLength[TransactionNumber] = int(T[1].strip())
            Transactions[TransactionNumber] = []
        elif not line.strip():
            TransactionNumber = None
        else:
            Transactions[TransactionNumber].append(line[:-1])

    for i in Transactions.keys():
        TransactionsDone[i] = False



def UndoLogs(x):
    i = 0
    CurrTransaction = TransactionsOrder[i]
    startFrom = 0
    while 1:
        #performing x instructions/actions of the Current Transactions transaction
        TrueCount = 0
        PerformLog(CurrTransaction,x,startFrom)
        i=i+1
        totalTransactions = len(Transactions)

        #Incrementing the start position to perform next x instructions of every transaction
        if i % totalTransactions == 0:
            i = 0
            startFrom+=x

        CurrTransaction = TransactionsOrder[i]
        for key,val in TransactionsDone.items():
            if val == True:
                TrueCount+=1;

        #If all the Transactions are performed Successfully
        if TrueCount == 3:
            break;


VarDisk = {}
VarMemory = {}
VarLocal = {}
TransactionsOrder = []
TransactionLength = {}
Transactions = {}
TransactionsDone = {}
LocalVar = {}
LocalValues = {}

inputFile = sys.argv[1]
x = int(sys.argv[2])
inputFile = open(inputFile ,'r')

ReadFile(inputFile)
outputfile = open("20171210_1.txt","w")
UndoLogs(x)
