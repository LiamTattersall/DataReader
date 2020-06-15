import datetime as dt
import pandas as pd
import numpy as np
import pytz

timeZone = pytz.timezone('Australia/ACT')
framedData = pd.read_csv("https://github.com/LiamTattersall/DataReader/raw/testing_data/testset1.csv", sep=",")
dataset = framedData.to_numpy()
