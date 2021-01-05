# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 22:30:05 2021

@author: Aaron
"""

import pandas as pd
import datetime
import matplotlib.pyplot as plt

def convert_to_right_format(x):
    year,month,day,hour=x.split("_")
    return datetime.datetime(year=int(year),month=int(month),day=int(day),hour=int(hour[1:]))

data=pd.read_csv("DATA_SET_1.csv")#Q1.1


data.loc[:,"Date/Time"]=data.loc[:,"Date/Time"].apply(lambda x:convert_to_right_format(x))#Q1.2
data=data.set_index("Date/Time")#Q1.2


mask_missing=data.isnull().sum(axis=1)>0#Q1.3
missing_index=data.loc[mask_missing,:].index.to_list()#Q1.3
print("Missing Index:",missing_index)#1.3


data=data.interpolate(method="time")#Q1.4


data=data.T#Q1.5


mask_year=data.T.index.year==2019#Q1.6
mask_month=data.T.index.month==10
safe=data.T.loc[mask_year & mask_month,"SAFEHARB 13 KV UNIT1 (DALMP) Average"]
face=data.T.loc[mask_year & mask_month,"FACEROCK 13 KV HOLT11 (DALMP) Average"]
fig, ax = plt.subplots(figsize=(12, 12))
ax.plot(safe,label="SAFEHARB 13 KV UNIT1 (DALMP) Average")
ax.plot(face,label="FACEROCK 13 KV HOLT11 (DALMP) Average")
ax.set(title="Oct 2019 DALMP",
xlabel="Time",
ylabel="DALMP")
plt.legend(loc="upper left")
plt.show()

mask_q7=(data.T.index.hour >=7)&(data.T.index.hour <=23)#Q1.7
data_q7=data.T.loc[mask_q7,:]
data_q7=data_q7.groupby(data_q7.index.month)[["SAFEHARB 13 KV UNIT1 (DALMP) Average","FACEROCK 13 KV HOLT11 (DALMP) Average"]].mean()
