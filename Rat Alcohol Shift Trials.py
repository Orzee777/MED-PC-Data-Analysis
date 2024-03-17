### Rat Alcohol Sucrose Script v1.0
### Last edited 03/09/2024
### works with getOperant program and Excel (https://github.com/SKhoo/GEToperant)
### can work with multiple sheets
### Shift Trials | N1 = 10 | N2 = 20

version = "1.0.240309"
# N (duration between nosepoke (door opening) and door closing) in seconds
lengthOfTrial = "10 and 20"
# trialAdjustment is adjusting for the delay between door closing time and additional licks
# using 1 second, seems to be approximately .7 seconds, though ideally is 0
trialAdjustment = 1.0

# Shift number is a constant number of the first trials before the shift occurs. Default is 4
shiftnum = 4

# N1 - Duration of trials before Shift in Seconds; N2 - Duration of trials after Shift in Seconds.
N1 = 10
N2 = 20

# Dependencies: Pandas, TKinter, datetime
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

# used for opening file dialog
root = tk.Tk()
root.withdraw()

# option for hardcoding input file path - comment out opening file dialog code above
#file_path = "C:\\Users\\Default\\Documents\\input.xlsx"

# CHANGE OUTPUT PATH HERE
out_path = "C:\\Users\\Default\\Documents\\outputfileSHIFT.txt"
file_path = filedialog.askopenfilename()

excelfile = pd.ExcelFile(file_path)

print("Opening file: ", file_path)

sheetnames = excelfile.sheet_names
print("sheetnames: ", sheetnames)

#print to file
output = open(out_path, "a")

# Start output file
print("==============================================", file=output)
print("    Rat Alcohol Sucrose Script", version, file=output)
print("    Run on", datetime.now(), file=output)
print("    N =", lengthOfTrial, "with an adjustment of", trialAdjustment, "sec", file=output)
print("==============================================", file=output)
print("Opening file: ", file_path, file=output)
print("Sheetnames: ", sheetnames, file=output)
print("==============================================", file=output)

