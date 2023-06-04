import json
import requests
import pandas as pd
import time
import numpy as np
import os
import re
import datetime
from requests import Request,Session
from requests.exceptions import ConnectionError,Timeout,TooManyRedirects

session = Session()

addresses = ['0x111cff45948819988857bbf1966a0399e0d1141e']
types = [1]

while True:
    i = 0
    sub_address = addresses[i]
    sub_type = types[i]
    # 地址余额是否有变动 监控的地址
    url_2 = 'https://services.tokenview.io/vipapi/addr/b/eth/' + sub_address + '?apikey=5u0dNQPd55eoEwFPwF2A'

    response = session.get(url_2)
    data = json.loads(response.text)
    print(data)
    code = str(data['code'])
    now_value = round(float(data['data']),2)
    if code == '1' and now_value > 1:
        # 读取上一时刻的余额数据
        pre_data = pd.read_csv('pre_data_1.csv')
        pre_data['date'] = pd.to_datetime(pre_data['date'])
        pre_data = pre_data.sort_values(by='date')
        pre_data = pre_data.reset_index(drop=True)
        # 读取上一时刻的变动数据
        pre_data_change = pd.read_csv('pre_data_change.csv')
        pre_data_change['date'] = pd.to_datetime(pre_data_change['date'])
        pre_data_change = pre_data_change.sort_values(by='date')
        pre_data_change = pre_data_change.reset_index(drop=True)

        change =  now_value - pre_data['value'][len(pre_data)-1] 
        #有btc转出时，余额变少了
        if change < -100 or change > 100:
            date_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #把余额变动数据写入csv文件中
            df_change = pd.DataFrame({'date':date_now,'address':sub_address,'change':change},index=[0])   
            df_change = pd.concat([pre_data_change,df_change])
            df_change['date'] = pd.to_datetime(df_change['date'])
            df_change = df_change.sort_values(by='date')
            df_change = df_change.reset_index(drop=True)
            #print(df_now)
            df_change.to_csv('pre_data_change.csv',index=False)

            #把最新地址余额数据写入csv文件中

            df_now = pd.DataFrame({'date':date_now,'address':sub_address,'value':now_value},index=[0]) 
            df_now = pd.concat([pre_data,df_now])
            df_now['date'] = pd.to_datetime(df_now['date'])
            df_now = df_now.sort_values(by='date')
            df_now = df_now.reset_index(drop=True)
            df_now = df_now[-10:]
            #print(df_now)
            df_now.to_csv('pre_data_1.csv',index=False)
            time.sleep(3)
        else:
            time.sleep(1)
            continue
    else:
        time.sleep(3)
        continue

    