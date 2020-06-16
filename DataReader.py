import datetime as dt   #Time functions
import pandas as pd     #Data analysis
import numpy as np      #Number manipulation
import pytz             #Time zone adjustment (needed as colab servers are not in Austrailia)

timeZone = pytz.timezone('Australia/ACT') #Gets time zone
framedData = pd.read_csv("https://github.com/LiamTattersall/DataReader/raw/testing_data/testset1.csv", sep=",") #Gets data
dataSet = framedData.to_numpy() #Reads data in usable format
timeTable = np.array([[8.4,9.2,10,10.4,11,11.4,12,12.2,13,13.4,14.2,14.4,15,15.4],['A','B','C','Recess','D','SG','none','E','Lunch','F','G','none','H','home'],['E','none','none','Recess','A','none','none','none','Lunch','C','none','G','none','home'],['F','none','none','Recess','B','none','none','none','Lunch','D','none','H','none','home'],['G','none','none','Recess','E','none','A','none','Lunch','C','none','none','none','home'],['D','none','none','Recess','F','none','B','none','Lunch','H','none','none','none','home']]) #Creates refrence timetable

scanNumber = dataSet.shape[0] #Gets the number of scans
for i in range(0, scanNumber): #For each scan, checks what time that scan was, then checks what line it was, to mark the student
  day = dt.date(int(str(dataSet[i,1])[0:4]), int(str(dataSet[i,1])[5:7]), int(str(dataSet[i,1])[8:10])).weekday() + 1 #Gets the correct timetable day
  time = float(str(dataSet[i,1])[11:13]) + float(str(dataSet[i,1])[14:16])/100 #Gets the time of scanning
  j = 0 #Gets the line
  while float(timeTable[0,j]) <= time:
    j += 1
  j -= 1
  while timeTable[day,j] == 'none':
    j -= 1
  print(timeTable[day,j])
