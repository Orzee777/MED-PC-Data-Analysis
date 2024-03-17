# MED-PC-Data-Analysis
Analyze rat alcohol and sucrose lick/nosepoke data for MED-PC.

Part of a BGSU study analyzing rat licks and nosepokes to determine the effect alcohol and sucrose have behaviorally.

# Requirements
Out of the box, the code supports a convention set up using GET-OPERANT (https://github.com/SKhoo/GEToperant) as an extractor for MED-PC data. It also suports multiple worksheets.
* Excel
* Python
  * Pandas
  * TKinter
  * datetime

# How to Use
Each trial consists of a rat being offered a solution blocked by a door. The rat must nosepoke in order to gain a set amount of time with the door open to access the solution.
The study also utilized shift trials - where the duration the door was open was modified after a certain number of nosepokes.

Open the program in an editor of choice and easily modify it, as needed, to change:
* The number of nosepokes per trial
* The amount of time the door is open (N, or N1 and N2 in shift trials)
* A modifier to account of door open duration
* Output file name and location
* Output values
* Rounding value

The program will request an Excel file to parse the data and return the following information in the console and to a output file:
1. The name of the program, run date/time, version, and length of trial
2. The name of the input file and its sheetnames
3. A peak of the first 9 lines of the file
4. Timestamps of licks
5. Timestamps of nosepokes
6. Nosepoke latencies
7. Nosepoke latency average
8. Timestamps of trial end-times (when the door closes)
9. Licks per trial
10. Rate of licks
11. Rate of licks per trial
