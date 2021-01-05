# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 22:35:50 2021

@author: Aaron
"""

import requests
import pandas as pd
import datetime
def code(series_id):
    x = requests.get('http://api.eia.gov/series/?api_key=efc04384b240ca9cce98f1389d32a4ff&series_id={}'.format(series_id))
    df=pd.DataFrame(x.json()['series'][0]['data']).rename(columns={0:"Period",1:"Net_Generation"})
    df.loc[:,"Period"]=df.loc[:,"Period"].apply(lambda x:datetime.datetime.strptime(x, '%Y%m'))
    df=df.set_index("Period")
    mask=df.index.year==2019
    df=df.loc[mask,:]
    return df
series_id="ELEC.GEN.ALL-PA-99.M"
print(code(series_id))