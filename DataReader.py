import datetime as dt   #Time functions
import pandas as pd     #Data analysis
import numpy as np      #Data importing
import math             #Number manipulation

framedData = pd.read_csv("https://github.com/LiamTattersall/DataReader/raw/testing_data/testset.csv", sep=",") #Gets data
dataSet = framedData.to_numpy() #Reads data in usable format
timeTable = np.array([[8.4,9.2,10,10.4,11,11.4,12,12.2,13,13.4,14.2,14.4,15,15.4],['A','B','C','Recess','D','SG','none','E','Lunch','F','G','none','H','home'],['E','none','none','Recess','A','none','none','none','Lunch','C','none','G','none','home'],['F','none','none','Recess','B','none','none','none','Lunch','D','none','H','none','home'],['G','none','none','Recess','E','none','A','none','Lunch','C','none','none','none','home'],['D','none','none','Recess','F','none','B','none','Lunch','H','none','none','none','home']]) #Creates refrence timetable

scanNumber = dataSet.shape[0] #Gets the number of scans

studentList = [] #Gets a list of students
for i in range(0, scanNumber):
  if dataSet[i,0] not in studentList:
    student = dataSet[i,0]
    studentList.extend([student])

attendance = np.empty((len(studentList)+1, 26), dtype=object) #Creates a roll
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
  markColumn = np.where(attendance == timeTable[day,j] + str(lineNumber))[1][0] #Gets the right column and row to mark
  markRow = np.where(attendance == dataSet[i,0])[0][0]
  k = j + 1 #Gets the end of the current class
  while timeTable[day,k] == 'none':
    k += 1
  duration = (math.floor(float(timeTable[0,k])) * 60 + float(timeTable[0,k])%1 * 100) - (math.floor(float(timeTable[0,j])) * 60 + + float(timeTable[0,j])%1 * 100) #Gets the duration of the current class
  if type(attendance[markRow,markColumn]) != float: #Calculates how late the student was, with a 3 minute start-of-class buffer
    late = duration - ((hours * 60 + minutes * 100) - (math.floor(float(timeTable[0,j])) * 60 + float(timeTable[0,j])%1 * 100))
    if late >= duration - 3:
      late = duration
  else:
    late = (math.floor(attendance[markRow,markColumn]) * 60 + attendance[markRow,markColumn]%1 * 100) - ((math.floor(float(timeTable[0,k])) * 60 + float(timeTable[0,k])%1 * 100) - (hours * 60 + minutes * 100))
  late = round(late, 0)
  late = math.floor(round(late, 0)/60) + round(late, 0)%60 / 100
  attendance[markRow,markColumn] = late #Marks the student on the roll

for i in range(0, attendance.shape[0]): #Sets the unattended classes to 0 attendance time
  for j in range(0, attendance.shape[1]):
    if isinstance(attendance[i,j], type(None)):
      attendance[i,j] = 0

for i in range(0, attendance.shape[0]): #Fixes missing leading 0's in ID's from importing
  attendance[i,0] = str(attendance[i,0])
  if i != 0:
    while len(str(attendance[i,0])) < 7:
      attendance[i,0] = '0' + attendance[i,0]

for i in range(0, attendance.shape[0]): #Converts numbers to times
  for j in range(0, attendance.shape[1]):
    if i != 0 and j != 0:
      if len(str(attendance[i,j])) > 1:
        attendance[i,j] = str(attendance[i,j])
        if len(attendance[i,j]) < 4:
          attendance[i,j] = attendance[i,j] + '0'
        attendance[i,j] = attendance[i,j].replace('.', ':')

for i in range(0, attendance.shape[0]): #Prints out the roll in a nice format
  for j in range(0, attendance.shape[1]):
    if j == 0:
      if i == 0:
        print('         ', end='')
      else:
        print(attendance[i,j] + '  ', end='')
    else:
      print(attendance[i,j], end='')
      for k in range(0, 6 - len(str(attendance[i,j]))):
        print(' ', end='')
  print('\n')
