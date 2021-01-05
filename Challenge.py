# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 22:37:02 2021

@author: Aaron
"""

import pandas as pd
import datetime
import requests
from tqdm import tqdm

category_id = requests.get("http://api.eia.gov/category/?api_key=efc04384b240ca9cce98f1389d32a4ff&category_id=902969")
category=category_id.json()["category"]['childcategories']
category_id_list=[]
category_id_list=[(ch['category_id'],ch['name']) for ch in category]
series_id=dict()
for t in tqdm(category_id_list):
    ch=t[0]
    name=t[1]
    temp = requests.get("http://api.eia.gov/category/?api_key=efc04384b240ca9cce98f1389d32a4ff&category_id={}".format(ch))
    for ch in temp.json()["category"]['childseries']:
        s=ch["name"]
        if "Electric fuel consumption" in s and "all fuels" in s and "monthly" in s:
            series_id[ch['series_id']]=name
            break
print("\n series_id has been successfully collected.")
total_df=pd.DataFrame()
for key,val in tqdm(series_id.items()):
    x = requests.get('http://api.eia.gov/series/?api_key=efc04384b240ca9cce98f1389d32a4ff&series_id={}'.format(key))
    df=pd.DataFrame(x.json()['series'][0]["data"]).rename(columns={0:"Period",1:val})
    df.loc[:,"Period"]=df.loc[:,"Period"].apply(lambda x:datetime.datetime.strptime(x, '%Y%m'))
    df=df.set_index("Period")
    mask=df.index.year==2019
    df=df.loc[mask,:].T
    total_df=pd.concat([total_df,df],ignore_index=False,axis=0)
total_df=total_df.dropna()
print(total_df)