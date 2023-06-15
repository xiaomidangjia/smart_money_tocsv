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
# ======= 正式开始执行
prop = fm.FontProperties(fname='/root/smart_money_tocsv/SimHei.ttf')

# 做图片
url ='https://services.tokenview.io/vipapi/address/balancetrend/eth/0x111cff45948819988857bbf1966a0399e0d1141e?apikey=5u0dNQPd55eoEwFPwF2A'
session = Session()
#url= 'https://services.tokenview.io/vipapi/pending/btc/2e0ec4a6caec1cf2f9cd9e58a5a3954c531d20c08bb88ae8d1a91dc0547f3561?apikey=5u0dNQPd55eoEwFPwF2A'
#session.headers.update(headers)
try:
    response = session.get(url)
    data = json.loads(response.text)
except:
    print(e)
date = []
ba = []
for i in range(len(data['data'])):
    ins = data['data'][i]
    date.append(next(iter(ins.keys())))
    ba.append(float(next(iter(ins.values()))))
sub_df = pd.DataFrame({'date':date,'value':ba})
print(sub_df)
url_address = [ 'https://api.glassnode.com/v1/metrics/market/price_usd_ohlc']
url_name = ['k_fold']
# insert your API key here
API_KEY = '26BLocpWTcSU7sgqDdKzMHMpJDm'
data_list = []
for num in range(len(url_name)):
    print(num)
    addr = url_address[num]
    name = url_name[num]
    # make API request
    res_addr = requests.get(addr,params={'a': 'ETH', 'api_key': API_KEY})
    # convert to pandas dataframe
    ins = pd.read_json(res_addr.text, convert_dates=['t'])
    #ins.to_csv('test.csv')
    #print(ins['o'])
    ins['date'] =  ins['t']
    ins['value'] =  ins['o']
    ins = ins[['date','value']]
    data_list.append(ins)
result_data = data_list[0][['date']]
for i in range(len(data_list)):
    df = data_list[i]
    result_data = result_data.merge(df,how='left',on='date')
#last_data = result_data[(result_data.date>='2016-01-01') & (result_data.date<='2020-01-01')]
last_data = result_data[(result_data.date>='2013-01-01')]
last_data = last_data.sort_values(by=['date'])
last_data = last_data.reset_index(drop=True)
print(type(last_data))
date = []
open_p = []
close_p = []
high_p = []
low_p = []
for i in range(len(last_data)):
    date.append(last_data['date'][i])
    open_p.append(last_data['value'][i]['o'])
    close_p.append(last_data['value'][i]['c'])
    high_p.append(last_data['value'][i]['h'])
    low_p.append(last_data['value'][i]['l'])
#res_data = pd.DataFrame({'date':date,'open':open_p,'close':close_p,'high':high_p,'low':low_p})
res_data = pd.DataFrame({'date':date,'close':close_p})
res_data = res_data.sort_values(by=['date'])
res_data = res_data.reset_index(drop=True)
sub_df['date'] = pd.to_datetime(sub_df['date'])
res_df = sub_df.merge(res_data[['date','close']],how='left',on=['date'])
res_df = res_df.sort_values(by='date')
res_df = res_df.reset_index(drop=True)
res_df.to_csv('/root/smart_money_tocsv/address_smart.csv',index=False)
import matplotlib.pyplot as plt
import seaborn as sns
# 绘画折线图
f, axes = plt.subplots(figsize=(20, 10))
axes_fu = axes.twinx()
sns.lineplot(x="date", y="value",color='red', linewidth=0.5,data=res_df, ax=axes)
sns.lineplot(x="date", y="close", data=res_df, ax=axes_fu)

plt.title('ETH聪明钱地址追踪', fontsize=20,fontproperties=prop) 
axes.set_xlabel('时间',fontsize=14,fontproperties=prop)
axes.set_ylabel("持仓量",fontsize=14,fontproperties=prop)
axes_fu.set_ylabel("ETH价格",fontsize=14,fontproperties=prop)

plt.savefig('ETH聪明钱地址追踪.png',  bbox_inches='tight')
plt.close()


from watermarker.marker import add_mark
add_mark(file = "ETH聪明钱地址追踪.png", out = "out",mark = "币coin---0XCarson出品", opacity=0.2, angle=30, space=30)
