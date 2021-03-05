import csv
import keras
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import matplotlib
from sklearn.metrics import mean_squared_error, r2_score
import math
import threading
from networktables import NetworkTables
import csv

cond = threading.Condition()
notified = [False]

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()

NetworkTables.initialize(server='10.56.36.2')
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

with cond:
    print("Waiting")
    if not notified[0]:
        cond.wait()

print("Connected!")

table = NetworkTables.getTable('SmartDashboard')

matplotlib.use('TkAgg')
videos = pd.read_csv("runs.csv")

lspeed = videos["L Speed"]
lpower = videos["Left Power"]
rspeed = videos["R Speed"]
rpower = videos["Right Power"]

lspeed = list(lspeed)
table2 = {}
for i in range(len(lspeed)):
    for j in range(len(rspeed)):
        table2[(round(lspeed[i],1),round(rspeed[j],1))] = (round(lpower[j],1),round(rpower[j],1))
def predictor(leftspeed,rightspeed):
    return table2[(round(leftspeed,1),round(rightspeed,1))]
print(predictor(lspeed[0],rspeed[0]))

otherNumber = table.getNumber('otherNumber')
table.putNumber('right speed', 0)
table.putNumber('left speed', 0)
while True:
    power = predictor(table.getNumber('left speed'),table.getNumber('right speed'))
    table.putNumber("left pw")
    table.putNumber("right pw")