# reads each sheet name
for z in range(0, len(sheetnames)):
    f = pd.read_excel(excelfile, sheet_name=sheetnames[z])

    #nosepoketimes = [] # from previous code
    licktimes = [] # used as input, then split into licktimes1 and licktimes2
    nptimes1 = []
    nptimes2 = []
    licktimes1 = []
    licktimes2 = []

    #N = lengthOfTrial # from previous code

    print(f.head(9))

    for index, row in f.iterrows():
        if row.iloc[0] == "Lick":
            licktimes.append((row.iloc[1])/2)
        if row.iloc[0] == "Nosepoke1":
            nptimes1.append((row.iloc[1])/2)
        if row.iloc[0] == "Nosepoke2":
            nptimes2.append((row.iloc[1])/2)

    print("lick times:\n", licktimes)
    print("np times1\n" , nptimes1)
    print("np times2\n" , nptimes2)
    
    def findLickIndex ():
        for i in range(0, len(licktimes)):
            if (licktimes[i] > nptimes2[0]):
                return i

    lickindex = findLickIndex()

    print("lick index: ", lickindex, " has value ", licktimes[lickindex])

    licktimes1 = licktimes[:lickindex]
    licktimes2 = licktimes[lickindex:]
    
    print("first licks:\n", licktimes1)
    print("lick times:\n", licktimes2)

    nplat1 = []
    nplat2 = []
    endRange1 = []
    endRange2 = []
    lickT1 = []
    lickT1perSec = []
    lickT2 = []
    lickT2perSec = []

    # find nosepokelatencies

    def findNPLatencies (lst):
        ans = []
        for i in range(0, len(lst) - 1):
            x = round((lst[i+1])-(lst[i]), 2)
            ans.append(x)
        return ans

    nplat1 = findNPLatencies(nptimes1)
    nplat2 = findNPLatencies(nptimes2)

    print("np latency 1:\n", nplat1)
    print("np latency 2:\n", nplat2)

    def Average(lst):
        if (len(lst)):
            av = sum(lst)/len(lst)
        else:
            av = 0
        return av

    nplatavg1 = round(Average(nplat1), 2)
    nplatavg2 = round(Average(nplat2), 2)
    print("np latency avg 1: ", nplatavg1)
    print("np latency avg 2: ", nplatavg2)

    def findEndRange (nosepoketimes, N):
        endRangeTemp = []
        for i in range(0, len(nosepoketimes)):
            # round because this is floating point arithmetic
            endRangeData = round(nosepoketimes[i]+N+trialAdjustment, 3)
            endRangeTemp.append(endRangeData)
        return endRangeTemp

    endRange1 = findEndRange(nptimes1, N1)
    endRange2 = findEndRange(nptimes2, N2)

    print("endRange1:", endRange1)
    print("endRange2:", endRange2)

    def findLickT (nosepoketimes, licktimes, endRange):
        lickT = []
        for i in range(0, len(nosepoketimes)):
            count = 0
            for j in range(0, len(licktimes)):
                if(licktimes[j] > nosepoketimes[i] and licktimes[j] <= endRange[i]):
                    count += 1
                    # for debugging
                    #print("COUNT INCREASED: ", count)
                    #print(nosepoketimes[i], " < ", licktimes[j]," <= ", endRange[i])
                elif (licktimes[j] > endRange[i]):
                    lickT.append(count)
                    #print("ADDED ", count, " to the list")
                    break
                # implied else
                
                # if we have hit the last lick, count it 
                if (j == len(licktimes)-1):
                        lickT.append(count)
                        #print("ADDED ", count, " to the list")
        return lickT

    lickT1 = findLickT(nptimes1, licktimes1, endRange1)
    lickT2 = findLickT(nptimes2, licktimes2, endRange2)

    print("LickT1: ", lickT1)
    print("LickT2: ", lickT2)

    lickcountavg1 = round(Average(lickT1), 2)
    lickcountavg2 = round(Average(lickT2), 2)
    
    print("lick count avg1: ", lickcountavg1)
    print("lick count avg2: ", lickcountavg2)

    lickrate1 = round(lickcountavg1/N1, 2)
    lickrate2 = round(lickcountavg2/N1, 2)
    print("lick rate 1:", lickrate1)
    print("lick rate 2:", lickrate2)

    def findLickTperSec(lickT, N):
        lickTperSec = []
        for i in range(0, len(lickT)):
            lickTperSec.append(lickT[i]/N)
        return lickTperSec

    lickTperSec1 = findLickTperSec(lickT1, N1)
    lickTperSec2 = findLickTperSec(lickT2, N2)
    
    print("lickTperSec1:\n", lickTperSec1)
    print("lickTperSec2:\n", lickTperSec2)

    def WriteListLineByLine(listname, lst, output):
        print(listname, file=output)
        for i in range(0, len(lst)):
            print(lst[i], file=output)
            
    print(f.head(9), file=output)

    print("licktimes 1 count:", len(licktimes1))
    #WriteListLineByLine("lick times 1:", licktimes1, output)
    WriteListLineByLine("np times 1: ", nptimes1, output)
    WriteListLineByLine("np latency 1: ", nplat1, output)
    WriteListLineByLine("endRange 1: ", endRange1, output)
    WriteListLineByLine("LicksPerTrial (LickT) 1: ", lickT1, output)
    print("lick count avg 1:\n", lickcountavg1, file=output)
    print("lick rate 1:\n", lickrate1, file=output)
    WriteListLineByLine("lickTperSec 1:", lickTperSec1, output)
    print("========SHIFT OCCURS HERE========", file=output)

    #WriteListLineByLine("lick times 2: ", licktimes2, output)
    print("licktimes 2 count:", len(licktimes2))
    WriteListLineByLine("np times 2: ", nptimes2, output)
    WriteListLineByLine("np latency 2: ", nplat2, output)
    WriteListLineByLine("endRange 2: ", endRange2, output)
    WriteListLineByLine("LicksPerTrial (LickT) 2: ", lickT2, output)
    print("lick count avg 2:\n", lickcountavg2, file=output)
    print("lick rate 2:\n", lickrate2, file=output)
    WriteListLineByLine("lickTperSec 2: ", lickTperSec2, output)

output.close()
