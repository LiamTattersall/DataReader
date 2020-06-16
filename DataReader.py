import datetime as dt   #Time functions
import pandas as pd     #Data analysis
import numpy as np      #Number manipulation
import pytz             #Time zone adjustment (needed as colab servers are not in Austrailia)

timeZone = pytz.timezone('Australia/ACT') #Gets time zone
framedData = pd.read_csv("https://github.com/LiamTattersall/DataReader/raw/testing_data/testset1.csv", sep=",") #Gets data
dataSet = framedData.to_numpy() #Reads data in usable format
timeTable = np.array([[8.4,9.2,10,10.4,11,11.4,12,12.2,13,13.4,14.2,14.4,15,15.4],['A','B','C','Recess','D','SG','none','E','Lunch','F','G','none','H','home'],['E','none','none','Recess','A','none','none','none','Lunch','C','none','G','none','home'],['F','none','none','Recess','B','none','none','none','Lunch','D','none','H','none','home'],['G','none','none','Recess','E','none','A','none','Lunch','C','none','none','none','home'],['D','none','none','Recess','F','none','B','none','Lunch','H','none','none','none','home']]) #Creates refrence timetable

scanNumber = dataSet.shape[0] #Gets the number of scans

studentList = []
for i in range(0, scanNumber):
  if dataSet[i,0] not in studentList:
    studentList.extend([dataSet[i,0]])

attendance = np.empty((len(studentList)+1, 26), dtype=object)
attendance[0,0] = ""
for i in range(0, len(studentList)):
  attendance[i+1,0] = studentList[i]
classes = ['A1','B1','C1','D1','SG1','E1','F1','G1','H1','E2','A2','C2','G2','F2','B2','D2','H2','G3','E3','A3','C3','D3','F3','B3','H3']
for i in range(0, len(classes)):
  attendance[0,i+1] = classes[i]

for i in range(0, scanNumber): #For each scan, checks what time that scan was, then checks what line it was, to mark the student
  day = dt.date(int(str(dataSet[i,1])[0:4]), int(str(dataSet[i,1])[5:7]), int(str(dataSet[i,1])[8:10])).weekday() + 1 #Gets the correct timetable day
  hours = float(str(dataSet[i,1])[11:13])
  minutes = float(str(dataSet[i,1])[14:16])/100
  time = hours + minutes #Gets the time of scanning
  j = 0 #Gets the line
  while float(timeTable[0,j]) <= time:
    j += 1
  j -= 1
  while timeTable[day,j] == 'none':
    j -= 1
  if day == 1:
    lineNumber = 1
  elif day == 2 or day == 3:
    lineNumber = 2
  else:
    lineNumber = 3
  markColumn = np.where(attendance == timeTable[day,j] + str(lineNumber))[1][0]
  markRow = np.where(attendance == dataSet[i,0])[0][0]
  attendance[markRow,markColumn] = 'Marked'

print(attendance)
