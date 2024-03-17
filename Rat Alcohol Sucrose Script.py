### Rat Alcohol Sucrose Script v1.0
### Last edited 03/09/2024
### works with getOperant program and Excel (https://github.com/SKhoo/GEToperant)
### can work with multiple sheets
### N = 10

version = "1.0.240309"
# N (duration between nosepoke (door opening) and door closing) in seconds
lengthOfTrial = 10
# trialAdjustment is adjusting for the delay between door closing time and additional licks
# using 1 second, seems to be approximately .7 seconds, though ideally is 0
trialAdjustment = 1.0

# Dependencies: Pandas, TKinter, datetime
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

# used for opening file dialog
root = tk.Tk()
root.withdraw()

# option for hardcoding input file path
#file_path = "C:\\Users\\Default\\Documents\\inputfile.xlsx"

# CHANGE OUTPUT PATH HERE
out_path = "C:\\Users\\Default\\Documents\\outputfile.txt"
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

    nosepoketimes = []
    licktimes = []

    N = lengthOfTrial

    print(f.head(9))

    for index, row in f.iterrows():
        if row.iloc[0] == "Lick":
            licktimes.append((row.iloc[1])/2)
        if row.iloc[0] == "Nosepoke":
            nosepoketimes.append((row.iloc[1])/2)


    print("lick times:\n", licktimes)
    print("np times:\n" , nosepoketimes)

    nplat = []
    endRange = []
    lickT = []
    lickTperSec = []

    # find nosepokelatencies

    for i in range(0, len(nosepoketimes) - 1):
        x = round((nosepoketimes[i+1])-(nosepoketimes[i]), 2)
        nplat.append(x)

    print("np latency:\n", nplat)

    def Average(lst):
        if (len(lst)):
            av = sum(lst)/len(lst)
        else:
            av = 0
        return av

    nplatavg = round(Average(nplat), 2)
    print("np latency avg: ", nplatavg)

    for i in range(0, len(nosepoketimes)):
        # round because this is floating point arithmetic
        endRangeData = round(nosepoketimes[i]+N+trialAdjustment, 3)
        endRange.append(endRangeData)
    print(endRange)

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

    print("LickT: ", lickT)

    lickcountavg = round(Average(lickT), 2)
    print("lick count avg: ", lickcountavg)

    lickrate = round(lickcountavg/N, 2)
    print("lick rate ", lickrate)

    for i in range(0, len(lickT)):
        lickTperSec.append(lickT[i]/N)

    print("lickTperSec:\n", lickTperSec)

    def WriteListLineByLine(listname, lst, output):
        print(listname, ":", file=output)
        for i in range(0, len(lst)):
            print(lst[i], file=output)
            
    print(f.head(9), file=output)
    #WriteListLineByLine("lick times", licktimes, output)
    WriteListLineByLine("np times", nosepoketimes, output)
    WriteListLineByLine("np latency", nplat, output)
    print("np latency avg: ", nplatavg, file=output)
    WriteListLineByLine("endRange", endRange, output)
    WriteListLineByLine("LicksPerTrial (LickT)", lickT, output)
    print("lick count avg", lickcountavg, file=output)
    print("lick rate ", lickrate, file=output)
    WriteListLineByLine("lickTperSec", lickTperSec, output)
    print("Sheet completed: ", sheetnames[z], file=output)

output.close()
    
